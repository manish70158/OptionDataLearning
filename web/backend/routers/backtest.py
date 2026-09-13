"""Backtest API router."""
import asyncio
import logging
import traceback

from fastapi import APIRouter, HTTPException

from web.backend.schemas import BacktestRequest, TaskStatus
from web.backend.engine.simulator import run_backtest
from web.backend.data.cache import save_backtest, get_saved_backtest, init_db
from web.backend import tasks

logger = logging.getLogger(__name__)

router = APIRouter(tags=["backtest"])


@router.post("/backtest", status_code=202)
async def start_backtest(request: BacktestRequest):
    """Start a backtest as a background task. Returns task_id for polling."""
    await init_db()
    task_id = tasks.create_task()
    tasks.update_task(task_id, status="running")

    async def _run():
        try:
            callback = tasks.task_progress_callback(task_id)
            result = await run_backtest(request.strategy, request.config, callback)
            result_dict = result.model_dump()

            # Auto-save the backtest
            backtest_id = await save_backtest(
                request.strategy.model_dump(),
                request.config.model_dump(mode="json"),
                result_dict,
            )
            result_dict["backtest_id"] = backtest_id

            tasks.update_task(task_id, status="completed", progress=100, result=result_dict)
        except Exception as e:
            logger.error(f"Backtest failed: {traceback.format_exc()}")
            tasks.update_task(task_id, status="failed", error=str(e))

    asyncio.create_task(_run())
    return {"task_id": task_id}


@router.get("/backtest/{task_id}/status")
async def get_backtest_status(task_id: str):
    """Poll backtest task status."""
    task = tasks.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskStatus(task_id=task_id, **task)


@router.get("/backtest/saved/{backtest_id}")
async def get_saved_backtest_result(backtest_id: str):
    """Retrieve a previously saved backtest."""
    await init_db()
    result = await get_saved_backtest(backtest_id)
    if not result:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return result
