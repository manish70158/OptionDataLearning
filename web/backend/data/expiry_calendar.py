"""Historical expiry calendar for Indian index options.

Upstox's live instruments master only lists future/live contracts, so a
backtest over a date range predating the earliest live expiry can't resolve
the correct historical expiry. This module provides a rule-based fallback:
per-underlying weekly-expiry-weekday history plus a holiday list. Edit the
constants below if you need to backtest periods where the cadence differs
from what's encoded here.

Weekday convention: Monday = 0, Tuesday = 1, ..., Friday = 4.
"""
from datetime import date, timedelta
from typing import Optional

# Each list is sorted ascending by `effective_from`. The last entry whose
# `effective_from <= dt` gives the weekday active on `dt`. Use `None` as the
# weekday to signal "no weekly cadence in this regime" (e.g. BANKNIFTY after
# the SEBI consolidation in Nov 2024).
WEEKLY_EXPIRY_WEEKDAY: dict[str, list[tuple[date, Optional[int]]]] = {
    # NIFTY weeklies launched Feb 2019 on Thursday. SEBI's Nov 2024 framework
    # briefly moved NIFTY to Wednesday; reverted; latest cadence is Tuesday
    # (effective Sep 2025). Adjust these transition dates if you know them
    # precisely for your backtest window.
    "NIFTY": [
        (date(2019, 2, 11), 3),   # Thursday (launch)
        (date(2024, 11, 20), 2),  # Wednesday
        (date(2025, 4, 4), 3),    # Thursday (reverted)
        (date(2025, 9, 1), 1),    # Tuesday (current)
    ],
    # BANKNIFTY weeklies discontinued from Nov 20 2024; monthly-only after.
    "BANKNIFTY": [
        (date(2019, 2, 11), 3),   # Thursday
        (date(2024, 11, 20), None),  # weekly retired
    ],
    # SENSEX BSE weeklies launched around April 2023 on Friday; BSE later
    # moved to Tuesday. Placeholder dates below — refine as needed.
    "SENSEX": [
        (date(2023, 4, 10), 4),   # Friday (BSE launch cadence)
        (date(2024, 11, 18), 1),  # Tuesday (SEBI consolidation era)
    ],
}


# Monthly expiries fall on the last <weekday> of the month. Historically NIFTY /
# BANKNIFTY monthlies were the last Thursday. Post SEBI consolidation the
# monthly weekday tracks the current weekly weekday. This keeps things
# consistent with what the instruments master usually shows.
def _last_weekday_of_month(year: int, month: int, weekday: int) -> date:
    if month == 12:
        first_next = date(year + 1, 1, 1)
    else:
        first_next = date(year, month + 1, 1)
    d = first_next - timedelta(days=1)
    while d.weekday() != weekday:
        d -= timedelta(days=1)
    return d


# NSE / BSE market holidays. Approximate list — kept small on purpose; extend
# as your backtest window requires. Only dates that fall on the resolved
# weekday need to be listed here; the shift-back logic uses this set.
HOLIDAYS: set[date] = {
    # 2024
    date(2024, 1, 26), date(2024, 3, 8), date(2024, 3, 25), date(2024, 3, 29),
    date(2024, 4, 11), date(2024, 4, 17), date(2024, 5, 1), date(2024, 6, 17),
    date(2024, 7, 17), date(2024, 8, 15), date(2024, 10, 2), date(2024, 11, 1),
    date(2024, 11, 15), date(2024, 12, 25),
    # 2025
    date(2025, 2, 26), date(2025, 3, 14), date(2025, 3, 31), date(2025, 4, 10),
    date(2025, 4, 14), date(2025, 4, 18), date(2025, 5, 1), date(2025, 8, 15),
    date(2025, 8, 27), date(2025, 10, 2), date(2025, 10, 21), date(2025, 10, 22),
    date(2025, 11, 5), date(2025, 12, 25),
    # 2026
    date(2026, 1, 26), date(2026, 3, 3), date(2026, 3, 19), date(2026, 4, 1),
    date(2026, 4, 3), date(2026, 5, 1), date(2026, 6, 26), date(2026, 8, 15),
    date(2026, 8, 17), date(2026, 10, 2), date(2026, 10, 20), date(2026, 11, 4),
    date(2026, 12, 25),
}


def _weekday_for(dt: date, underlying: str) -> Optional[int]:
    """Return the weekly-expiry weekday active on `dt` for the underlying."""
    history = WEEKLY_EXPIRY_WEEKDAY.get(underlying, [])
    applicable: Optional[int] = None
    for effective_from, wd in history:
        if dt >= effective_from:
            applicable = wd
        else:
            break
    return applicable


def _shift_back_if_holiday(exp: date) -> date:
    """If `exp` is a holiday or weekend, move to the previous business day."""
    while exp in HOLIDAYS or exp.weekday() >= 5:
        exp -= timedelta(days=1)
    return exp


def historical_weekly_expiry(dt: date, underlying: str) -> Optional[date]:
    """Return the weekly expiry date active for a trade on `dt`.

    Rules:
    - Look up the weekly-expiry weekday active on `dt` from the calendar.
    - Return the next occurrence of that weekday on/after `dt`.
    - If that date is a holiday or weekend, shift back to the previous
      business day (standard exchange convention).
    - Returns None if there is no weekly cadence in that regime.
    """
    wd = _weekday_for(dt, underlying)
    if wd is None:
        return None
    days_ahead = (wd - dt.weekday()) % 7
    exp = dt + timedelta(days=days_ahead)
    return _shift_back_if_holiday(exp)


def historical_monthly_expiry(dt: date, underlying: str) -> Optional[date]:
    """Return the monthly expiry (last <weekday> of the month) for `dt`."""
    wd = _weekday_for(dt, underlying)
    if wd is None:
        # Fallback for BANKNIFTY-post-Nov-2024: monthly stays Thursday.
        wd = 3
    exp = _last_weekday_of_month(dt.year, dt.month, wd)
    if exp < dt:
        # Trade date is after this month's monthly; roll to next month.
        y, m = (dt.year, dt.month + 1) if dt.month < 12 else (dt.year + 1, 1)
        exp = _last_weekday_of_month(y, m, wd)
    return _shift_back_if_holiday(exp)


def historical_expiry(dt: date, underlying: str, expiry_type: str) -> Optional[date]:
    """Dispatch to weekly or monthly based on `expiry_type`."""
    if expiry_type == "monthly":
        return historical_monthly_expiry(dt, underlying)
    return historical_weekly_expiry(dt, underlying)
