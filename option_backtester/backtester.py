"""Core backtesting engine: load data, compute DTE, run strategy simulations."""
import pandas as pd
import numpy as np
from option_backtester.strategies import (
    calculate_strategy_pnl, calculate_intraday_max_loss,
    calculate_intraday_max_profit, calculate_pnl_at_spot,
)


REQUIRED_COLUMNS = [
    'date', 'nifty_open', 'nifty_high', 'nifty_low', 'nifty_close',
    'vix_open', 'vix_close', 'is_nifty_expiry', 'fii_view', 'pro_view',
]


def load_data(csv_path):
    """Load historical data from CSV into a DataFrame.

    Args:
        csv_path: Path to the CSV file

    Returns:
        DataFrame with parsed dates and validated columns
    """
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'])

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f'Missing required columns: {missing}')

    return df


def compute_days_to_expiry(df):
    """Calculate days to next expiry for each row.

    Uses is_nifty_expiry column to find expiry days, then counts calendar
    days forward from each row to the next expiry.

    Expiry days themselves get dte=0.5 (for pricing purposes, avoids T=0).
    """
    df = df.copy()
    df['is_nifty_expiry'] = df['is_nifty_expiry'].fillna(0).astype(int)

    # Find indices of expiry days
    expiry_indices = df.index[df['is_nifty_expiry'] == 1].tolist()

    dte = np.full(len(df), np.nan)

    for i in range(len(df)):
        if df.iloc[i]['is_nifty_expiry'] == 1:
            dte[i] = 0.5  # Expiry day: use 0.5 for pricing
        else:
            # Find the next expiry day after this row
            future_expiries = [ei for ei in expiry_indices if ei > i]
            if future_expiries:
                next_expiry_idx = future_expiries[0]
                # Count calendar days between this date and the next expiry date
                days_diff = (df.iloc[next_expiry_idx]['date'] - df.iloc[i]['date']).days
                dte[i] = max(days_diff, 1)
            else:
                # No future expiry found, use a default
                dte[i] = 3

    df['days_to_expiry'] = dte
    return df


