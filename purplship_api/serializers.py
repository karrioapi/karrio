from rest_framework import serializers
from purplship.domain.Types.units import (
    PackagingUnit,
    DimensionUnit,
    WeightUnit,
    PayorType,
    Country,
    Currency
)


Countries = [(c.name, c.value) for c in list(Country)]
Currencies = [(c.name, c.value) for c in list(Currency)]
PackagingChoices = [(u.name, u.value) for u in list(PackagingUnit)]
WeightChoices = [(u.name, u.value) for u in list(WeightUnit)]
DimensionChoices = [(u.name, u.value) for u in list(DimensionUnit)]
PayorChoices = [(u.name, u.value) for u in list(PayorType)]


class StringListField(serializers.ListField):
    child = serializers.CharField()

# Types serializers

class Item(serializers.Serializer):
    id = serializers.CharField(required=False, help_text="item id")
    weight = serializers.FloatField(help_text="item weight")
    width = serializers.FloatField(required=False, default=10, help_text="item width")
    height = serializers.FloatField(required=False, default=10, help_text="item height")
    length = serializers.FloatField(required=False, default=10, help_text="item lenght")
    packaging_type = serializers.ChoiceField(
        required=False, 
        default="BOX",
        choices=PackagingChoices,
        help_text=""" 
        item packaging type
        default: 'BOX'
        """
    )
    description = serializers.CharField(required=False, help_text="item description")
    content = serializers.CharField(required=False, help_text="item content details")
    quantity = serializers.IntegerField(required=False, default=1, help_text="item quantity")
    sku = serializers.CharField(required=False, help_text="item SKU")
    code = serializers.CharField(required=False, help_text="item code (supported by few carriers)")
    value_amount = serializers.FloatField(required=False, help_text="item value")
    value_currency = serializers.ChoiceField(
        required=False, 
        choices=Currencies,
        help_text="""item value currency"""
    )
    origin_country = serializers.CharField(required=False, help_text="item origin country (check the docs)")
    extra = serializers.DictField(required=False, help_text="extra field for special details supported by a specific carriers")


class Customs(serializers.Serializer):
    description = serializers.CharField(required=False, help_text='shipment description')
    terms_of_trade = serializers.CharField(required=False, help_text='Terms of trades (check the docs)')
    no_eei = serializers.CharField(required=False, help_text='NOEEI type of the shipment.')
    aes = serializers.CharField(required=False, help_text='AES / ITN reference of the shipment.')
    items = serializers.ListField(child=Item(), help_text='list of items for customs')
    commercial_invoice = serializers.BooleanField(required=False, help_text='Specify if shipment is commercial')
    extra = serializers.DictField(required=False, help_text="extra field for special details supported by a specific carriers")


class Doc(serializers.Serializer):
    format = serializers.CharField(required=False, help_text='label format')
    type = serializers.CharField(required=False, help_text='label type')
    image = serializers.CharField(required=False, help_text='image type')
    extra = serializers.DictField(required=False, help_text="extra field for special details supported by a specific carriers")


class Invoice(serializers.Serializer):
    date = serializers.CharField(required=False, help_text='invoice date')
    identifier = serializers.CharField(required=False, help_text='invoice identifier')
    type = serializers.CharField(required=False, help_text='invoice type')
    copies = serializers.IntegerField(required=False, help_text='Number of copies')
    extra = serializers.DictField(required=False, help_text="extra field for special details supported by a specific carriers")


class Party(serializers.Serializer):
    postal_code = serializers.CharField(required=False, help_text='postal code')
    city = serializers.CharField(required=False, help_text='city')
    type = serializers.CharField(required=False, help_text='type (supported by certain carriers)')
    tax_id = serializers.CharField(required=False, help_text='Tax Identification Number')
    person_name = serializers.CharField(required=False, help_text='Attention Name')
    company_name = serializers.CharField(required=False, help_text='Company Name')
    country_name = serializers.CharField(required=False, help_text='Country Name')
    country_code = serializers.CharField(required=False, help_text='Country Code')
    phone_number = serializers.CharField(required=False, help_text='Phone Number')
    email_address = serializers.CharField(required=False, help_text='Email Address')
    state_code = serializers.CharField(required=False, help_text='Province or State name')
    suburb = serializers.CharField(required=False, help_text='Suburb code')
    postal_code = serializers.CharField(required=False, help_text='postal code')
    address_lines = StringListField(required=False, help_text='Address lines')
    account_number = serializers.CharField(required=False, help_text='Account Number')
    extra = serializers.DictField(required=False, help_text="extra field for special details supported by a specific carriers")


class Option(serializers.Serializer):
    code = serializers.CharField(required=False, help_text="option codename")
    value = serializers.DictField(required=False, help_text="extra field for special details supported by a specific carriers")
    extra = serializers.DictField(required=False, help_text="extra field for special details supported by a specific carriers")


