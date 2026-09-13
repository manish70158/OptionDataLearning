"""In-memory task registry for background operations."""
import uuid
from typing import Any, Optional


_tasks: dict[str, dict] = {}


def create_task() -> str:
    """Create a new task and return its ID."""
    task_id = str(uuid.uuid4())[:8]
    _tasks[task_id] = {
        "status": "pending",
        "progress": 0,
        "result": None,
        "error": None,
    }
    return task_id


def update_task(task_id: str, status: Optional[str] = None,
                progress: Optional[int] = None,
                result: Optional[Any] = None,
                error: Optional[str] = None):
    """Update a task's state."""
    if task_id not in _tasks:
        return
    if status is not None:
        _tasks[task_id]["status"] = status
    if progress is not None:
        _tasks[task_id]["progress"] = progress
    if result is not None:
        _tasks[task_id]["result"] = result
    if error is not None:
        _tasks[task_id]["error"] = error


def get_task(task_id: str) -> Optional[dict]:
    """Get a task's current state."""
    return _tasks.get(task_id)


def task_progress_callback(task_id: str):
    """Return a progress callback for use in async operations."""
    def callback(progress: int, total: int, message: str):
        pct = int(progress / total * 100) if total > 0 else progress
        update_task(task_id, progress=pct)
    return callback
