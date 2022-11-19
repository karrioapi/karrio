import enum
import rest_framework as drf

import karrio.core.units as units
import karrio.server.serializers as serializers
import karrio.server.core.validators as validators
import karrio.server.providers.models as providers


class ShipmentStatus(enum.Enum):
    draft = "draft"
    purchased = "purchased"
    cancelled = "cancelled"
    shipped = "shipped"
    in_transit = "in_transit"
    delivered = "delivered"


class TrackerStatus(enum.Enum):
    pending = "pending"
    in_transit = "in_transit"
    incident = "incident"
    delivered = "delivered"
    unknown = "unknown"


Serializer = serializers.Serializer
HTTP_STATUS = [getattr(drf.status, a) for a in dir(drf.status) if "HTTP" in a]
SHIPMENT_STATUS = [(c.name, c.name) for c in list(ShipmentStatus)]
TRACKER_STATUS = [(c.name, c.name) for c in list(TrackerStatus)]
CUSTOMS_CONTENT_TYPE = [(c.name, c.name) for c in list(units.CustomsContentType)]
INCOTERMS = [(c.name, c.name) for c in list(units.Incoterm)]
CARRIERS = [(k, k) for k in sorted(providers.MODELS.keys())]
COUNTRIES = [(c.name, c.name) for c in list(units.Country)]
CURRENCIES = [(c.name, c.name) for c in list(units.Currency)]
WEIGHT_UNIT = [(c.name, c.name) for c in list(units.WeightUnit)]
DIMENSION_UNIT = [(c.name, c.name) for c in list(units.DimensionUnit)]
PACKAGING_UNIT = [(c.name, c.name) for c in list(units.PackagingUnit)]
PAYMENT_TYPES = [(c.name, c.name) for c in list(units.PaymentType)]
LABEL_TYPES = [(c.name, c.name) for c in list(units.LabelType)]
LABEL_TEMPLATE_TYPES = [
    ("SVG", "SVG"),
    ("ZPL", "ZPL"),
]


class CarrierSettings(serializers.Serializer):
    id = serializers.CharField(required=True, help_text="A unique address identifier")
    carrier_name = serializers.ChoiceField(
        choices=CARRIERS, required=True, help_text="Indicates a carrier (type)"
    )
    carrier_id = serializers.CharField(
        required=True, help_text="Indicates a specific carrier configuration name."
    )
    test_mode = serializers.BooleanField(
        required=True,
        help_text="""
    The test flag indicates whether to use a carrier configured for test.
    """,
    )
    active = serializers.BooleanField(
        required=True,
        help_text="""
    The active flag indicates whether the carrier account is active or not.
    """,
    )
    object_type = serializers.CharField(default="carrier", help_text="Specifies the object type")


class APIError(serializers.Serializer):
    message = serializers.CharField(required=False, help_text="The error or warning message")
    code = serializers.CharField(required=False, help_text="The message code")
    details = serializers.DictField(required=False, help_text="any additional details")


class Message(APIError):

    carrier_name = serializers.CharField(required=False, help_text="The targeted carrier")
    carrier_id = serializers.CharField(
        required=False, help_text="The targeted carrier name (unique identifier)"
    )


class AddressValidation(serializers.Serializer):
    success = serializers.BooleanField(help_text="True if the address is valid")
    meta = serializers.PlainDictField(
        required=False, allow_null=True, help_text="validation service details"
    )


class AddressData(validators.AugmentedAddressSerializer):

    postal_code = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=10,
        help_text="""
    The address postal code

    **(required for shipment purchase)**
    """,
    )
    city = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=50,
        help_text="""
    The address city.

    **(required for shipment purchase)**
    """,
    )
    federal_tax_id = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=50,
        help_text="The party frederal tax id",
    )
    state_tax_id = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=50,
        help_text="The party state id",
    )
    person_name = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=50,
        help_text="""
    attention to

    **(required for shipment purchase)**
    """,
    )
    company_name = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=50,
        help_text="The company name if the party is a company",
    )
    country_code = serializers.ChoiceField(
        required=True,
        choices=COUNTRIES,
        help_text="The address country code",
    )
    email = serializers.CharField(
        required=False, allow_blank=True, allow_null=True, help_text="The party email"
    )
    phone_number = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=50,
        help_text="The party phone number.",
    )

    state_code = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=20,
        help_text="The address state code",
    )
    suburb = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=20,
        help_text="The address suburb if known",
    )
    residential = serializers.BooleanField(
        allow_null=True,
        required=False,
        default=False,
        help_text="Indicate if the address is residential or commercial (enterprise)",
    )

    address_line1 = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=100,
        help_text="""
        The address line with street number <br/>
        **(required for shipment purchase)**
        """,
    )
    address_line2 = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=100,
        help_text="The address line with suite number",
    )
    validate_location = serializers.BooleanField(
        required=False,
        allow_null=True,
        default=False,
        help_text="Indicate if the address should be validated",
    )


