import karrio.server.graph.utils as utils
import strawberry


@strawberry.input
class TaskExecutionFilter(utils.Paginated):
    """Filter for task execution records."""

    status: str | None = strawberry.UNSET
    task_name: str | None = strawberry.UNSET
    date_after: str | None = strawberry.UNSET
    date_before: str | None = strawberry.UNSET


@strawberry.input
class RevokeTaskInput(utils.BaseInput):
    task_id: str


@strawberry.input
class CleanupTaskExecutionsInput(utils.BaseInput):
    retention_days: int | None = strawberry.UNSET
    statuses: list[str] | None = strawberry.UNSET


@strawberry.input
class ResetStuckTasksInput(utils.BaseInput):
    threshold_minutes: int | None = strawberry.UNSET
    statuses: list[str] | None = strawberry.UNSET
