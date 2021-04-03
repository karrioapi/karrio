import graphene
import graphene_django
from graphene.types import generic

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework_tracking.models import APIRequestLog

import purpleserver.providers.models as providers
import purpleserver.manager.models as manager
import purpleserver.events.models as events
import purpleserver.graph.models as graph

User = get_user_model()


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
        return getattr(self, 'data', self).carrier_name


class SystemConnectionType(graphene_django.DjangoObjectType, ConnectionType):

    class Meta:
        model = providers.Carrier
        fields = ('created_at', 'updated_at', 'id', 'active', 'test', 'carrier_id', 'carrier_name')


class LogType(graphene_django.DjangoObjectType):

    class Meta:
        model = APIRequestLog
        filter_fields = {'path': ['icontains']}
        interfaces = (CustomNode,)


class TokenType(graphene_django.DjangoObjectType):
    class Meta:
        model = Token
        exclude = ('user', )


class CommodityType(graphene_django.DjangoObjectType):
    class Meta:
        model = manager.Commodity
        exclude = ('customs_set', )


class AddressType(graphene_django.DjangoObjectType):
    validation = generic.GenericScalar()

    class Meta:
        model = manager.Address
        exclude = ('payment_set', 'pickup_set', 'recipient', 'shipper', 'template')


class ParcelType(graphene_django.DjangoObjectType):
    class Meta:
        model = manager.Parcel
        exclude = ('shipment_parcels', 'template', )


class PaymentType(graphene_django.DjangoObjectType):
    contact = graphene.Field(AddressType)

    class Meta:
        model = manager.Payment
        exclude = ('shipment_set', 'customs_set', )


class CustomsType(graphene_django.DjangoObjectType):
    duty = graphene.Field(PaymentType)
    commodities = graphene.List(CommodityType)
    options = generic.GenericScalar()

    class Meta:
        model = manager.Customs
        exclude = ('shipment_set', 'template')

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


class TrackerType(graphene_django.DjangoObjectType):
    tracking_carrier = graphene.Field(SystemConnectionType)
    events = generic.GenericScalar()

    class Meta:
        model = manager.Tracking
        filter_fields = ['delivered']
        interfaces = (CustomNode,)


class ShipmentType(graphene_django.DjangoObjectType):
    carrier_id = graphene.String()
    carrier_name = graphene.String()

    shipper = graphene.Field(AddressType)
    recipient = graphene.Field(AddressType)
    customs = graphene.Field(CustomsType)
    payment = graphene.Field(PaymentType)
    parcels = graphene.List(ParcelType)

    services = graphene.List(graphene.String)
    carrier_ids = graphene.List(graphene.String)
    options = generic.GenericScalar()
    meta = generic.GenericScalar()
    messages = generic.GenericScalar()
    selected_rate = generic.GenericScalar()
    rates = generic.GenericScalar()

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
    class Meta:
        model = model_type
        exclude = ('carrier_ptr', )

    return type(model_type.__name__, (graphene_django.DjangoObjectType, ConnectionType), dict(Meta=Meta))


class ConnectionType(graphene.Union):

    class Meta:
        types = tuple(setup_carrier_model(carrier_model) for carrier_model in providers.MODELS.values())