class Address(serializers.EntitySerializer, AddressData):
    object_type = serializers.CharField(default="address", help_text="Specifies the object type")
    validation = AddressValidation(
        required=False, allow_null=True, help_text="Specify address validation result"
    )


class CommodityData(serializers.Serializer):

    weight = serializers.FloatField(required=True, help_text="The commodity's weight")
    weight_unit = serializers.ChoiceField(
        required=True,
        choices=WEIGHT_UNIT,
        help_text="The commodity's weight unit",
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=250,
        help_text="A description of the commodity",
    )
    quantity = serializers.IntegerField(
        required=False,
        default=1,
        help_text="The commodity's quantity (number or item)",
    )
    sku = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=100,
        help_text="The commodity's sku number",
    )
    hs_code = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=100,
        help_text="The commodity's hs_code number",
    )
    value_amount = serializers.FloatField(
        required=False,
        allow_null=True,
        help_text="The monetary value of the commodity",
    )
    value_currency = serializers.ChoiceField(
        required=False,
        allow_null=True,
        choices=CURRENCIES,
        help_text="The currency of the commodity value amount",
    )
    origin_country = serializers.ChoiceField(
        required=False,
        allow_null=True,
        choices=COUNTRIES,
        help_text="The origin or manufacture country",
    )
    parent_id = serializers.CharField(
        required=False,
        allow_null=True,
        help_text="The id of the related order line item.",
    )
    metadata = serializers.PlainDictField(
        required=False,
        allow_null=True,
        help_text="""
        <details>
        <summary>Commodity user references metadata.</summary>

        ```
        {
            "part_number": "5218487281",
            "reference1": "# ref 1",
            "reference2": "# ref 2",
            "reference3": "# ref 3",
            "reference4": "# ref 4",
            ...
        }
        ```
        </details>
        """,
    )


class Commodity(serializers.EntitySerializer, CommodityData):
    object_type = serializers.CharField(default="commodity", help_text="Specifies the object type")


class ParcelData(validators.PresetSerializer):

    weight = serializers.FloatField(required=True, help_text="The parcel's weight")
    width = serializers.FloatField(required=False, allow_null=True, help_text="The parcel's width")
    height = serializers.FloatField(
        required=False, allow_null=True, help_text="The parcel's height"
    )
    length = serializers.FloatField(
        required=False, allow_null=True, help_text="The parcel's length"
    )
    packaging_type = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=50,
        help_text=f"""
        The parcel's packaging type.

        **Note that the packaging is optional when using a package preset**

        values: <br/>
        {' '.join([f'`{pkg}`' for pkg, _ in PACKAGING_UNIT])}

        For carrier specific packaging types, please consult the reference.
        """,
    )
    package_preset = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=50,
        help_text="""
    The parcel's package preset.

    For carrier specific package presets, please consult the reference.
    """,
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=250,
        help_text="The parcel's description",
    )
    content = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=100,
        help_text="The parcel's content description",
    )
    is_document = serializers.BooleanField(
        required=False,
        allow_null=True,
        default=False,
        help_text="Indicates if the parcel is composed of documents only",
    )
    weight_unit = serializers.ChoiceField(
        required=True, choices=WEIGHT_UNIT, help_text="The parcel's weight unit"
    )
    dimension_unit = serializers.ChoiceField(
        required=False,
        allow_blank=True,
        allow_null=True,
        choices=DIMENSION_UNIT,
        help_text="The parcel's dimension unit",
    )
    items = CommodityData(required=False, many=True, help_text="The parcel items.")
    reference_number = serializers.CharField(
        required=False,
        allow_null=True,
        max_length=100,
        help_text="The parcel reference number. (can be used as tracking number for custom carriers)",
    )
    freight_class = serializers.CharField(
        required=False,
        allow_null=True,
        max_length=6,
        help_text="The parcel's freight class for pallet and freight shipments.",
    )
    options = serializers.PlainDictField(
        required=False,
        default={},
        help_text="""
        <details>
        <summary>Parcel specific options.</summary>

        ```
        {
            "insurance": "100.00",
            "insured_by": "carrier",
        }
        ```

        Please check the docs for more details.
        </details>
        """,
    )


