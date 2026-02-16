import logging
from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)


def register_huey_signals():
    """Register Huey signal handlers to track task execution lifecycle.

    Uses split create/update pattern instead of update_or_create to avoid
    SELECT ... FOR UPDATE lock contention when multiple tasks are enqueued
    in rapid succession (e.g. background_trackers_update dispatching
    per-carrier batches).
    """
    try:
        from huey.signals import (
            SIGNAL_ENQUEUED,
            SIGNAL_EXECUTING,
            SIGNAL_COMPLETE,
            SIGNAL_ERROR,
            SIGNAL_RETRYING,
            SIGNAL_REVOKED,
            SIGNAL_EXPIRED,
        )
        from huey.contrib.djhuey import HUEY as huey_instance
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
        try:
            from karrio.server.admin.worker.models import TaskExecution

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

            # ENQUEUED: create a new record (no SELECT FOR UPDATE needed)
            if signal == SIGNAL_ENQUEUED:
                TaskExecution.objects.create(
                    task_id=task_id,
                    task_name=task_name,
                    status=status,
                    queued_at=now,
                    args_summary=str(task.args)[:500] if task.args else None,
                )
                return

            # All other signals: lightweight UPDATE (no row lock)
            updates = {"status": status, "task_name": task_name}

            if signal == SIGNAL_EXECUTING:
                updates["started_at"] = now

            elif signal in (SIGNAL_COMPLETE, SIGNAL_ERROR, SIGNAL_REVOKED, SIGNAL_EXPIRED):
                updates["completed_at"] = now

            if signal == SIGNAL_ERROR and exc:
                updates["error"] = str(exc)[:2000]

            # Calculate duration inline to avoid a second UPDATE round-trip
            if signal in (SIGNAL_COMPLETE, SIGNAL_ERROR):
                obj = TaskExecution.objects.filter(task_id=task_id).values("started_at").first()
                if obj and obj["started_at"]:
                    updates["duration_ms"] = int(
                        (now - obj["started_at"]).total_seconds() * 1000
                    )

            TaskExecution.objects.filter(task_id=task_id).update(**updates)

        except Exception:
            # Handle duplicate records from race conditions on ENQUEUED
            try:
                from karrio.server.admin.worker.models import TaskExecution

                if signal == SIGNAL_ENQUEUED:
                    # Duplicate task_id — just update the existing record
                    TaskExecution.objects.filter(task_id=task_id).update(
                        task_name=task_name,
                        status="queued",
                        queued_at=now,
                        args_summary=str(task.args)[:500] if task.args else None,
                    )
                    return
            except Exception:
                pass

            logger.exception("Failed to record task signal")