class Shipment(serializers.Serializer):
    items = serializers.ListField(child=Item(), help_text='list of shipment items')
    insured_amount = serializers.FloatField(required=False, help_text='Insured amount')
    total_items = serializers.IntegerField(required=False, help_text='Number of items')
    packaging_type = serializers.ChoiceField(
        required=False, 
        default="BOX",
        choices=PackagingChoices,
        help_text=""" 
        shipment packaging type
        default: 'BOX'
        """
    )
    is_document = serializers.BooleanField(required=False, help_text='Document only shipment flag. (Non dutiable for international shipping)')
    currency = serializers.ChoiceField(
        required=False, 
        choices=Currencies,
        help_text="""General shipment values currency"""
    )
    total_weight = serializers.FloatField(required=False, help_text='Total shipment weight')
    weight_unit = serializers.ChoiceField(
        required=False, 
        default='KG',
        choices=WeightChoices, 
        help_text="""
        General package weight unit.
        Supported Units: "LB" (Pound), "KG" (Kilogram)
        default: 'KG'
        """
    )
    dimension_unit = serializers.ChoiceField(
        required=False, 
        default='CM',
        choices=DimensionChoices, 
        help_text="""
        General package dimensions unit.
        Supported Units: "IN" (Inch), "CM" (Centimeter)
        default: 'CM'
        """
    )
    paid_by = serializers.ChoiceField(
        required=False, 
        choices=PayorChoices,
        help_text="""
        Shipment paid by.
        Values: "SENDER", "THIRD_PARTY", "RECIPIENT"
        """
    )
    payment_country_code = serializers.CharField(required=False, help_text='Payment country code')
    payment_account_number = serializers.CharField(required=False, help_text='Shipment payment account number')
    services = StringListField(required=False, help_text='Shipment services (check carriers services docs)')
    options = serializers.ListField(child=Option(), required=False, help_text='Shipping sepcial services and option')
    date = serializers.CharField(required=False, help_text='Shipment date')
    payment_type = serializers.CharField(required=False, help_text="""
    Payment type: account_number, credit_card
    """)
    duty_paid_by = serializers.ChoiceField(
        required=False, 
        default='SENDER',
        choices=PayorChoices,
        help_text="""
        Shipment paid by.
        Values: "SENDER", "THIRD_PARTY", "RECIPIENT"
        default: 'SENDER'
        """
    )
    duty_payment_account = serializers.CharField(required=False, help_text='Duty payer account number')
    declared_value = serializers.FloatField(required=False, help_text='Shipment total value')
    customs = Customs(required=False, help_text='Customs paperwork details')
    references = StringListField(required=False, help_text="""
    Shipment references.
    Ex: order number, platform reference...
    """)
    label = Doc(required=False, help_text='Label specification details')
    invoice = Invoice(required=False, help_text='Shipment invoice details')
    doc_images = serializers.ListField(child=Doc(), required=False, help_text='All required documents files. eg: invoice...')
    ship_date = serializers.CharField(required=False, help_text='Expected shipment date (supported by certain carriers)')
    extra = serializers.DictField(required=False, help_text="extra field for special details supported by a specific carriers")


class ShipmentRequest(serializers.Serializer):
    shipper = Party(help_text='Shipper (Sender/ShipFrom) details')
    recipient = Party(help_text='Recipient (Receiver/ShipTo) details')
    shipment = Shipment(help_text='Shipment details')


class RateRequest(ShipmentRequest):

    # additional field for API
    carriers = StringListField(required=False, help_text="""
    Note: the 'carriers' field allow you to specify the list of carriers
    your request is targetting. 
    When no carriers is specified the request is sent to all of them

    This server is currently configured with these carriers: 'ups', 'dhl'
    """)


class TrackingRequest(serializers.Serializer):
    tracking_numbers = StringListField(help_text='List of tracking numbers')
    language_code = serializers.CharField(required=False, help_text='Language code (supported by certain carriers)')
    extra = serializers.DictField(required=False, help_text="extra field for special details supported by a specific carriers")


class PickupRequest(serializers.Serializer):
    date = serializers.CharField(required=False, help_text='Pickup date')
    account_number = serializers.CharField(required=False, help_text='Shipper account number')
    weight = serializers.FloatField(required=False, help_text='Shipment total weight')
    weight_unit = serializers.ChoiceField(
        required=False, 
        default="KG",
        choices=WeightChoices, 
        help_text="""
        General package weight unit.
        Supported Units: "LB" (Pound), "KG" (Kilogram)
        default: 'KG'
        """
    )
    pieces = serializers.FloatField(required=False, help_text='Number of shipment pieces')
    ready_time = serializers.CharField(required=False, help_text="""
    Shipment ready time for pickup.
    Format: '00:00', 'TT:MM'
    """)
    closing_time = serializers.CharField(required=False, help_text="""
    Pickup location closing time.
    Format: '00:00', 'TT:MM'
    """)
    instruction = serializers.CharField(required=False, help_text='Pickup instruction')
    package_location = serializers.CharField(required=False, help_text="""
    Shipment items location.
    Ex: Back of the entrance door
    """)

    city = serializers.CharField(required=False, help_text='Pickup address city')
    postal_code = serializers.CharField(required=False, help_text='Pickup address postal code')
    state = serializers.CharField(required=False, help_text='Pickup address state or province name')
    state_code = serializers.CharField(required=False, help_text='Pickup address state or province code')
    country_name = serializers.CharField(required=False, help_text='Pickup address country name')
    country_code = serializers.CharField(required=False, help_text='Pickup address country code')

    person_name = serializers.CharField(required=False, help_text='Pickup attention name')
    company_name = serializers.CharField(required=False, help_text='Pickup company name (if company)')
    phone_number = serializers.CharField(required=False, help_text='Phone number')
    email_address = serializers.CharField(required=False, help_text='Email address')
    is_business = serializers.BooleanField(required=False, help_text='Flag to specify if pickup address is a business')

    confirmation_number = serializers.CharField(required=False, help_text='Pickup confirmation number (only required for a pickup update)')

    address_lines = StringListField(required=False, help_text='Address lines')
    extra = serializers.DictField(required=False, help_text="extra field for special details supported by a specific carriers")


