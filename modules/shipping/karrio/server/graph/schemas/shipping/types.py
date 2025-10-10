import typing
import datetime
import strawberry

import karrio.server.graph.utils as utils
import karrio.server.core.filters as filters
import karrio.server.shipping.models as models
import karrio.server.graph.schemas.base as base
import karrio.server.shipping.filters as filters
import karrio.server.graph.schemas.shipping.inputs as inputs

@strawberry.type
class ShippingMethodType:
    id: str
    object_type: str
    name: str
    slug: str
    description: typing.Optional[str]
    carrier_code: str
    carrier_service: str
    carrier_id: typing.Optional[str]
    carrier_options: utils.JSON
    metadata: utils.JSON
    is_active: bool
    test_mode: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: base.types.UserType

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["ShippingMethodType"]:
        return models.ShippingMethod.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.ShippingMethodFilter] = strawberry.UNSET,
    ) -> utils.Connection["ShippingMethodType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.ShippingMethodFilter()
        queryset = filters.ShippingMethodFilters(
            _filter.to_dict(), models.ShippingMethod.access_by(info.context.request)
        ).qs
        
        return utils.paginated_connection(queryset, **_filter.pagination())
