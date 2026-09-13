"""Data sync API router."""
import asyncio
import logging
import traceback
from datetime import date

from fastapi import APIRouter, HTTPException

from option_backtester.pricing import calculate_atm_strike
from web.backend.engine.pricing import _bucket_1m_to_5m
from web.backend.schemas import SyncRequest, TaskStatus
from web.backend.data.upstox_fetcher import UpstoxHistoricalFetcher, UpstoxAuthError
from web.backend.data.cache import (
    init_db, get_cache_stats, insert_option_premiums_batch,
    insert_intraday_batch, insert_index_intraday_batch,
    has_intraday_data, has_index_intraday,
)
from web.backend.data.iv_calibration import implied_vol
from web.backend.data.nse_bhavcopy import fetch_and_parse, business_days
from web.backend import tasks

logger = logging.getLogger(__name__)

router = APIRouter(tags=["data"])


@router.post("/data/sync", status_code=202)
async def start_data_sync(request: SyncRequest):
    """Start historical data sync as a background task."""
    await init_db()

    fetcher = UpstoxHistoricalFetcher()
    if not fetcher.is_authenticated():
        raise HTTPException(
            status_code=401,
            detail="Upstox credentials not configured. Set UPSTOX_API_KEY, UPSTOX_API_SECRET, and UPSTOX_ACCESS_TOKEN environment variables.",
        )

    task_id = tasks.create_task()
    tasks.update_task(task_id, status="running")

    async def _sync():
        try:
            callback = tasks.task_progress_callback(task_id)
            await fetcher.sync_data(
                request.underlying.value,
                request.start_date.isoformat(),
                request.end_date.isoformat(),
                progress_callback=callback,
            )
            tasks.update_task(task_id, status="completed", progress=100,
                              result={"message": "Data sync completed"})
        except UpstoxAuthError as e:
            tasks.update_task(task_id, status="failed", error=str(e))
        except Exception as e:
            logger.error(f"Data sync failed: {traceback.format_exc()}")
            tasks.update_task(task_id, status="failed", error=str(e))

    asyncio.create_task(_sync())
    return {"task_id": task_id}


@router.get("/data/sync/{task_id}/status")
async def get_sync_status(task_id: str):
    """Poll data sync task status."""
    task = tasks.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskStatus(task_id=task_id, **task)


@router.get("/data/status")
async def get_data_status():
    """Get current state of the historical data cache."""
    await init_db()
    stats = await get_cache_stats()
    return stats


