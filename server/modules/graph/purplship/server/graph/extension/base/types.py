import typing
import graphene
import django_filters
from graphene.types import generic
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from karrio.core.utils import DP
from karrio.server.events.serializers import EventTypes
import karrio.server.core.serializers as serializers
import karrio.server.providers.models as providers
import karrio.server.manager.models as manager
import karrio.server.events.models as events
import karrio.server.graph.models as graph
import karrio.server.user.models as auth
import karrio.server.core.models as core
import karrio.server.graph.utils as utils

User = get_user_model()


class UserType(utils.BaseObjectType):
    class Meta:
        model = User
        fields = ("email", "full_name", "is_staff", "last_login", "date_joined")


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
        choices=[(s, s) for s in utils.HTTP_STATUS],
    )

    class Meta:
        model = core.APILog
        fields: typing.List[str] = []

    def status_filter(self, queryset, name, value):
        if value == "succeeded":
            return queryset.filter(status_code__range=[200, 399])
        elif value == "failed":
            return queryset.filter(status_code__range=[400, 599])

        return queryset

    def entity_filter(self, queryset, name, value):
        return queryset.filter(response__icontains=value)


class LogType(utils.BaseObjectType):
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
        interfaces = (utils.CustomNode,)

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


class TokenType(utils.BaseObjectType):
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
    currency = utils.CurrencyCodeEnum()


class RateType(graphene.ObjectType):
    id = graphene.String(required=True)
    carrier_name = graphene.String(required=True)
    carrier_id = graphene.String(required=True)
    currency = utils.CurrencyCodeEnum()
    transit_days = graphene.Int()
    service = graphene.String(required=True)
    discount = graphene.Float()
    base_charge = graphene.Float(required=True)
    total_charge = graphene.Float(required=True)
    duties_and_taxes = graphene.Float()
    extra_charges = graphene.List(graphene.NonNull(ChargeType), default_value=[])
    test_mode = graphene.Boolean(required=True)
    meta = generic.GenericScalar()


class CommodityType(utils.BaseObjectType):
    weight_unit = utils.WeightUnitEnum()
    origin_country = utils.CountryCodeEnum()
    value_currency = utils.CurrencyCodeEnum()
    parent_id = graphene.String()
    metadata = generic.GenericScalar()

    class Meta:
        model = manager.Commodity
        exclude = (*manager.Commodity.HIDDEN_PROPS,)

    def resolve_parent_id(self, info):
        return self.parent_id


class AddressType(utils.BaseObjectType):
    validation = generic.GenericScalar()
    country_code = utils.CountryCodeEnum(required=True)

    class Meta:
        model = manager.Address
        exclude = (*manager.Address.HIDDEN_PROPS, "template")


class ParcelType(utils.BaseObjectType):
    weight_unit = utils.WeightUnitEnum()
    dimension_unit = utils.DimensionUnitEnum()

    class Meta:
        model = manager.Parcel
        exclude = (
            *manager.Parcel.HIDDEN_PROPS,
            "template",
        )


class DutyType(graphene.ObjectType):
    paid_by = utils.PaidByEnum()
    currency = utils.CurrencyCodeEnum()
    account_number = graphene.String()
    declared_value = graphene.Float()
    bill_to = graphene.Field(AddressType)
    id = graphene.String()


class CustomsType(utils.BaseObjectType):
    content_type = utils.CustomsContentTypeEnum()
    incoterm = utils.IncotermCodeEnum()
    duty = graphene.Field(DutyType)
    options = generic.GenericScalar()

    class Meta:
        model = manager.Customs
        exclude = (*manager.Customs.HIDDEN_PROPS, "template")

    def resolve_commodities(self, info):
        return self.commodities.all()


class AddressTemplateType(utils.BaseObjectType):
    address = graphene.Field(AddressType, required=True)

    class Meta:
        model = graph.Template
        exclude = (*graph.Template.HIDDEN_PROPS, "customs", "parcel")
        filter_fields = {
            "label": ["icontains"],
            "address__address_line1": ["icontains"],
        }
        interfaces = (utils.CustomNode,)


