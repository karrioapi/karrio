import typing
import datetime
import strawberry

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.base as base
import karrio.server.orders.serializers as serializers

OrderStatusEnum: typing.Any = strawberry.enum(serializers.OrderStatus)


@strawberry.input
class CreateOrderMutationInput(utils.BaseInput):
    order_date: datetime.date
    shipping_to: base.inputs.AddressInput
    line_items: base.inputs.CommodityInput
    shipping_from: typing.Optional[base.inputs.AddressInput] = strawberry.UNSET
    billing_address: typing.Optional[base.inputs.AddressInput] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET
    options: typing.Optional[utils.JSON] = strawberry.UNSET
    test_mode: typing.Optional[bool] = strawberry.UNSET


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


@strawberry.input
class PartialOrderUpdateMutationInput(utils.BaseInput):
    id: str
    order_date: datetime.date = strawberry.UNSET
    shipping_to: base.inputs.AddressInput = strawberry.UNSET
    line_items: base.inputs.CommodityInput = strawberry.UNSET
    shipping_from: typing.Optional[base.inputs.AddressInput] = strawberry.UNSET
    billing_address: typing.Optional[base.inputs.AddressInput] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET
    options: typing.Optional[utils.JSON] = strawberry.UNSET
    test_mode: typing.Optional[bool] = strawberry.UNSET
