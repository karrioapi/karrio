from karrio.server.core.utils import *
import typing
import base64
import logging
import functools
import strawberry
import dataclasses
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _

import karrio.lib as lib
import karrio.server.core.utils as utils
import karrio.server.core.models as core
import karrio.server.orders.models as orders
import karrio.server.manager.models as manager
import karrio.server.providers.models as providers
import karrio.server.core.permissions as permissions
import karrio.server.core.serializers as serializers

Cursor = str
T = typing.TypeVar("T")
GenericType = typing.TypeVar("GenericType")
logger = logging.getLogger(__name__)

error_logger = utils.error_wrapper

JSON: typing.Any = strawberry.scalar(
    typing.NewType("JSON", object),
    description="The `JSON` scalar type represents JSON values as specified by ECMA-404",
)
MANUAL_SHIPMENT_STATUSES = [
    (_.name, _.name)
    for _ in [
        serializers.ShipmentStatus.in_transit,
        serializers.ShipmentStatus.needs_attention,
        serializers.ShipmentStatus.delivery_failed,
        serializers.ShipmentStatus.delivered,
    ]
]

CurrencyCodeEnum: typing.Any = strawberry.enum(  # type: ignore
    lib.Enum("CurrencyCodeEnum", serializers.CURRENCIES)
)
CountryCodeEnum: typing.Any = strawberry.enum(  # type: ignore
    lib.Enum("CountryCodeEnum", serializers.COUNTRIES)
)
DimensionUnitEnum: typing.Any = strawberry.enum(  # type: ignore
    lib.Enum("DimensionUnitEnum", serializers.DIMENSION_UNIT)
)
WeightUnitEnum: typing.Any = strawberry.enum(  # type: ignore
    lib.Enum("WeightUnitEnum", serializers.WEIGHT_UNIT)
)
CustomsContentTypeEnum: typing.Any = strawberry.enum(  # type: ignore
    lib.Enum("CustomsContentTypeEnum", serializers.CUSTOMS_CONTENT_TYPE)
)
IncotermCodeEnum: typing.Any = strawberry.enum(  # type: ignore
    lib.Enum("IncotermCodeEnum", serializers.INCOTERMS)
)
PaidByEnum: typing.Any = strawberry.enum(  # type: ignore
    lib.Enum("PaidByEnum", serializers.PAYMENT_TYPES)
)
LabelTypeEnum: typing.Any = strawberry.enum(  # type: ignore
    lib.Enum("LabelTypeEnum", serializers.LABEL_TYPES)
)
LabelTemplateTypeEnum: typing.Any = strawberry.enum(  # type: ignore
    lib.Enum("LabelTemplateTypeEnum", serializers.LABEL_TEMPLATE_TYPES)
)
ShipmentStatusEnum: typing.Any = strawberry.enum(  # type: ignore
    lib.Enum("ShipmentStatusEnum", serializers.SHIPMENT_STATUS)
)
ManualShipmentStatusEnum: typing.Any = strawberry.enum(  # type: ignore
    lib.Enum("ManualShipmentStatusEnum", MANUAL_SHIPMENT_STATUSES)
)
TrackerStatusEnum: typing.Any = strawberry.enum(  # type: ignore
    lib.Enum("TrackerStatusEnum", serializers.TRACKER_STATUS)
)
CarrierNameEnum: typing.Any = strawberry.enum(  # type: ignore
    lib.Enum("CarrierNameEnum", serializers.CARRIERS)
)
MetafieldTypeEnum: typing.Any = strawberry.enum(  # type: ignore
    lib.Enum("MetafieldTypeEnum", core.METAFIELD_TYPE)
)


class MetadataObjectType(lib.Enum):
    carrier = providers.Carrier
    commodity = manager.Commodity
    shipment = manager.Shipment
    tracker = manager.Tracking
    order = orders.Order


MetadataObjectTypeEnum: typing.Any = strawberry.enum(  # type: ignore
    lib.StrEnum(
        "MetadataObjectTypeEnum", [(c.name, c.name) for c in list(MetadataObjectType)]
    )
)


def authentication_required(func):
    @functools.wraps(func)
    def wrapper(info, **kwargs):
        user = getattr(info.context.request, 'user', None)

        if user is None or user.is_anonymous:
            raise exceptions.AuthenticationFailed(
                _("You are not authenticated"), code="authentication_required"
            )

        if not user.is_verified():
            raise exceptions.AuthenticationFailed(
                _("Authentication Token not verified"), code="two_factor_required"
            )

        return func(info, **kwargs)

    return wrapper


