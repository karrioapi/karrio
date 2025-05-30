import rest_framework as drf

import karrio.core.units as units
import karrio.core.utils as utils
import karrio.server.serializers as serializers
import karrio.server.core.dataunits as dataunits
import karrio.server.core.validators as validators


class ShipmentStatus(utils.Enum):
    draft = "draft"
    purchased = "purchased"
    cancelled = "cancelled"
    shipped = "shipped"
    in_transit = "in_transit"
    delivered = "delivered"
    needs_attention = "needs_attention"
    out_for_delivery = "out_for_delivery"
    delivery_failed = "delivery_failed"


class TrackerStatus(utils.Enum):
    pending = "pending"
    unknown = "unknown"
    on_hold = "on_hold"
    cancelled = "cancelled"
    delivered = "delivered"
    in_transit = "in_transit"
    delivery_delayed = "delivery_delayed"
    out_for_delivery = "out_for_delivery"
    ready_for_pickup = "ready_for_pickup"
    delivery_failed = "delivery_failed"
    return_to_sender = "return_to_sender"


Serializer = serializers.Serializer
HTTP_STATUS = [getattr(drf.status, a) for a in dir(drf.status) if "HTTP" in a]
SHIPMENT_STATUS = [(c.name, c.name) for c in list(ShipmentStatus)]
TRACKER_STATUS = [(c.name, c.name) for c in list(TrackerStatus)]
INCOTERMS = [(c.name, c.name) for c in list(units.Incoterm)]
CARRIERS = [(k, k) for k in dataunits.CARRIER_NAMES]
COUNTRIES = [(c.name, c.name) for c in list(units.Country)]
CURRENCIES = [(c.name, c.name) for c in list(units.Currency)]
WEIGHT_UNIT = [(c.name, c.name) for c in list(units.WeightUnit)]
PAYMENT_TYPES = [(c.name, c.name) for c in list(units.PaymentType)]
DIMENSION_UNIT = [(c.name, c.name) for c in list(units.DimensionUnit)]
PACKAGING_UNIT = [(c.name, c.name) for c in list(units.PackagingUnit)]
CUSTOMS_CONTENT_TYPE = [(c.name, c.name) for c in list(units.CustomsContentType)]
UPLOAD_DOCUMENT_TYPE = [(c.name, c.name) for c in list(units.UploadDocumentType)]
LABEL_TYPES = [(c.name, c.name) for c in list(units.LabelType)]
LABEL_TEMPLATE_TYPES = [("SVG", "SVG"), ("ZPL", "ZPL")]


class CarrierDetails(serializers.Serializer):
    carrier_name = serializers.ChoiceField(
        choices=CARRIERS,
        help_text="Indicates a carrier (type)",
    )
    display_name = serializers.CharField(
        help_text="The carrier verbose name.",
    )
    integration_status = serializers.ChoiceField(
        choices=[
            ("in-development", "In Development"),
            ("beta", "Beta"),
            ("production-ready", "Production Ready"),
        ],
        help_text="The carrier integration status.",
    )
    capabilities = serializers.StringListField(
        default=[],
        help_text="""The carrier supported and enabled capabilities.""",
    )
    connection_fields = serializers.PlainDictField(
        default={},
        help_text="The carrier connection fields.",
    )
    config_fields = serializers.PlainDictField(
        default={},
        help_text="The carrier connection config.",
    )
    shipping_services = serializers.PlainDictField(
        default={},
        help_text="The carrier shipping services.",
    )
    shipping_options = serializers.PlainDictField(
        default={},
        help_text="The carrier shipping options.",
    )

class CarrierSettings(serializers.Serializer):
    id = serializers.CharField(required=True, help_text="A unique address identifier")
    object_type = serializers.CharField(
        default="carrier", help_text="Specifies the object type"
    )
    carrier_id = serializers.CharField(
        required=True, help_text="Indicates a specific carrier configuration name."
    )
    carrier_name = serializers.ChoiceField(
        choices=CARRIERS, required=True, help_text="Indicates a carrier (type)"
    )
    display_name = serializers.CharField(
        required=False, help_text="The carrier verbose name."
    )
    test_mode = serializers.BooleanField(
        required=True,
        help_text="The test flag indicates whether to use a carrier configured for test.",
    )
    active = serializers.BooleanField(
        required=True,
        help_text="The active flag indicates whether the carrier account is active or not.",
    )
    capabilities = serializers.StringListField(
        required=False,
        allow_null=True,
        help_text="""The carrier supported and enabled capabilities.""",
    )
    metadata = serializers.PlainDictField(
        required=False, default={}, help_text="The carrier user metadata."
    )
    config = serializers.PlainDictField(
        required=False, default={}, help_text="The carrier connection config."
    )


