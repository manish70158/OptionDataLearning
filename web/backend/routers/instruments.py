"""Instruments metadata API router."""
from datetime import date, timedelta

from fastapi import APIRouter, HTTPException, Query

from web.backend.data.cache import (
    init_db, get_ohlcv_range, get_option_premiums_for_date, get_synced_date_range,
)
from web.backend.schemas import UnderlyingInfo

router = APIRouter(tags=["instruments"])

UNDERLYINGS = {
    "NIFTY": UnderlyingInfo(
        name="NIFTY",
        lot_size=65,
        strike_interval=50,
        trading_symbol="NIFTY 50",
    ),
    "BANKNIFTY": UnderlyingInfo(
        name="BANKNIFTY",
        lot_size=30,
        strike_interval=100,
        trading_symbol="NIFTY BANK",
    ),
    "SENSEX": UnderlyingInfo(
        name="SENSEX",
        lot_size=20,
        strike_interval=100,
        trading_symbol="SENSEX",
    ),
}


@router.get("/instruments/underlyings")
async def list_underlyings():
    """Return list of supported underlyings with metadata."""
    return list(UNDERLYINGS.values())


@router.get("/instruments/{underlying}/expiries")
async def list_expiries(underlying: str):
    """Return available expiry dates from cached data."""
    await init_db()
    underlying = underlying.upper()
    if underlying not in UNDERLYINGS:
        raise HTTPException(status_code=404, detail=f"Unknown underlying: {underlying}")

    range_info = await get_synced_date_range(underlying)
    if not range_info:
        return {"weekly": [], "monthly": [], "data_available": False}

    start = date.fromisoformat(range_info["first_date"])
    end = date.fromisoformat(range_info["last_date"])

    # Generate weekly expiries (Thursdays)
    weekly = []
    current = start
    while current <= end:
        days_to_thu = (3 - current.weekday()) % 7
        thursday = current + timedelta(days=days_to_thu)
        if thursday <= end and thursday not in weekly:
            weekly.append(thursday.isoformat())
        current = thursday + timedelta(days=1)

    # Generate monthly expiries (last Thursday of each month)
    import calendar
    monthly = []
    current_year = start.year
    current_month = start.month
    while date(current_year, current_month, 1) <= end:
        last_day = calendar.monthrange(current_year, current_month)[1]
        last_date = date(current_year, current_month, last_day)
        while last_date.weekday() != 3:
            last_date -= timedelta(days=1)
        if start <= last_date <= end:
            monthly.append(last_date.isoformat())
        if current_month == 12:
            current_year += 1
            current_month = 1
        else:
            current_month += 1

    return {"weekly": weekly, "monthly": monthly, "data_available": True}


@router.get("/instruments/{underlying}/strikes")
async def list_strikes(
    underlying: str,
    dt: str = Query(..., alias="date", description="Trading date YYYY-MM-DD"),
    expiry_date: str = Query(..., description="Expiry date YYYY-MM-DD"),
):
    """Return available strikes for a given date and expiry."""
    await init_db()
    underlying = underlying.upper()
    if underlying not in UNDERLYINGS:
        raise HTTPException(status_code=404, detail=f"Unknown underlying: {underlying}")

    from option_backtester.pricing import calculate_atm_strike
    from web.backend.data.cache import get_ohlcv

    ohlcv = await get_ohlcv(underlying, dt)
    if not ohlcv:
        raise HTTPException(status_code=404, detail=f"No data available for {dt}")

    atm = calculate_atm_strike(ohlcv["open"])

    # Get available strikes from option premiums
    premiums = await get_option_premiums_for_date(underlying, dt, expiry_date)
    if premiums:
        strikes = sorted(set(p["strike"] for p in premiums))
    else:
        # Generate theoretical strikes
        info = UNDERLYINGS[underlying]
        interval = info.strike_interval
        range_pts = 1000 if underlying == "NIFTY" else 2000  # NIFTY narrower; BANKNIFTY/SENSEX wider
        strikes = []
        s = atm - range_pts
        while s <= atm + range_pts:
            strikes.append(s)
            s += interval

    return {"strikes": strikes, "atm_strike": atm}
