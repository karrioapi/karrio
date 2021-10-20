import functools
import graphene
import graphene_django
from graphene.types import generic
import django_filters
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

import purplship.server.core.models as core
import purplship.server.providers.models as providers
import purplship.server.manager.models as manager
import purplship.server.events.models as events
import purplship.server.graph.models as graph
import purplship.server.user.models as auth

User = get_user_model()


def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        *a, info = args
        if info.context.user.is_anonymous:
            raise exceptions.AuthenticationFailed(_('You are not authenticated'), code='login_required')

        return func(*args, **kwargs)
    return wrapper


class CustomNode(graphene.Node):
    class Meta:
        name = 'CustomNode'

    @classmethod
    def to_global_id(cls, type, id):
        return id


class UserType(graphene_django.DjangoObjectType):
    class Meta:
        model = User
        fields = ('email', 'full_name', 'is_staff', 'last_login', 'date_joined')


class ConnectionType:
    carrier_name = graphene.String(required=True)

    def resolve_carrier_name(self, info):
        return getattr(self, 'settings', self).carrier_name


class SystemConnectionType(graphene_django.DjangoObjectType, ConnectionType):
    enabled = graphene.Boolean(required=True)

    class Meta:
        model = providers.Carrier
        fields = ('created_at', 'updated_at', 'id', 'test', 'carrier_id', 'carrier_name', 'active', 'test', 'capabilities')

    def resolve_enabled(self, info):
        if hasattr(self, 'org'):
            return self.active_orgs.filter(id=info.context.org.id).exists()

        return self.active_users.filter(id=info.context.user.id).exists()


class LogFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        method='status_filter', choices=[('succeeded', 'succeeded'), ('failed', 'failed')])

    class Meta:
        model = core.APILog
        fields = {'path': ['contains']}

    def status_filter(self, queryset, name, value):
        if value == 'succeeded':
            return queryset.filter(status_code__range=[200, 399])
        elif value == 'failed':
            return queryset.filter(status_code__range=[400, 599])

        return queryset


class LogType(graphene_django.DjangoObjectType):
    class Meta:
        model = core.APILog
        interfaces = (CustomNode,)


class TokenType(graphene_django.DjangoObjectType):
    class Meta:
        model = auth.Token
        exclude = ('user', )


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
        exclude = ('customs_set', )


class AddressType(graphene_django.DjangoObjectType):
    validation = generic.GenericScalar()

    class Meta:
        model = manager.Address
        exclude = ('pickup_set', 'recipient', 'shipper', 'template')


class ParcelType(graphene_django.DjangoObjectType):
    class Meta:
        model = manager.Parcel
        exclude = ('shipment_parcels', 'template', )


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

    class Meta:
        model = manager.Customs
        exclude = ('shipment_set', 'template', 'options')

    def resolve_commodities(self, info):
        return self.commodities.all()


class AddressTemplateType(graphene_django.DjangoObjectType):
    address = graphene.Field(AddressType, required=True)

    class Meta:
        model = graph.Template
        exclude = ('customs', 'parcel')
        filter_fields = {
            'label': ['icontains'],
            'address__address_line1': ['icontains']
        }
        interfaces = (CustomNode,)


class CustomsTemplateType(graphene_django.DjangoObjectType):
    customs = graphene.Field(CustomsType, required=True)

    class Meta:
        model = graph.Template
        exclude = ('address', 'parcel')
        filter_fields = {'label': ['icontains']}
        interfaces = (CustomNode,)


class ParcelTemplateType(graphene_django.DjangoObjectType):
    parcel = graphene.Field(ParcelType, required=True)

    class Meta:
        model = graph.Template
        exclude = ('address', 'customs')
        filter_fields = {'label': ['icontains']}
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


class TrackerType(graphene_django.DjangoObjectType):
    tracking_carrier = graphene.Field(SystemConnectionType)
    events = graphene.List(TrackingEventType)

    class Meta:
        model = manager.Tracking
        filter_fields = ['delivered']
        interfaces = (CustomNode,)


class PaymentType(graphene.ObjectType):
    paid_by = graphene.String()
    currency = graphene.String()
    account_number = graphene.String()
    id = graphene.String()


class ShipmentType(graphene_django.DjangoObjectType):
    carrier_id = graphene.String()
    carrier_name = graphene.String()

    shipper = graphene.Field(AddressType)
    recipient = graphene.Field(AddressType)
    customs = graphene.Field(CustomsType)
    parcels = graphene.List(ParcelType)
    payment = graphene.Field(PaymentType)

    services = graphene.List(graphene.String)
    carrier_ids = graphene.List(graphene.String)
    messages = graphene.List(MessageType)
    selected_rate = graphene.Field(RateType)
    rates = graphene.List(RateType)

    options = generic.GenericScalar()
    meta = generic.GenericScalar()

    class Meta:
        model = manager.Shipment
        exclude = ('pickup_shipments', 'selected_rate_carrier', 'carriers')
        filter_fields = ['status']
        interfaces = (CustomNode,)

    def resolve_carrier_ids(self, info):
        return [c.carrier_id for c in self.carriers or []]

    def resolve_parcels(self, info):
        return self.parcels.all()

    def resolve_carrier_id(self, info):
        return getattr(self.selected_rate_carrier, 'carrier_id', None)

    def resolve_carrier_name(self, info):
        return getattr(self.selected_rate_carrier, 'carrier_name', None)


class WebhookType(graphene_django.DjangoObjectType):
    class Meta:
        model = events.Webhook
        exclude = ('failure_streak_count', )
        filter_fields = {'description': ['icontains']}
        interfaces = (CustomNode,)


def setup_carrier_model(model_type):
    _extra_fields = {}

    if hasattr(model_type, 'account_country_code'):
        _extra_fields.update(account_country_code=graphene.String(required=True))

    class Meta:
        model = model_type
        exclude = ('carrier_ptr', )

    return type(model_type.__name__, (graphene_django.DjangoObjectType, ConnectionType), {
        'Meta': Meta,
        **_extra_fields
    })


class ConnectionType(graphene.Union):

    class Meta:
        types = tuple(setup_carrier_model(carrier_model) for carrier_model in providers.MODELS.values())