class APIError(serializers.Serializer):
    message = serializers.CharField(
        required=False, help_text="The error or warning message"
    )
    code = serializers.CharField(required=False, help_text="The message code")
    details = serializers.DictField(required=False, help_text="any additional details")


class Message(APIError):
    carrier_name = serializers.CharField(
        required=False, help_text="The targeted carrier"
    )
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
        help_text="""The address postal code
        **(required for shipment purchase)**
        """,
    )
    city = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=30,
        help_text="""The address city.
        **(required for shipment purchase)**
        """,
    )
    federal_tax_id = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=20,
        help_text="The party frederal tax id",
    )
    state_tax_id = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=20,
        help_text="The party state id",
    )
    person_name = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=50,
        help_text="""Attention to
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
        max_length=20,
        help_text="The party phone number.",
    )
    state_code = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=20,
        help_text="The address state code",
    )
    residential = serializers.BooleanField(
        allow_null=True,
        required=False,
        default=False,
        help_text="Indicate if the address is residential or commercial (enterprise)",
    )

    street_number = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=20,
        help_text="""The address street number""",
    )
    address_line1 = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=50,
        help_text="""The address line with street number <br/>
        **(required for shipment purchase)**
        """,
    )
    address_line2 = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=50,
        help_text="The address line with suite number",
    )
    validate_location = serializers.BooleanField(
        required=False,
        allow_null=True,
        default=False,
        help_text="Indicate if the address should be validated",
    )


class Address(serializers.EntitySerializer, AddressData):
    object_type = serializers.CharField(
        default="address", help_text="Specifies the object type"
    )
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
    title = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=35,
        help_text="A description of the commodity",
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=100,
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
        max_length=35,
        help_text="The commodity's sku number",
    )
    hs_code = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=35,
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
        help_text="""<details>
        <summary>Commodity user references metadata.</summary>

        {
            "part_number": "5218487281",
            "reference1": "# ref 1",
            "reference2": "# ref 2",
            "reference3": "# ref 3",
            ...
        }
        </details>
        """,
    )


class Commodity(serializers.EntitySerializer, CommodityData):
    object_type = serializers.CharField(
        default="commodity", help_text="Specifies the object type"
    )


@serializers.allow_model_id(
    [
        ("items", "karrio.server.manager.models.Commodity"),
    ]
)
class ParcelData(validators.PresetSerializer):
    weight = serializers.FloatField(required=True, help_text="The parcel's weight")
    width = serializers.FloatField(
        required=False, allow_null=True, help_text="The parcel's width"
    )
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
        help_text=f"""The parcel's packaging type.<br/>
        **Note that the packaging is optional when using a package preset.**<br/>
        values: <br/>
        {' '.join([f'`{pkg}`' for pkg, _ in PACKAGING_UNIT])}<br/>
        For carrier specific packaging types, please consult the reference.
        """,
    )
    package_preset = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=50,
        help_text="""The parcel's package preset.<br/>
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
        allow_blank=False,
        allow_null=True,
        choices=DIMENSION_UNIT,
        help_text="The parcel's dimension unit",
    )
    items = CommodityData(required=False, many=True, help_text="The parcel items.")
    reference_number = serializers.CharField(
        required=False,
        allow_null=True,
        max_length=100,
        help_text="""The parcel reference number.<br/>
        (can be used as tracking number for custom carriers)
        """,
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
        help_text="""<details>
        <summary>Parcel specific options.</summary>

        {
            "insurance": "100.00",
            "insured_by": "carrier",
        }
        </details>
        """,
    )


class Parcel(serializers.EntitySerializer, ParcelData):
    object_type = serializers.CharField(
        default="parcel", help_text="Specifies the object type"
    )
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


