import csv
import attr
import typing
import pathlib
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models

import karrio.schemas.dhl_parcel_de.shipping_request as ship_req


# System config schema for runtime settings (e.g., API credentials)
# Format: Dict[str, Tuple[default_value, description, type]]
# Note: The actual env values are read by the server (constance.py) using decouple
SYSTEM_CONFIG = {
    "DHL_PARCEL_DE_USERNAME": (
        "",
        "DHL Parcel DE API username for production",
        str,
    ),
    "DHL_PARCEL_DE_PASSWORD": (
        "",
        "DHL Parcel DE API password for production",
        str,
    ),
    "DHL_PARCEL_DE_CLIENT_ID": (
        "",
        "DHL Parcel DE OAuth client ID for production",
        str,
    ),
    "DHL_PARCEL_DE_CLIENT_SECRET": (
        "",
        "DHL Parcel DE OAuth client secret for production",
        str,
    ),
    "DHL_PARCEL_DE_SANDBOX_USERNAME": (
        "user-valid",
        "DHL Parcel DE API username for sandbox/test mode",
        str,
    ),
    "DHL_PARCEL_DE_SANDBOX_PASSWORD": (
        "SandboxPasswort2023!",
        "DHL Parcel DE API password for sandbox/test mode",
        str,
    ),
    "DHL_PARCEL_DE_SANDBOX_CLIENT_ID": (
        "",
        "DHL Parcel DE OAuth client ID for sandbox/test mode",
        str,
    ),
    "DHL_PARCEL_DE_SANDBOX_CLIENT_SECRET": (
        "",
        "DHL Parcel DE OAuth client secret for sandbox/test mode",
        str,
    ),
}


class ShippingService(lib.Enum):
    """Carrier specific services"""

    dhl_parcel_de_paket = "V01PAK"
    dhl_parcel_de_kleinpaket = "V62KP"
    dhl_parcel_de_europaket = "V54EPAK"
    dhl_parcel_de_paket_international = "V53WPAK"
    dhl_parcel_de_warenpost_international = "V66WPI"


@attr.s(auto_attribs=True)
class ServiceBillingNumberType:
    """Typed object for service-specific billing number configuration."""

    service: ShippingService  # Required: shipping service enum
    billing_number: str  # Required: billing number for this service

    name: typing.Optional[str] = None  # Optional: friendly name for this entry


# Default test/sandbox billing numbers from DHL documentation
# https://developer.dhl.com/api-reference/parcel-de-shipping-post-parcel-germany-v2
DEFAULT_TEST_BILLING_NUMBERS: typing.List[ServiceBillingNumberType] = [
    # V01PAK - DHL Paket (incl. services)
    ServiceBillingNumberType(
        service="dhl_parcel_de_paket", billing_number="33333333330102"
    ),
    # V53WPAK - DHL Paket International
    ServiceBillingNumberType(
        service="dhl_parcel_de_paket_international", billing_number="33333333335301"
    ),
    # V54EPAK - DHL Europaket
    ServiceBillingNumberType(
        service="dhl_parcel_de_europaket", billing_number="33333333335401"
    ),
    # V62KP - DHL Kleinpaket
    ServiceBillingNumberType(
        service="dhl_parcel_de_kleinpaket", billing_number="33333333336201"
    ),
    # V66WPI - Warenpost International
    ServiceBillingNumberType(
        service="dhl_parcel_de_warenpost_international", billing_number="33333333336601"
    ),
]

# Default test billing number (V01PAK with services)
DEFAULT_TEST_BILLING_NUMBER = "33333333330102"


