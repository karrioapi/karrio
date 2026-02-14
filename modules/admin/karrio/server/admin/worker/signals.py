import logging
from django.utils import timezone

logger = logging.getLogger(__name__)


def register_huey_signals():
    """Register Huey signal handlers to track task execution lifecycle."""
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

            defaults = {"status": status, "task_name": task_name}

            if signal == SIGNAL_ENQUEUED:
                defaults["queued_at"] = now
                defaults["args_summary"] = str(task.args)[:500] if task.args else None

            elif signal == SIGNAL_EXECUTING:
                defaults["started_at"] = now

            elif signal in (SIGNAL_COMPLETE, SIGNAL_ERROR, SIGNAL_REVOKED, SIGNAL_EXPIRED):
                defaults["completed_at"] = now

            if signal == SIGNAL_ERROR and exc:
                defaults["error"] = str(exc)[:2000]

            if signal == SIGNAL_RETRYING:
                TaskExecution.objects.filter(task_id=task_id).update(
                    retries=models.F("retries") + 1,
                    status="retrying",
                )
                return

            obj, created = TaskExecution.objects.update_or_create(
                task_id=task_id,
                defaults=defaults,
            )

            # Calculate duration if completing and started_at is known
            if signal in (SIGNAL_COMPLETE, SIGNAL_ERROR) and obj.started_at:
                duration = (now - obj.started_at).total_seconds() * 1000
                TaskExecution.objects.filter(pk=obj.pk).update(
                    duration_ms=int(duration)
                )

        except Exception:
            logger.exception("Failed to record task signal")


# Import models for F() expression
from django.db import models
