import logging
from datetime import timedelta
from django.utils import timezone

logger = logging.getLogger(__name__)


def cleanup_old_task_executions(retention_days=7):
    """Remove task execution records older than the retention period."""
    from karrio.server.admin.worker.models import TaskExecution

    cutoff = timezone.now() - timedelta(days=retention_days)
    deleted_count, _ = TaskExecution.objects.filter(queued_at__lt=cutoff).delete()

    if deleted_count:
        logger.info(f"Cleaned up {deleted_count} old task execution records")

    return deleted_count