class Parcel(serializers.EntitySerializer, ParcelData):
    object_type = serializers.CharField(default="parcel", help_text="Specifies the object type")
    items = Commodity(required=False, many=True, help_text="The parcel items.")


class Payment(serializers.Serializer):

    paid_by = serializers.ChoiceField(
        required=False,
        choices=PAYMENT_TYPES,
        default=PAYMENT_TYPES[0][0],
        help_text="The payor type",
    )
    currency = serializers.ChoiceField(
        required=False,
        allow_blank=True,
        allow_null=True,
        choices=CURRENCIES,
        help_text="The payment amount currency",
    )
    account_number = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The payor account number",
    )


class Duty(serializers.Serializer):

    paid_by = serializers.ChoiceField(
        required=False,
        choices=PAYMENT_TYPES,
        allow_blank=True,
        allow_null=True,
        help_text="The duty payer",
    )
    currency = serializers.ChoiceField(
        required=False,
        choices=CURRENCIES,
        allow_blank=True,
        allow_null=True,
        help_text="The declared value currency",
    )
    declared_value = serializers.FloatField(
        required=False, allow_null=True, help_text="The package declared value"
    )
    account_number = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The duty payment account number",
    )
    bill_to = Address(
        required=False, allow_null=True, help_text="The duty billing address"
    )


@serializers.allow_model_id(
    [
        ("commodities", "karrio.server.manager.models.Commodity"),
    ]
)
class CustomsData(serializers.Serializer):

    commodities = CommodityData(
        many=True, allow_empty=False, help_text="The parcel content items"
    )
    duty = Duty(
        required=False,
        allow_null=True,
        help_text="""
    The payment details.<br/>
    Note that this is required for a Dutiable parcel shipped internationally.
    """,
    )
    content_type = serializers.ChoiceField(
        required=False, choices=CUSTOMS_CONTENT_TYPE, allow_blank=True, allow_null=True
    )
    content_description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    incoterm = serializers.ChoiceField(
        required=False,
        allow_null=True,
        choices=INCOTERMS,
        help_text="The customs 'term of trade' also known as 'incoterm'",
    )
    invoice = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        max_length=50,
        help_text="The invoice reference number",
    )
    invoice_date = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        validators=[validators.valid_date_format("invoice_date")],
        help_text="The invoice date",
    )
    commercial_invoice = serializers.BooleanField(
        required=False,
        allow_null=True,
        help_text="Indicates if the shipment is commercial",
    )
    certify = serializers.BooleanField(
        required=False,
        allow_null=True,
        help_text="Indicate that signer certified confirmed all",
    )
    signer = serializers.CharField(required=False, max_length=50, allow_blank=True, allow_null=True)
    options = serializers.PlainDictField(
        required=False,
        default={},
        help_text="""
    <details>
    <summary>Customs identification options.</summary>

    ```
    {
        "aes": "5218487281",
        "eel_pfc": "5218487281",
        "license_number": "5218487281",
        "certificate_number": "5218487281",
        "nip_number": "5218487281",
        "eori_number": "5218487281",
        "vat_registration_number": "5218487281",
    }
    ```

    Please check the docs for carrier specific options.
    </details>
    """,
    )


class Customs(serializers.EntitySerializer, CustomsData):
    object_type = serializers.CharField(
        default="customs_info", help_text="Specifies the object type"
    )
    commodities = Commodity(
        required=False, many=True, help_text="The parcel content items"
    )


