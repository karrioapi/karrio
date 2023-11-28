import typing
import datetime
import strawberry

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.base as base
import karrio.server.graph.schemas.orders.inputs as inputs
import karrio.server.orders.filters as filters
import karrio.server.orders.models as models


@strawberry.type
class LineItemType:
    id: str
    object_type: str
    quantity: int
    weight: float
    metadata: utils.JSON
    sku: typing.Optional[str]
    title: typing.Optional[str]
    hs_code: typing.Optional[str]
    description: typing.Optional[str]
    value_amount: typing.Optional[float]
    weight_unit: typing.Optional[utils.WeightUnitEnum]
    origin_country: typing.Optional[utils.CountryCodeEnum]
    value_currency: typing.Optional[utils.CurrencyCodeEnum]
    created_at: typing.Optional[datetime.datetime]
    updated_at: typing.Optional[datetime.datetime]
    created_by: typing.Optional[base.types.UserType]
    parent_id: typing.Optional[str] = None
    unfulfilled_quantity: typing.Optional[int] = None
    parent: typing.Optional[base.types.CommodityType] = None


@strawberry.type
class OrderType:
    id: str
    object_type: str
    order_id: str
    source: str
    shipping_to: base.types.AddressType
    shipping_from: typing.Optional[base.types.AddressType]
    billing_address: typing.Optional[base.types.AddressType]
    metadata: utils.JSON
    options: utils.JSON
    meta: utils.JSON
    status: inputs.OrderStatusEnum
    test_mode: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: base.types.UserType

    @strawberry.field
    def line_items(self: models.Order) -> typing.List[LineItemType]:
        return self.line_items.all()

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
        try:
            _filter = filter if not utils.is_unset(filter) else inputs.OrderFilter()
            queryset = filters.OrderFilters(
                _filter.to_dict(), models.Order.access_by(info.context.request)
            ).qs
            return utils.paginated_connection(queryset, **_filter.pagination())
        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.exception(e)
            raise e
