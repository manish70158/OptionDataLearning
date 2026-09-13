"""Web-adapted backtest simulation engine."""
import logging
import math
from collections import Counter
from datetime import date, timedelta
from typing import Optional

from option_backtester.pricing import calculate_atm_strike
from web.backend.data import cache
from web.backend.data.expiry_calendar import historical_expiry
from web.backend.data.upstox_fetcher import UpstoxHistoricalFetcher
from web.backend.engine.pricing import get_option_price, get_spot_price
from web.backend.schemas import (
    BacktestConfig, BacktestResult, BacktestSummary,
    DrawdownPoint, EquityCurvePoint, StrategyDefinition,
    TradeRecord,
)

logger = logging.getLogger(__name__)

DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
LOT_SIZES = {"NIFTY": 65, "BANKNIFTY": 30, "SENSEX": 20}


async def _spot_at_entry_time(fetcher: UpstoxHistoricalFetcher, underlying: str,
                                dt_str: str, entry_time: str,
                                fallback_spot: float) -> float:
    """Resolve the index spot at entry_time using cached 5-min index candles;
    fetch on-demand if missing. Falls back to `fallback_spot` (daily open)."""
    if not await cache.has_index_intraday(underlying, dt_str):
        try:
            candles = await fetcher.fetch_index_intraday(underlying, dt_str, "minutes", 5)
        except Exception as e:
            logger.debug(f"Index intraday fetch failed for {underlying} {dt_str}: {e}")
            candles = []
        if candles:
            await cache.insert_index_intraday_batch([
                {
                    "instrument": underlying,
                    "date": dt_str,
                    "time": c["time"],
                    "open": c["open"],
                    "high": c["high"],
                    "low": c["low"],
                    "close": c["close"],
                }
                for c in candles
            ])
    candle = await cache.get_index_intraday_at_or_after(underlying, dt_str, entry_time)
    if candle and candle.get("open") is not None:
        return float(candle["open"])
    return fallback_spot


def _infer_weekly_expiry_weekday(fetcher: UpstoxHistoricalFetcher, underlying: str) -> Optional[int]:
    """Guess the current weekly-expiry weekday from cached instrument expiries.

    Instruments master only lists live/future contracts, so historical dates
    fall back to the earliest cached expiry — usually a distant monthly. We use
    the most common weekday among near-term expiries as a stand-in cadence.
    """
    if fetcher._instruments_cache is None:
        return None
    weekdays: list[int] = []
    for key in fetcher._instruments_cache.keys():
        if key[0] != underlying:
            continue
        try:
            exp = date.fromisoformat(key[2])
        except ValueError:
            continue
        # Skip month-end monthlies to avoid biasing toward the monthly weekday
        if exp.day >= 20:
            continue
        weekdays.append(exp.weekday())
    if not weekdays:
        return None
    return Counter(weekdays).most_common(1)[0][0]


def _compute_dte(
    dt: date,
    resolved_expiry: date,
    weekly_expiry_wd: Optional[int],
    expiry_type: str,
) -> tuple[int, date]:
    """Return (dte, effective_expiry) — always the expiry the engine actually
    priced against. Projecting a "hypothetical weekly" would produce DTE=0
    for trades that are really 14 days from expiry (Upstox's instruments
    master only lists live/future contracts, not historical ones), so we
    stay honest with the resolved expiry.
    """
    del weekly_expiry_wd, expiry_type  # kept in signature for callers
    return (resolved_expiry - dt).days, resolved_expiry


