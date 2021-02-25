import graphene
from graphene_django import DjangoObjectType

from django.contrib.auth import get_user_model

from purpleserver.core.gateway import Carriers
from purpleserver.providers.models import Carrier, MODELS
from purpleserver.manager.models import (
    Address, Parcel, Commodity, Payment, Customs, Pickup, Tracking, Shipment
)

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('password', 'carrier_set', 'is_active')


class CarrierType(DjangoObjectType):
    class Meta:
        model = Carrier


class AddressType(DjangoObjectType):
    class Meta:
        model = Address
        exclude = ('payment_set', 'pickup_set', 'recipient', 'shipper')


class ParcelType(DjangoObjectType):
    class Meta:
        model = Parcel
        exclude = ('shipment_parcels', )


class CommodityType(DjangoObjectType):
    class Meta:
        model = Commodity
        exclude = ('customs_set', )


class PaymentType(DjangoObjectType):
    class Meta:
        model = Payment
        exclude = ('customs_set', 'shipment_set')


class CustomsType(DjangoObjectType):
    class Meta:
        model = Customs
        exclude = ('shipment_set', 'shipment_commodities')


class PickupType(DjangoObjectType):
    class Meta:
        model = Pickup


class TrackingType(DjangoObjectType):
    class Meta:
        model = Tracking


class ShipmentType(DjangoObjectType):
    class Meta:
        model = Shipment
        exclude = ('pickup_shipments', )


def setup_carrier_model(model_type):
    class Meta:
        model = model_type

    return type(model_type.__name__, (DjangoObjectType,), dict(Meta=Meta))


class ConnectionType(graphene.Union):
    class Meta:
        types = tuple(setup_carrier_model(carrier_model) for carrier_model in MODELS.values())


class Query(graphene.ObjectType):
    user = graphene.Field(UserType)
    user_carriers = graphene.List(ConnectionType)
    system_carriers = graphene.List(CarrierType)
    addresses = graphene.List(AddressType)
    parcels = graphene.List(ParcelType)
    customs = graphene.List(CustomsType)
    pickups = graphene.List(PickupType)
    trackers = graphene.List(TrackingType)
    shipments = graphene.List(ShipmentType)

    def resolve_user(self, info):
        return info.context.user

    def resolve_user_carriers(self, info, **kwargs):
        connections = info.context.user.carrier_set.all().order_by('-created_at')
        return [connection.settings for connection in connections]

    def resolve_system_carriers(self, _, **kwargs):
        return Carriers.list(system_only=True, **kwargs)

    def resolve_addresses(self, info, **kwargs):
        return info.context.user.address_set.all()

    def resolve_payments(self, info, **kwargs):
        return info.context.user.commodity_set.all()


schema = graphene.Schema(query=Query)
