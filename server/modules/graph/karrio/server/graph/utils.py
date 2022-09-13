import functools
import typing
import graphene
import graphene_django
from django import conf as django
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _
from graphene_django.types import ErrorType

from karrio.core.utils import Enum
from karrio.server.manager.serializers.shipment import reset_related_shipment_rates
import karrio.server.manager.models as manager
import karrio.server.providers.models as providers
import karrio.server.core.permissions as permissions
import karrio.server.core.serializers as serializers
import karrio.server.core.dataunits as dataunits


def authentication_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        *__, info = args
        if info.context.user.is_anonymous:
            raise exceptions.AuthenticationFailed(
                _("You are not authenticated"), code="authentication_required"
            )

        if not info.context.user.is_verified():
            raise exceptions.AuthenticationFailed(
                _("Authentication Token not verified"), code="two_factor_required"
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


def authorization_required(keys: typing.List[str] = None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            *__, info = args
            permissions.check_permissions(
                context=info.context,
                keys=keys or [],
            )

            return func(*args, **kwargs)

        return wrapper

    return decorator


def metadata_object_types() -> Enum:
    _types = [
        ("carrier", providers.Carrier),
        ("commodity", manager.Commodity),
        ("shipment", manager.Shipment),
        ("tracker", manager.Tracking),
    ]

    if django.settings.ORDERS_MANAGEMENT:
        import karrio.server.orders.models as orders

        _types.append(("order", orders.Order))

    if django.settings.APPS_MANAGEMENT:
        import karrio.server.apps.models as apps

        _types.append(("app", apps.App))

    return Enum("MetadataObjectType", _types)


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
        @authentication_required
        @authorization_required()
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

            return cls(id=id)  # type:ignore

    return type(name, (_DeleteMutation, ClientMutation), {})


HTTP_STATUS = serializers.HTTP_STATUS
CARRIER_NAMES = dataunits.CARRIER_NAMES
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
LabelTemplateTypeEnum = graphene.Enum(
    "LabelTemplateTypeEnum", serializers.LABEL_TEMPLATE_TYPES
)
ShipmentStatusEnum = graphene.Enum("ShipmentStatusEnum", serializers.SHIPMENT_STATUS)
TrackerStatusEnum = graphene.Enum("TrackerStatusEnum", serializers.TRACKER_STATUS)

MetadataObjectType = metadata_object_types()
MetadataObjectTypeEnum = graphene.Enum.from_enum(MetadataObjectType)