async def run_backtest(strategy: StrategyDefinition,
                        config: BacktestConfig,
                        progress_callback=None) -> BacktestResult:
    """Run a full backtest simulation.

    For each trading day in the date range:
    1. Filter by weekday and VIX
    2. Price all legs at entry time
    3. Check intraday SL/TP using high/low extremes
    4. Price at exit time
    5. Record trade result
    """
    underlying = strategy.underlying.value
    expiry_type = strategy.expiry_type.value
    lot_size = LOT_SIZES.get(underlying, 75)

    # Create fetcher instance for expiry lookup
    fetcher = UpstoxHistoricalFetcher()
    await fetcher.fetch_instruments_master()  # Load instruments for expiry resolution

    # Infer the weekly-expiry weekday from the instruments cache so historical
    # dates outside the cache's expiry range still get a realistic DTE.
    weekly_expiry_wd = _infer_weekly_expiry_weekday(fetcher, underlying)

    # Get all trading days from OHLCV cache
    ohlcv_data = await cache.get_ohlcv_range(
        underlying,
        config.start_date.isoformat(),
        config.end_date.isoformat(),
    )

    if not ohlcv_data:
        return _empty_result()

    trades: list[TradeRecord] = []
    cumulative_pnl = 0.0
    total_days = len(ohlcv_data)

    for idx, day_data in enumerate(ohlcv_data):
        dt_str = day_data["date"]
        dt = date.fromisoformat(dt_str)

        # Report progress
        if progress_callback and idx % 10 == 0:
            pct = int(idx / total_days * 100)
            progress_callback(pct, 100, f"Simulating {dt_str}...")

        # Filter by weekday
        if dt.weekday() not in config.weekdays:
            continue

        # Filter by VIX (use the spot data as proxy if VIX not available)
        # For now we skip VIX filtering if we don't have VIX data in cache
        # The engine can be extended to fetch VIX from a separate source

        spot_open = day_data["open"]
        spot_close = day_data["close"]
        spot_high = day_data["high"]
        spot_low = day_data["low"]

        # ATM is fixed at entry — use the 5-min index candle at entry_time so
        # a 09:20 entry doesn't inherit the 09:15 opening tick's spot.
        entry_time_str = config.entry_time.strftime("%H:%M")
        spot_at_entry = await _spot_at_entry_time(
            fetcher, underlying, dt_str, entry_time_str, spot_open
        )
        atm_strike = calculate_atm_strike(spot_at_entry)

        # Resolve expiry for this date. Prefer the historical rule-based expiry
        # (accurate to the regime that was in effect on `dt`); fall back to the
        # instruments-master lookup only when the calendar has no coverage.
        hist_expiry = historical_expiry(dt, underlying, expiry_type)
        live_expiry = fetcher._get_nearest_expiry(dt, underlying, expiry_type)
        expiry_date = hist_expiry or live_expiry
        if not expiry_date:
            logger.warning(f"No expiry found for {underlying} on {dt}, skipping")
            continue
        expiry_str = expiry_date.isoformat()
        days_to_expiry = max((expiry_date - dt).days, 0.5)

        # Estimate VIX from price range if not available
        daily_range_pct = (spot_high - spot_low) / spot_open * 100
        estimated_vix = daily_range_pct * math.sqrt(252) * 0.6  # rough estimate
        vix = max(estimated_vix, 10.0)

        # Price all legs at entry
        entry_premiums = []
        entry_total = 0.0
        any_real = False

        for leg in strategy.legs:
            strike = atm_strike + leg.strike_offset
            opt_type = leg.option_type.value

            price_info = await get_option_price(
                underlying, dt_str, strike, opt_type, expiry_str,
                time_of_day="open", vix=vix, days_to_expiry=days_to_expiry,
                time_hhmm=config.entry_time.strftime("%H:%M"),
            )
            premium = price_info["price"]
            if price_info["source"] == "real":
                any_real = True

            multiplier = leg.lots * lot_size
            if leg.position.value == "buy":
                entry_total -= premium * multiplier  # Pay premium
            else:
                entry_total += premium * multiplier  # Receive premium

            entry_premiums.append({
                "strike": strike,
                "option_type": opt_type,
                "position": leg.position.value,
                "lots": leg.lots,
                "premium": premium,
                "source": price_info["source"],
            })

        # Determine per-leg SL trigger prices/times from cached intraday
        # candles when sl_scope == "per_leg". These pre-empt the combined
        # intraday SL/TP block below.
        exit_reason = "time_exit"
        exit_time = config.exit_time.strftime("%H:%M")
        exit_pnl = None
        per_leg_stops: list[Optional[dict]] = [None] * len(strategy.legs)
        exit_time_str = config.exit_time.strftime("%H:%M")

        if (config.sl_scope.value == "per_leg"
                and config.stop_loss_enabled
                and config.stop_loss_value > 0):
            # Preload index intraday for the day so BS-simulated per-leg checks
            # can walk through the spot journey.
            index_candles = await cache.get_index_intraday_at_or_after(
                underlying, dt_str, entry_time_str
            )
            all_index = []
            if index_candles is not None:
                # get_index_intraday_at_or_after returns just one candle; we
                # want the whole window. Query directly via a small helper.
                db = await cache.get_db()
                try:
                    cursor = await db.execute(
                        """SELECT time, open, high, low, close FROM index_intraday
                           WHERE instrument = ? AND date = ?
                           AND time >= ? AND time <= ? ORDER BY time ASC""",
                        (underlying, dt_str, entry_time_str, exit_time_str),
                    )
                    rows = await cursor.fetchall()
                    all_index = [dict(r) for r in rows]
                finally:
                    await db.close()

            for i, leg in enumerate(strategy.legs):
                strike = atm_strike + leg.strike_offset
                opt_type = leg.option_type.value
                entry_px = entry_premiums[i]["premium"]
                # Per-leg SL price relative to entry premium
                if config.stop_loss_mode.value == "percentage":
                    pct = config.stop_loss_value / 100
                    if leg.position.value == "sell":
                        sl_price = entry_px * (1 + pct)  # SELL loses when price rises
                    else:
                        sl_price = entry_px * (1 - pct)  # BUY loses when price falls
                else:  # points
                    if leg.position.value == "sell":
                        sl_price = entry_px + config.stop_loss_value
                    else:
                        sl_price = entry_px - config.stop_loss_value

                # Prefer real per-leg 5-min candles when we have them.
                leg_candles = await cache.get_intraday_candles_between(
                    underlying, dt_str, strike, opt_type, expiry_str,
                    entry_time_str, exit_time_str,
                )
                triggered = False
                for c in leg_candles:
                    if leg.position.value == "sell":
                        breach = c["high"] >= sl_price
                    else:
                        breach = c["low"] <= sl_price
                    if breach:
                        per_leg_stops[i] = {"time": c["time"], "price": sl_price}
                        triggered = True
                        break

                if triggered:
                    continue

                # Fallback: BS-simulate the leg's premium at each cached index
                # candle's spot high/low. Prefer the calibrated IV from
                # bhavcopy over the coarse spot-range vix estimate.
                from option_backtester.pricing import estimate_premium
                opt_type_bs = "call" if opt_type == "CE" else "put"
                premium_row = await cache.get_option_premium(
                    underlying, dt_str, strike, opt_type, expiry_str
                )
                if premium_row and premium_row.get("implied_vol"):
                    sigma_pct = premium_row["implied_vol"] * 100.0
                    skew = 1.0
                else:
                    sigma_pct = vix
                    offset = strike - atm_strike
                    if offset > 0 and opt_type_bs == "call":
                        skew = 0.95
                    elif offset < 0 and opt_type_bs == "put":
                        skew = 1.10
                    else:
                        skew = 1.0
                for c in all_index:
                    # Extreme spot in this 5-min window that would maximise
                    # loss on this leg.
                    if leg.position.value == "sell":
                        adverse_spot = c["high"] if opt_type == "CE" else c["low"]
                    else:
                        adverse_spot = c["low"] if opt_type == "CE" else c["high"]
                    bs_px = estimate_premium(
                        adverse_spot, strike, sigma_pct,
                        max(days_to_expiry, 0.1), opt_type_bs, skew,
                    )
                    bs_px = max(bs_px, 0.05)
                    if leg.position.value == "sell":
                        breach = bs_px >= sl_price
                    else:
                        breach = bs_px <= sl_price
                    if breach:
                        per_leg_stops[i] = {"time": c["time"], "price": sl_price}
                        break

        # Evaluate strategy P&L at spot_high and spot_low (combined-mode SL/TP)
        pnl_at_high = await _evaluate_strategy_pnl(
            strategy, underlying, dt_str, expiry_str,
            atm_strike, spot_high, vix, days_to_expiry,
            entry_premiums, lot_size,
        )
        pnl_at_low = await _evaluate_strategy_pnl(
            strategy, underlying, dt_str, expiry_str,
            atm_strike, spot_low, vix, days_to_expiry,
            entry_premiums, lot_size,
        )

        intraday_worst = min(pnl_at_high, pnl_at_low)
        intraday_best = max(pnl_at_high, pnl_at_low)

        # Net premium for SL/TP percentage calculation
        net_premium_abs = abs(entry_total)
        if net_premium_abs == 0:
            net_premium_abs = 1.0  # Avoid division by zero

        combined_sl_mode = config.sl_scope.value == "combined"

        # Combined stop loss check (only when SL scope is combined)
        if combined_sl_mode and config.stop_loss_enabled and config.stop_loss_value > 0:
            if config.stop_loss_mode.value == "percentage":
                sl_threshold = -net_premium_abs * (config.stop_loss_value / 100)
            else:
                sl_threshold = -config.stop_loss_value * lot_size

            if intraday_worst <= sl_threshold:
                exit_pnl = sl_threshold
                exit_reason = "stop_loss"
                exit_time = "intraday"

        # Target profit check (only if SL didn't trigger)
        if exit_reason == "time_exit" and config.target_profit_enabled and config.target_profit_value > 0:
            if config.target_profit_mode.value == "percentage":
                tp_threshold = net_premium_abs * (config.target_profit_value / 100)
            else:
                tp_threshold = config.target_profit_value * lot_size

            if intraday_best >= tp_threshold:
                exit_pnl = tp_threshold
                exit_reason = "target_profit"
                exit_time = "intraday"

        # Trailing SL check
        if (exit_reason == "time_exit" and config.trailing_sl_enabled
                and config.trailing_sl_value > 0 and config.stop_loss_enabled
                and combined_sl_mode):
            trail_distance = config.trailing_sl_value * lot_size
            if intraday_best > 0:
                trailing_sl_level = intraday_best - trail_distance
                if trailing_sl_level > 0 and intraday_worst <= trailing_sl_level:
                    exit_pnl = trailing_sl_level
                    exit_reason = "trailing_sl"
                    exit_time = "intraday"

        # Per-leg SL: if any leg stopped out, tag the exit accordingly.
        # exit_pnl is left None here so it is computed from real per-leg prices
        # (with SL-triggered legs using their sl_price) below.
        if any(per_leg_stops):
            latest_stop_time = max(s["time"] for s in per_leg_stops if s)
            exit_time = latest_stop_time
            exit_reason = (
                "stop_loss"
                if all(per_leg_stops[i] is not None for i in range(len(strategy.legs)))
                else "stop_loss (partial)"
            )

        # Fetch real per-leg exit premiums at the configured exit time.
        # ``exit_total`` is the net cash flow of closing all positions: for
        # long legs we sell (receive premium), for short legs we buy back (pay).
        # For per-leg-SL triggered legs, the exit premium is the SL price and
        # the leg's source is marked as "stop_loss".
        exit_premiums = []
        exit_total = 0.0
        for i, leg in enumerate(strategy.legs):
            strike = atm_strike + leg.strike_offset
            opt_type = leg.option_type.value

            stop_info = per_leg_stops[i]
            if stop_info is not None:
                exit_premium = stop_info["price"]
                leg_source = "stop_loss"
            else:
                price_info = await get_option_price(
                    underlying, dt_str, strike, opt_type, expiry_str,
                    time_of_day="close", vix=vix, days_to_expiry=max(days_to_expiry - 0.7, 0.1),
                    time_hhmm=config.exit_time.strftime("%H:%M"),
                )
                exit_premium = price_info["price"]
                leg_source = price_info["source"]

            multiplier = leg.lots * lot_size
            if leg.position.value == "buy":
                exit_total += exit_premium * multiplier
            else:
                exit_total -= exit_premium * multiplier

            exit_premiums.append({
                "strike": strike,
                "option_type": opt_type,
                "position": leg.position.value,
                "lots": leg.lots,
                "entry_premium": entry_premiums[i]["premium"],
                "exit_premium": exit_premium,
                "source": leg_source,
            })

        # If no intraday combined SL/TP triggered, compute exit P&L from real
        # per-leg prices (which include per-leg SL prices where applicable).
        # Include slippage of 2 points per leg to match _evaluate_strategy_pnl.
        if exit_pnl is None:
            exit_pnl = entry_total + exit_total - 2 * len(strategy.legs) * lot_size

        # Convert to points (divide by lot_size to get per-lot P&L)
        pnl_points = exit_pnl / lot_size if lot_size > 0 else exit_pnl
        pnl_inr = exit_pnl

        cumulative_pnl += pnl_points
        entry_premium_display = abs(entry_total) / lot_size
        # Time-exit and per-leg SL: show the actual net premium at exit.
        # Combined intraday SL/TP: back into a nominal exit level from entry + P&L.
        if exit_reason.startswith("stop_loss") and any(per_leg_stops):
            exit_premium_display = abs(exit_total) / lot_size
        elif exit_reason == "time_exit":
            exit_premium_display = abs(exit_total) / lot_size
        else:
            exit_premium_display = entry_premium_display + pnl_points

        dte, effective_expiry = _compute_dte(
            dt, expiry_date, weekly_expiry_wd, expiry_type
        )
        trade = TradeRecord(
            date=dt_str,
            day_of_week=DAY_NAMES[dt.weekday()],
            entry_time=config.entry_time.strftime("%H:%M"),
            exit_time=exit_time,
            entry_premium=round(entry_premium_display, 2),
            exit_premium=round(exit_premium_display, 2),
            pnl_points=round(pnl_points, 2),
            pnl_inr=round(pnl_inr, 2),
            exit_reason=exit_reason,
            cumulative_pnl=round(cumulative_pnl, 2),
            vix=round(vix, 2),
            pricing_source="real" if any_real else "estimated",
            dte=dte,
            expiry_date=effective_expiry.isoformat(),
            legs=exit_premiums,  # Include leg details
        )
        trades.append(trade)

    if not trades:
        return _empty_result()

    # Compute summary statistics
    summary = _compute_summary(trades, lot_size)
    equity_curve = _compute_equity_curve(trades)
    drawdown = _compute_drawdown(trades)
    monthly_pnl = _compute_monthly_pnl(trades)

    return BacktestResult(
        summary=summary,
        trades=trades,
        equity_curve=equity_curve,
        drawdown=drawdown,
        monthly_pnl=monthly_pnl,
    )