@router.post("/data/backfill-bhavcopy", status_code=202)
async def backfill_bhavcopy(request: SyncRequest):
    """Backfill historical option premiums from NSE/BSE bhavcopy CSVs.

    Unlike the Upstox sync (which needs live instrument_keys and therefore
    can only fetch the current/future weekly for each date), this loads real
    OHLC data for every option contract that traded on each day — including
    already-expired weeklies. Populates ``option_premiums`` with the correct
    historical expiry.
    """
    await init_db()
    task_id = tasks.create_task()
    tasks.update_task(task_id, status="running")
    underlying = request.underlying.value

    # Prefetch config: number of strikes each side of ATM, and how many
    # nearest expiries to cover. Small enough to keep total time reasonable;
    # covers ATM straddles/strangles/condors within ±5 strikes.
    STRIKE_WINDOW = 5
    NUM_EXPIRIES = 2  # nearest weekly + one more (usually next-week weekly)
    STRIKE_INTERVAL = {"NIFTY": 50, "BANKNIFTY": 100, "SENSEX": 100}.get(underlying, 50)
    EXCHANGE_PREFIX = "BSE_FO" if underlying == "SENSEX" else "NSE_FO"

    async def _run():
        try:
            dates = business_days(request.start_date, request.end_date)
            total = len(dates)
            if total == 0:
                tasks.update_task(task_id, status="completed", progress=100,
                                  result={"message": "No trading days in range"})
                return

            fetcher = UpstoxHistoricalFetcher()
            upstox_ok = fetcher.is_authenticated()

            total_rows = 0
            intraday_fetched = 0
            intraday_failed = 0

            for i, dt in enumerate(dates):
                dt_str = dt.isoformat()
                rows = await fetch_and_parse(dt, {underlying})
                if rows:
                    premium_rows = []
                    for r in rows:
                        try:
                            trade_dt = date.fromisoformat(r["trade_date"])
                            exp_dt = date.fromisoformat(r["expiry"])
                            dte = max((exp_dt - trade_dt).days, 0.5)
                        except ValueError:
                            dte = 1.0
                        opt_type_bs = "call" if r["option_type"] == "CE" else "put"
                        iv = None
                        if r.get("underlying_close") and r.get("close"):
                            iv = implied_vol(
                                r["underlying_close"], r["strike"], r["close"],
                                dte, opt_type_bs,
                            )
                        premium_rows.append({
                            "instrument": r["underlying"],
                            "date": r["trade_date"],
                            "expiry": r["expiry"],
                            "strike": r["strike"],
                            "option_type": r["option_type"],
                            "open_premium": r["open"],
                            "close_premium": r["close"],
                            "high_premium": r["high"],
                            "low_premium": r["low"],
                            "implied_vol": iv,
                            "underlying_close": r.get("underlying_close"),
                            "nse_token": r.get("nse_token") or None,
                        })
                    await insert_option_premiums_batch(premium_rows)
                    total_rows += len(premium_rows)

                    # --- Prefetch index intraday + real 5-min for ATM ± window ---
                    if upstox_ok:
                        # Index 5-min intraday (spot journey) for the day
                        if not await has_index_intraday(underlying, dt_str):
                            try:
                                index_candles = await fetcher.fetch_index_intraday(
                                    underlying, dt_str, "minutes", 5
                                )
                                if index_candles:
                                    await insert_index_intraday_batch([
                                        {
                                            "instrument": underlying,
                                            "date": dt_str,
                                            **c,
                                        }
                                        for c in index_candles
                                    ])
                            except Exception as e:
                                logger.debug(f"Index intraday fetch failed {dt_str}: {e}")

                        # Pick the nearest N expiries relative to trade date
                        by_expiry: dict[str, list[dict]] = {}
                        for r in premium_rows:
                            by_expiry.setdefault(r["expiry"], []).append(r)
                        upcoming = sorted(
                            [e for e in by_expiry if e >= dt_str]
                        )[:NUM_EXPIRIES]
                        # ATM strike from bhavcopy underlying close
                        atm = None
                        for r in premium_rows:
                            if r.get("underlying_close"):
                                atm = calculate_atm_strike(r["underlying_close"], STRIKE_INTERVAL)
                                break

                        for exp in upcoming:
                            candidates = by_expiry[exp]
                            if atm is not None:
                                lo = atm - STRIKE_WINDOW * STRIKE_INTERVAL
                                hi = atm + STRIKE_WINDOW * STRIKE_INTERVAL
                                candidates = [c for c in candidates if lo <= c["strike"] <= hi]
                            for r in candidates:
                                if not r.get("nse_token"):
                                    continue
                                if await has_intraday_data(
                                    underlying, dt_str, r["strike"],
                                    r["option_type"], r["expiry"],
                                ):
                                    continue
                                try:
                                    raw = await fetcher.fetch_expired_option_intraday(
                                        EXCHANGE_PREFIX, int(r["nse_token"]),
                                        r["expiry"], dt_str, "1minute",
                                    )
                                    candles = _bucket_1m_to_5m(raw)
                                    if candles:
                                        await insert_intraday_batch([
                                            {
                                                "instrument": underlying,
                                                "date": dt_str,
                                                "strike": r["strike"],
                                                "option_type": r["option_type"],
                                                "expiry": r["expiry"],
                                                **c,
                                            }
                                            for c in candles
                                        ])
                                        intraday_fetched += 1
                                    else:
                                        intraday_failed += 1
                                except Exception as e:
                                    intraday_failed += 1
                                    logger.debug(
                                        f"Expired intraday fetch failed "
                                        f"{underlying} {r['expiry']} {r['strike']}{r['option_type']} {dt_str}: {e}"
                                    )

                pct = int((i + 1) / total * 100)
                tasks.update_task(
                    task_id, status="running", progress=pct,
                    result={"message": (
                        f"{dt}: {len(rows)} daily rows | intraday cached: "
                        f"{intraday_fetched} ok, {intraday_failed} skipped"
                    )},
                )

            tasks.update_task(
                task_id, status="completed", progress=100,
                result={"message": (
                    f"Backfilled {total_rows} daily rows across {total} trading days; "
                    f"{intraday_fetched} contracts have real 5-min intraday cached "
                    f"({intraday_failed} skipped due to fetch failure — will fall back to BS)."
                )},
            )
        except Exception as e:
            logger.error(f"Bhavcopy backfill failed: {traceback.format_exc()}")
            tasks.update_task(task_id, status="failed", error=str(e))

    asyncio.create_task(_run())
    return {"task_id": task_id}
