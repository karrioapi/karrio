"""
Immediate Task Backend

Executes tasks synchronously in the calling process.
Used for tests (replaces WORKER_IMMEDIATE_MODE / HUEY.immediate = True).

Exceptions from handlers are caught and logged (not propagated),
matching Huey's immediate mode behavior where task failures don't
crash the enqueuing caller.
"""

import logging
import uuid

from karrio.server.core.task_backend import TaskBackend, get_handler

logger = logging.getLogger(__name__)


class ImmediateBackend(TaskBackend):
    """Backend that runs task handlers synchronously in-process.

    No queue, no serialization, no worker process.
    Exceptions are caught and logged to match Huey's immediate mode
    behavior — the caller is not affected by task failures.
    """

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
        task_id = str(uuid.uuid4())

        logger.debug("ImmediateBackend: executing '%s' synchronously", task_name)

        try:
            handler = get_handler(task_name)
            handler(*args, **kwargs)
        except Exception as e:
            logger.error("ImmediateBackend: task '%s' failed: %s", task_name, e)

        return task_id

    def start_consumer(self, queues: list[str] | None = None) -> None:
        logger.info("ImmediateBackend: no consumer needed (tasks run inline)")

    def shutdown(self, timeout: int = 30) -> None:
        pass
