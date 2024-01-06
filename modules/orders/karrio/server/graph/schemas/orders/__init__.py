import strawberry
from strawberry.types import Info

import karrio.server.graph.utils as utils
import karrio.server.orders.models as models
import karrio.server.graph.schemas.base as base
import karrio.server.graph.schemas.orders.types as types
import karrio.server.graph.schemas.orders.inputs as inputs
import karrio.server.graph.schemas.orders.mutations as mutations

extra_types: list = []


@strawberry.type
class Query:
    order: types.OrderType = strawberry.field(resolver=types.OrderType.resolve)
    orders: utils.Connection[types.OrderType] = strawberry.field(
        resolver=types.OrderType.resolve_list
    )


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_order(
        self, info: Info, input: inputs.CreateOrderMutationInput
    ) -> mutations.CreateOrderMutation:
        return mutations.CreateOrderMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_order(
        self, info: Info, input: inputs.UpdateOrderMutationInput
    ) -> mutations.UpdateOrderMutation:
        return mutations.UpdateOrderMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_order(
        self, info: Info, input: inputs.DeleteOrderMutationInput
    ) -> mutations.DeleteOrderMutation:
        return mutations.DeleteOrderMutation.mutate(
            info, model=models.Order, **input.to_dict()
        )
