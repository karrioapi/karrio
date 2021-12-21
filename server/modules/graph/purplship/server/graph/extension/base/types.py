import functools
import graphene
import django_filters
import graphene_django
import rest_framework.status as http_status
from graphene.types import generic
from graphene.types.scalars import Scalar
from rest_framework import exceptions
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from purplship.core.utils import DP
from purplship.server.events.serializers import EventTypes
import purplship.server.core.serializers as serializers
import purplship.server.core.models as core
import purplship.server.providers.models as providers
import purplship.server.manager.models as manager
import purplship.server.events.models as events
import purplship.server.graph.models as graph
import purplship.server.user.models as auth

User = get_user_model()
CARRIER_NAMES = list(providers.MODELS.keys())
HTTP_STATUS = [getattr(http_status, a) for a in dir(http_status) if "HTTP" in a]


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


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class ObjectType(Scalar):
    @staticmethod
    def serialize(data):
        return data


class CustomNode(graphene.Node):
    class Meta:
        name = "CustomNode"

    @classmethod
    def to_global_id(cls, type, id):
        return id


class UserType(graphene_django.DjangoObjectType):
    class Meta:
        model = User
        fields = ("email", "full_name", "is_staff", "last_login", "date_joined")


class BaseConnectionType:
    carrier_name = graphene.String(required=True)

    def resolve_carrier_name(self, info):
        return getattr(self, "settings", self).carrier_name


class SystemConnectionType(graphene_django.DjangoObjectType, BaseConnectionType):
    enabled = graphene.Boolean(required=True)

    class Meta:
        model = providers.Carrier
        fields = (
            "created_at",
            "updated_at",
            "id",
            "test",
            "carrier_id",
            "carrier_name",
            "active",
            "test",
            "capabilities",
        )

    def resolve_enabled(self, info):
        if hasattr(self, "active_orgs"):
            return self.active_orgs.filter(id=info.context.org.id).exists()

        return self.active_users.filter(id=info.context.user.id).exists()


class LogFilter(django_filters.FilterSet):
    api_endpoint = django_filters.CharFilter(field_name="path", lookup_expr="icontains")
    date_after = django_filters.DateTimeFilter(
        field_name="requested_at", lookup_expr="gte"
    )
    date_before = django_filters.DateTimeFilter(
        field_name="requested_at", lookup_expr="lte"
    )
    entity_id = django_filters.CharFilter(method="entity_filter", field_name="response")
    method = django_filters.MultipleChoiceFilter(
        field_name="method",
        choices=[
            ("GET", "GET"),
            ("POST", "POST"),
            ("PATCH", "PATCH"),
            ("DELETE", "DELETE"),
        ],
    )
    status = django_filters.ChoiceFilter(
        method="status_filter",
        choices=[("succeeded", "succeeded"), ("failed", "failed")],
    )
    status_code = django_filters.TypedMultipleChoiceFilter(
        coerce=int,
        field_name="status_code",
        choices=[(s, s) for s in HTTP_STATUS],
    )

    class Meta:
        model = core.APILog
        fields = []

    def status_filter(self, queryset, name, value):
        if value == "succeeded":
            return queryset.filter(status_code__range=[200, 399])
        elif value == "failed":
            return queryset.filter(status_code__range=[400, 599])

        return queryset

    def entity_filter(self, queryset, name, value):
        return queryset.filter(response__icontains=value)


class LogType(graphene_django.DjangoObjectType):
    data = generic.GenericScalar()
    response = generic.GenericScalar()
    query_params = generic.GenericScalar()

    class Meta:
        model = core.APILog
        exclude = (
            "errors",
            "view",
            "view_method",
        )
        interfaces = (CustomNode,)

    def resolve_response(self, info):
        try:
            return DP.to_dict(self.response)
        except:
            return self.response

    def resolve_data(self, info):
        try:
            return DP.to_dict(self.data)
        except:
            return self.data

    def resolve_query_params(self, info):
        try:
            return DP.to_dict(self.query_params)
        except:
            return self.query_params


class TokenType(graphene_django.DjangoObjectType):
    class Meta:
        model = auth.Token
        exclude = ("user",)


class MessageType(graphene.ObjectType):
    carrier_name = graphene.String()
    carrier_id = graphene.String()
    message = graphene.String()
    code = graphene.String()
    details = generic.GenericScalar()


class ChargeType(graphene.ObjectType):
    name = graphene.String()
    amount = graphene.Float()
    currency = graphene.String()


class RateType(graphene.ObjectType):
    carrier_name = graphene.String()
    carrier_id = graphene.String()
    currency = graphene.String()
    transit_days = graphene.Int()
    service = graphene.String()
    discount = graphene.Float()
    base_charge = graphene.Float()
    total_charge = graphene.Float()
    duties_and_taxes = graphene.Float()
    extra_charges = graphene.List(ChargeType)
    meta = generic.GenericScalar()
    id = graphene.String()


class CommodityType(graphene_django.DjangoObjectType):
    class Meta:
        model = manager.Commodity
        exclude = ("customs_set",)


