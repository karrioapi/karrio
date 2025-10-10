import typing
import strawberry

import karrio.server.graph.utils as utils


@strawberry.input
class ShippingMethodFilter(utils.Paginated):
    search: typing.Optional[str] = strawberry.UNSET
    created_after: typing.Optional[str] = strawberry.UNSET
    created_before: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class CreateShippingMethodMutationInput(utils.BaseInput):
    name: str
    description: typing.Optional[str] = strawberry.UNSET
    carrier_code: str
    carrier_service: str
    carrier_id: typing.Optional[str] = strawberry.UNSET
    carrier_options: typing.Optional[utils.JSON] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET
    is_active: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class UpdateShippingMethodMutationInput(utils.BaseInput):
    id: str
    name: typing.Optional[str] = strawberry.UNSET
    description: typing.Optional[str] = strawberry.UNSET
    carrier_code: typing.Optional[str] = strawberry.UNSET
    carrier_service: typing.Optional[str] = strawberry.UNSET
    carrier_id: typing.Optional[str] = strawberry.UNSET
    carrier_options: typing.Optional[utils.JSON] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET
    is_active: typing.Optional[bool] = strawberry.UNSET
