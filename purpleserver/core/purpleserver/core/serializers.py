from purpleserver.core.models import MODELS
from purplship.core.units import (
    Country, WeightUnit, DimensionUnit, PackagingUnit, PaymentType, Currency, PrinterType
)
from rest_framework.serializers import (
    Serializer, CharField, FloatField, BooleanField, IntegerField, ListField,
    ChoiceField, ListSerializer, UUIDField, DictField, URLField
)

CARRIERS = [(k, k) for k in MODELS.keys()]
COUNTRIES = [(c.name, c.name) for c in list(Country)]
CURRENCIES = [(c.name, c.name) for c in list(Currency)]
WEIGHT_UNIT = [(c.name, c.name) for c in list(WeightUnit)]
DIMENSION_UNIT = [(c.name, c.name) for c in list(DimensionUnit)]
PACKAGING_UNIT = [(c.name, c.name) for c in list(PackagingUnit)]
PAYMENT_TYPES = [(c.name, c.name) for c in list(PaymentType)]
PRINTER_TYPES = [(c.name, c.name) for c in list(PrinterType)]


class StringListField(ListField):
    child = CharField()


class CarrierSettings(Serializer):
    carrier = ChoiceField(choices=CARRIERS, required=True, help_text="Indicates a carrier (type)")
    carrier_name = CharField(required=True, help_text="Indicates a specific carrier configuration name.")
    test = BooleanField(required=True, help_text="""
    The test flag indicates whether to use a carrier configured for test. 
    """)


class CarrierFilters(Serializer):
    carrier = ChoiceField(choices=CARRIERS, required=False, help_text="Indicates a carrier (type)")
    carrierName = CharField(required=False, help_text="Indicates a specific carrier configuration name.")
    test = BooleanField(required=False, default=False, help_text="""
    The test flag indicates whether to use a carrier configured for test. 
    """)


class TestFilters(Serializer):
    test = BooleanField(required=False, default=False, help_text="""
    The test flag indicates whether to use a carrier configured for test. 
    """)


class CarrierSettingsList(ListSerializer):
    child = CarrierSettings()


class Address(Serializer):

    id = UUIDField(required=False, help_text="A unique address identifier")
    postal_code = CharField(required=False, help_text="The address postal code")
    city = CharField(required=False, help_text="The address city")
    federal_tax_id = CharField(required=False, help_text="The party frederal tax id")
    state_tax_id = CharField(required=False, help_text="The party state id")
    person_name = CharField(required=False, help_text="attention to")
    company_name = CharField(required=False, help_text="The company name if the party is a not residential")
    country_code = ChoiceField(required=True, choices=COUNTRIES, help_text="The address country code")
    email = CharField(required=False, help_text="The party email")
    phone_number = CharField(required=False, help_text="""
    The party phone number.
    
    Note that the expected format is: **1 514 0000000**
    
    Country Code | Area Code | Phone
    --- | --- | ---
    1 | 514 | 0000000
    """)

    state_code = CharField(required=False, help_text="The address state code")
    suburb = CharField(required=False, help_text="The address suburb if known")
    residential = BooleanField(
        required=False,
        help_text="Indicates if The address is residential or commercial (enterprise)"
    )

    address_line1 = CharField(required=False, help_text="The address line with street number")
    address_line2 = CharField(required=False, help_text="The address line with suite number")


class ShippingAddress(Serializer):

    id = UUIDField(required=False, help_text="A unique address identifier")
    postal_code = CharField(required=False, help_text="The address postal code")
    city = CharField(required=True, help_text="The address city")
    federal_tax_id = CharField(required=False, help_text="The party frederal tax id")
    state_tax_id = CharField(required=False, help_text="The party state id")
    person_name = CharField(required=True, help_text="attention to")
    company_name = CharField(required=False, help_text="The company name if the party is a company")
    country_code = ChoiceField(required=True, choices=COUNTRIES, help_text="The address country code")
    email = CharField(required=False, help_text="The party email")
    phone_number = CharField(required=False, help_text="""
    The party phone number.
    
    Note that the expected format is: **1 514 0000000**
    
    Country Code | Area Code | Phone
    --- | --- | ---
    1 | 514 | 0000000
    """)

    state_code = CharField(required=False, help_text="The address state code")
    suburb = CharField(required=False, help_text="The address suburb if known")
    residential = BooleanField(
        required=False,
        help_text="Indicate if the address is residential or commercial (enterprise)"
    )

    address_line1 = CharField(required=True, help_text="The address line with street number")
    address_line2 = CharField(required=False, help_text="The address line with suite number")


