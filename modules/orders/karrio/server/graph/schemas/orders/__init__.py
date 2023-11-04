import strawberry
from strawberry.types import Info

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.orders.mutations as mutations
import karrio.server.graph.schemas.orders.inputs as inputs
import karrio.server.graph.schemas.orders.types as types

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
    def partial_order_update(
        self, info: Info, input: inputs.PartialOrderUpdateMutationInput
    ) -> mutations.PartialOrderUpdateMutation:
        return mutations.PartialOrderUpdateMutation.mutate(info, **input.to_dict())
