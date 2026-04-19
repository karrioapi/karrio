import typing

import karrio.server.graph.schemas.base as base
import karrio.server.graph.utils as utils
import karrio.server.orders.serializers as serializers
import strawberry

OrderStatusEnum: typing.Any = strawberry.enum(serializers.OrderStatus)  # type: ignore


@strawberry.input
class CreateOrderMutationInput(utils.BaseInput):
    shipping_to: base.inputs.AddressInput
    line_items: list[base.inputs.CommodityInput]
    order_id: str | None = strawberry.UNSET
    order_date: str | None = strawberry.UNSET
    shipping_from: base.inputs.AddressInput | None = strawberry.UNSET
    billing_address: base.inputs.AddressInput | None = strawberry.UNSET
    metadata: utils.JSON | None = strawberry.UNSET
    options: utils.JSON | None = strawberry.UNSET


@strawberry.input
class UpdateOrderMutationInput(utils.BaseInput):
    id: str
    order_id: str | None = strawberry.UNSET
    order_date: str | None = strawberry.UNSET
    shipping_to: base.inputs.UpdateAddressInput | None = strawberry.UNSET
    shipping_from: base.inputs.UpdateAddressInput | None = strawberry.UNSET
    billing_address: base.inputs.UpdateAddressInput | None = strawberry.UNSET
    metadata: utils.JSON | None = strawberry.UNSET
    options: utils.JSON | None = strawberry.UNSET
    line_items: list[base.inputs.UpdateCommodityInput] | None = strawberry.UNSET


@strawberry.input
class DeleteOrderMutationInput(utils.BaseInput):
    id: str


@strawberry.input
class OrderFilter(utils.Paginated):
    id: list[str] | None = strawberry.UNSET
    keyword: str | None = strawberry.UNSET
    source: list[str] | None = strawberry.UNSET
    order_id: list[str] | None = strawberry.UNSET
    option_key: list[str] | None = strawberry.UNSET
    address: list[str] | None = strawberry.UNSET
    option_value: list[str] | None = strawberry.UNSET
    metadata_key: list[str] | None = strawberry.UNSET
    metadata_value: list[str] | None = strawberry.UNSET
    status: list[OrderStatusEnum] | None = strawberry.UNSET
    request_id: str | None = strawberry.UNSET