class Charge(serializers.Serializer):

    name = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The charge description",
    )
    amount = serializers.FloatField(
        required=False, allow_null=True, help_text="The charge monetary value"
    )
    currency = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The charge amount currency",
    )


@serializers.allow_model_id(
    [
        ("shipper", "karrio.server.manager.models.Address"),
        ("recipient", "karrio.server.manager.models.Address"),
        ("parcels", "karrio.server.manager.models.Parcel"),
    ]
)
class RateRequest(validators.OptionDefaultSerializer):
    shipper = AddressData(
        required=True,
        help_text="""
    The address of the party

    Origin address (ship from) for the **shipper**<br/>
    Destination address (ship to) for the **recipient**
    """,
    )
    recipient = AddressData(
        required=True,
        help_text="""
    The address of the party

    Origin address (ship from) for the **shipper**<br/>
    Destination address (ship to) for the **recipient**
    """,
    )
    parcels = ParcelData(
        many=True,
        allow_empty=False,
        help_text="The shipment's parcels",
    )

    services = serializers.StringListField(
        required=False,
        allow_null=True,
        help_text="""
    The requested carrier service for the shipment.<br/>
    Please consult the reference for specific carriers services.

    Note that this is a list because on a Multi-carrier rate request you could specify a service per carrier.
    """,
    )
    options = serializers.PlainDictField(
        required=False,
        default={},
        help_text="""
    <details>
    <summary>The options available for the shipment.</summary>

    ```
    {
        "currency": "USD",
        "insurance": 100.00,
        "cash_on_delivery": 30.00,
        "shipment_date": "2020-01-01",
        "dangerous_good": true,
        "declared_value": 150.00,
        "email_notification": true,
        "email_notification_to": "shipper@mail.com",
        "signature_confirmation": true,
    }
    ```

    Please check the docs for carrier specific options.
    </details>
    """,
    )
    reference = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment reference",
    )
    carrier_ids = serializers.StringListField(
        required=False,
        allow_null=True,
        help_text="""
    The list of configured carriers you wish to get rates from.
    """,
    )


class TrackingRequest(serializers.Serializer):

    tracking_numbers = serializers.StringListField(
        required=True, help_text="a list of tracking numbers to fetch."
    )
    language_code = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        default="en",
        help_text="The tracking details language code",
    )
    level_of_details = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The level of event details.",
    )
    options = serializers.PlainDictField(
        required=False,
        default={},
        help_text="additional tracking options",
    )


@serializers.allow_model_id(
    [
        ("address", "karrio.server.manager.models.Address"),
        ("parcels", "karrio.server.manager.models.Parcel"),
    ]
)
class PickupRequest(serializers.Serializer):

    pickup_date = serializers.CharField(
        required=True,
        validators=[validators.valid_date_format("pickup_date")],
        help_text="""
    The expected pickup date

    Date Format: `YYYY-MM-DD`
    """,
    )
    address = AddressData(required=True, help_text="The pickup address")
    parcels = ParcelData(
        many=True,
        allow_empty=False,
        help_text="The shipment parcels to pickup.",
    )
    ready_time = serializers.CharField(
        required=True,
        validators=[validators.valid_time_format("ready_time")],
        help_text="""
    The ready time for pickup.

    Time Format: `HH:MM`
    """,
    )
    closing_time = serializers.CharField(
        required=True,
        validators=[validators.valid_time_format("closing_time")],
        help_text="""
    The closing or late time of the pickup

    Time Format: `HH:MM`
    """,
    )
    instruction = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="""
    The pickup instruction.

    eg: Handle with care.
    """,
    )
    package_location = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="""
    The package(s) location.

    eg: Behind the entrance door.
    """,
    )
    options = serializers.PlainDictField(
        required=False,
        allow_null=True,
        help_text="Advanced carrier specific pickup options",
    )