@serializers.allow_model_id(
    [
        ("commodities", "karrio.server.manager.models.Commodity"),
        ("duty_billing_address", "karrio.server.manager.models.Address"),
    ]
)
class CustomsData(serializers.Serializer):
    commodities = CommodityData(
        many=True, allow_empty=False, help_text="The parcel content items"
    )
    duty = Duty(
        required=False,
        allow_null=True,
        help_text="""The payment details.<br/>
        **Note that this is required for a Dutiable parcel shipped internationally.**
        """,
    )
    duty_billing_address = AddressData(
        required=False, allow_null=True, help_text="The duty payor address."
    )
    content_type = serializers.ChoiceField(
        required=False, choices=CUSTOMS_CONTENT_TYPE, allow_blank=True, allow_null=True
    )
    content_description = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
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
        help_text="""The invoice date.<br/>
        Date Format: `YYYY-MM-DD`
        """,
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
    signer = serializers.CharField(
        required=False, max_length=50, allow_blank=True, allow_null=True
    )
    options = serializers.PlainDictField(
        required=False,
        default={},
        help_text="""<details>
        <summary>Customs identification options.</summary>

        {
            "aes": "5218487281",
            "eel_pfc": "5218487281",
            "license_number": "5218487281",
            "certificate_number": "5218487281",
            "nip_number": "5218487281",
            "eori_number": "5218487281",
            "vat_registration_number": "5218487281",
        }
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
    duty_billing_address = Address(
        required=False, allow_null=True, help_text="The duty payor address."
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
        help_text="""The address of the party<br/>
        Origin address (ship from) for the **shipper**<br/>
        Destination address (ship to) for the **recipient**
        """,
    )
    recipient = AddressData(
        required=True,
        help_text="""The address of the party<br/>
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
        default=[],
        help_text="""The requested carrier service for the shipment.<br/>
        Please consult the reference for specific carriers services.<br/>
        Note that this is a list because on a Multi-carrier rate request you could specify a service per carrier.
        """,
    )
    options = serializers.PlainDictField(
        required=False,
        default={},
        help_text="""<details>
        <summary>The options available for the shipment.</summary>

        {
            "currency": "USD",
            "insurance": 100.00,
            "cash_on_delivery": 30.00,
            "dangerous_good": true,
            "declared_value": 150.00,
            "sms_notification": true,
            "email_notification": true,
            "email_notification_to": "shipper@mail.com",
            "hold_at_location": true,
            "paperless_trade": true,
            "preferred_service": "fedex_express_saver",
            "shipment_date": "2020-01-01",  # TODO: deprecate
            "shipping_date": "2020-01-01T00:00",
            "shipment_note": "This is a shipment note",
            "signature_confirmation": true,
            "saturday_delivery": true,
            "is_return": true,
            "shipper_instructions": "This is a shipper instruction",
            "recipient_instructions": "This is a recipient instruction",
            "doc_files": [
                {
                    "doc_type": "commercial_invoice",
                    "doc_file": "base64 encoded file",
                    "doc_name": "commercial_invoice.pdf",
                    "doc_format": "pdf",
                }
            ],
            "doc_references": [
                {
                    "doc_id": "123456789",
                    "doc_type": "commercial_invoice",
                }
            ],
        }
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
        default=[],
        help_text="The list of configured carriers you wish to get rates from.",
    )


class TrackingInfo(serializers.Serializer):
    carrier_tracking_link = serializers.CharField(
        required=False, allow_null=True, help_text="The carrier tracking link"
    )
    customer_name = serializers.CharField(
        required=False, allow_null=True, help_text="The customer name"
    )
    expected_delivery = serializers.CharField(
        required=False, allow_null=True, help_text="The expected delivery date"
    )
    note = serializers.CharField(
        required=False, allow_null=True, help_text="A tracking note"
    )
    order_date = serializers.CharField(
        required=False, allow_null=True, help_text="The package order date"
    )
    order_id = serializers.CharField(
        required=False, allow_null=True, help_text="The package order id or number"
    )
    package_weight = serializers.CharField(
        required=False, allow_null=True, help_text="The package weight"
    )
    package_weight_unit = serializers.CharField(
        required=False, allow_null=True, help_text="The package weight unit"
    )
    shipment_package_count = serializers.CharField(
        required=False, allow_null=True, help_text="The package count"
    )
    shipment_pickup_date = serializers.CharField(
        required=False, allow_null=True, help_text="The shipment pickup date"
    )
    shipment_delivery_date = serializers.CharField(
        required=False, allow_null=True, help_text="The shipment delivery date"
    )
    shipment_service = serializers.CharField(
        required=False, allow_null=True, help_text="The shipment service"
    )
    shipment_origin_country = serializers.CharField(
        required=False, allow_null=True, help_text="The shipment origin country"
    )
    shipment_origin_postal_code = serializers.CharField(
        required=False, allow_null=True, help_text="The shipment origin postal code"
    )
    shipment_destination_country = serializers.CharField(
        required=False, allow_null=True, help_text="The shipment destination country"
    )
    shipment_destination_postal_code = serializers.CharField(
        required=False,
        allow_null=True,
        help_text="The shipment destination postal code",
    )
    shipping_date = serializers.CharField(
        required=False, allow_null=True, help_text="The shipping date"
    )
    signed_by = serializers.CharField(
        required=False,
        allow_null=True,
        help_text="The person who signed for the package",
    )
    source = serializers.CharField(
        required=False, allow_null=True, help_text="The tracker source"
    )


class TrackingData(serializers.Serializer):
    tracking_number = serializers.CharField(
        required=True,
        help_text="The package tracking number",
    )
    carrier_name = serializers.ChoiceField(
        choices=dataunits.NON_HUBS_CARRIERS,
        required=True,
        help_text="The tracking carrier",
    )
    account_number = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipper account number",
    )
    reference = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment reference",
    )
    info = TrackingInfo(
        required=False,
        allow_null=True,
        help_text="The package and shipment tracking details",
    )
    metadata = serializers.PlainDictField(
        required=False, default={}, help_text="The carrier user metadata."
    )


class TrackingRequest(serializers.Serializer):
    tracking_numbers = serializers.StringListField(
        required=True, help_text="a list of tracking numbers to fetch."
    )
    account_number = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipper account number",
    )
    reference = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment reference",
    )
    options = serializers.PlainDictField(
        required=False,
        default={},
        help_text="additional tracking options",
    )
    info = TrackingInfo(
        required=False,
        allow_null=True,
        help_text="The package and shipment tracking details",
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
        help_text="""The expected pickup date.<br/>
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
        help_text="""The ready time for pickup.<br/>
        Time Format: `HH:MM`
        """,
    )
    closing_time = serializers.CharField(
        required=True,
        validators=[validators.valid_time_format("closing_time")],
        help_text="""The closing or late time of the pickup.<br/>
        Time Format: `HH:MM`
        """,
    )
    instruction = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=50,
        help_text="""The pickup instruction.<br/>
        eg: Handle with care.
        """,
    )
    package_location = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=50,
        help_text="""The package(s) location.<br/>
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
        help_text="""The expected pickup date.<br/>
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
        help_text="""The ready time for pickup.
        Time Format: `HH:MM`
        """,
    )
    closing_time = serializers.CharField(
        required=True,
        validators=[validators.valid_time_format("closing_time")],
        help_text="""The closing or late time of the pickup.<br/>
        Time Format: `HH:MM`
        """,
    )
    instruction = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=50,
        help_text="""The pickup instruction.<br/>
        eg: Handle with care.
        """,
    )
    package_location = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=50,
        help_text="""The package(s) location.<br/>
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
    object_type = serializers.CharField(
        default="pickup", help_text="Specifies the object type"
    )
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
    metadata = serializers.PlainDictField(
        required=False, default={}, help_text="User metadata for the pickup"
    )
    meta = serializers.PlainDictField(
        required=False, allow_null=True, help_text="provider specific metadata"
    )


class Pickup(PickupDetails, PickupRequest):
    address = Address(required=True, help_text="The pickup address")
    parcels = Parcel(
        many=True,
        allow_empty=False,
        help_text="The shipment parcels to pickup.",
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
        help_text="""The pickup date.<br/>
        Date Format: `YYYY-MM-DD`
        """,
    )
    reason = serializers.CharField(
        required=False, help_text="The reason of the pickup cancellation"
    )


class Images(serializers.Serializer):
    delivery_image = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="A delivery image in base64 string",
    )
    signature_image = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="A signature image in base64 string",
    )


class TrackingEvent(serializers.Serializer):
    date = serializers.CharField(
        required=False, help_text="The tracking event's date. Format: `YYYY-MM-DD`"
    )
    description = serializers.CharField(
        required=False, help_text="The tracking event's description"
    )
    location = serializers.CharField(
        required=False, help_text="The tracking event's location"
    )
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
        help_text="The tracking event's time. Format: `HH:MM AM/PM`",
    )
    latitude = serializers.FloatField(
        required=False,
        allow_null=True,
        help_text="""The tracking event's latitude.""",
    )
    longitude = serializers.FloatField(
        required=False,
        allow_null=True,
        help_text="""The tracking event's longitude.""",
    )


