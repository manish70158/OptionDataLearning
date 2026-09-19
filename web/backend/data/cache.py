"""Async SQLite cache layer for historical data."""
import json
import os
import uuid
from datetime import datetime, date
from typing import Optional

import aiosqlite

from web.backend.data.models import TABLES, INDICES

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "cache.db")


async def get_db() -> aiosqlite.Connection:
    """Get a database connection."""
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    return db


async def init_db():
    """Create all tables and indices if they don't exist."""
    db = await get_db()
    try:
        for table_sql in TABLES.values():
            await db.execute(table_sql)
        for index_sql in INDICES:
            await db.execute(index_sql)
        await db.commit()
    finally:
        await db.close()


async def insert_ohlcv(instrument: str, dt: str, open_: float, high: float,
                        low: float, close: float, volume: int = 0,
                        interval: str = "day"):
    """Insert or replace an OHLCV candle."""
    db = await get_db()
    try:
        await db.execute(
            """INSERT OR REPLACE INTO ohlcv_candles
               (instrument, date, interval, open, high, low, close, volume)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (instrument, dt, interval, open_, high, low, close, volume),
        )
        await db.commit()
    finally:
        await db.close()


async def insert_ohlcv_batch(rows: list[dict]):
    """Insert multiple OHLCV candles in one transaction."""
    if not rows:
        return
    db = await get_db()
    try:
        await db.executemany(
            """INSERT OR REPLACE INTO ohlcv_candles
               (instrument, date, interval, open, high, low, close, volume)
               VALUES (:instrument, :date, :interval, :open, :high, :low, :close, :volume)""",
            rows,
        )
        await db.commit()
    finally:
        await db.close()


async def insert_option_premiums(instrument: str, dt: str, expiry: str,
                                  strike: float, option_type: str,
                                  open_premium: Optional[float] = None,
                                  close_premium: Optional[float] = None,
                                  high_premium: Optional[float] = None,
                                  low_premium: Optional[float] = None):
    """Insert or replace an option premium record."""
    db = await get_db()
    try:
        await db.execute(
            """INSERT OR REPLACE INTO option_premiums
               (instrument, date, expiry, strike, option_type,
                open_premium, close_premium, high_premium, low_premium)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (instrument, dt, expiry, strike, option_type,
             open_premium, close_premium, high_premium, low_premium),
        )
        await db.commit()
    finally:
        await db.close()


async def insert_option_premiums_batch(rows: list[dict]):
    """Insert multiple option premium records in one transaction. Rows may
    optionally carry ``implied_vol`` and ``underlying_close`` for calibrated
    intraday BS pricing."""
    if not rows:
        return
    # Normalise: ensure all optional columns exist so the executemany bind works.
    for r in rows:
        r.setdefault("implied_vol", None)
        r.setdefault("underlying_close", None)
        r.setdefault("nse_token", None)
    db = await get_db()
    try:
        await db.executemany(
            """INSERT OR REPLACE INTO option_premiums
               (instrument, date, expiry, strike, option_type,
                open_premium, close_premium, high_premium, low_premium,
                implied_vol, underlying_close, nse_token)
               VALUES (:instrument, :date, :expiry, :strike, :option_type,
                        :open_premium, :close_premium, :high_premium, :low_premium,
                        :implied_vol, :underlying_close, :nse_token)""",
            rows,
        )
        await db.commit()
    finally:
        await db.close()


async def get_ohlcv(instrument: str, dt: str, interval: str = "day") -> Optional[dict]:
    """Get OHLCV data for an instrument on a specific date."""
    db = await get_db()
    try:
        cursor = await db.execute(
            """SELECT * FROM ohlcv_candles
               WHERE instrument = ? AND date = ? AND interval = ?""",
            (instrument, dt, interval),
        )
        row = await cursor.fetchone()
        return dict(row) if row else None
    finally:
        await db.close()


async def get_ohlcv_range(instrument: str, start_date: str, end_date: str,
                           interval: str = "day") -> list[dict]:
    """Get OHLCV data for an instrument over a date range."""
    db = await get_db()
    try:
        cursor = await db.execute(
            """SELECT * FROM ohlcv_candles
               WHERE instrument = ? AND date >= ? AND date <= ? AND interval = ?
               ORDER BY date""",
            (instrument, start_date, end_date, interval),
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]
    finally:
        await db.close()


async def insert_intraday_batch(rows: list[dict]):
    """Insert multiple intraday option candles in one transaction."""
    if not rows:
        return
    db = await get_db()
    try:
        await db.executemany(
            """INSERT OR REPLACE INTO intraday_candles
               (instrument, date, strike, option_type, expiry, time, open, high, low, close)
               VALUES (:instrument, :date, :strike, :option_type, :expiry, :time,
                       :open, :high, :low, :close)""",
            rows,
        )
        await db.commit()
    finally:
        await db.close()