def password_required(func):
    @functools.wraps(func)
    def wrapper(info, **kwargs):
        password = kwargs.get("password")

        if not info.context.request.user.check_password(password):
            raise exceptions.ValidationError({"password": "Invalid password"})

        return func(info, **kwargs)

    return wrapper


def authorization_required(keys: typing.List[str] = None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(info, **kwargs):
            permissions.check_permissions(
                context=info.context.request,
                keys=keys or [],
            )

            return func(info, **kwargs)

        return wrapper

    return decorator


@strawberry.type
class ErrorType:
    field: str
    messages: typing.List[str]

    @staticmethod
    def from_errors(errors):
        return []


@strawberry.input
class BaseInput:
    def pagination(self) -> typing.Dict[str, typing.Any]:
        return {
            k: v
            for k, v in dataclass_to_dict(self).items()
            if k in ["offset", "before", "after", "first", "last"]
        }

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return dataclass_to_dict(self)


@strawberry.type
class BaseMutation:
    errors: typing.Optional[typing.List[ErrorType]] = None


@strawberry.type
class UsageStatType:
    date: typing.Optional[str] = None
    label: typing.Optional[str] = None
    count: typing.Optional[float] = None

    @staticmethod
    def parse(value: dict) -> "UsageStatType":
        return UsageStatType(
            **{k: v for k, v in value.items() if k in UsageStatType.__annotations__}
        )


@strawberry.input
class UsageFilter(BaseInput):
    date_after: typing.Optional[str] = strawberry.UNSET
    date_before: typing.Optional[str] = strawberry.UNSET
    omit: typing.Optional[typing.List[str]] = strawberry.UNSET


@dataclasses.dataclass
@strawberry.type
class Connection(typing.Generic[GenericType]):
    """Represents a paginated relationship between two entities
    This pattern is used when the relationship itself has attributes.
    In a Facebook-based domain example, a friendship between two people
    would be a connection that might have a `friendshipStartTime`
    """

    page_info: "PageInfo"
    edges: typing.List["Edge[GenericType]"]


@dataclasses.dataclass
@strawberry.type
class PageInfo:
    """Pagination context to navigate objects with cursor-based pagination
    Instead of classic offset pagination via `page` and `limit` parameters,
    here we have a cursor of the last object and we fetch items starting from that one
    Read more at:
        - https://graphql.org/learn/pagination/#pagination-and-edges
        - https://relay.dev/graphql/connections.htm
    """

    count: int
    has_next_page: bool
    has_previous_page: bool
    start_cursor: typing.Optional[str]
    end_cursor: typing.Optional[str]


@dataclasses.dataclass
@strawberry.type
class Edge(typing.Generic[GenericType]):
    """An edge may contain additional information of the relationship. This is the trivial case"""

    node: GenericType
    cursor: str


@strawberry.input
class Paginated(BaseInput):
    offset: typing.Optional[int] = strawberry.UNSET
    first: typing.Optional[int] = strawberry.UNSET


def build_entity_cursor(entity: T):
    """Adapt this method to build an *opaque* ID from an instance"""
    entityid = f"{getattr(entity, 'id', id(entity))}".encode("utf-8")
    return base64.b64encode(entityid).decode()


def paginated_connection(
    queryset,
    first: int = 25,
    offset: int = 0,
) -> Connection[T]:
    """A non-trivial implementation should efficiently fetch only
    the necessary books after the offset.
    For simplicity, here we build the list and then slice it accordingly
    """

    # Fetch the requested results plus one, just to calculate `has_next_page`
    # fmt: off
    results = queryset[offset:offset+first+1]
    # fmt: on

    edges: typing.List[typing.Any] = [
        Edge(node=typing.cast(T, entity), cursor=build_entity_cursor(entity))
        for entity in results
    ]
    return Connection(
        page_info=PageInfo(
            count=queryset.count(),
            has_previous_page=False,
            has_next_page=len(results) > first,
            start_cursor=edges[0].cursor if edges else None,
            end_cursor=edges[-2].cursor if len(edges) > 1 else None,
        ),
        edges=(edges[:-1] if len(edges) > first else edges),
    )


def is_unset(v: typing.Any) -> bool:
    return isinstance(v, type(strawberry.UNSET)) or v == strawberry.UNSET


def _dict_factory(items):
    if isinstance(next(iter(items), None), tuple):
        return dict(
            [
                (key, _dict_factory(value) if isinstance(value, list) else value)
                for key, value in items
                if not is_unset(value)
            ]
        )

    return items


def dataclass_to_dict(data):
    return lib.to_dict(
        dataclasses.asdict(
            data,
            dict_factory=_dict_factory,
        ),
        clear_empty=False,
    )