class CustomsTemplateType(utils.BaseObjectType):
    customs = graphene.Field(CustomsType, required=True)

    class Meta:
        model = graph.Template
        exclude = (*graph.Template.HIDDEN_PROPS, "address", "parcel")
        filter_fields = {"label": ["icontains"]}
        interfaces = (utils.CustomNode,)


class ParcelTemplateType(utils.BaseObjectType):
    parcel = graphene.Field(ParcelType, required=True)

    class Meta:
        model = graph.Template
        exclude = (*graph.Template.HIDDEN_PROPS, "address", "customs")
        filter_fields = {"label": ["icontains"]}
        interfaces = (utils.CustomNode,)


class DefaultTemplatesType(graphene.ObjectType):
    default_address = graphene.Field(AddressTemplateType, required=False)
    default_customs = graphene.Field(CustomsTemplateType, required=False)
    default_parcel = graphene.Field(ParcelTemplateType, required=False)


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
        choices=[(c, c) for c in utils.CARRIER_NAMES],
    )
    status = django_filters.MultipleChoiceFilter(
        field_name="status",
        choices=[(c.value, c.value) for c in list(serializers.TrackerStatus)],
    )
    test_mode = django_filters.BooleanFilter(field_name="test_mode")

    class Meta:
        model = manager.Tracking
        fields: typing.List[str] = []

    def carrier_filter(self, queryset, name, values):
        _filters = [
            Q(**{f"tracking_carrier__{value.replace('_', '')}settings__isnull": False})
            for value in values
        ]
        query = _filters.pop()

        for item in _filters:
            query |= item

        return queryset.filter(query)


class TrackerType(utils.BaseObjectType):
    carrier_id = graphene.String(required=True)
    carrier_name = graphene.String(required=True)

    events = graphene.List(graphene.NonNull(TrackingEventType), default_value=[])
    messages = graphene.List(graphene.NonNull(MessageType), default_value=[])
    status = utils.TrackerStatusEnum(required=True)
    metadata = generic.GenericScalar()

    class Meta:
        model = manager.Tracking
        exclude = (*manager.Tracking.HIDDEN_PROPS,)
        interfaces = (utils.CustomNode,)

    def resolve_carrier_id(self, info):
        return getattr(self.tracking_carrier, "carrier_id", None)

    def resolve_carrier_name(self, info):
        return getattr(self.tracking_carrier, "carrier_name", None)


class PaymentType(graphene.ObjectType):
    paid_by = utils.PaidByEnum(required=False)
    currency = utils.CurrencyCodeEnum(required=False)
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
        choices=[(c, c) for c in utils.CARRIER_NAMES],
    )
    reference = django_filters.CharFilter(
        field_name="reference", lookup_expr="icontains"
    )
    service = utils.CharInFilter(
        method="service_filter", field_name="selected_rate__service", lookup_expr="in"
    )
    status = django_filters.MultipleChoiceFilter(
        field_name="status",
        choices=[(c.value, c.value) for c in list(serializers.ShipmentStatus)],
    )
    option_key = utils.CharInFilter(
        field_name="options",
        method="option_key_filter",
    )
    option_value = django_filters.CharFilter(
        field_name="options",
        method="option_value_filter",
    )
    metadata_key = utils.CharInFilter(
        field_name="metadata",
        method="metadata_key_filter",
    )
    metadata_value = django_filters.CharFilter(
        field_name="metadata",
        method="metadata_value_filter",
    )
    test_mode = django_filters.BooleanFilter(field_name="test_mode")

    class Meta:
        model = manager.Shipment
        fields: typing.List[str] = []

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

    def metadata_key_filter(self, queryset, name, value):
        return queryset.filter(Q(options__has_key=value))

    def metadata_value_filter(self, queryset, name, value):
        return queryset.filter(Q(metadata__values__contains=value))

    def service_filter(self, queryset, name, values):
        return queryset.filter(Q(selected_rate__service__in=values))