class TrackingDetails(serializers.Serializer):
    carrier_name = serializers.CharField(
        required=True, help_text="The tracking carrier"
    )
    carrier_id = serializers.CharField(
        required=True, help_text="The tracking carrier configured identifier"
    )
    tracking_number = serializers.CharField(
        required=True, help_text="The shipment tracking number"
    )
    info = TrackingInfo(
        required=False,
        allow_null=True,
        default={},
        help_text="The package and shipment tracking details",
    )
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
    images = Images(
        required=False,
        allow_null=True,
        help_text="The tracker documents",
    )


class TrackerDetails(serializers.EntitySerializer, TrackingDetails):
    object_type = serializers.CharField(
        default="tracker", help_text="Specifies the object type"
    )
    metadata = serializers.PlainDictField(
        required=False, default={}, help_text="User metadata for the tracker"
    )
    messages = Message(
        required=False,
        many=True,
        default=[],
        help_text="The list of note or warning messages",
    )


class TrackingStatus(TrackerDetails):
    images = None
    delivery_image_url = serializers.URLField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment invoice URL",
    )
    signature_image_url = serializers.URLField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment invoice URL",
    )


class Documents(serializers.Serializer):
    label = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="A shipping label in base64 string",
    )
    invoice = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="A shipping invoice in base64 string",
    )


