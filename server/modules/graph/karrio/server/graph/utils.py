import functools
import typing
import graphene
import django_filters
import graphene_django
from karrio.server.manager.serializers.shipment import reset_related_shipment_rates
import rest_framework.status as http_status
from rest_framework import exceptions
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from graphene_django.types import ErrorType

from karrio.core.utils import Enum
import karrio.server.manager.models as manager
import karrio.server.providers.models as providers
import karrio.server.core.serializers as serializers


def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        *__, info = args
        if info.context.user.is_anonymous:
            raise exceptions.AuthenticationFailed(
                _("You are not authenticated"), code="login_required"
            )

        return func(*args, **kwargs)

    return wrapper


def password_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        *__, info = args
        password = kwargs.get("password")

        if not info.context.user.check_password(password):
            raise exceptions.ValidationError({"password": "Invalid password"})

        return func(*args, **kwargs)

    return wrapper


def metadata_object_types() -> Enum:
    _types = [
        ("carrier", providers.Carrier),
        ("commodity", manager.Commodity),
        ("shipment", manager.Shipment),
        ("tracker", manager.Tracking),
    ]

    if settings.ORDERS_MANAGEMENT:
        import karrio.server.orders.models as orders

        _types.append(("order", orders.Order))

    if settings.APPS_MANAGEMENT:
        import karrio.server.apps.models as apps

        _types.append(("app", apps.App))

    return Enum("MetadataObjectType", _types)


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class CustomNode(graphene.Node):
    class Meta:
        name = "CustomNode"

    @classmethod
    def to_global_id(cls, type, id):
        return id


class BaseObjectType(graphene_django.DjangoObjectType):
    class Meta:
        abstract = True

    object_type = graphene.String(required=True)

    def resolve_object_type(self, info):
        return getattr(self, "object_type", "")


class ClientMutation(graphene.relay.ClientIDMutation):
    class Meta:
        abstract = True

    errors = graphene.List(
        ErrorType, description="May contain more than one error for same field."
    )


def create_delete_mutation(
    name: str, model, validator: typing.Callable = None, **filter
):
    class _DeleteMutation:
        id = graphene.String()

        class Input:
            id = graphene.String(required=True)

        @classmethod
        @login_required
        def mutate_and_get_payload(cls, root, info, id: str = None):
            queryset = (
                model.access_by(info.context)
                if hasattr(model, "access_by")
                else model.objects
            )
            instance = queryset.get(id=id, **filter)

            if validator:
                validator(instance, context=info.context)

            shipment = getattr(instance, "shipment", None)
            instance.delete(keep_parents=True)

            if shipment is not None:
                reset_related_shipment_rates(shipment)

            return cls(id=id)

    return type(name, (_DeleteMutation, ClientMutation), {})


CARRIER_NAMES = list(providers.MODELS.keys())
HTTP_STATUS = [getattr(http_status, a) for a in dir(http_status) if "HTTP" in a]
CountryCodeEnum = graphene.Enum("CountryCodeEnum", serializers.COUNTRIES)
CurrencyCodeEnum = graphene.Enum("CurrencyCodeEnum", serializers.CURRENCIES)
DimensionUnitEnum = graphene.Enum("DimensionUnitEnum", serializers.DIMENSION_UNIT)
WeightUnitEnum = graphene.Enum("WeightUnitEnum", serializers.WEIGHT_UNIT)
CustomsContentTypeEnum = graphene.Enum(
    "CustomsContentTypeEnum", serializers.CUSTOMS_CONTENT_TYPE
)
IncotermCodeEnum = graphene.Enum("IncotermCodeEnum", serializers.INCOTERMS)
PaidByEnum = graphene.Enum("PaidByEnum", serializers.PAYMENT_TYPES)
LabelTypeEnum = graphene.Enum("LabelTypeEnum", serializers.LABEL_TYPES)
ShipmentStatusEnum = graphene.Enum("ShipmentStatusEnum", serializers.SHIPMENT_STATUS)
TrackerStatusEnum = graphene.Enum("TrackerStatusEnum", serializers.TRACKER_STATUS)

MetadataObjectType = metadata_object_types()
MetadataObjectTypeEnum = graphene.Enum.from_enum(MetadataObjectType)