async def get_intraday_candle_at_or_after(instrument: str, dt: str, strike: float,
                                            option_type: str, expiry: str,
                                            time_str: str) -> Optional[dict]:
    """Get the first intraday candle at or after a given time (HH:MM)."""
    db = await get_db()
    try:
        cursor = await db.execute(
            """SELECT * FROM intraday_candles
               WHERE instrument = ? AND date = ? AND strike = ?
               AND option_type = ? AND expiry = ? AND time >= ?
               ORDER BY time ASC LIMIT 1""",
            (instrument, dt, strike, option_type, expiry, time_str),
        )
        row = await cursor.fetchone()
        return dict(row) if row else None
    finally:
        await db.close()


async def get_intraday_candles_between(instrument: str, dt: str, strike: float,
                                        option_type: str, expiry: str,
                                        start_time: str, end_time: str) -> list[dict]:
    """All intraday candles for this option between start_time and end_time (inclusive), ordered by time."""
    db = await get_db()
    try:
        cursor = await db.execute(
            """SELECT time, open, high, low, close FROM intraday_candles
               WHERE instrument = ? AND date = ? AND strike = ?
               AND option_type = ? AND expiry = ?
               AND time >= ? AND time <= ?
               ORDER BY time ASC""",
            (instrument, dt, strike, option_type, expiry, start_time, end_time),
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]
    finally:
        await db.close()


async def has_intraday_data(instrument: str, dt: str, strike: float,
                             option_type: str, expiry: str) -> bool:
    """Check whether any intraday candles exist for this option on this date."""
    db = await get_db()
    try:
        cursor = await db.execute(
            """SELECT 1 FROM intraday_candles
               WHERE instrument = ? AND date = ? AND strike = ?
               AND option_type = ? AND expiry = ? LIMIT 1""",
            (instrument, dt, strike, option_type, expiry),
        )
        row = await cursor.fetchone()
        return row is not None
    finally:
        await db.close()


async def insert_index_intraday_batch(rows: list[dict]):
    """Insert multiple 5-min index candles."""
    if not rows:
        return
    db = await get_db()
    try:
        await db.executemany(
            """INSERT OR REPLACE INTO index_intraday
               (instrument, date, time, open, high, low, close)
               VALUES (:instrument, :date, :time, :open, :high, :low, :close)""",
            rows,
        )
        await db.commit()
    finally:
        await db.close()


async def get_index_intraday_at_or_after(instrument: str, dt: str,
                                          time_str: str) -> Optional[dict]:
    """First 5-min index candle at or after a given time (HH:MM)."""
    db = await get_db()
    try:
        cursor = await db.execute(
            """SELECT * FROM index_intraday
               WHERE instrument = ? AND date = ? AND time >= ?
               ORDER BY time ASC LIMIT 1""",
            (instrument, dt, time_str),
        )
        row = await cursor.fetchone()
        return dict(row) if row else None
    finally:
        await db.close()


async def has_index_intraday(instrument: str, dt: str) -> bool:
    """Check whether any 5-min index candles exist for this date."""
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT 1 FROM index_intraday WHERE instrument = ? AND date = ? LIMIT 1",
            (instrument, dt),
        )
        row = await cursor.fetchone()
        return row is not None
    finally:
        await db.close()


async def get_option_premium(instrument: str, dt: str, strike: float,
                              option_type: str, expiry: str) -> Optional[dict]:
    """Get option premium for a specific strike/type/date/expiry."""
    db = await get_db()
    try:
        cursor = await db.execute(
            """SELECT * FROM option_premiums
               WHERE instrument = ? AND date = ? AND strike = ?
               AND option_type = ? AND expiry = ?""",
            (instrument, dt, strike, option_type, expiry),
        )
        row = await cursor.fetchone()
        return dict(row) if row else None
    finally:
        await db.close()


async def get_option_premiums_for_date(instrument: str, dt: str,
                                        expiry: str) -> list[dict]:
    """Get all option premiums for a date and expiry."""
    db = await get_db()
    try:
        cursor = await db.execute(
            """SELECT * FROM option_premiums
               WHERE instrument = ? AND date = ? AND expiry = ?
               ORDER BY strike, option_type""",
            (instrument, dt, expiry),
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]
    finally:
        await db.close()


async def get_synced_date_range(instrument: str) -> Optional[dict]:
    """Get the synced date range for an instrument."""
    db = await get_db()
    try:
        cursor = await db.execute(
            """SELECT MIN(date) as first_date, MAX(date) as last_date,
                      COUNT(DISTINCT date) as trading_days
               FROM ohlcv_candles WHERE instrument = ? AND interval = 'day'""",
            (instrument,),
        )
        row = await cursor.fetchone()
        if row and row["first_date"]:
            return dict(row)
        return None
    finally:
        await db.close()