class AddressType(graphene_django.DjangoObjectType):
    validation = generic.GenericScalar()

    class Meta:
        model = manager.Address
        exclude = ("pickup_set", "recipient", "shipper", "template")


class ParcelType(graphene_django.DjangoObjectType):
    class Meta:
        model = manager.Parcel
        exclude = (
            "shipment_parcels",
            "template",
        )


class DutyType(graphene.ObjectType):
    paid_by = graphene.String()
    currency = graphene.String()
    account_number = graphene.String()
    declared_value = graphene.Float()
    bill_to = graphene.Field(AddressType)
    id = graphene.String()


class CustomsType(graphene_django.DjangoObjectType):
    commodities = graphene.List(CommodityType)
    duty = graphene.Field(DutyType)
    options = generic.GenericScalar()

    class Meta:
        model = manager.Customs
        exclude = ("shipment_set", "template")

    def resolve_commodities(self, info):
        return self.commodities.all()


class AddressTemplateType(graphene_django.DjangoObjectType):
    address = graphene.Field(AddressType, required=True)

    class Meta:
        model = graph.Template
        exclude = ("customs", "parcel")
        filter_fields = {
            "label": ["icontains"],
            "address__address_line1": ["icontains"],
        }
        interfaces = (CustomNode,)


class CustomsTemplateType(graphene_django.DjangoObjectType):
    customs = graphene.Field(CustomsType, required=True)

    class Meta:
        model = graph.Template
        exclude = ("address", "parcel")
        filter_fields = {"label": ["icontains"]}
        interfaces = (CustomNode,)


class ParcelTemplateType(graphene_django.DjangoObjectType):
    parcel = graphene.Field(ParcelType, required=True)

    class Meta:
        model = graph.Template
        exclude = ("address", "customs")
        filter_fields = {"label": ["icontains"]}
        interfaces = (CustomNode,)


class TemplateType(graphene_django.DjangoObjectType):
    address = graphene.Field(AddressType)
    customs = graphene.Field(CustomsType)
    parcel = graphene.Field(ParcelType)

    class Meta:
        model = graph.Template
        interfaces = (CustomNode,)


class TrackingEventType(graphene.ObjectType):
    description = graphene.String()
    location = graphene.String()
    code = graphene.String()
    date = graphene.String()
    time = graphene.String()


class TrackerFilter(django_filters.FilterSet):
    created_after = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )
    carrier_name = django_filters.MultipleChoiceFilter(
        method="carrier_filter",
        choices=[(c, c) for c in CARRIER_NAMES],
    )
    status = django_filters.MultipleChoiceFilter(
        field_name="status",
        choices=[(c.value, c.value) for c in list(serializers.TrackerStatus)],
    )
    test_mode = django_filters.BooleanFilter(field_name="test_mode")

    class Meta:
        model = manager.Tracking
        fields = []

    def carrier_filter(self, queryset, name, values):
        _filters = [
            Q(**{f"tracking_carrier__{value.replace('_', '')}settings__isnull": False})
            for value in values
        ]
        query = _filters.pop()

        for item in _filters:
            query |= item

        return queryset.filter(query)


class TrackerType(graphene_django.DjangoObjectType):
    carrier_id = graphene.String(required=True)
    carrier_name = graphene.String(required=True)

    events = graphene.List(TrackingEventType, required=True)
    messages = graphene.List(MessageType, required=True)
    status = graphene.Enum.from_enum(serializers.TrackerStatus)(required=True)

    class Meta:
        model = manager.Tracking
        filter_fields = ["tracking_carrier"]
        interfaces = (CustomNode,)

    def resolve_carrier_id(self, info):
        return getattr(self.tracking_carrier, "carrier_id", None)

    def resolve_carrier_name(self, info):
        return getattr(self.tracking_carrier, "carrier_name", None)


class PaymentType(graphene.ObjectType):
    paid_by = graphene.String()
    currency = graphene.String()
    account_number = graphene.String()
    id = graphene.String()


class ShipmentFilter(django_filters.FilterSet):
    address = django_filters.CharFilter(
        field_name="recipient__address_line1", lookup_expr="icontains"
    )
    created_after = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )
    carrier_name = django_filters.MultipleChoiceFilter(
        method="carrier_filter",
        choices=[(c, c) for c in CARRIER_NAMES],
    )
    reference = django_filters.CharFilter(
        field_name="reference", lookup_expr="icontains"
    )
    service = CharInFilter(
        method="service_filter", field_name="selected_rate__service", lookup_expr="in"
    )
    status = django_filters.MultipleChoiceFilter(
        field_name="status",
        choices=[(c.value, c.value) for c in list(serializers.ShipmentStatus)],
    )
    option_key = CharInFilter(
        field_name="options",
        method="option_key_filter",
    )
    option_value = django_filters.CharFilter(
        field_name="options",
        method="option_value_filter",
    )
    test_mode = django_filters.BooleanFilter(field_name="test_mode")

    class Meta:
        model = manager.Shipment
        fields = []

    def carrier_filter(self, queryset, name, values):
        _filters = [
            Q(
                **{
                    f"selected_rate_carrier__{value.replace('_', '')}settings__isnull": False
                }
            )
            for value in values
        ]
        query = Q(meta__rate_provider__in=values)

        for item in _filters:
            query |= item

        return queryset.filter(query)

    def option_key_filter(self, queryset, name, value):
        return queryset.filter(Q(options__has_key=value))

    def option_value_filter(self, queryset, name, value):
        return queryset.filter(Q(options__values__contains=value))

    def service_filter(self, queryset, name, values):
        return queryset.filter(Q(selected_rate__service__in=values))


