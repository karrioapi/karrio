import datetime

import karrio.server.admin.utils as admin
import karrio.server.graph.utils as utils
import strawberry
from django.utils import timezone
from strawberry.types import Info


@strawberry.type
class RevokeTaskMutation(utils.BaseMutation):
    task_id: str | None = None

    @staticmethod
    @utils.authentication_required
    @admin.superuser_required
    def mutate(info: Info, **input) -> "RevokeTaskMutation":
        from karrio.server.admin.worker.models import TaskExecution

        from huey.contrib.djhuey import HUEY as huey_instance

        task_id = input["task_id"]
        huey_instance.revoke_by_id(task_id)

        TaskExecution.objects.filter(task_id=task_id).update(
            status="revoked",
            completed_at=timezone.now(),
            error="Revoked by admin",
        )

        return RevokeTaskMutation(task_id=task_id)


@strawberry.type
class CleanupTaskExecutionsMutation(utils.BaseMutation):
    deleted_count: int = 0

    @staticmethod
    @utils.authentication_required
    @admin.superuser_required
    def mutate(info: Info, **input) -> "CleanupTaskExecutionsMutation":
        from karrio.server.admin.worker.models import TaskExecution

        retention_days = input.get("retention_days") or 7
        statuses = input.get("statuses") or []
        cutoff = timezone.now() - datetime.timedelta(days=retention_days)

        qs = TaskExecution.objects.filter(queued_at__lt=cutoff)
        if statuses:
            qs = qs.filter(status__in=statuses)

        deleted_count, _ = qs.delete()

        return CleanupTaskExecutionsMutation(deleted_count=deleted_count)


@strawberry.type
class ResetStuckTasksMutation(utils.BaseMutation):
    updated_count: int = 0

    @staticmethod
    @utils.authentication_required
    @admin.superuser_required
    def mutate(info: Info, **input) -> "ResetStuckTasksMutation":
        from karrio.server.admin.worker.models import TaskExecution

        threshold_minutes = input.get("threshold_minutes") or 60
        statuses = input.get("statuses") or ["executing", "queued"]
        cutoff = timezone.now() - datetime.timedelta(minutes=threshold_minutes)

        updated_count = TaskExecution.objects.filter(
            status__in=statuses,
            queued_at__lt=cutoff,
        ).update(
            status="error",
            error="Reset by admin",
            completed_at=timezone.now(),
        )

        return ResetStuckTasksMutation(updated_count=updated_count)