@serializers.allow_model_id(
    [
        ("address", "karrio.server.manager.models.Address"),
        ("parcels", "karrio.server.manager.models.Parcel"),
    ]
)
class PickupUpdateRequest(serializers.Serializer):
    pickup_date = serializers.CharField(
        required=True,
        help_text="""
    The expected pickup date

    Date Format: `YYYY-MM-DD`
    """,
    )
    address = Address(required=True, help_text="The pickup address")
    parcels = Parcel(
        many=True,
        allow_empty=False,
        help_text="The shipment parcels to pickup.",
    )
    confirmation_number = serializers.CharField(
        required=True, help_text="pickup identification number"
    )
    ready_time = serializers.CharField(
        required=True,
        validators=[(validators.valid_time_format("ready_time"))],
        help_text="""
    The ready time for pickup.

    Time Format: `HH:MM`
    """,
    )
    closing_time = serializers.CharField(
        required=True,
        validators=[validators.valid_time_format("closing_time")],
        help_text="""
    The closing or late time of the pickup

    Time Format: `HH:MM`
    """,
    )
    instruction = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="""
    The pickup instruction.

    eg: Handle with care.
    """,
    )
    package_location = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="""
    The package(s) location.

    eg: Behind the entrance door.
    """,
    )
    options = serializers.PlainDictField(
        required=False,
        allow_null=True,
        help_text="Advanced carrier specific pickup options",
    )


class PickupDetails(serializers.Serializer):
    id = serializers.CharField(required=False, help_text="A unique pickup identifier")
    object_type = serializers.CharField(default="pickup", help_text="Specifies the object type")
    carrier_name = serializers.CharField(required=True, help_text="The pickup carrier")
    carrier_id = serializers.CharField(
        required=True, help_text="The pickup carrier configured name"
    )
    confirmation_number = serializers.CharField(
        required=True, help_text="The pickup confirmation identifier"
    )
    pickup_date = serializers.CharField(
        required=False, allow_null=True, help_text="The pickup date"
    )
    pickup_charge = Charge(
        required=False, allow_null=True, help_text="The pickup cost details"
    )
    ready_time = serializers.CharField(
        required=False, allow_null=True, help_text="The pickup expected ready time"
    )
    closing_time = serializers.CharField(
        required=False,
        allow_null=True,
        help_text="The pickup expected closing or late time",
    )


class Pickup(PickupDetails, PickupRequest):
    address = Address(required=True, help_text="The pickup address")
    parcels = Parcel(
        many=True,
        allow_empty=False,
        help_text="The shipment parcels to pickup.",
    )
    metadata = serializers.PlainDictField(
        required=False, default={}, help_text="User metadata for the pickup"
    )
    test_mode = serializers.BooleanField(
        required=True,
        help_text="Specified whether it was created with a carrier in test mode",
    )


@serializers.allow_model_id(
    [
        ("address", "karrio.server.manager.models.Address"),
    ]
)
class PickupCancelRequest(serializers.Serializer):
    confirmation_number = serializers.CharField(
        required=True, help_text="The pickup confirmation identifier"
    )
    address = AddressData(required=False, help_text="The pickup address")
    pickup_date = serializers.CharField(
        required=False,
        allow_null=True,
        validators=[validators.valid_date_format("pickup_date")],
        help_text="""
    The pickup date

    Date Format: `YYYY-MM-DD`
    """,
    )
    reason = serializers.CharField(
        required=False, help_text="The reason of the pickup cancellation"
    )


class TrackingEvent(serializers.Serializer):

    date = serializers.CharField(required=False, help_text="The tracking event's date")
    description = serializers.CharField(
        required=False, help_text="The tracking event's description"
    )
    location = serializers.CharField(required=False, help_text="The tracking event's location")
    code = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The tracking event's code",
    )
    time = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The tracking event's time",
    )


class Rate(serializers.EntitySerializer):
    object_type = serializers.CharField(default="rate", help_text="Specifies the object type")
    carrier_name = serializers.CharField(required=True, help_text="The rate's carrier")
    carrier_id = serializers.CharField(
        required=True, help_text="The targeted carrier's name (unique identifier)"
    )
    currency = serializers.CharField(
        required=False, help_text="The rate monetary values currency code"
    )
    service = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The carrier's rate (quote) service",
    )
    total_charge = serializers.FloatField(
        default=0.0,
        help_text="""
    The rate's monetary amount of the total charge.<br/>
    This is the gross amount of the rate after adding the additional charges
    """,
    )
    transit_days = serializers.IntegerField(
        required=False, allow_null=True, help_text="The estimated delivery transit days"
    )
    extra_charges = Charge(
        many=True,
        allow_empty=True,
        default=[],
        help_text="list of the rate's additional charges",
    )
    meta = serializers.PlainDictField(
        required=False, allow_null=True, help_text="provider specific metadata"
    )
    test_mode = serializers.BooleanField(
        required=True,
        help_text="Specified whether it was created with a carrier in test mode",
    )