class Commodity(Serializer):

    id = UUIDField(required=False, help_text="A unique commodity's identifier")
    weight = FloatField(required=False, help_text="The commodity's weight")
    width = FloatField(required=False, help_text="The commodity's width")
    height = FloatField(required=False, help_text="The commodity's height")
    length = FloatField(required=False, help_text="The commodity's lenght")
    description = CharField(required=False, help_text="A description of the commodity")
    quantity = IntegerField(required=False, help_text="The commodity's quantity (number or item)")
    sku = CharField(required=False, help_text="The commodity's sku number")
    value_amount = FloatField(required=False, help_text="The monetary value of the commodity")
    value_currency = CharField(required=False, help_text="The currency of the commodity value amount")
    origin_country = CharField(required=False, help_text="The origin or manufacture country")


class Parcel(Serializer):

    id = CharField(required=False, help_text="A unique parcel identifier")
    weight = FloatField(required=False, help_text="The parcel's weight")
    width = FloatField(required=False, help_text="The parcel's width")
    height = FloatField(required=False, help_text="The parcel's height")
    length = FloatField(required=False, help_text="The parcel's length")
    packaging_type = ChoiceField(required=False, choices=PACKAGING_UNIT, help_text="""
    The parcel's packaging type.
    
    Note that the packaging is optional when using a package preset
    
    For specific carriers packaging type, please consult the reference.
    """)
    package_preset = CharField(required=False, help_text="""
    The parcel's package preset.
    
    For specific carriers package preset, please consult the reference.
    """)
    description = CharField(required=False, help_text="The parcel's description")
    content = CharField(required=False, help_text="The parcel's content description")
    is_document = BooleanField(required=False, help_text="Indicates if the parcel is composed of documents only")
    weight_unit = ChoiceField(required=False, choices=WEIGHT_UNIT, help_text="The parcel's weight unit")
    dimension_unit = ChoiceField(required=False, choices=DIMENSION_UNIT, help_text="The parcel's dimension unit")


class Invoice(Serializer):

    date = CharField(required=True, help_text="The invoice date")
    identifier = CharField(required=False, help_text="The internal invoice document identifier")
    type = CharField(required=False, help_text="The invoice type")
    copies = IntegerField(required=False, help_text="The number of invoice copies")


class Card(Serializer):

    type = CharField(required=True, help_text="The credit card type")
    number = CharField(required=True, help_text="The credit card number")
    expiry_month = CharField(required=True, help_text="The credit card expiry month (MM)")
    expiry_year = CharField(required=True, help_text="The credit card expiry year (YYYY)")
    security_code = CharField(required=True, help_text="The credit card security code often at the back (000)")
    name = CharField(required=False, help_text="The name inscribed on the credit card")
    postal_code = CharField(required=False, help_text="The credit card registration address postal code")


class Payment(Serializer):

    paid_by = ChoiceField(required=True, choices=PAYMENT_TYPES, help_text="The payment payer")
    amount = FloatField(required=False, help_text="The payment amount if known")
    currency = ChoiceField(required=True, choices=CURRENCIES, help_text="The payment amount currency")
    account_number = CharField(required=False, help_text="The selected rate carrier payer account number")
    credit_card = Card(required=False, help_text="The payment credit card for payment by card")
    contact = Address(required=False, help_text="The billing address")


class Customs(Serializer):

    no_eei = CharField(required=False)
    aes = CharField(required=False)
    description = CharField(required=False)
    terms_of_trade = CharField(required=False, help_text="The customs 'term of trade' also known as 'incoterm'")
    commodities = ListField(child=Commodity(), required=False, help_text="The parcel content items")
    duty = Payment(required=False, help_text="""
    The duty payment details.
    
    Note that this is required for a Dutiable parcel shipped internationally.
    """)
    invoice = Invoice(required=False, help_text="The shipment invoice required for commercial shipment.")
    commercial_invoice = BooleanField(required=False, help_text="Indicates if the shipment is commercial")


class Doc(Serializer):

    type = CharField(required=True, help_text="The document type")
    image = CharField(required=True, help_text="encoded base64 string of the document")
    format = CharField(required=False, help_text="The document format")


class COD(Serializer):

    amount = FloatField(required=True, help_text="The amount to collect on delivery")


class Notification(Serializer):

    email = CharField(required=False, help_text="""
    The alternative notification email.
    
    Note that by default the recipient email will be used.
    """)
    locale = CharField(required=False, default='en')


class Insurance(Serializer):

    amount = FloatField(required=True, help_text="The insurance coverage amount.")