async def get_missing_dates(instrument: str, start_date: str,
                             end_date: str) -> list[str]:
    """Get dates in range that are NOT in the cache."""
    db = await get_db()
    try:
        cursor = await db.execute(
            """SELECT DISTINCT date FROM ohlcv_candles
               WHERE instrument = ? AND date >= ? AND date <= ? AND interval = 'day'
               ORDER BY date""",
            (instrument, start_date, end_date),
        )
        rows = await cursor.fetchall()
        cached_dates = {row["date"] for row in rows}

        # Generate all weekdays in range
        from datetime import timedelta
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
        all_dates = []
        current = start
        while current <= end:
            if current.weekday() < 5:  # Mon-Fri
                all_dates.append(current.isoformat())
            current += timedelta(days=1)

        return [d for d in all_dates if d not in cached_dates]
    finally:
        await db.close()


async def log_sync(instrument: str, start_date: str, end_date: str,
                    status: str = "completed"):
    """Log a completed data sync."""
    db = await get_db()
    try:
        await db.execute(
            """INSERT INTO sync_log (instrument, start_date, end_date, synced_at, status)
               VALUES (?, ?, ?, ?, ?)""",
            (instrument, start_date, end_date, datetime.utcnow().isoformat(), status),
        )
        await db.commit()
    finally:
        await db.close()


async def get_last_sync(instrument: str) -> Optional[dict]:
    """Get the last sync log entry for an instrument."""
    db = await get_db()
    try:
        cursor = await db.execute(
            """SELECT * FROM sync_log
               WHERE instrument = ? ORDER BY synced_at DESC LIMIT 1""",
            (instrument,),
        )
        row = await cursor.fetchone()
        return dict(row) if row else None
    finally:
        await db.close()


# Saved backtests

async def save_backtest(strategy_config: dict, backtest_config: dict,
                         results: dict) -> str:
    """Save a backtest result. Returns the backtest ID."""
    backtest_id = str(uuid.uuid4())
    db = await get_db()
    try:
        await db.execute(
            """INSERT INTO saved_backtests (id, strategy_config, backtest_config, results, created_at)
               VALUES (?, ?, ?, ?, ?)""",
            (backtest_id, json.dumps(strategy_config), json.dumps(backtest_config),
             json.dumps(results), datetime.utcnow().isoformat()),
        )
        await db.commit()
    finally:
        await db.close()
    return backtest_id


async def get_saved_backtest(backtest_id: str) -> Optional[dict]:
    """Get a saved backtest by ID."""
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT * FROM saved_backtests WHERE id = ?", (backtest_id,)
        )
        row = await cursor.fetchone()
        if row:
            data = dict(row)
            data["strategy_config"] = json.loads(data["strategy_config"])
            data["backtest_config"] = json.loads(data["backtest_config"])
            data["results"] = json.loads(data["results"])
            return data
        return None
    finally:
        await db.close()


async def upsert_upstox_credentials(access_token: str, refresh_token: Optional[str] = None,
                                     expires_at: Optional[str] = None):
    """Store/refresh the Upstox OAuth token. Single-row table (id=1)."""
    db = await get_db()
    try:
        await db.execute(
            """INSERT INTO upstox_credentials (id, access_token, refresh_token, expires_at, updated_at)
               VALUES (1, ?, ?, ?, ?)
               ON CONFLICT(id) DO UPDATE SET
                 access_token=excluded.access_token,
                 refresh_token=excluded.refresh_token,
                 expires_at=excluded.expires_at,
                 updated_at=excluded.updated_at""",
            (access_token, refresh_token, expires_at, datetime.utcnow().isoformat()),
        )
        await db.commit()
    finally:
        await db.close()


async def get_upstox_credentials() -> Optional[dict]:
    """Return the persisted Upstox OAuth token, or None if never authorised."""
    db = await get_db()
    try:
        cursor = await db.execute("SELECT * FROM upstox_credentials WHERE id = 1")
        row = await cursor.fetchone()
        return dict(row) if row else None
    finally:
        await db.close()


async def get_cache_stats() -> dict:
    """Get overall cache statistics."""
    db = await get_db()
    try:
        stats = {}
        for instrument in ["NIFTY", "BANKNIFTY", "SENSEX"]:
            cursor = await db.execute(
                """SELECT MIN(date) as first_date, MAX(date) as last_date,
                          COUNT(DISTINCT date) as trading_days
                   FROM ohlcv_candles WHERE instrument = ? AND interval = 'day'""",
                (instrument,),
            )
            row = await cursor.fetchone()
            sync_cursor = await db.execute(
                "SELECT synced_at FROM sync_log WHERE instrument = ? ORDER BY synced_at DESC LIMIT 1",
                (instrument,),
            )
            sync_row = await sync_cursor.fetchone()

            stats[instrument] = {
                "first_date": row["first_date"] if row else None,
                "last_date": row["last_date"] if row else None,
                "trading_days_count": row["trading_days"] if row else 0,
                "last_sync_timestamp": sync_row["synced_at"] if sync_row else None,
            }

        # Get cache file size
        cache_size_mb = 0
        if os.path.exists(DB_PATH):
            cache_size_mb = round(os.path.getsize(DB_PATH) / (1024 * 1024), 2)
        stats["cache_size_mb"] = cache_size_mb

        return stats
    finally:
        await db.close()