class Rate(serializers.EntitySerializer):
    object_type = serializers.CharField(
        default="rate", help_text="Specifies the object type"
    )
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
        help_text="""The rate's monetary amount of the total charge.<br/>
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
    estimated_delivery = serializers.CharField(
        required=False,
        allow_null=True,
        help_text="The delivery estimated date",
    )
    meta = serializers.PlainDictField(
        required=False, allow_null=True, help_text="provider specific metadata"
    )
    test_mode = serializers.BooleanField(
        required=True,
        help_text="Specified whether it was created with a carrier in test mode",
    )


@serializers.allow_model_id(
    [
        ("shipper", "karrio.server.manager.models.Address"),
        ("recipient", "karrio.server.manager.models.Address"),
        ("parcels", "karrio.server.manager.models.Parcel"),
        ("customs", "karrio.server.manager.models.Customs"),
        ("return_address", "karrio.server.manager.models.Address"),
        ("billing_address", "karrio.server.manager.models.Address"),
    ]
)
class ShippingData(validators.OptionDefaultSerializer):
    recipient = AddressData(
        required=True,
        help_text="""The address of the party.<br/>
        Origin address (ship from) for the **shipper**<br/>
        Destination address (ship to) for the **recipient**
        """,
    )
    shipper = AddressData(
        required=True,
        help_text="""The address of the party.<br/>
        Origin address (ship from) for the **shipper**<br/>
        Destination address (ship to) for the **recipient**
        """,
    )
    return_address = AddressData(
        required=False,
        allow_null=True,
        help_text="The return address for this shipment. Defaults to the shipper address.",
    )
    billing_address = AddressData(
        required=False,
        allow_null=True,
        help_text="The payor address.",
    )
    parcels = ParcelData(
        many=True,
        allow_empty=False,
        help_text="The shipment's parcels",
    )
    options = serializers.PlainDictField(
        required=False,
        default={},
        help_text="""<details>
        <summary>The options available for the shipment.</summary>

        {
            "currency": "USD",
            "insurance": 100.00,
            "cash_on_delivery": 30.00,
            "dangerous_good": true,
            "declared_value": 150.00,
            "sms_notification": true,
            "email_notification": true,
            "email_notification_to": "shipper@mail.com",
            "hold_at_location": true,
            "paperless_trade": true,
            "preferred_service": "fedex_express_saver",
            "shipment_date": "2020-01-01",  # TODO: deprecate
            "shipping_date": "2020-01-01T00:00",
            "shipment_note": "This is a shipment note",
            "signature_confirmation": true,
            "saturday_delivery": true,
            "is_return": true,
            "shipper_instructions": "This is a shipper instruction",
            "recipient_instructions": "This is a recipient instruction",
            "doc_files": [
                {
                    "doc_type": "commercial_invoice",
                    "doc_file": "base64 encoded file",
                    "doc_name": "commercial_invoice.pdf",
                    "doc_format": "pdf",
                }
            ],
            "doc_references": [
                {
                    "doc_id": "123456789",
                    "doc_type": "commercial_invoice",
                }
            ],
        }
        </details>
        """,
    )
    payment = Payment(
        required=False,
        default={},
        help_text="The payment details",
    )
    customs = CustomsData(
        required=False,
        allow_null=True,
        help_text="""The customs details.<br/>
        **Note that this is required for the shipment of an international Dutiable parcel.**
        """,
    )
    reference = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=35,
        help_text="The shipment reference",
    )
    label_type = serializers.ChoiceField(
        required=False,
        choices=LABEL_TYPES,
        default=units.LabelType.PDF.name,
        help_text="The shipment label file type.",
    )


class ShippingRequest(ShippingData):
    selected_rate_id = serializers.CharField(
        required=True, help_text="The shipment selected rate."
    )
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
        help_text="""The requested carrier service for the shipment.<br/>
        Please consult the reference for specific carriers services.<br/>
        **Note that this is a list because on a Multi-carrier rate request
        you could specify a service per carrier.**
        """,
    )
    carrier_ids = serializers.StringListField(
        required=False,
        allow_null=True,
        default=[],
        help_text="""The list of configured carriers you wish to get rates from.<br/>
        **Note that the request will be sent to all carriers in nothing is specified**
        """,
    )
    metadata = serializers.PlainDictField(
        required=False,
        default={},
        help_text="User metadata for the shipment",
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
    object_type = serializers.CharField(
        default="shipment", help_text="Specifies the object type"
    )
    tracking_url = serializers.URLField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment tracking url",
    )
    shipper = Address(
        required=True,
        help_text="""The address of the party.<br/>
        Origin address (ship from) for the **shipper**<br/>
        Destination address (ship to) for the **recipient**
        """,
    )
    recipient = Address(
        required=True,
        help_text="""The address of the party.<br/>
        Origin address (ship from) for the **shipper**<br/>
        Destination address (ship to) for the **recipient**
        """,
    )
    return_address = AddressData(
        required=False,
        allow_null=True,
        help_text="The return address for this shipment. Defaults to the shipper address.",
    )
    billing_address = AddressData(
        required=False,
        allow_null=True,
        help_text="The payor address.",
    )
    parcels = Parcel(
        many=True,
        allow_empty=False,
        help_text="The shipment's parcels",
    )
    services = serializers.StringListField(
        required=False,
        allow_null=True,
        default=[],
        help_text="""The carriers services requested for the shipment.<br/>
        Please consult the reference for specific carriers services.<br/>
        **Note that this is a list because on a Multi-carrier rate request you could specify a service per carrier.**
        """,
    )
    options = serializers.PlainDictField(
        required=False,
        default={},
        help_text="""<details>
        <summary>The options available for the shipment.</summary>

        {
            "currency": "USD",
            "insurance": 100.00,
            "cash_on_delivery": 30.00,
            "dangerous_good": true,
            "declared_value": 150.00,
            "sms_notification": true,
            "email_notification": true,
            "email_notification_to": "shipper@mail.com",
            "hold_at_location": true,
            "paperless_trade": true,
            "preferred_service": "fedex_express_saver",
            "shipment_date": "2020-01-01",  # TODO: deprecate
            "shipping_date": "2020-01-01T00:00",
            "shipment_note": "This is a shipment note",
            "signature_confirmation": true,
            "saturday_delivery": true,
            "is_return": true,
            "shipper_instructions": "This is a shipper instruction",
            "recipient_instructions": "This is a recipient instruction",
            "doc_files": [
                {
                    "doc_type": "commercial_invoice",
                    "doc_file": "base64 encoded file",
                    "doc_name": "commercial_invoice.pdf",
                    "doc_format": "pdf",
                }
            ],
            "doc_references": [
                {
                    "doc_id": "123456789",
                    "doc_type": "commercial_invoice",
                }
            ],
        }
        </details>
        """,
    )
    payment = Payment(
        required=False,
        default={},
        help_text="The payment details",
    )
    customs = Customs(
        required=False,
        allow_null=True,
        help_text="""The customs details.<br/>
        **Note that this is required for the shipment of an international Dutiable parcel.**
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
        help_text="""The list of configured carriers you wish to get rates from.<br/>
        **Note that the request will be sent to all carriers in nothing is specified**
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
        help_text="""The shipment creation datetime.<br/>
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
        required=True,
        help_text="The shipment identifier returned during creation.",
    )
    service = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The selected shipment service",
    )
    carrier_id = serializers.CharField(
        required=False,
        help_text="The shipment carrier_id for specific connection selection.",
    )
    options = serializers.PlainDictField(
        required=False,
        default={},
        help_text="Advanced carrier specific cancellation options.",
    )