async def _evaluate_strategy_pnl(
    strategy: StrategyDefinition,
    underlying: str, dt_str: str, expiry_str: str,
    atm_strike: float, spot_level: float,
    vix: float, dte: float,
    entry_premiums: list[dict],
    lot_size: int,
) -> float:
    """Evaluate combined strategy P&L at a given spot level."""
    total_pnl = 0.0

    for i, leg in enumerate(strategy.legs):
        strike = atm_strike + leg.strike_offset
        opt_type = leg.option_type.value
        entry_data = entry_premiums[i]
        entry_premium = entry_data["premium"]

        # Price at the given spot level using BS (since we need price at arbitrary spot)
        from option_backtester.pricing import estimate_premium
        opt_type_bs = "call" if opt_type == "CE" else "put"

        # Skew
        offset = strike - atm_strike
        if offset > 0 and opt_type_bs == "call":
            skew = 0.95
        elif offset < 0 and opt_type_bs == "put":
            skew = 1.10
        else:
            skew = 1.0

        exit_premium = estimate_premium(spot_level, strike, vix, dte, opt_type_bs, skew)
        exit_premium = max(exit_premium, 0.05)

        multiplier = leg.lots * lot_size
        if leg.position.value == "buy":
            total_pnl += (exit_premium - entry_premium) * multiplier
        else:
            total_pnl += (entry_premium - exit_premium) * multiplier

    # Deduct slippage (2 points per leg)
    total_pnl -= 2 * len(strategy.legs) * lot_size

    return total_pnl


