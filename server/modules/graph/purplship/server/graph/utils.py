import functools
import typing
import graphene
import django_filters
import graphene_django
import rest_framework.status as http_status
from rest_framework import exceptions
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from graphene_django.types import ErrorType
from graphene_django.rest_framework import mutation

from purplship.core.utils import Enum
import purplship.server.manager.models as manager
import purplship.server.providers.models as providers
import purplship.server.core.serializers as serializers


def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        *a, info = args
        if info.context.user.is_anonymous:
            raise exceptions.AuthenticationFailed(
                _("You are not authenticated"), code="login_required"
            )

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
        import purplship.server.orders.models as orders

        _types.append(("order", orders.Order))

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


class SerializerMutation(mutation.SerializerMutation):
    class Meta:
        abstract = True

    @classmethod
    @login_required
    def get_serializer_kwargs(cls, root, info, **input):
        data = input.copy()

        if "id" in input:
            instance = cls._meta.model_class.access_by(info.context).get(
                id=data.pop("id")
            )

            return {
                "instance": instance,
                "data": data,
                "partial": True,
                "context": info.context,
            }

        return {"data": data, "partial": False, "context": info.context}


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

            instance.delete(keep_parents=True)

            if hasattr(instance, "shipment"):
                serializers.manager.reset_related_shipment_rates(
                    instance.shipment.first()
                )

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
ShipmentStatusEnum = graphene.Enum.from_enum(serializers.ShipmentStatus)
TrackerStatusEnum = graphene.Enum.from_enum(serializers.TrackerStatus)

MetadataObjectType = metadata_object_types()
MetadataObjectTypeEnum = graphene.Enum.from_enum(MetadataObjectType)