class ShipmentOption(Serializer):
    cod = COD(required=False, help_text="The cash that should be collected on delivery.")
    currency = ChoiceField(required=False, choices=CURRENCIES, help_text="The shipment currency")
    insurance = Insurance(required=False, help_text="adding an insurance to the shipment")
    notification = Notification(required=False, help_text="The notification configuration")
    printing = ChoiceField(required=False, choices=PRINTER_TYPES, help_text="The label printing type")
    option1 = CharField(required=False, help_text="""
    Please consult the reference for additional specific carriers options.
    """)
    option2 = CharField(required=False, help_text="""
    Please consult the reference for additional specific carriers options.
    """)


class RateShipperAddress(Address):
    pass


class RateRecipientAddress(Address):
    pass


class RateRequest(Serializer):
    shipper = RateShipperAddress(required=True, help_text="The origin address of the shipment (address from)")
    recipient = RateRecipientAddress(required=True, help_text="The shipment destination address (address to)")
    parcel = Parcel(required=True, help_text="The shipment's parcel")

    services = StringListField(required=False, help_text="""
    The requested carrier service for the shipment.
    
    Please consult the reference for specific carriers services.
    
    Note that this is a list because on a Multi-carrier rate request you could specify a service per carrier.
    """)
    options = DictField(required=False, help_text=f"""
    The options available for the shipment.

    Please consult the reference for additional specific carriers options.
    """)
    reference = CharField(required=False, help_text="The shipment reference")


class TrackingRequest(Serializer):

    tracking_numbers = StringListField(required=True, help_text="a list of tracking numbers to fetch.")
    language_code = CharField(required=False, default="en", help_text="The tracking details language code")
    level_of_details = CharField(required=False, help_text="The level of event details.")


class PickupRequest(Serializer):

    date = CharField(required=True, help_text="The expected pickup date")
    address = Address(required=True, help_text="The pickup address")
    parcels = ListField(child=Parcel(), required=False, help_text="The shipment parcels to pickup.")

    ready_time = CharField(required=True, help_text="The ready time for pickup.")
    closing_time = CharField(required=True, help_text="The closing or late time of the pickup")
    instruction = CharField(required=False, help_text="""
    The pickup instruction.
    
    eg: Handle with care.
    """)
    package_location = CharField(required=False, help_text="""
    The package(s) location.
    
    eg: Behind the entrance door.
    """)


class PickupUpdateRequest(Serializer):

    date = CharField(required=True, help_text="The expected pickup date")
    address = Address(required=True, help_text="The pickup address")
    parcels = ListField(child=Parcel(), required=False, help_text="The shipment parcels to pickup.")

    confirmation_number = CharField(required=True, help_text="pickup identification number")

    ready_time = CharField(required=True, help_text="The ready time for pickup.")
    closing_time = CharField(required=True, help_text="The closing or late time of the pickup")
    instruction = CharField(required=False, help_text="""
    The pickup instruction.
    
    eg: Handle with care.
    """)
    package_location = CharField(required=False, help_text="""
    The package(s) location.
    
    eg: Behind the entrance door.
    """)


class PickupCancellationRequest(Serializer):

    pickup_date = CharField(required=True, help_text="The expected pickup date")
    confirmation_number = CharField(required=True, help_text="pickup identification number")
    person_name = CharField(required=False, help_text="responsible party name")
    country_code = ChoiceField(required=False, choices=COUNTRIES, help_text="pickup address country code")


class Message(Serializer):

    carrier = CharField(required=True, help_text="The targeted carrier")
    carrier_name = CharField(required=True, help_text="The targeted carrier name (unique identifier)")
    message = CharField(required=False, help_text="The error or warning message")
    code = CharField(required=False, help_text="The message code")
    details = DictField(required=False, help_text="any additional details")


class ChargeDetails(Serializer):

    name = CharField(required=False, help_text="The charge description")
    amount = FloatField(required=False, help_text="The charge monetary value")
    currency = CharField(required=False, help_text="The charge amount currency")


class TrackingEvent(Serializer):

    date = CharField(required=True, help_text="The tracking event's date")
    description = CharField(required=True, help_text="The tracking event's description")
    location = CharField(required=True, help_text="The tracking event's location")
    code = CharField(required=False, help_text="The tracking event's code")
    time = CharField(required=False, help_text="The tracking event's time")
    signatory = CharField(required=False, help_text="The tracking signature on delivery")