class ShipmentType(utils.BaseObjectType):
    carrier_id = graphene.String()
    carrier_name = graphene.String()

    shipper = graphene.Field(AddressType, required=True)
    recipient = graphene.Field(AddressType, required=True)
    customs = graphene.Field(CustomsType)
    parcels = graphene.List(
        graphene.NonNull(ParcelType), required=True, default_value=[]
    )
    payment = graphene.Field(PaymentType, default_value={})

    service = graphene.String()
    services = graphene.List(
        graphene.NonNull(graphene.String), required=True, default_value=[]
    )
    carrier_ids = graphene.List(
        graphene.NonNull(graphene.String), required=True, default_value=[]
    )
    messages = graphene.List(
        graphene.NonNull(MessageType), required=True, default_value=[]
    )
    selected_rate_id = graphene.String()
    selected_rate = graphene.Field(RateType)
    rates = graphene.List(graphene.NonNull(RateType), default_value=[])

    options = generic.GenericScalar()
    meta = generic.GenericScalar()
    metadata = generic.GenericScalar(required=True, default_value={})
    tracker_id = graphene.String()

    label_type = utils.LabelTypeEnum()
    label_url = graphene.String()
    invoice_url = graphene.String()
    status = utils.ShipmentStatusEnum(required=True)
    tracker = graphene.Field(TrackerType)

    class Meta:
        model = manager.Shipment
        exclude = (*manager.Shipment.HIDDEN_PROPS,)
        interfaces = (utils.CustomNode,)

    def resolve_parcels(self, info):
        return self.parcels.all()

    def resolve_carrier_id(self, info):
        return getattr(self.selected_rate_carrier, "carrier_id", None)

    def resolve_carrier_ids(self, info):
        return getattr(self, "carrier_ids", None)

    def resolve_carrier_name(self, info):
        return getattr(self.selected_rate_carrier, "carrier_name", None)

    def resolve_tracker(self, info):
        return self.tracker


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
        fields: typing.List[str] = []

    def events_filter(self, queryset, name, values):
        return queryset.filter(
            Q(enabled_events__contains=values) | Q(enabled_events__contains=["all"])
        )


class WebhookType(utils.BaseObjectType):
    class Meta:
        model = events.Webhook
        exclude = ("failure_streak_count",)
        interfaces = (utils.CustomNode,)


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
        fields: typing.List[str] = []

    def entity_filter(self, queryset, name, value):
        try:
            return queryset.filter(data__icontains=value)
        except:
            return queryset

    def types_filter(self, queryset, name, values):
        return queryset.filter(Q(type__in=values))


class EventType(utils.BaseObjectType):
    data = generic.GenericScalar()

    class Meta:
        model = events.Event
        interfaces = (utils.CustomNode,)


class ServiceLevelType(utils.BaseObjectType):
    class Meta:
        model = providers.ServiceLevel
        exclude = ("dhlpolandsettings_set",)
        interfaces = (utils.CustomNode,)


class LabelTemplateType(utils.BaseObjectType):
    class Meta:
        model = providers.LabelTemplate
        interfaces = (utils.CustomNode,)


class BaseConnectionType:
    carrier_name = graphene.String(required=True)

    def resolve_carrier_name(self, info):
        return getattr(self, "settings", self).carrier_name


class SystemConnectionType(BaseConnectionType, utils.BaseObjectType):
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


class ConnectionType(graphene.Interface, BaseConnectionType):
    id = graphene.String(required=True)

    def resolve_id(self, info):
        return self.id


def CreateCarrierSettingTypes(carrier_model):
    _extra_fields: dict = dict(metadata=generic.GenericScalar(default_value={}))

    if hasattr(carrier_model, "account_country_code"):
        _extra_fields.update(account_country_code=graphene.String(required=True))

    if hasattr(carrier_model, "label_template"):
        _extra_fields.update(
            label_template=graphene.Field(LabelTemplateType),
        )

    if hasattr(carrier_model, "services"):

        def resolve_services(self, info):
            return self.services.all()

        _extra_fields.update(
            services=graphene.List(
                graphene.NonNull(ServiceLevelType), default_value=[]
            ),
            resolve_services=resolve_services,
        )

    class Meta:
        model = carrier_model
        exclude = ("carrier_ptr",)
        interfaces = (ConnectionType,)

    return type(
        carrier_model.__name__,
        (
            BaseConnectionType,
            utils.BaseObjectType,
        ),
        {"Meta": Meta, **_extra_fields},
    )


CarrierSettings = {
    f"{model.__name__.lower()}": CreateCarrierSettingTypes(model)
    for _, model in providers.MODELS.items()
}
