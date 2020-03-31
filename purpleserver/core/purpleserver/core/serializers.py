from purplship.package.mappers import Providers
from rest_framework.serializers import (
    Serializer, CharField, FloatField, BooleanField, IntegerField, ListField, DictField, ChoiceField, ListSerializer,
    UUIDField
)

CARRIERS = [(k, k) for k in Providers.keys()]


class StringListField(ListField):
    child = CharField()


class CarrierSettings(Serializer):
    carrier = ChoiceField(choices=CARRIERS)
    settings = DictField(required=True)


class CarrierSettingsList(ListSerializer):
    child = CarrierSettings()


class Address(Serializer):

    id = CharField(required=False)
    postal_code = CharField(required=True)
    city = CharField(required=False)
    federal_tax_id = CharField(required=False)
    state_tax_id = CharField(required=False)
    person_name = CharField(required=False)
    company_name = CharField(required=False)
    country_code = CharField(required=False)
    email = CharField(required=False)
    phone_number = CharField(required=False)

    state_code = CharField(required=False)
    suburb = CharField(required=False)
    residential = BooleanField(required=False)

    address_line1 = CharField(required=False)
    address_line2 = CharField(required=False)


class ShippingAddress(Serializer):

    id = CharField(required=False)
    postal_code = CharField(required=True)
    city = CharField(required=True)
    federal_tax_id = CharField(required=False)
    state_tax_id = CharField(required=False)
    person_name = CharField(required=True)
    company_name = CharField(required=True)
    country_code = CharField(required=True)
    email = CharField(required=False)
    phone_number = CharField(required=False)

    state_code = CharField(required=True)
    suburb = CharField(required=False)
    residential = BooleanField(required=False)

    address_line1 = CharField(required=True)
    address_line2 = CharField(required=False)


class Commodity(Serializer):

    id = CharField(required=False)
    weight = FloatField(required=False)
    width = FloatField(required=False)
    height = FloatField(required=False)
    length = FloatField(required=False)
    description = CharField(required=False)
    quantity = IntegerField(required=False)
    sku = CharField(required=False)
    value_amount = FloatField(required=False)
    value_currency = CharField(required=False)
    origin_country = CharField(required=False)


class Parcel(Serializer):

    id = CharField(required=False)
    weight = FloatField(required=False)
    width = FloatField(required=False)
    height = FloatField(required=False)
    length = FloatField(required=False)
    packaging_type = CharField(required=False)
    package_preset = CharField(required=False)
    reference = CharField(required=False)
    description = CharField(required=False)
    content = CharField(required=False)
    is_document = BooleanField(required=False)
    weight_unit = CharField(required=False)
    dimension_unit = CharField(required=False)
    services = StringListField(required=False)


class Invoice(Serializer):

    date = CharField(required=True)
    identifier = CharField(required=False)
    type = CharField(required=False)
    copies = IntegerField(required=False)


class Card(Serializer):

    type = CharField(required=True)
    number = CharField(required=True)
    expiry_month = CharField(required=True)
    expiry_year = CharField(required=True)
    security_code = CharField(required=True)
    name = CharField(required=False)
    postal_code = CharField(required=False)


class Payment(Serializer):

    paid_by = CharField(required=True)
    amount = FloatField(required=False)
    currency = CharField(required=False)
    account_number = CharField(required=False)
    credit_card = Card(required=False)
    contact = Address(required=False)


class Customs(Serializer):

    no_eei = CharField(required=False)
    aes = CharField(required=False)
    description = CharField(required=False)
    terms_of_trade = CharField(required=False)
    commodities = ListField(child=Commodity(), required=False)
    duty = Payment(required=False)
    invoice = Invoice(required=False)
    commercial_invoice = BooleanField(required=False)


class Doc(Serializer):

    type = CharField(required=False)
    format = CharField(required=False)
    image = CharField(required=False)


class RateRequest(Serializer):
    shipper = Address(required=True)
    recipient = Address(required=True)
    parcel = Parcel(required=True)

    options = DictField(required=False)


