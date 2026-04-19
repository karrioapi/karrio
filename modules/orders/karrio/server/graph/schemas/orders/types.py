import datetime
import typing
import uuid

import karrio.server.graph.schemas.base as base
import karrio.server.graph.schemas.orders.inputs as inputs
import karrio.server.graph.utils as utils
import karrio.server.orders.filters as filters
import karrio.server.orders.models as models
import strawberry
from strawberry.types import Info


@strawberry.type
class LineItemType:
    object_type: str = "line_item"
    id: str | None = None
    quantity: int = 1
    weight: float = 0.0
    metadata: utils.JSON | None = None
    sku: str | None = None
    title: str | None = None
    hs_code: str | None = None
    description: str | None = None
    value_amount: float | None = None
    weight_unit: utils.WeightUnitEnum | None = None
    origin_country: utils.CountryCodeEnum | None = None
    value_currency: utils.CurrencyCodeEnum | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None
    created_by: base.types.UserType | None = None
    parent_id: str | None = None
    unfulfilled_quantity: int | None = None
    parent: base.types.CommodityType | None = None

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
    def request_id(self: models.Order) -> str | None:
        return (self.meta or {}).get("request_id")

    @strawberry.field
    def shipping_to(self: models.Order) -> base.types.AddressType:
        # shipping_to is a JSON field, parse it to AddressType
        return base.types.AddressType.parse(self.shipping_to)

    @strawberry.field
    def shipping_from(self: models.Order) -> base.types.AddressType | None:
        # shipping_from is a JSON field, parse it to AddressType
        return base.types.AddressType.parse(self.shipping_from)

    @strawberry.field
    def billing_address(self: models.Order) -> base.types.AddressType | None:
        # billing_address is a JSON field, parse it to AddressType
        return base.types.AddressType.parse(self.billing_address)

    @strawberry.field
    def line_items(self: models.Order) -> list[LineItemType]:
        # line_items is now a JSON field, return parsed LineItemType objects
        return [LineItemType.parse(item) for item in (self.line_items or [])]

    @strawberry.field
    def shipments(self: models.Order) -> list[base.types.ShipmentType]:
        return self.shipments.all()

    @staticmethod
    @utils.authentication_required
    def resolve(info: Info, id: str) -> typing.Optional["OrderType"]:
        return models.Order.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info: Info,
        filter: inputs.OrderFilter | None = strawberry.UNSET,
    ) -> utils.Connection["OrderType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.OrderFilter()
        queryset = filters.OrderFilters(_filter.to_dict(), models.Order.access_by(info.context.request)).qs
        return utils.paginated_connection(queryset, **_filter.pagination())