@serializers.allow_model_id(
    [
        ("address", "karrio.server.manager.models.Address"),
    ]
)
class ManifestRequestData(serializers.Serializer):
    carrier_name = serializers.CharField(
        required=True, help_text="The manifest's carrier"
    )
    address = AddressData(
        required=True,
        help_text="The address of the warehouse or location where the shipments originate.",
    )
    options = serializers.PlainDictField(
        required=False,
        default={},
        help_text="""<details>
        <summary>The options available for the manifest.</summary>

        {
            "shipments": [
                {
                    "tracking_number": "123456789",
                    ...
                    "meta": {...}
                }
            ]
        }
        </details>
        """,
    )
    reference = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The manifest reference",
    )


class ManifestRequest(ManifestRequestData):
    shipment_identifiers = serializers.StringListField(
        required=True,
        help_text="""The list of shipment identifiers you want to add to your manifest.<br/>
        shipment_identifier is often a tracking_number or shipment_id returned when you purchase a label.
        """,
    )


class ManifestData(ManifestRequestData):
    shipment_ids = serializers.StringListField(
        required=True,
        help_text="""The list of existing shipment object ids with label purchased.""",
    )


class ManifestDocument(serializers.Serializer):
    manifest = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="A manifest file in base64 string",
    )


class ManifestDetails(serializers.Serializer):
    id = serializers.CharField(required=False, help_text="A unique manifest identifier")
    object_type = serializers.CharField(
        default="manifest", help_text="Specifies the object type"
    )
    carrier_name = serializers.CharField(
        required=True, help_text="The manifest carrier"
    )
    carrier_id = serializers.CharField(
        required=True, help_text="The manifest carrier configured name"
    )
    doc = ManifestDocument(
        required=False,
        allow_null=True,
        help_text="The manifest documents",
    )
    meta = serializers.PlainDictField(
        required=False, allow_null=True, help_text="provider specific metadata"
    )
    test_mode = serializers.BooleanField(
        required=True,
        help_text="Specified whether it was created with a carrier in test mode",
    )