class PickupCancellationRequest(serializers.Serializer):
    pickup_date = serializers.CharField(required=False, help_text='Expected pickup date')
    confirmation_number = serializers.CharField(required=False, help_text='Pickup confirmation number')
    person_name = serializers.CharField(required=False, help_text='Attention name')
    country_code = serializers.CharField(required=False, help_text='Country code')
    extra = serializers.DictField(required=False, help_text="extra field for special details supported by a specific carriers")



""" Responses Details type """

class Error(serializers.Serializer):
    message = serializers.CharField(help_text='Error message')
    code = serializers.CharField(required=False, help_text='Error code from carrier')
    carrier = serializers.CharField(required=False, help_text='Carrier name')


class ChargeDetails(serializers.Serializer):
    name = serializers.CharField(help_text='Charge indentification description')
    amount = serializers.CharField(help_text='Monetary value')
    currency = serializers.CharField(help_text='Monetary currency')


class ReferenceDetails(serializers.Serializer):
    value = serializers.CharField(help_text='Reference value')
    type = serializers.CharField(required=False, help_text='type details')


class TimeDetails(serializers.Serializer):
    value = serializers.CharField(required=False, help_text='Time value')
    name = serializers.CharField(required=False, help_text='Specified time description')


class TrackingEvent(serializers.Serializer):
    date = serializers.CharField(help_text='Date')
    time = serializers.CharField(required=False, help_text='Time')
    description = serializers.CharField(help_text='Description')
    location = serializers.CharField(help_text='Current Location')
    code = serializers.CharField(help_text='Carrier attached code')
    signatory = serializers.CharField(required=False, help_text='Shipment signatory details')


class QuoteDetails(serializers.Serializer):
    carrier = serializers.CharField(help_text='Quote (Rate) details')
    service_name = serializers.CharField(help_text='Service name')
    service_type = serializers.CharField(help_text='Service type')
    base_charge = serializers.CharField(help_text='value before any discount or extra fees')
    duties_and_taxes = serializers.CharField(help_text='Duties and taxes value')
    total_charge = serializers.CharField(help_text='Final total shipment charge value')
    discount = serializers.CharField(help_text='Discount value')
    extra_charges = serializers.ListField(child=ChargeDetails(), help_text='Extra charges details')
    delivery_date = serializers.CharField(required=False, help_text='Expected delivery date')


class TrackingDetails(serializers.Serializer):
    carrier = serializers.CharField(help_text='carrier name')
    shipment_date = serializers.CharField(required=False, help_text='Expected shipment date')
    tracking_number = serializers.CharField(help_text='Tracking number')
    events = serializers.ListField(child=TrackingEvent(), help_text='Tracking event list')


class ShipmentDetails(serializers.Serializer):
    carrier = serializers.CharField(help_text='Carrier name')
    tracking_number = serializers.CharField(help_text='Tracking number')
    shipment_date = serializers.CharField(help_text='Shipment expected date')
    documents = StringListField(required=False, help_text='documents/images list')
    service = serializers.CharField(help_text='Carrier service indentifier')
    reference = ReferenceDetails(help_text='Shipment reference')
    total_charge = ChargeDetails(help_text='Shipment charges')


class PickupDetails(serializers.Serializer):
    carrier = serializers.CharField(help_text='Carrier name')
    confirmation_number = serializers.CharField(help_text='Confirmation number')
    pickup_date = serializers.CharField(help_text='Pickup date')
    pickup_charge = ChargeDetails(help_text='Pickup charge')
    ref_times = serializers.ListField(child=TimeDetails(), help_text='Response reference times')


""" Responses Serializers """

class rate_response(QuoteDetails):
    rates = serializers.ListField(child=QuoteDetails())
    errors = serializers.ListField(child=Error())

class multi_tracking_response(serializers.Serializer):
    tracking = serializers.ListField(child=TrackingDetails())
    errors = serializers.ListField(child=Error())

class tracking_response(serializers.Serializer):
    tracking = TrackingDetails()
    errors = serializers.ListField(child=Error())

class shipping_response(serializers.Serializer):
    shipment = ShipmentDetails()
    errors = serializers.ListField(child=Error())

class pickup_response(serializers.Serializer):
    pickup = PickupDetails()
    errors = serializers.ListField(child=Error())