class TrackingDetails(serializers.Serializer):

    carrier_name = serializers.CharField(required=True, help_text="The tracking carrier")
    carrier_id = serializers.CharField(
        required=True, help_text="The tracking carrier configured identifier"
    )
    tracking_number = serializers.CharField(required=True, help_text="The shipment tracking number")
    events = TrackingEvent(
        many=True,
        required=False,
        allow_null=True,
        allow_empty=True,
        help_text="The tracking details events",
    )
    delivered = serializers.BooleanField(
        required=False, help_text="Specified whether the related shipment was delivered"
    )
    test_mode = serializers.BooleanField(
        required=True,
        help_text="Specified whether the object was created with a carrier in test mode",
    )
    status = serializers.ChoiceField(
        required=False,
        default=TRACKER_STATUS[0][0],
        choices=TRACKER_STATUS,
        help_text="The current tracking status",
    )
    estimated_delivery = serializers.CharField(
        required=False,
        help_text="The delivery estimated date",
    )
    meta = serializers.PlainDictField(
        required=False, allow_null=True, help_text="provider specific metadata"
    )


class TrackingStatus(serializers.EntitySerializer, TrackingDetails):
    object_type = serializers.CharField(default="tracker", help_text="Specifies the object type")
    metadata = serializers.PlainDictField(
        required=False, default={}, help_text="User metadata for the tracker"
    )
    messages = Message(
        required=False,
        many=True,
        default=[],
        help_text="The list of note or warning messages",
    )


@serializers.allow_model_id(
    [
        ("shipper", "karrio.server.manager.models.Address"),
        ("recipient", "karrio.server.manager.models.Address"),
        ("parcels", "karrio.server.manager.models.Parcel"),
        ("customs", "karrio.server.manager.models.Customs"),
    ]
)
class ShippingData(validators.OptionDefaultSerializer):
    shipper = AddressData(
        required=True,
        help_text="""
    The address of the party

    Origin address (ship from) for the **shipper**<br/>
    Destination address (ship to) for the **recipient**
    """,
    )
    recipient = AddressData(
        required=True,
        help_text="""
    The address of the party

    Origin address (ship from) for the **shipper**<br/>
    Destination address (ship to) for the **recipient**
    """,
    )
    parcels = ParcelData(
        many=True, allow_empty=False, help_text="The shipment's parcels"
    )
    options = serializers.PlainDictField(
        required=False,
        default={},
        help_text="""
    <details>
    <summary>The options available for the shipment.</summary>

    ```
    {
        "currency": "USD",
        "insurance": 100.00,
        "cash_on_delivery": 30.00,
        "shipment_date": "2020-01-01",
        "dangerous_good": true,
        "declared_value": 150.00,
        "email_notification": true,
        "email_notification_to": "shipper@mail.com",
        "signature_confirmation": true,
    }
    ```

    Please check the docs for carrier specific options.
    </details>
    """,
    )
    payment = Payment(required=False, default={}, help_text="The payment details")
    customs = CustomsData(
        required=False,
        allow_null=True,
        help_text="""
    The customs details.<br/>
    Note that this is required for the shipment of an international Dutiable parcel.
    """,
    )
    reference = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=100,
        help_text="The shipment reference",
    )
    label_type = serializers.ChoiceField(
        required=False,
        choices=LABEL_TYPES,
        default=units.LabelType.PDF.name,
        help_text="The shipment label file type.",
    )


class ShippingRequest(ShippingData):
    selected_rate_id = serializers.CharField(required=True, help_text="The shipment selected rate.")
    rates = Rate(many=True, help_text="The list for shipment rates fetched previously")