class ShipmentType(graphene_django.DjangoObjectType):
    carrier_id = graphene.String()
    carrier_name = graphene.String()

    shipper = graphene.Field(AddressType, required=True)
    recipient = graphene.Field(AddressType, required=True)
    customs = graphene.Field(CustomsType)
    parcels = graphene.List(ParcelType, required=True)
    payment = graphene.Field(PaymentType)

    service = graphene.String()
    services = graphene.List(graphene.String)
    carrier_ids = graphene.List(graphene.String)
    messages = graphene.List(MessageType)
    selected_rate_id = graphene.String()
    selected_rate = graphene.Field(RateType)
    rates = graphene.List(RateType, required=True)

    carrier_ids = graphene.List(graphene.String)
    options = generic.GenericScalar()
    meta = generic.GenericScalar()
    tracker_id = graphene.String()

    status = graphene.Enum.from_enum(serializers.ShipmentStatus)(required=True)

    class Meta:
        model = manager.Shipment
        exclude = ("pickup_shipments", "selected_rate_carrier", "carriers")
        filter_fields = ["status"]
        interfaces = (CustomNode,)

    def resolve_parcels(self, info):
        return self.parcels.all()

    def resolve_carrier_id(self, info):
        return getattr(self.selected_rate_carrier, "carrier_id", None)

    def resolve_carrier_ids(self, info):
        return getattr(self, "carrier_ids", None)

    def resolve_carrier_name(self, info):
        return getattr(self.selected_rate_carrier, "carrier_name", None)


class WebhookFilter(django_filters.FilterSet):
    created_after = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )
    description = django_filters.CharFilter(
        field_name="description", lookup_expr="icontains"
    )
    events = django_filters.MultipleChoiceFilter(
        field_name="enabled_events",
        method="events_filter",
        choices=[(c.value, c.value) for c in list(EventTypes)],
    )
    disabled = django_filters.BooleanFilter(field_name="disabled")
    test_mode = django_filters.BooleanFilter(field_name="test_mode")
    url = django_filters.CharFilter(field_name="url", lookup_expr="icontains")

    class Meta:
        model = events.Webhook
        fields = []

    def events_filter(self, queryset, name, values):
        return queryset.filter(
            Q(enabled_events__contains=values) | Q(enabled_events__contains=["all"])
        )


class WebhookType(graphene_django.DjangoObjectType):
    class Meta:
        model = events.Webhook
        exclude = ("failure_streak_count",)
        interfaces = (CustomNode,)


class EventFilter(django_filters.FilterSet):
    date_after = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    date_before = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )
    entity_id = django_filters.CharFilter(method="entity_filter", field_name="response")
    type = django_filters.MultipleChoiceFilter(
        field_name="type",
        method="types_filter",
        choices=[(c.value, c.value) for c in list(EventTypes) if c != EventTypes.all],
    )

    class Meta:
        model = events.Event
        fields = []

    def entity_filter(self, queryset, name, value):
        try:
            return queryset.filter(data__icontains=value)
        except:
            return queryset

    def types_filter(self, queryset, name, values):
        return queryset.filter(Q(type__in=values))


class EventType(graphene_django.DjangoObjectType):
    data = generic.GenericScalar()

    class Meta:
        model = events.Event
        interfaces = (CustomNode,)


class ServiceLevelType(graphene_django.DjangoObjectType):
    class Meta:
        model = providers.ServiceLevel
        exclude = ("dhlpolandsettings_set",)
        interfaces = (CustomNode,)


class LabelTemplateType(graphene_django.DjangoObjectType):
    class Meta:
        model = providers.LabelTemplate
        exclude = ("genericsettings_set",)
        interfaces = (CustomNode,)


def setup_carrier_model(model_type):
    _extra_fields = {}

    if hasattr(model_type, "account_country_code"):
        _extra_fields.update(account_country_code=graphene.String(required=True))

    if hasattr(model_type, "label_template"):
        _extra_fields.update(
            label_template=graphene.Field(LabelTemplateType),
        )

    if hasattr(model_type, "services"):

        def resolve_services(self, info):
            return self.services.all()

        _extra_fields.update(
            services=graphene.List(ServiceLevelType), resolve_services=resolve_services
        )

    class Meta:
        model = model_type
        exclude = ("carrier_ptr",)

    return type(
        model_type.__name__,
        (graphene_django.DjangoObjectType, BaseConnectionType),
        {"Meta": Meta, **_extra_fields},
    )


class ConnectionType(graphene.Union):
    class Meta:
        types = tuple(
            setup_carrier_model(carrier_model)
            for carrier_model in providers.MODELS.values()
        )