def run_backtest(df, strategies, config, stop_loss_pct=None, rr_ratio=None,
                 move_exit_pct=None):
    """Run backtest across all trading days and strategies.

    Args:
        df: DataFrame with market data and days_to_expiry column
        strategies: List of Strategy objects
        config: Config module with parameters
        stop_loss_pct: dict of strategy_name -> SL percentage threshold, or None to disable.
        rr_ratio: Risk:Reward ratio for take profit. If set (e.g. 1.0 for 1:1),
                  TP = SL * rr_ratio. When intraday best P&L >= TP, position closes at TP.
                  None = no take profit (hold till close).
        move_exit_pct: Exit when NIFTY moves this % from open (either direction).
                       E.g., 0.5 = exit when NIFTY moves 0.5% up or down from open.
                       Calculates actual strategy P&L at the move level. None = disabled.
                       Priority: move_exit > SL/TP (if move triggers, it overrides SL/TP logic).

    Returns:
        DataFrame with per-trade results including SL/TP/move exit tracking
    """
    # Resolve stop loss config
    if stop_loss_pct is None and getattr(config, 'STOP_LOSS_ENABLED', False):
        stop_loss_pct = getattr(config, 'STOP_LOSS_PCT', {})

    results = []

    for idx, row in df.iterrows():
        spot_open = row['nifty_open']
        spot_close = row['nifty_close']
        spot_high = row['nifty_high']
        spot_low = row['nifty_low']
        vix_open = row['vix_open']
        vix_close = row['vix_close']
        dte = row['days_to_expiry']

        # Pre-compute move exit levels for this day
        move_exit_triggered = False
        move_exit_spot = None
        if move_exit_pct is not None:
            move_threshold = spot_open * move_exit_pct / 100.0
            up_level = spot_open + move_threshold
            down_level = spot_open - move_threshold

            # Check if either level was hit intraday
            hit_up = spot_high >= up_level
            hit_down = spot_low <= down_level

            if hit_up and hit_down:
                # Both levels hit — use close direction as tiebreaker
                if spot_close >= spot_open:
                    move_exit_spot = up_level  # Likely went up first
                else:
                    move_exit_spot = down_level
                move_exit_triggered = True
            elif hit_up:
                move_exit_spot = up_level
                move_exit_triggered = True
            elif hit_down:
                move_exit_spot = down_level
                move_exit_triggered = True

        for strategy in strategies:
            daily_pnl = calculate_strategy_pnl(
                strategy, spot_open, spot_close, vix_open, vix_close,
                dte, config.SLIPPAGE_PER_LEG,
            )
            intraday_loss = calculate_intraday_max_loss(
                strategy, spot_open, spot_high, spot_low, vix_open, dte,
            )
            intraday_profit = calculate_intraday_max_profit(
                strategy, spot_open, spot_high, spot_low, vix_open, dte,
            )

            sl_hit = False
            tp_hit = False
            move_hit = False
            effective_pnl = daily_pnl
            sl_points_today = 0.0
            tp_points_today = 0.0
            exit_type = 'close'

            # Move exit takes priority — if NIFTY moved enough, exit at move level
            if move_exit_triggered and move_exit_spot is not None:
                move_pnl = calculate_pnl_at_spot(
                    strategy, spot_open, move_exit_spot, vix_open, dte,
                )
                # Only use move exit if it's a profit (the point is to lock in gains)
                if move_pnl > 0:
                    move_hit = True
                    effective_pnl = move_pnl
                    exit_type = 'move'

            # If move exit didn't apply, check SL/TP
            if not move_hit and stop_loss_pct:
                sl_pct = stop_loss_pct.get(strategy.name)
                if sl_pct is not None:
                    sl_points_today = spot_open * sl_pct / 100.0

                    if rr_ratio is not None:
                        tp_points_today = sl_points_today * rr_ratio

                    could_hit_sl = intraday_loss < -sl_points_today
                    could_hit_tp = rr_ratio is not None and intraday_profit >= tp_points_today

                    if could_hit_tp and could_hit_sl:
                        if daily_pnl >= 0:
                            tp_hit = True
                            effective_pnl = tp_points_today
                            exit_type = 'tp'
                        else:
                            sl_hit = True
                            effective_pnl = -sl_points_today
                            exit_type = 'sl'
                    elif could_hit_tp:
                        tp_hit = True
                        effective_pnl = tp_points_today
                        exit_type = 'tp'
                    elif could_hit_sl:
                        sl_hit = True
                        effective_pnl = -sl_points_today
                        exit_type = 'sl'

            results.append({
                'date': row['date'],
                'nifty_open': spot_open,
                'nifty_close': spot_close,
                'fii_view': row['fii_view'],
                'pro_view': row['pro_view'],
                'is_expiry': int(row['is_nifty_expiry']),
                'strategy_name': strategy.name,
                'daily_pnl': round(effective_pnl, 2),
                'pnl_per_lot_rs': round(effective_pnl * 25, 2),
                'intraday_max_loss': round(intraday_loss, 2),
                'intraday_max_profit': round(intraday_profit, 2),
                'sl_hit': sl_hit,
                'tp_hit': tp_hit,
                'move_exit': move_hit,
                'exit_type': exit_type,
                'sl_points': round(sl_points_today, 2),
                'tp_points': round(tp_points_today, 2),
                'vix_open': vix_open,
                'nifty_change_pct': round((spot_close - spot_open) / spot_open * 100, 2),
            })

    results_df = pd.DataFrame(results)

    results_df['cumulative_pnl'] = results_df.groupby('strategy_name')['daily_pnl'].cumsum().round(2)
    results_df['cumulative_pnl_rs'] = (results_df['cumulative_pnl'] * 25).round(2)

    return results_df
