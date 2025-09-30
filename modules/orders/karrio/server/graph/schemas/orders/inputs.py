import typing
import strawberry

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.base as base
import karrio.server.orders.serializers as serializers

OrderStatusEnum: typing.Any = strawberry.enum(serializers.OrderStatus)  # type: ignore


@strawberry.input
class CreateOrderMutationInput(utils.BaseInput):
    shipping_to: base.inputs.AddressInput
    line_items: typing.List[base.inputs.CommodityInput]
    order_id: typing.Optional[str] = strawberry.UNSET
    order_date: typing.Optional[str] = strawberry.UNSET
    shipping_from: typing.Optional[base.inputs.AddressInput] = strawberry.UNSET
    billing_address: typing.Optional[base.inputs.AddressInput] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET
    options: typing.Optional[utils.JSON] = strawberry.UNSET


@strawberry.input
class UpdateOrderMutationInput(utils.BaseInput):
    id: str
    order_id: typing.Optional[str] = strawberry.UNSET
    order_date: typing.Optional[str] = strawberry.UNSET
    shipping_to: typing.Optional[base.inputs.UpdateAddressInput] = strawberry.UNSET
    shipping_from: typing.Optional[base.inputs.UpdateAddressInput] = strawberry.UNSET
    billing_address: typing.Optional[base.inputs.UpdateAddressInput] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET
    options: typing.Optional[utils.JSON] = strawberry.UNSET
    line_items: typing.Optional[typing.List[base.inputs.UpdateCommodityInput]] = (
        strawberry.UNSET
    )


@strawberry.input
class DeleteOrderMutationInput(utils.BaseInput):
    id: str


@strawberry.input
class OrderFilter(utils.Paginated):
    id: typing.Optional[typing.List[str]] = strawberry.UNSET
    keyword: typing.Optional[str] = strawberry.UNSET
    source: typing.Optional[typing.List[str]] = strawberry.UNSET
    order_id: typing.Optional[typing.List[str]] = strawberry.UNSET
    ontion_key: typing.Optional[typing.List[str]] = strawberry.UNSET
    address: typing.Optional[typing.List[str]] = strawberry.UNSET
    ontion_value: typing.Optional[typing.List[str]] = strawberry.UNSET
    metadata_key: typing.Optional[typing.List[str]] = strawberry.UNSET
    metadata_value: typing.Optional[typing.List[str]] = strawberry.UNSET
    status: typing.Optional[typing.List[OrderStatusEnum]] = strawberry.UNSET