class LabelType(lib.Enum):
    """Carrier specific label type"""

    PDF_A4 = ("PDF", "A4")
    ZPL2_A4 = ("ZPL2", "A4")
    PDF_910_300_700 = ("PDF", "910-300-700")
    ZPL2_910_300_700 = ("ZPL2", "910-300-700")
    PDF_910_300_700_oz = ("PDF", "910-300-700-oz")
    ZPL2_910_300_700_oz = ("ZPL2", "910-300-700-oz")
    PDF_910_300_710 = ("PDF", "910-300-710")
    ZPL2_910_300_710 = ("ZPL2", "910-300-710")
    PDF_910_300_600 = ("PDF", "910-300-600")
    ZPL2_910_300_600 = ("ZPL2", "910-300-600")
    PDF_910_300_610 = ("PDF", "910-300-610")
    ZPL2_910_300_610 = ("ZPL2", "910-300-610")
    PDF_910_300_400 = ("PDF", "910-300-400")
    ZPL2_910_300_400 = ("ZPL2", "910-300-400")
    PDF_910_300_410 = ("PDF", "910-300-410")
    ZPL2_910_300_410 = ("ZPL2", "910-300-410")
    PDF_910_300_300 = ("PDF", "910-300-300")
    ZPL2_910_300_300 = ("ZPL2", "910-300-300")
    PDF_910_300_300_oz = ("PDF", "910-300-300-oz")
    ZPL2_910_300_300_oz = ("ZPL2", "910-300-300-oz")

    """ Unified Label type mapping """
    PDF = PDF_A4
    ZPL = ZPL2_A4
    PNG = PDF_A4


