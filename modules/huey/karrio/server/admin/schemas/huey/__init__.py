import karrio.server.admin.schemas.huey.inputs as inputs
import karrio.server.admin.schemas.huey.mutations as mutations
import karrio.server.admin.schemas.huey.types as types
import karrio.server.graph.utils as utils
import strawberry
from strawberry.types import Info

extra_types = []


@strawberry.type
class Query:
    task_executions: utils.Connection[types.TaskExecutionType] = strawberry.field(
        resolver=types.TaskExecutionType.resolve_list
    )
    worker_health: types.WorkerHealthType = strawberry.field(resolver=types.WorkerHealthType.resolve)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def revoke_task(self, info: Info, input: inputs.RevokeTaskInput) -> mutations.RevokeTaskMutation:
        return mutations.RevokeTaskMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def cleanup_task_executions(
        self, info: Info, input: inputs.CleanupTaskExecutionsInput
    ) -> mutations.CleanupTaskExecutionsMutation:
        return mutations.CleanupTaskExecutionsMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def reset_stuck_tasks(self, info: Info, input: inputs.ResetStuckTasksInput) -> mutations.ResetStuckTasksMutation:
        return mutations.ResetStuckTasksMutation.mutate(info, **input.to_dict())
