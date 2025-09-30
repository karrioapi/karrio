import typing
import strawberry
from strawberry.types import Info

import karrio.server.graph.schemas.shipping.mutations as mutations
import karrio.server.graph.schemas.shipping.inputs as inputs
import karrio.server.graph.schemas.shipping.types as types
import karrio.server.graph.schemas.base as base
import karrio.server.shipping.models as models
import karrio.server.graph.utils as utils

extra_types: list = []


@strawberry.type
class Query:
    shipping_method: typing.Optional[types.ShippingMethodType] = strawberry.field(
        resolver=types.ShippingMethodType.resolve
    )
    shipping_methods: utils.Connection[types.ShippingMethodType] = strawberry.field(
        resolver=types.ShippingMethodType.resolve_list
    )


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_shipping_method(
        self, info: Info, input: inputs.CreateShippingMethodMutationInput
    ) -> mutations.CreateShippingMethodMutation:
        return mutations.CreateShippingMethodMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_shipping_method(
        self, info: Info, input: inputs.UpdateShippingMethodMutationInput
    ) -> mutations.UpdateShippingMethodMutation:
        return mutations.UpdateShippingMethodMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_shipping_method(
        self, info: Info, input: base.inputs.DeleteMutationInput
    ) -> base.mutations.DeleteMutation:
        return base.mutations.DeleteMutation.mutate(
            info, model=models.ShippingMethod, **input.to_dict()
        )