class ShipmentData(ShippingData):
    service = serializers.CharField(
        required=False,
        allow_blank=False,
        allow_null=False,
        help_text="**Specify a service to Buy a label in one call without rating.**",
    )
    services = serializers.StringListField(
        required=False,
        allow_null=True,
        default=[],
        help_text="""
    The requested carrier service for the shipment.

    Please consult the reference for specific carriers services.<br/>
    Note that this is a list because on a Multi-carrier rate request you could specify a service per carrier.
    """,
    )
    carrier_ids = serializers.StringListField(
        required=False,
        allow_null=True,
        default=[],
        help_text="""
    The list of configured carriers you wish to get rates from.

    *Note that the request will be sent to all carriers in nothing is specified*
    """,
    )
    metadata = serializers.PlainDictField(
        required=False, default={}, help_text="User metadata for the shipment"
    )


class Documents(serializers.Serializer):
    label = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment label in base64 string",
    )
    invoice = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment invoice in base64 string",
    )


class ShipmentDetails(serializers.Serializer):
    status = serializers.ChoiceField(
        required=False,
        default=ShipmentStatus.draft.value,
        choices=SHIPMENT_STATUS,
        help_text="The current Shipment status",
    )
    carrier_name = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment carrier",
    )
    carrier_id = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment carrier configured identifier",
    )
    tracking_number = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment tracking number",
    )
    shipment_identifier = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment carrier system identifier",
    )
    selected_rate = Rate(
        required=False, allow_null=True, help_text="The shipment selected rate"
    )
    docs = Documents(
        required=False,
        allow_null=True,
        help_text="The shipment documents",
    )
    meta = serializers.PlainDictField(
        required=False, allow_null=True, help_text="provider specific metadata"
    )

    service = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The selected service",
    )
    selected_rate_id = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment selected rate.",
    )
    tracking_url = serializers.URLField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment tracking url",
    )
    test_mode = serializers.BooleanField(
        required=True,
        help_text="Specified whether it was created with a carrier in test mode",
    )


class ShipmentContent(serializers.Serializer):
    object_type = serializers.CharField(default="shipment", help_text="Specifies the object type")
    tracking_url = serializers.URLField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment tracking url",
    )
    shipper = Address(
        required=True,
        help_text="""
    The address of the party

    Origin address (ship from) for the **shipper**<br/>
    Destination address (ship to) for the **recipient**
    """,
    )
    recipient = Address(
        required=True,
        help_text="""
    The address of the party

    Origin address (ship from) for the **shipper**<br/>
    Destination address (ship to) for the **recipient**
    """,
    )
    parcels = Parcel(many=True, allow_empty=False, help_text="The shipment's parcels")

    services = serializers.StringListField(
        required=False,
        allow_null=True,
        default=[],
        help_text="""
    The carriers services requested for the shipment.

    Please consult the reference for specific carriers services.<br/>
    Note that this is a list because on a Multi-carrier rate request you could specify a service per carrier.
    """,
    )
    options = serializers.PlainDictField(
        required=False,
        default={},
        help_text="""
    <details>
    <summary>The options available for the shipment.</summary>

    ```
    {
        "currency": "USD",
        "insurance": 100.00,
        "cash_on_delivery": 30.00,
        "shipment_date": "2020-01-01",
        "dangerous_good": true,
        "declared_value": 150.00,
        "email_notification": true,
        "email_notification_to": "shipper@mail.com",
        "signature_confirmation": true,
    }
    ```

    Please check the docs for carrier specific options.
    </details>
    """,
    )

    payment = Payment(required=False, default={}, help_text="The payment details")
    customs = Customs(
        required=False,
        allow_null=True,
        help_text="""
    The customs details.<br/>
    Note that this is required for the shipment of an international Dutiable parcel.
    """,
    )
    rates = Rate(
        many=True,
        required=False,
        default=[],
        help_text="The list for shipment rates fetched previously",
    )
    reference = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment reference",
    )
    label_type = serializers.ChoiceField(
        required=False,
        choices=LABEL_TYPES,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment label file type.",
    )
    carrier_ids = serializers.StringListField(
        required=False,
        allow_null=True,
        default=[],
        help_text="""
    The list of configured carriers you wish to get rates from.

    *Note that the request will be sent to all carriers in nothing is specified*
    """,
    )
    tracker_id = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The attached tracker id",
    )
    created_at = serializers.CharField(
        required=True,
        help_text="""
    The shipment creation datetime

    Date Format: `YYYY-MM-DD HH:MM:SS.mmmmmmz`
    """,
    )
    metadata = serializers.PlainDictField(
        required=False, default={}, help_text="User metadata for the shipment"
    )
    messages = Message(
        required=False,
        many=True,
        default=[],
        help_text="The list of note or warning messages",
    )


