import typing
import datetime
import strawberry
import uuid

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.base as base
import karrio.server.graph.schemas.orders.inputs as inputs
import karrio.server.orders.filters as filters
import karrio.server.orders.models as models


@strawberry.type
class LineItemType:
    object_type: str = "line_item"
    id: typing.Optional[str] = None
    quantity: int = 1
    weight: float = 0.0
    metadata: typing.Optional[utils.JSON] = None
    sku: typing.Optional[str] = None
    title: typing.Optional[str] = None
    hs_code: typing.Optional[str] = None
    description: typing.Optional[str] = None
    value_amount: typing.Optional[float] = None
    weight_unit: typing.Optional[utils.WeightUnitEnum] = None
    origin_country: typing.Optional[utils.CountryCodeEnum] = None
    value_currency: typing.Optional[utils.CurrencyCodeEnum] = None
    created_at: typing.Optional[datetime.datetime] = None
    updated_at: typing.Optional[datetime.datetime] = None
    created_by: typing.Optional[base.types.UserType] = None
    parent_id: typing.Optional[str] = None
    unfulfilled_quantity: typing.Optional[int] = None
    parent: typing.Optional[base.types.CommodityType] = None

    @staticmethod
    def parse(item: dict) -> typing.Optional["LineItemType"]:
        if not item:
            return None
        # Generate an id if not present
        item_id = item.get("id") or f"item_{uuid.uuid4().hex[:8]}"
        return LineItemType(
            id=item_id,
            object_type=item.get("object_type", "line_item"),
            **{k: v for k, v in item.items() if k in LineItemType.__annotations__ and k not in ("id", "object_type")},
        )


@strawberry.type
class OrderType:
    id: str
    object_type: str
    order_id: str
    source: str
    metadata: utils.JSON
    options: utils.JSON
    meta: utils.JSON
    status: inputs.OrderStatusEnum
    test_mode: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: base.types.UserType

    @strawberry.field
    def shipping_to(self: models.Order) -> base.types.AddressType:
        # shipping_to is a JSON field, parse it to AddressType
        return base.types.AddressType.parse(self.shipping_to)

    @strawberry.field
    def shipping_from(self: models.Order) -> typing.Optional[base.types.AddressType]:
        # shipping_from is a JSON field, parse it to AddressType
        return base.types.AddressType.parse(self.shipping_from)

    @strawberry.field
    def billing_address(self: models.Order) -> typing.Optional[base.types.AddressType]:
        # billing_address is a JSON field, parse it to AddressType
        return base.types.AddressType.parse(self.billing_address)

    @strawberry.field
    def line_items(self: models.Order) -> typing.List[LineItemType]:
        # line_items is now a JSON field, return parsed LineItemType objects
        return [LineItemType.parse(item) for item in (self.line_items or [])]

    @strawberry.field
    def shipments(self: models.Order) -> typing.List[base.types.ShipmentType]:
        return self.shipments.all()

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["OrderType"]:
        return models.Order.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.OrderFilter] = strawberry.UNSET,
    ) -> utils.Connection["OrderType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.OrderFilter()
        queryset = filters.OrderFilters(
            _filter.to_dict(), models.Order.access_by(info.context.request)
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())
