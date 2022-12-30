import strawberry
from strawberry.types import Info

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.base as base
import karrio.server.graph.schemas.data.mutations as mutations
import karrio.server.graph.schemas.data.inputs as inputs
import karrio.server.graph.schemas.data.types as types
import karrio.server.data.models as models

extra_types: list = []


@strawberry.type
class Query:
    data_template: types.DataTemplateType = strawberry.field(
        resolver=types.DataTemplateType.resolve
    )
    data_templates: utils.Connection[types.DataTemplateType] = strawberry.field(
        resolver=types.DataTemplateType.resolve_list
    )

    batch_operation: types.BatchOperationType = strawberry.field(
        resolver=types.BatchOperationType.resolve
    )
    batch_operations: utils.Connection[types.BatchOperationType] = strawberry.field(
        resolver=types.BatchOperationType.resolve_list
    )


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_data_template(
        self, info: Info, input: inputs.CreateDataTemplateMutationInput
    ) -> mutations.CreateDataTemplateMutation:
        return mutations.CreateDataTemplateMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_data_template(
        self, info: Info, input: inputs.UpdateDataTemplateMutationInput
    ) -> mutations.UpdateDataTemplateMutation:
        return mutations.UpdateDataTemplateMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_data_template(
        self, info: Info, input: base.inputs.DeleteMutationInput
    ) -> base.mutations.DeleteMutation:
        return base.mutations.DeleteMutation.mutate(
            info, model=models.DataTemplate, **input.to_dict()
        )