def _compute_summary(trades: list[TradeRecord], lot_size: int) -> BacktestSummary:
    """Compute summary statistics from trade records."""
    pnls = [t.pnl_points for t in trades]
    wins = [p for p in pnls if p > 0]
    losses = [p for p in pnls if p <= 0]

    total_pnl = sum(pnls)
    num_trades = len(trades)
    win_rate = (len(wins) / num_trades * 100) if num_trades > 0 else 0

    # Max drawdown
    peak = 0.0
    max_dd = 0.0
    cumulative = 0.0
    for p in pnls:
        cumulative += p
        if cumulative > peak:
            peak = cumulative
        dd = cumulative - peak
        if dd < max_dd:
            max_dd = dd
    max_dd_pct = (max_dd / peak * 100) if peak > 0 else 0

    # Sharpe ratio (annualized, assuming 252 trading days)
    if len(pnls) > 1:
        import numpy as np
        pnl_arr = np.array(pnls)
        mean_daily = pnl_arr.mean()
        std_daily = pnl_arr.std()
        sharpe = (mean_daily / std_daily * math.sqrt(252)) if std_daily > 0 else 0
    else:
        sharpe = 0

    avg_win = sum(wins) / len(wins) if wins else 0
    avg_loss = sum(losses) / len(losses) if losses else 0

    # Profit factor
    gross_profit = sum(wins)
    gross_loss = abs(sum(losses))
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else float("inf")

    # Max consecutive wins/losses
    max_consec_wins = _max_consecutive(pnls, lambda x: x > 0)
    max_consec_losses = _max_consecutive(pnls, lambda x: x <= 0)

    return BacktestSummary(
        total_pnl=round(total_pnl, 2),
        total_pnl_inr=round(total_pnl * lot_size, 2),
        num_trades=num_trades,
        win_rate=round(win_rate, 2),
        max_drawdown=round(max_dd, 2),
        max_drawdown_pct=round(max_dd_pct, 2),
        sharpe_ratio=round(sharpe, 4),
        avg_win=round(avg_win, 2),
        avg_loss=round(avg_loss, 2),
        profit_factor=round(min(profit_factor, 999.99), 2),
        max_consecutive_wins=max_consec_wins,
        max_consecutive_losses=max_consec_losses,
    )