class ConnectionConfig(lib.Enum):
    label_type = lib.OptionEnum(
        "label_type",
        lib.units.create_enum("LabelType", [_.name for _ in LabelType]),  # type: ignore
    )
    language = lib.OptionEnum(
        "language",
        lib.units.create_enum("Language", ["de", "en"]),
    )
    default_billing_number = lib.OptionEnum("default_billing_number")
    service_billing_numbers = lib.OptionEnum(
        "service_billing_numbers", typing.List[ServiceBillingNumberType]
    )
    profile = lib.OptionEnum("profile")
    cost_center = lib.OptionEnum("cost_center")
    creation_software = lib.OptionEnum("creation_software")
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type"""

    PACKAGE = "PACKAGE"

    """ Unified Packaging type mapping """
    envelope = PACKAGE
    pak = PACKAGE
    tube = PACKAGE
    pallet = PACKAGE
    small_box = PACKAGE
    medium_box = PACKAGE
    your_packaging = PACKAGE


class CustomsContentType(lib.StrEnum):
    other = "OTHER"
    present = "PRESENT"
    document = "DOCUMENT"
    return_of_goods = "RETURN_OF_GOODS"
    commercial_goods = "COMMERCIAL_GOODS"
    commercial_sample = "COMMERCIAL_SAMPLE"

    """ Unified Content type mapping """
    gift = present
    documents = document
    sample = commercial_sample
    merchandise = commercial_goods
    return_merchandise = return_of_goods


class Incoterm(lib.StrEnum):
    """Carrier specific incoterm"""

    DDU = "DDU"
    DAP = "DAP"
    DDP = "DDP"
    DDX = "DDX"
    DXV = "DXV"


class ShippingDocumentCategory(lib.StrEnum):
    """Carrier specific document category types.

    Maps DHL Germany document types to standard ShippingDocumentCategory.
    Values match the exact syntax used by DHL Germany API.
    """

    shipping_label = "shippingLabel"
    return_label = "returnLabel"
    export_document = "exportDocument"
    receipt = "receipt"
    cod_document = "codLabel"
    enclosed_return_label = "enclosedReturnLabel"
    harmonized_label = "harmonizedLabel"
    international_shipping_label = "internationalShippingLabel"
    warenpost_national = "warenpostNational"
    return_label_international = "returnLabelInternational"
    warenpost_international = "warenpostInternational"
    error_label = "errorLabel"
    qr_code = "qrCode"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    # fmt: off
    dhl_parcel_de_preferred_neighbour = lib.OptionEnum(
        "preferredNeighbour",
        meta=dict(compatible_services=["V01PAK"])
    )
    dhl_parcel_de_preferred_location = lib.OptionEnum(
        "preferredLocation",
        meta=dict(compatible_services=["V01PAK"])
    )
    dhl_parcel_de_named_person_only = lib.OptionEnum(
        "namedPersonOnly", bool,
        meta=dict(compatible_services=["V01PAK"])
    )
    dhl_parcel_de_signed_for_by_recipient = lib.OptionEnum(
        "signedForByRecipient", bool,
        meta=dict(category="SIGNATURE", compatible_services=["V01PAK"])
    )
    dhl_parcel_de_preferred_day = lib.OptionEnum(
        "preferredDay",
        meta=dict(category="DELIVERY_OPTIONS", compatible_services=["V01PAK"])
    )
    dhl_parcel_de_no_neighbour_delivery = lib.OptionEnum(
        "noNeighbourDelivery", bool,
        meta=dict(category="DELIVERY_OPTIONS", compatible_services=["V01PAK"])
    )
    dhl_parcel_de_additional_insurance = lib.OptionEnum(
        "additionalInsurance", float,
        meta=dict(category="INSURANCE", compatible_services=["V01PAK", "V53WPAK", "V54EPAK", "V62KP"])
    )
    dhl_parcel_de_bulky_goods = lib.OptionEnum(
        "bulkyGoods", bool,
        meta=dict(compatible_services=["V01PAK", "V62KP"])
    )
    dhl_parcel_de_cash_on_delivery = lib.OptionEnum(
        "cashOnDelivery", float,
        meta=dict(category="COD", compatible_services=["V01PAK", "V62KP"])
    )
    dhl_parcel_de_individual_sender_requirement = lib.OptionEnum("individualSenderRequirement")
    dhl_parcel_de_premium = lib.OptionEnum(
        "premium", bool,
        meta=dict(compatible_services=["V53WPAK", "V66WPI"])
    )
    dhl_parcel_de_closest_drop_point = lib.OptionEnum(
        "closestDropPoint", bool,
        meta=dict(category="PUDO", compatible_services=["V01PAK", "V53WPAK", "V62KP"])
    )
    dhl_parcel_de_parcel_outlet_routing = lib.OptionEnum(
        "parcelOutletRouting",
        meta=dict(compatible_services=["V01PAK", "V53WPAK", "V62KP"])
    )
    dhl_parcel_de_postal_delivery_duty_paid = lib.OptionEnum(
        "postalDeliveryDutyPaid", bool,
        meta=dict(compatible_services=["V53WPAK"])
    )
    dhl_parcel_de_postal_charges = lib.OptionEnum("postalCharges", float)
    dhl_parcel_de_post_number = lib.OptionEnum("postNumber")
    dhl_parcel_de_retail_id = lib.OptionEnum("retailID")
    dhl_parcel_de_po_box_id = lib.OptionEnum("poBoxID")
    dhl_parcel_de_shipper_customs_ref = lib.OptionEnum("shipperCustomsRef")
    dhl_parcel_de_consignee_customs_ref = lib.OptionEnum("consigneeCustomsRef")
    dhl_parcel_de_permit_no = lib.OptionEnum("permitNo")
    dhl_parcel_de_attestation_no = lib.OptionEnum("attestationNo")
    dhl_parcel_de_has_electronic_export_notification = lib.OptionEnum("hasElectronicExportNotification")
    dhl_parcel_de_MRN = lib.OptionEnum("MRN")
    dhl_parcel_de_locker_id = lib.OptionEnum(
        "lockerID", lib.to_int,
        meta=dict(category="LOCKER", compatible_services=["V01PAK", "V62KP"])
    )

    dhl_parcel_de_ident_check = lib.OptionEnum(
        "identCheck", ship_req.IdentCheckType,
        meta=dict(compatible_services=["V01PAK"])
    )
    dhl_parcel_de_dhl_retoure = lib.OptionEnum(
        "dhlRetoure", ship_req.DhlRetoureType,
        meta=dict(category="RETURN", compatible_services=["V01PAK", "V62KP"])
    )
    dhl_parcel_de_visual_check_of_age = lib.OptionEnum(
        "visualCheckOfAge",
        lib.units.create_enum("VisualCheckOfAge", ["A16", "A18"]),  # type: ignore
        meta=dict(compatible_services=["V01PAK"])
    )
    dhl_parcel_de_endorsement = lib.OptionEnum(
        "endorsement",
        lib.units.create_enum("endorsement", ["RETURN", "SIGNATURE"]),  # type: ignore
        default="RETURN",
        meta=dict(compatible_services=["V01PAK", "V53WPAK", "V62KP", "V66WPI"])
    )

    """ Unified Option type mapping """
    signature_confirmation = dhl_parcel_de_signed_for_by_recipient
    hold_at_location = dhl_parcel_de_closest_drop_point
    cash_on_delivery = dhl_parcel_de_cash_on_delivery
    shipping_charges = dhl_parcel_de_postal_charges
    insurance = dhl_parcel_de_additional_insurance
    locker_id = dhl_parcel_de_locker_id
    # fmt: on


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """
    Apply default values to the given options.
    """

    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption or key in units.ShippingOption  # type: ignore

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class CustomsOption(lib.Enum):
    mrn = lib.OptionEnum("MRN")
    permit_number = lib.OptionEnum("permitNo")
    attestation_number = lib.OptionEnum("attestationNo")
    shipper_customs_ref = lib.OptionEnum("shipperCustomsRef")
    consignee_customs_ref = lib.OptionEnum("consigneeCustomsRef")
    electronic_export_notification = lib.OptionEnum("electronicExportNotification")


class TrackingStatus(lib.Enum):
    """Maps DHL Parcel DE tracking codes to normalized status.

    ICE (International Coded Event) codes from DHL Parcel DE Tracking API:
    - SHRCU: Shipment received at collection unit
    - LDTMV: Loaded to/moving on transportation
    - PCKDU: Picked up
    - ULFMV: Unloaded from transportation
    - SRTED: Sorted
    - DLVRD: Delivered
    - ARRVD: Arrived
    - HLDCC: Held at customs

    RIC (Reason Instruction Code) codes:
    - PCKST: Packstation
    - MVMTV: Movement
    - PUBCR: Public carrier
    - UNLDD: Unloaded
    - NRQRD: No reason required
    - OTHER: Other

    Standard event codes:
    - ES: Einlieferung / Posting
    - AA: Processing at origin parcel center
    - AE: Pick-up successful
    - EE: Destination parcel center
    - PO: Loaded onto delivery vehicle
    - ZU: Delivery successful
    """

    delivered = ["delivered", "dlvrd", "zu"]
    in_transit = [
        "transit",
        "shrcu",
        "ldtmv",
        "pckdu",
        "ulfmv",
        "srted",
        "arrvd",
        "hldcc",
        "es",
        "aa",
        "ae",
        "ee",
        "po",
    ]
    delivery_failed = ["failure", "ntdel", "rtrnd", "adurs"]
    delivery_delayed = ["unknown", "delay"]
    out_for_delivery = ["po", "in delivery"]


class TrackingIncidentReason(lib.Enum):
    """Maps DHL Germany exception codes to normalized TrackingIncidentReason."""

    # Carrier-caused issues
    carrier_damaged_parcel = ["damaged", "package_damaged", "parcel_damaged"]
    carrier_sorting_error = ["misrouted", "sorting_error", "wrong_route"]
    carrier_address_not_found = [
        "address_not_found",
        "invalid_address",
        "unknown_address",
    ]
    carrier_parcel_lost = ["lost", "missing", "not_found"]
    carrier_not_enough_time = ["time_constraint", "insufficient_time"]
    carrier_vehicle_issue = ["vehicle_issue", "transport_problem", "mechanical_issue"]

    # Consignee-caused issues
    consignee_refused = ["refused", "delivery_refused", "recipient_refused"]
    consignee_business_closed = ["business_closed", "closed", "shop_closed"]
    consignee_not_available = [
        "not_available",
        "recipient_not_available",
        "unavailable",
    ]
    consignee_not_home = ["not_home", "nobody_home", "recipient_absent"]
    consignee_incorrect_address = ["incorrect_address", "wrong_address", "bad_address"]
    consignee_access_restricted = ["access_restricted", "no_access", "restricted"]

    # Customs-related issues
    customs_delay = [
        "customs_delay",
        "customs_hold",
        "customs_processing",
        "clearance_delay",
    ]
    customs_documentation = [
        "customs_documents",
        "missing_documents",
        "documentation_required",
    ]
    customs_duties_unpaid = ["duties_unpaid", "customs_fees", "payment_required"]

    # Weather/Force majeure
    weather_delay = ["weather_delay", "weather", "severe_weather", "weather_conditions"]
    natural_disaster = ["natural_disaster", "emergency", "catastrophe"]

    # Delivery exceptions
    delivery_exception_hold = ["hold", "held", "on_hold", "depot_hold"]
    delivery_exception_undeliverable = [
        "undeliverable",
        "cannot_deliver",
        "delivery_impossible",
    ]

    # Other issues
    unknown = []


def load_services_from_csv() -> list:
    """
    Load service definitions from CSV file.
    CSV format: service_code,service_name,zone_label,country_codes,min_weight,max_weight,max_length,max_width,max_height,rate,currency,transit_days,domicile,international
    """
    csv_path = pathlib.Path(__file__).resolve().parent / "services.csv"

    if not csv_path.exists():
        # Fallback to simple default if CSV doesn't exist
        return [
            models.ServiceLevel(
                service_name="DHL Paket",
                service_code="dhl_parcel_de_paket",
                currency="EUR",
                domicile=True,
                zones=[models.ServiceZone(rate=0.0)],
            )
        ]

    # Group zones by service
    services_dict: dict[str, dict] = {}

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            service_code = row["service_code"]
            service_name = row["service_name"]

            # Map carrier service code to karrio service code
            karrio_service_code = ShippingService.map(service_code).name_or_key

            # Initialize service if not exists
            if karrio_service_code not in services_dict:
                services_dict[karrio_service_code] = {
                    "service_name": service_name,
                    "service_code": karrio_service_code,
                    "currency": row.get("currency", "EUR"),
                    "min_weight": (
                        float(row["min_weight"]) if row.get("min_weight") else None
                    ),
                    "max_weight": (
                        float(row["max_weight"]) if row.get("max_weight") else None
                    ),
                    "max_length": (
                        float(row["max_length"]) if row.get("max_length") else None
                    ),
                    "max_width": (
                        float(row["max_width"]) if row.get("max_width") else None
                    ),
                    "max_height": (
                        float(row["max_height"]) if row.get("max_height") else None
                    ),
                    "weight_unit": "KG",
                    "dimension_unit": "CM",
                    "domicile": row.get("domicile", "").lower() == "true",
                    "international": (
                        True if row.get("international", "").lower() == "true" else None
                    ),
                    "zones": [],
                }

            # Parse country codes
            country_codes = [
                c.strip() for c in row.get("country_codes", "").split(",") if c.strip()
            ]

            # Create zone
            zone = models.ServiceZone(
                label=row.get("zone_label", "Default Zone"),
                rate=float(row.get("rate", 0.0)),
                transit_days=(
                    int(row["transit_days"]) if row.get("transit_days") else None
                ),
                country_codes=country_codes if country_codes else None,
            )

            services_dict[karrio_service_code]["zones"].append(zone)

    # Convert to ServiceLevel objects
    return [
        models.ServiceLevel(**service_data) for service_data in services_dict.values()
    ]


DEFAULT_SERVICES = load_services_from_csv()
