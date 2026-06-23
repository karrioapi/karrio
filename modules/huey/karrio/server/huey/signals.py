"""
Huey signal handlers for task execution lifecycle tracking.

Wires into Huey's signal system to create/update TaskExecution records
in the admin module, enabling task monitoring via the admin GraphQL API.
"""

import logging

from django.db import models, transaction
from django.utils import timezone

logger = logging.getLogger(__name__)


def register_huey_signals():
    """Register Huey signal handlers to track task execution lifecycle.

    Uses split create/update pattern instead of update_or_create to avoid
    SELECT ... FOR UPDATE lock contention when multiple tasks are enqueued
    in rapid succession.
    """
    try:
        from huey.contrib.djhuey import HUEY as huey_instance
        from huey.signals import (
            SIGNAL_COMPLETE,
            SIGNAL_ENQUEUED,
            SIGNAL_ERROR,
            SIGNAL_EXECUTING,
            SIGNAL_EXPIRED,
            SIGNAL_RETRYING,
            SIGNAL_REVOKED,
        )
    except ImportError:
        logger.debug("Huey not available, skipping signal registration")
        return

    @huey_instance.signal(
        SIGNAL_ENQUEUED,
        SIGNAL_EXECUTING,
        SIGNAL_COMPLETE,
        SIGNAL_ERROR,
        SIGNAL_RETRYING,
        SIGNAL_REVOKED,
        SIGNAL_EXPIRED,
    )
    def task_signal_handler(signal, task, exc=None):
        # Wrap in its own savepoint so that IntegrityError (e.g. duplicate
        # task_id) does not abort the caller's transaction — PostgreSQL marks
        # the entire transaction as invalid after an unhandled error, even if
        # Python catches the exception.
        try:
            with transaction.atomic():
                _record_task_signal(signal, task, exc)
        except Exception:
            logger.exception("Failed to record task signal")


def _record_task_signal(signal, task, exc=None):
    """Record a task lifecycle event in the TaskExecution table."""
    from karrio.server.admin.worker.models import TaskExecution

    from huey.signals import (
        SIGNAL_COMPLETE,
        SIGNAL_ENQUEUED,
        SIGNAL_ERROR,
        SIGNAL_EXECUTING,
        SIGNAL_EXPIRED,
        SIGNAL_RETRYING,
        SIGNAL_REVOKED,
    )

    now = timezone.now()
    task_id = task.id
    task_name = task.name or "unknown"

    SIGNAL_STATUS_MAP = {
        SIGNAL_ENQUEUED: "queued",
        SIGNAL_EXECUTING: "executing",
        SIGNAL_COMPLETE: "complete",
        SIGNAL_ERROR: "error",
        SIGNAL_RETRYING: "retrying",
        SIGNAL_REVOKED: "revoked",
        SIGNAL_EXPIRED: "expired",
    }

    status = SIGNAL_STATUS_MAP.get(signal, signal)

    if signal == SIGNAL_RETRYING:
        TaskExecution.objects.filter(task_id=task_id).update(
            retries=models.F("retries") + 1,
            status="retrying",
        )
        return

    if signal == SIGNAL_ENQUEUED:
        TaskExecution.objects.create(
            task_id=task_id,
            task_name=task_name,
            status=status,
            queued_at=now,
            args_summary=str(task.args)[:500] if task.args else None,
        )
        return

    updates = {"status": status, "task_name": task_name}

    if signal == SIGNAL_EXECUTING:
        updates["started_at"] = now

    elif signal in (SIGNAL_COMPLETE, SIGNAL_ERROR, SIGNAL_REVOKED, SIGNAL_EXPIRED):
        updates["completed_at"] = now

    if signal == SIGNAL_ERROR and exc:
        updates["error"] = str(exc)[:2000]

    if signal in (SIGNAL_COMPLETE, SIGNAL_ERROR):
        obj = TaskExecution.objects.filter(task_id=task_id).values("started_at").first()
        if obj and obj["started_at"]:
            updates["duration_ms"] = int((now - obj["started_at"]).total_seconds() * 1000)

    TaskExecution.objects.filter(task_id=task_id).update(**updates)