def _max_consecutive(values: list[float], condition) -> int:
    """Count max consecutive elements matching a condition."""
    max_count = 0
    count = 0
    for v in values:
        if condition(v):
            count += 1
            max_count = max(max_count, count)
        else:
            count = 0
    return max_count


def _compute_equity_curve(trades: list[TradeRecord]) -> list[EquityCurvePoint]:
    return [
        EquityCurvePoint(date=t.date, cumulative_pnl=t.cumulative_pnl)
        for t in trades
    ]


def _compute_drawdown(trades: list[TradeRecord]) -> list[DrawdownPoint]:
    """Compute drawdown series from trades."""
    points = []
    peak = 0.0
    for t in trades:
        if t.cumulative_pnl > peak:
            peak = t.cumulative_pnl
        dd_pct = ((t.cumulative_pnl - peak) / peak * 100) if peak > 0 else 0
        points.append(DrawdownPoint(date=t.date, drawdown_pct=round(dd_pct, 2)))
    return points


def _compute_monthly_pnl(trades: list[TradeRecord]) -> dict[str, float]:
    """Aggregate P&L by month."""
    monthly: dict[str, float] = {}
    for t in trades:
        month_key = t.date[:7]  # YYYY-MM
        monthly[month_key] = monthly.get(month_key, 0) + t.pnl_points
    return {k: round(v, 2) for k, v in monthly.items()}


def _empty_result() -> BacktestResult:
    return BacktestResult(
        summary=BacktestSummary(
            total_pnl=0, num_trades=0, win_rate=0,
            max_drawdown=0, max_drawdown_pct=0, sharpe_ratio=0,
            avg_win=0, avg_loss=0, profit_factor=0,
            max_consecutive_wins=0, max_consecutive_losses=0,
        ),
        trades=[],
        equity_curve=[],
        drawdown=[],
        monthly_pnl={},
    )