class RateDetails(Serializer):

    id = UUIDField(required=False, help_text="A unique rate identifier")
    carrier = CharField(required=True, help_text="The rate's carrier")
    carrier_name = CharField(required=True, help_text="The targeted carrier's name (unique identifier)")
    currency = CharField(required=True, help_text="The rate monetary values currency code")
    service = CharField(required=False, help_text="The carrier's rate (quote) service")
    discount = FloatField(required=False, help_text="The monetary amount of the discount on the rate")
    base_charge = FloatField(default=0.0, help_text="""
    The rate's monetary amount of the base charge.
    
    This is the net amount of the rate before additional charges
    """)
    total_charge = FloatField(default=0.0, help_text="""
    The rate's monetary amount of the total charge.
    
    This is the gross amount of the rate after adding the additional charges
    """)
    duties_and_taxes = FloatField(required=False, help_text="The monetary amount of the duties and taxes if applied")
    estimated_delivery = CharField(required=False, help_text="The estimated delivery date")
    extra_charges = ListField(child=ChargeDetails(), required=False, help_text="list of the rate's additional charges")


class TrackingDetails(Serializer):

    carrier = CharField(required=True, help_text="The tracking carrier")
    carrier_name = CharField(required=True, help_text="The tracking carrier configured identifier")
    tracking_number = CharField(required=True, help_text="The shipment tracking number")
    events = ListField(child=TrackingEvent(), help_text="The tracking details events")


class ShipmentDetails(Serializer):

    id = UUIDField(required=False, help_text="A unique shipment identifier")
    carrier = CharField(required=True, help_text="The shipment carrier")
    carrier_name = CharField(required=True, help_text="The shipment carrier configured identifier")
    label = CharField(required=True, help_text="The shipment label in base64 string")
    tracking_number = CharField(required=True, help_text="The shipment tracking number")
    selected_rate = RateDetails(required=False, help_text="The shipment selected rate")


class PickupDetails(Serializer):

    id = CharField(required=False, help_text="A unique pickup identifier")
    carrier = CharField(required=True, help_text="The pickup carrier")
    carrier_name = CharField(required=True, help_text="The pickup carrier configured name")
    confirmation_number = CharField(required=True, help_text="The pickup confirmation identifier")
    pickup_date = CharField(required=False, help_text="The pickup date")
    pickup_charge = ChargeDetails(required=False, help_text="The pickup cost details")
    ready_time = CharField(required=False, help_text="The pickup expected ready time")
    closing_time = CharField(required=False, help_text="The pickup expected closing or late time")


class ShipmentRate(RateRequest):
    rates = ListField(child=RateDetails(), help_text="The list of returned ")


class ShipmentShipperAddress(ShippingAddress):
    pass


class ShipmentRecipientAddress(ShippingAddress):
    pass


class ShipmentRequest(Serializer):
    selected_rate_id = UUIDField(required=True, help_text="The selected shipment rate unique identifier")

    rates = ListField(child=RateDetails(), help_text="The list for shipment rates fetched previously")

    shipper = ShipmentShipperAddress(required=True, help_text="The origin address of the shipment (address from)")
    recipient = ShipmentRecipientAddress(required=True, help_text="The shipment destination address (address to)")
    parcel = Parcel(required=True, help_text="The shipment's parcel")

    services = StringListField(required=False, help_text="""
    The requested carrier service for the shipment.

    Please consult the reference for specific carriers services.
    
    Note that this is a list because on a Multi-carrier rate request you could specify a service per carrier.
    """)
    options = DictField(required=False, help_text="""
    The options available for the shipment.

    Please consult the reference for additional specific carriers options.
    """)

    payment = Payment(required=True, help_text="The payment details")
    customs = Customs(required=False, help_text="""
    The customs details.
    
    Note that this is required for the shipment of an international Dutiable parcel.
    """)
    doc_images = ListField(child=Doc(), required=False, help_text="""
    The list of documents to attach for a paperless interantional trade.
    
    eg: Invoices...
    """)
    reference = CharField(required=False, help_text="The shipment reference")


class Shipment(ShipmentDetails, ShipmentRequest):
    selected_rate_id = UUIDField(required=True, help_text="The shipment selected rate.")
    tracking_url = URLField(required=False, help_text="The shipment tracking url")


class ErrorResponse(Serializer):
    messages = ListField(child=Message(), required=False, help_text="The list of error messages")


class RateResponse(Serializer):
    messages = ListField(child=Message(), required=False, help_text="The list of note, error or warning messages")
    shipment = ShipmentRate(required=False, help_text="The newly rated shipment")


class ShipmentResponse(Serializer):
    messages = ListField(child=Message(), required=False, help_text="The list of note or warning messages")
    shipment = Shipment(required=False, help_text="The submitted shipment's summary")


class TrackingResponse(Serializer):
    messages = ListField(child=Message(), required=False, help_text="The list of note or warning messages")
    tracking_details = TrackingDetails(required=False, help_text="The tracking details retrieved")
