"""Option pricing with real data lookup and Black-Scholes fallback."""
import logging
from typing import Optional

from web.backend.data import cache
from web.backend.data.upstox_fetcher import UpstoxHistoricalFetcher
from option_backtester.pricing import estimate_premium, calculate_atm_strike

logger = logging.getLogger(__name__)

# Module-level fetcher shared across pricing calls so instruments master and HTTP
# clients are reused. Populated lazily on first intraday fetch.
_fetcher: Optional[UpstoxHistoricalFetcher] = None


async def _get_fetcher() -> UpstoxHistoricalFetcher:
    global _fetcher
    if _fetcher is None:
        _fetcher = UpstoxHistoricalFetcher()
        await _fetcher.fetch_instruments_master()
    return _fetcher


def _bucket_1m_to_5m(candles: list[dict]) -> list[dict]:
    """Aggregate 1-minute candles into 5-minute buckets aligned on 09:15/09:20/..."""
    if not candles:
        return []
    buckets: dict[str, list[dict]] = {}
    for c in candles:
        h, m = c["time"].split(":")
        bucket_min = (int(m) // 5) * 5
        key = f"{h}:{bucket_min:02d}"
        buckets.setdefault(key, []).append(c)
    out = []
    for key in sorted(buckets.keys()):
        rows = buckets[key]
        out.append({
            "time": key,
            "open": rows[0]["open"],
            "high": max(r["high"] for r in rows),
            "low": min(r["low"] for r in rows),
            "close": rows[-1]["close"],
        })
    return out


async def _ensure_intraday_cached(instrument: str, dt: str, strike: float,
                                    option_type: str, expiry: str) -> bool:
    """Fetch 5-minute option candles from Upstox and cache them, once per option.

    Tries the live instruments master first; falls back to Upstox's
    expired-instruments endpoint using the NSE token stored during the
    bhavcopy backfill.

    Returns True if the cache now has intraday data for this option, else False.
    """
    if await cache.has_intraday_data(instrument, dt, strike, option_type, expiry):
        return True
    try:
        fetcher = await _get_fetcher()
    except Exception as e:
        logger.debug(f"Fetcher init failed for intraday {instrument} {dt}: {e}")
        return False
    if not fetcher.is_authenticated():
        return False

    candles: list[dict] = []
    inst_key = fetcher._resolve_instrument_key(instrument, strike, expiry, option_type)
    if inst_key:
        try:
            candles = await fetcher.fetch_option_intraday(inst_key, dt, "minutes", 5)
        except Exception as e:
            logger.debug(f"Live intraday fetch failed for {inst_key} on {dt}: {e}")

    if not candles:
        # Fallback: expired-instruments endpoint. Needs the NSE token which
        # bhavcopy backfill stored in option_premiums.nse_token.
        premium_row = await cache.get_option_premium(instrument, dt, strike, option_type, expiry)
        token = (premium_row or {}).get("nse_token")
        if token:
            exchange_prefix = "BSE_FO" if instrument == "SENSEX" else "NSE_FO"
            try:
                # v2 endpoint only accepts 1minute / 30minute / day; use 1minute
                # and downsample to 5-min buckets for cache parity.
                raw = await fetcher.fetch_expired_option_intraday(
                    exchange_prefix, int(token), expiry, dt, "1minute"
                )
                candles = _bucket_1m_to_5m(raw)
            except Exception as e:
                logger.debug(f"Expired intraday fetch failed for {instrument} {expiry} {strike}{option_type}: {e}")

    if not candles:
        return False
    rows = [
        {
            "instrument": instrument,
            "date": dt,
            "strike": strike,
            "option_type": option_type,
            "expiry": expiry,
            "time": c["time"],
            "open": c["open"],
            "high": c["high"],
            "low": c["low"],
            "close": c["close"],
        }
        for c in candles
    ]
    await cache.insert_intraday_batch(rows)
    return True


async def get_option_price(instrument: str, dt: str, strike: float,
                            option_type: str, expiry: str,
                            time_of_day: str = "open",
                            vix: float = 15.0,
                            days_to_expiry: float = 5.0,
                            time_hhmm: Optional[str] = None) -> dict:
    """Get option price, preferring real data over Black-Scholes estimation.

    When ``time_hhmm`` is provided (e.g. "09:20"), the 1-minute candle at or
    after that time is used — which matches the user's configured entry/exit
    time. Falls back to daily open/close, then Black-Scholes.
    """
    # Prefer the specific intraday minute when a time is requested
    if time_hhmm:
        if await _ensure_intraday_cached(instrument, dt, strike, option_type, expiry):
            candle = await cache.get_intraday_candle_at_or_after(
                instrument, dt, strike, option_type, expiry, time_hhmm
            )
            if candle and candle.get("open") is not None:
                return {"price": candle["open"], "source": "real"}

    # Fall back to the daily premium (open/close/high/low).
    # If the caller wants a specific intraday time and we have a calibrated
    # IV for this contract, defer the "real"-source shortcut and use
    # BS-with-calibrated-IV at the intraday spot below — that's a much better
    # answer than returning the 9:15 open for a 15:14 entry.
    premium = await cache.get_option_premium(instrument, dt, strike, option_type, expiry)

    if premium and not (time_hhmm and premium.get("implied_vol")):
        if time_of_day == "open" and premium.get("open_premium") is not None:
            return {"price": premium["open_premium"], "source": "real"}
        elif time_of_day == "close" and premium.get("close_premium") is not None:
            return {"price": premium["close_premium"], "source": "real"}
        elif time_of_day == "high" and premium.get("high_premium") is not None:
            return {"price": premium["high_premium"], "source": "real"}
        elif time_of_day == "low" and premium.get("low_premium") is not None:
            return {"price": premium["low_premium"], "source": "real"}

    # Fallback to Black-Scholes estimation. Prefer spot at the requested time
    # from index_intraday if available, else the day's intraday cache lookup,
    # else the daily open/close. This keeps intraday-time behaviour realistic
    # for historical (bhavcopy-only) days.
    ohlcv = await cache.get_ohlcv(instrument, dt)
    spot: Optional[float] = None
    if time_hhmm:
        index_candle = await cache.get_index_intraday_at_or_after(instrument, dt, time_hhmm)
        if index_candle and index_candle.get("open") is not None:
            spot = float(index_candle["open"])
    if spot is None:
        if ohlcv and time_of_day == "open":
            spot = ohlcv["open"]
        elif ohlcv:
            spot = ohlcv["close"]
        else:
            spot = strike

    # Map option_type to pricing module format
    opt_type = "call" if option_type == "CE" else "put"

    # Prefer the per-contract calibrated IV (from bhavcopy close) over the
    # coarse VIX-derived estimate. This makes BS pricing consistent with the
    # observed close of that specific contract on that day.
    sigma_pct: float = vix
    skew = 1.0
    if premium and premium.get("implied_vol") is not None and premium["implied_vol"] > 0:
        sigma_pct = premium["implied_vol"] * 100.0  # estimate_premium expects "vix" scale
    else:
        # No calibrated IV — apply the coarse skew adjustment as before.
        atm = calculate_atm_strike(spot)
        offset = strike - atm
        if offset > 0 and opt_type == "call":
            skew = 0.95
        elif offset < 0 and opt_type == "put":
            skew = 1.10

    price = estimate_premium(spot, strike, sigma_pct, days_to_expiry, opt_type, skew)
    source = "iv_calibrated" if (premium and premium.get("implied_vol")) else "estimated"
    return {"price": max(price, 0.05), "source": source}


async def get_spot_price(instrument: str, dt: str,
                          time_of_day: str = "open") -> Optional[float]:
    """Get the spot/index price from OHLCV cache."""
    ohlcv = await cache.get_ohlcv(instrument, dt)
    if not ohlcv:
        return None
    if time_of_day == "open":
        return ohlcv["open"]
    elif time_of_day == "close":
        return ohlcv["close"]
    elif time_of_day == "high":
        return ohlcv["high"]
    elif time_of_day == "low":
        return ohlcv["low"]
    return ohlcv["close"]