class TrackingRequest(Serializer):

    tracking_numbers = StringListField(required=True)
    language_code = CharField(required=False)
    level_of_details = CharField(required=False)


class PickupRequest(Serializer):

    date = CharField(required=True)

    address = Address(required=True)
    parcels = ListField(child=Parcel(), required=False)

    ready_time = CharField(required=False)
    closing_time = CharField(required=False)
    instruction = CharField(required=False)
    package_location = CharField(required=False)


class PickupUpdateRequest(Serializer):

    date = CharField(required=True)
    address = Address(required=True)
    parcels = ListField(child=Parcel(), required=False)

    confirmation_number = CharField(required=False)
    ready_time = CharField(required=False)
    closing_time = CharField(required=False)
    instruction = CharField(required=False)
    package_location = CharField(required=False)


class PickupCancellationRequest(Serializer):

    pickup_date = CharField(required=True)
    confirmation_number = CharField(required=True)
    person_name = CharField(required=False)
    country_code = CharField(required=False)


class COD(Serializer):

    amount = FloatField(required=True)


class Notification(Serializer):

    email = CharField(required=False)
    locale = CharField(required=False, default='en')


class Insurance(Serializer):

    amount = FloatField(required=True)


class Message(Serializer):

    carrier = CharField(required=True)
    carrier_name = CharField(required=True)
    message = CharField(required=False)
    code = CharField(required=False)
    details = DictField(required=False)


class ChargeDetails(Serializer):

    name = CharField(required=False)
    amount = FloatField(required=False)
    currency = CharField(required=False)


class TrackingEvent(Serializer):

    date = CharField(required=True)
    description = CharField(required=True)
    location = CharField(required=True)
    code = CharField(required=False)
    time = CharField(required=False)
    signatory = CharField(required=False)


class RateDetails(Serializer):

    id = UUIDField(required=False)
    carrier = CharField(required=True)
    carrier_name = CharField(required=True)
    currency = CharField(required=True)
    service = CharField(required=False)
    discount = FloatField(required=False)
    base_charge = FloatField(default=0.0)
    total_charge = FloatField(default=0.0)
    duties_and_taxes = FloatField(required=False)
    estimated_delivery = CharField(required=False)
    extra_charges = ListField(child=ChargeDetails(), required=False)


class TrackingDetails(Serializer):

    carrier = CharField(required=True)
    carrier_name = CharField(required=True)
    tracking_number = CharField(required=True)
    events = ListField(child=TrackingEvent())


class ShipmentDetails(Serializer):

    id = CharField(required=False)
    carrier = CharField(required=True)
    carrier_name = CharField(required=True)
    label = CharField(required=True)
    tracking_number = CharField(required=True)
    selected_rate = RateDetails()


class PickupDetails(Serializer):

    carrier = CharField(required=True)
    carrier_name = CharField(required=True)
    confirmation_number = CharField(required=True)
    pickup_date = CharField(required=False)
    pickup_charge = ChargeDetails(required=False)
    pickup_time = CharField(required=False)
    pickup_max_time = CharField(required=False)
    id = CharField(required=False)


class ShipmentRate(RateRequest):
    rates = ListField(child=RateDetails())


class ShipmentRequest(Serializer):
    selected_rate_id = CharField(required=True)

    rates = ListField(child=RateDetails())

    shipper = ShippingAddress(required=True)
    recipient = ShippingAddress(required=True)
    parcel = Parcel(required=True)

    options = DictField(required=False)

    payment = Payment(required=True)
    customs = Customs(required=False)
    doc_images = ListField(child=Doc(), required=False)


class Shipment(ShipmentRequest, ShipmentDetails):
    selected_rate_id = CharField(required=True)


class RateResponse(Serializer):
    messages = ListField(child=Message())
    shipment = ShipmentRate()


class ShipmentResponse(Serializer):
    messages = ListField(child=Message())
    shipment = Shipment()


class TrackingResponse(Serializer):
    messages = ListField(child=Message())
    tracking_details = TrackingDetails()
