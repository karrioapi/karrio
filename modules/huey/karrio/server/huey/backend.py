"""
Huey Task Backend

Wraps the existing Huey task queue as a TaskBackend implementation.
This is the default backend — all existing behavior is preserved.

For tasks still using @db_task (unmigrated), the backend delegates to
their Huey TaskWrapper objects. For tasks migrated to @background_task,
a generic Huey dispatcher enqueues them through the HUEY instance.
"""

import contextlib
import logging
import typing

from karrio.server.core.task_backend import TaskBackend, TaskLockError, get_handler

from huey.contrib.djhuey import HUEY as huey_instance
from huey.contrib.djhuey import db_periodic_task as huey_db_periodic_task
from huey.contrib.djhuey import db_task as huey_db_task
from huey.exceptions import TaskLockedException

logger = logging.getLogger(__name__)

_huey_wrappers: dict[str, typing.Any] = {}


def _ensure_huey_wrappers() -> None:
    """Lazily import and cache Huey TaskWrapper objects via TASK_DEFINITIONS discovery.

    Uses the same discovery mechanism as karrio.server.events.tasks — iterates
    all registered TASK_DEFINITIONS and caches wrappers that expose Huey's
    `call_local` + `revoke` interface.
    """
    if _huey_wrappers:
        return

    try:
        import karrio.server.events.tasks as tasks_module

        for wrapper in getattr(tasks_module, "TASK_DEFINITIONS", []):
            if hasattr(wrapper, "call_local") and hasattr(wrapper, "revoke"):
                _huey_wrappers[wrapper.task_class.__name__] = wrapper
    except ImportError:
        logger.debug("karrio.server.events.tasks not available — Huey wrappers not loaded")


# ─────────────────────────────────────────────────────────────────
# Generic dispatcher — registered eagerly at module level so that
# both the API process (enqueue side) and the Huey worker process
# (consumer side) have it in the TaskRegistry at import time.
# ─────────────────────────────────────────────────────────────────


@huey_db_task()
def _huey_generic_dispatch(task_name, args_list, kwargs_dict):
    handler = get_handler(task_name)
    handler(*args_list, **kwargs_dict)


class HueyBackend(TaskBackend):
    """Backend that delegates to Huey's existing task infrastructure."""

    def enqueue(
        self,
        task_name: str,
        args: tuple,
        kwargs: dict,
        *,
        queue: str | None = None,
        retries: int = 0,
        retry_delay: int = 60,
    ) -> str:
        _ensure_huey_wrappers()

        wrapper = _huey_wrappers.get(task_name)
        if wrapper is not None:
            result = wrapper(*args, **kwargs)
            return getattr(result, "id", str(result)) if result else ""

        result = _huey_generic_dispatch(task_name, list(args), dict(kwargs))

        logger.debug(
            "HueyBackend: dispatched migrated task '%s' via generic dispatcher",
            task_name,
        )

        return getattr(result, "id", str(result)) if result else ""

    def lock_task(self, name: str) -> contextlib.AbstractContextManager:
        """Acquire a named task lock via Huey's Redis-backed lock.

        Raises TaskLockError if the lock is already held.
        """
        return _HueyLockContext(name)

    def register_periodic(
        self,
        func: typing.Callable,
        *,
        name: str | None = None,
        minute: str = "*",
        hour: str = "*",
        day: str = "*",
        month: str = "*",
        day_of_week: str = "*",
    ) -> typing.Callable:
        """Register a periodic task with Huey's cron scheduler."""
        from huey import crontab

        schedule = crontab(
            minute=minute,
            hour=hour,
            day=day,
            month=month,
            day_of_week=day_of_week,
        )

        task_name = name or func.__name__

        @huey_db_periodic_task(schedule, name=task_name)
        def _wrapper():
            func()

        logger.debug("HueyBackend: registered periodic task '%s'", task_name)
        return _wrapper

    def start_consumer(self, queues: list[str] | None = None) -> None:
        raise NotImplementedError(
            "HueyBackend consumer is managed by 'karrio run_huey'. Do not call start_consumer() directly."
        )

    def shutdown(self, timeout: int = 30) -> None:
        pass


class _HueyLockContext:
    """Context manager that wraps Huey's task lock, translating its
    exception to the generic TaskLockError."""

    def __init__(self, name: str):
        self._lock = huey_instance.lock_task(name)

    def __enter__(self):
        try:
            return self._lock.__enter__()
        except TaskLockedException:
            raise TaskLockError(f"Task lock '{self._lock}' is already held") from None

    def __exit__(self, *exc_info):
        return self._lock.__exit__(*exc_info)
