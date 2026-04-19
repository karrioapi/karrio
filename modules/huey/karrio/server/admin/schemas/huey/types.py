import datetime

import karrio.server.admin.schemas.huey.inputs as inputs
import karrio.server.admin.utils as admin
import karrio.server.graph.utils as utils
import strawberry
from strawberry.types import Info


@strawberry.type
class TaskExecutionType:
    """Admin type for Huey task execution records."""

    id: int
    task_id: str
    task_name: str
    status: str
    queued_at: datetime.datetime | None = None
    started_at: datetime.datetime | None = None
    completed_at: datetime.datetime | None = None
    duration_ms: int | None = None
    error: str | None = None
    retries: int = 0
    args_summary: str | None = None

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve_list(
        info: Info,
        filter: inputs.TaskExecutionFilter | None = strawberry.UNSET,
    ) -> utils.Connection["TaskExecutionType"]:
        from karrio.server.admin.worker.models import TaskExecution

        _filter = filter if not utils.is_unset(filter) else inputs.TaskExecutionFilter()
        _filter_data = _filter.to_dict()
        _queryset_filters = {}

        if _filter_data.get("status"):
            _queryset_filters["status"] = _filter_data["status"]
        if _filter_data.get("task_name"):
            _queryset_filters["task_name__icontains"] = _filter_data["task_name"]
        if _filter_data.get("date_after"):
            _queryset_filters["queued_at__gte"] = _filter_data["date_after"]
        if _filter_data.get("date_before"):
            _queryset_filters["queued_at__lte"] = _filter_data["date_before"]

        queryset = TaskExecution.objects.filter(**_queryset_filters)
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class QueueInfoType:
    pending_count: int
    scheduled_count: int
    result_count: int


@strawberry.type
class WorkerHealthType:
    is_available: bool
    queue: QueueInfoType | None = None

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(info: Info) -> "WorkerHealthType":
        try:
            from huey.contrib.djhuey import HUEY as huey_instance

            storage = huey_instance.storage
            return WorkerHealthType(
                is_available=True,
                queue=QueueInfoType(
                    pending_count=storage.queue_size(),
                    scheduled_count=storage.schedule_size(),
                    result_count=storage.result_store_size(),
                ),
            )
        except Exception:
            return WorkerHealthType(is_available=False)