class Manifest(ManifestDetails, ManifestRequest):
    doc = None
    metadata = serializers.PlainDictField(
        required=False, default={}, help_text="User metadata for the pickup"
    )
    manifest_url = serializers.URLField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The Manifest file URL",
    )
    messages = Message(
        required=False,
        many=True,
        default=[],
        help_text="The list of note or warning messages",
    )


class ManifestResponse(serializers.Serializer):
    messages = Message(
        required=False, many=True, help_text="The list of note or warning messages"
    )
    manifest = ManifestDetails(required=False, help_text="The manifest details")


class Operation(serializers.Serializer):
    operation = serializers.CharField(required=True, help_text="Operation performed")
    success = serializers.BooleanField(
        required=True, help_text="Specify whether the operation was successful"
    )


class OperationConfirmation(Operation):
    carrier_name = serializers.CharField(
        required=True, help_text="The operation carrier"
    )
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
    tracking = TrackerDetails(
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
        help_text="The file name",
    )
    doc_format = serializers.CharField(
        required=False,
        allow_blank=False,
        allow_null=True,
        help_text="The file format",
    )
    doc_type = serializers.CharField(
        required=False,
        allow_blank=False,
        allow_null=True,
        max_length=50,
        default="other",
        help_text=f"""
        Shipment document type

        values: <br/>
        {' '.join([f'`{pkg}`' for pkg, _ in UPLOAD_DOCUMENT_TYPE])}

        For carrier specific packaging types, please consult the reference.
        """,
    )


class DocumentUploadData(serializers.Serializer):
    shipment_id = serializers.CharField(
        required=True, help_text="The documents related shipment."
    )
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
    doc_id = serializers.CharField(
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