class Shipment(serializers.EntitySerializer, ShipmentContent, ShipmentDetails):
    docs = None
    label_url = serializers.URLField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment label URL",
    )
    invoice_url = serializers.URLField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment invoice URL",
    )


class ShipmentCancelRequest(serializers.Serializer):
    shipment_identifier = serializers.CharField(
        required=True, help_text="The shipment identifier returned during creation"
    )
    service = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The selected shipment service",
    )
    options = serializers.PlainDictField(
        required=False,
        default={},
        help_text="Advanced carrier specific cancellation options",
    )


class Operation(serializers.Serializer):
    operation = serializers.CharField(required=True, help_text="Operation performed")
    success = serializers.BooleanField(
        required=True, help_text="Specify whether the operation was successful"
    )


class OperationConfirmation(Operation):
    carrier_name = serializers.CharField(required=True, help_text="The operation carrier")
    carrier_id = serializers.CharField(
        required=True, help_text="The targeted carrier's name (unique identifier)"
    )


class OperationResponse(serializers.Serializer):
    messages = Message(
        required=False, many=True, help_text="The list of note or warning messages"
    )
    confirmation = OperationConfirmation(
        required=False, help_text="The operation details"
    )


class PickupResponse(serializers.Serializer):
    messages = Message(
        required=False, many=True, help_text="The list of note or warning messages"
    )
    pickup = Pickup(required=False, help_text="The scheduled pickup's summary")


class RateResponse(serializers.Serializer):
    messages = Message(
        required=False, many=True, help_text="The list of note or warning messages"
    )
    rates = Rate(many=True, help_text="The list of returned rates")


class TrackingResponse(serializers.Serializer):
    messages = Message(
        required=False, many=True, help_text="The list of note or warning messages"
    )
    tracking = TrackingStatus(
        required=False, help_text="The tracking details retrieved"
    )


class DocumentFileData(serializers.Serializer):
    doc_file = serializers.CharField(
        required=True,
        validators=[validators.valid_base64("doc_file")],
        help_text="A base64 file to upload",
    )
    doc_name = serializers.CharField(
        required=True,
        help_text="A file name",
    )
    doc_type = serializers.CharField(
        required=False,
        allow_blank=False,
        allow_null=True,
        max_length=50,
        default="other",
        help_text="Shipping document type",
    )


class DocumentUploadData(serializers.Serializer):
    shipment_id = serializers.CharField(required=True, help_text="The documents related shipment.")
    document_files = DocumentFileData(
        many=True,
        allow_empty=False,
        help_text="Shipping document files",
    )
    reference = serializers.CharField(
        required=False,
        allow_blank=False,
        allow_null=True,
        max_length=50,
        help_text="Shipping document file reference",
    )


class DocumentDetails(serializers.Serializer):
    document_id = serializers.CharField(
        required=False,
        help_text="The uploaded document id.",
    )
    file_name = serializers.CharField(
        required=False,
        help_text="The uploaded document file name.",
    )


class DocumentUploadRecord(serializers.EntitySerializer):
    carrier_name = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment carrier",
    )
    carrier_id = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment carrier configured identifier",
    )
    documents = DocumentDetails(
        many=True,
        default=[],
        required=False,
        help_text="the carrier shipping document ids",
    )
    meta = serializers.PlainDictField(
        required=False,
        allow_null=True,
        help_text="provider specific metadata",
    )
    reference = serializers.CharField(
        required=False,
        allow_blank=False,
        allow_null=True,
        max_length=50,
        help_text="Shipping document file reference",
    )
    messages = Message(
        required=False,
        many=True,
        default=[],
        help_text="The list of note or warning messages",
    )


class ErrorMessages(serializers.Serializer):
    messages = Message(
        many=True,
        required=False,
        help_text="The list of error messages",
    )


class ErrorResponse(serializers.Serializer):
    errors = APIError(many=True, required=False, help_text="The list of API errors")
