"""ParcelOne units and enums."""

import typing
import karrio.lib as lib
import karrio.core.units as units


class LabelFormat(lib.StrEnum):
    """Supported label formats."""

    PDF = "PDF"
    ZPL = "ZPL"
    PNG = "PNG"


class LabelSize(lib.StrEnum):
    """Supported label sizes."""

    parcelone_100x150 = "100x150"
    parcelone_100x200 = "100x200"


class WeightUnit(lib.StrEnum):
    """Supported weight units."""

    KG = "KG"
    G = "G"


class DimensionUnit(lib.StrEnum):
    """Supported dimension units."""

    CM = "CM"
    MM = "MM"


class CEP(lib.StrEnum):
    """Available carriers through ParcelOne (CEP = Courier, Express, Parcel)."""

    DHL = "DHL"
    DPD = "DPD"
    UPS = "UPS"
    GLS = "GLS"
    HERMES = "HERMES"


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type."""

    PACKAGE = "PACKAGE"
    PALLET = "PALLET"

    # Unified Packaging type mapping
    envelope = PACKAGE
    pak = PACKAGE
    tube = PACKAGE
    pallet = PALLET
    small_box = PACKAGE
    medium_box = PACKAGE
    your_packaging = PACKAGE


class ConnectionConfig(lib.Enum):
    """ParcelOne connection configuration options."""

    label_format = lib.OptionEnum("label_format", LabelFormat, default="PDF")
    label_size = lib.OptionEnum("label_size", LabelSize, default="100x150")
    default_cep = lib.OptionEnum("default_cep", CEP)
    shipping_services = lib.OptionEnum("shipping_services", list)
    shipping_options = lib.OptionEnum("shipping_options", list)


class ShippingService(lib.StrEnum):
    """Carrier + Product combinations.

    Format: parcelone_{cep}_{product}
    The service code maps to CEPID_PRODUCTID internally.
    """

    # DHL services
    parcelone_dhl_paket = "DHL_PAKET"
    parcelone_dhl_paket_international = "DHL_PAKETINT"
    parcelone_dhl_express = "DHL_EXPRESS"
    parcelone_dhl_retoure = "DHL_RETOURE"

    # DPD services
    parcelone_dpd_classic = "DPD_CLASSIC"
    parcelone_dpd_express = "DPD_EXPRESS"
    parcelone_dpd_international = "DPD_INT"

    # UPS services
    parcelone_ups_standard = "UPS_STANDARD"
    parcelone_ups_express = "UPS_EXPRESS"
    parcelone_ups_express_saver = "UPS_EXPSAVER"

    # GLS services
    parcelone_gls_business = "GLS_BUSINESS"
    parcelone_gls_express = "GLS_EXPRESS"

    # Hermes services
    parcelone_hermes_standard = "HERMES_STANDARD"
    parcelone_hermes_xl = "HERMES_XL"


def parse_service_code(service_code: str) -> tuple:
    """Parse a service code to extract CEP ID and Product ID.

    Args:
        service_code: Service code in format "CEPID_PRODUCTID"

    Returns:
        Tuple of (cep_id, product_id)
    """
    if "_" in service_code:
        parts = service_code.split("_", 1)
        return parts[0], parts[1] if len(parts) > 1 else ""
    return service_code, ""


class ShippingOption(lib.Enum):
    """Carrier specific options."""

    # ParcelOne services (ServiceID values)
    parcelone_cod = lib.OptionEnum("COD", float)  # Cash on delivery
    parcelone_cod_currency = lib.OptionEnum("COD_CURRENCY", str)
    parcelone_insurance = lib.OptionEnum("INS", float)  # Insurance
    parcelone_insurance_currency = lib.OptionEnum("INS_CURRENCY", str)
    parcelone_signature = lib.OptionEnum("SIG", bool)  # Signature required
    parcelone_saturday_delivery = lib.OptionEnum("SAT", bool)
    parcelone_notification_email = lib.OptionEnum("MAIL", str)
    parcelone_notification_sms = lib.OptionEnum("SMS", str)
    parcelone_age_verification = lib.OptionEnum("AGE", int)  # Age check (16, 18)
    parcelone_ident_check = lib.OptionEnum("IDENT", bool)  # Identity check
    parcelone_personally = lib.OptionEnum("PERS", bool)  # Personal delivery
    parcelone_neighbor_delivery = lib.OptionEnum("NEIGHBOR", bool)
    parcelone_drop_off_point = lib.OptionEnum("DROP", str)  # Parcel shop delivery
    parcelone_premium = lib.OptionEnum("PREMIUM", bool)
    parcelone_bulky_goods = lib.OptionEnum("BULKY", bool)
    parcelone_no_neighbor = lib.OptionEnum("NONEIGHBOR", bool)

    # Unified option mappings
    cash_on_delivery = parcelone_cod
    insurance = parcelone_insurance
    signature_required = parcelone_signature
    saturday_delivery = parcelone_saturday_delivery
    email_notification = parcelone_notification_email


def shipping_services_initializer(
    services: typing.List[str],
    **kwargs,
) -> units.Services:
    """Apply default service codes to the list of services."""
    _services = list(set(services or []))

    # If no services specified, return empty
    if not _services:
        return units.Services([], ShippingService)

    return units.Services(_services, ShippingService)


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """Apply default values to the given options."""
    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class TrackingStatus(lib.Enum):
    """Carrier tracking status mapping.

    Maps ParcelOne tracking status codes to Karrio unified status.
    """

    pending = [
        "CREATED",
        "REGISTERED",
        "DATA_RECEIVED",
        "LABEL_PRINTED",
    ]
    delivered = [
        "DELIVERED",
        "POD",
        "DELIVERED_NEIGHBOR",
        "DELIVERED_SAFE_PLACE",
        "DELIVERED_PARCELSHOP",
    ]
    in_transit = [
        "IN_TRANSIT",
        "DEPARTED",
        "ARRIVED",
        "PROCESSED",
        "SORTING",
        "IN_DELIVERY_VEHICLE",
        "EXPORTED",
        "IMPORTED",
    ]
    out_for_delivery = [
        "OUT_FOR_DELIVERY",
        "ON_DELIVERY_VEHICLE",
        "DELIVERY_IN_PROGRESS",
    ]
    on_hold = [
        "HELD",
        "CUSTOMS",
        "CUSTOMS_CLEARANCE",
        "PAYMENT_REQUIRED",
        "AWAITING_PICKUP",
    ]
    delivery_failed = [
        "FAILED",
        "EXCEPTION",
        "NOT_DELIVERED",
        "REFUSED",
        "ADDRESSEE_NOT_FOUND",
        "WRONG_ADDRESS",
    ]
    delivery_delayed = [
        "DELAYED",
        "RESCHEDULED",
        "REDIRECTED",
    ]
    ready_for_pickup = [
        "READY_FOR_PICKUP",
        "AT_PARCELSHOP",
        "AVAILABLE_FOR_COLLECTION",
    ]


class TrackingIncidentReason(lib.Enum):
    """Maps ParcelOne exception codes to normalized TrackingIncidentReason.

    These codes map carrier-specific exception/status codes to standardized
    incident reasons for tracking events.
    """

    # Carrier-caused issues
    carrier_damaged_parcel = ["DAMAGED", "DMG", "DAMAGE"]
    carrier_sorting_error = ["MISROUTED", "MSR", "WRONG_ROUTE"]
    carrier_address_not_found = ["ADDRESS_NOT_FOUND", "ANF", "NO_LOCATION"]
    carrier_parcel_lost = ["LOST", "LP", "MISSING"]
    carrier_not_enough_time = ["LATE", "NO_TIME", "TIME_OUT"]
    carrier_vehicle_issue = ["VEHICLE_BREAKDOWN", "VB", "MECHANICAL"]

    # Consignee-caused issues
    consignee_refused = ["REFUSED", "REJECTED", "RE"]
    consignee_business_closed = ["BUSINESS_CLOSED", "BC", "CLOSED"]
    consignee_not_available = ["NOT_AVAILABLE", "NA", "UNAVAILABLE"]
    consignee_not_home = ["NOT_HOME", "NH", "ABSENT"]
    consignee_incorrect_address = ["WRONG_ADDRESS", "INCORRECT_ADDRESS", "BAD_ADDRESS"]
    consignee_access_restricted = ["ACCESS_RESTRICTED", "NO_ACCESS", "SECURITY"]

    # Customs-related issues
    customs_delay = ["CUSTOMS_DELAY", "CUSTOMS_HOLD", "CH"]
    customs_documentation = ["CUSTOMS_DOCS", "MISSING_DOCS", "CP"]
    customs_duties_unpaid = ["DUTIES_UNPAID", "DU", "CUSTOMS_UNPAID"]

    # Weather/Force majeure
    weather_delay = ["WEATHER", "WE", "WEATHER_DELAY"]
    natural_disaster = ["NATURAL_DISASTER", "ND", "EMERGENCY"]

    # Other issues
    unknown = []


DEFAULT_SERVICES = [
    # DHL services
    {
        "service_code": "parcelone_dhl_paket",
        "service_name": "DHL Paket",
        "currency": "EUR",
    },
    {
        "service_code": "parcelone_dhl_paket_international",
        "service_name": "DHL Paket International",
        "currency": "EUR",
    },
    {
        "service_code": "parcelone_dhl_express",
        "service_name": "DHL Express",
        "currency": "EUR",
    },
    # DPD services
    {
        "service_code": "parcelone_dpd_classic",
        "service_name": "DPD Classic",
        "currency": "EUR",
    },
    {
        "service_code": "parcelone_dpd_express",
        "service_name": "DPD Express",
        "currency": "EUR",
    },
    # UPS services
    {
        "service_code": "parcelone_ups_standard",
        "service_name": "UPS Standard",
        "currency": "EUR",
    },
    {
        "service_code": "parcelone_ups_express",
        "service_name": "UPS Express",
        "currency": "EUR",
    },
    # GLS services
    {
        "service_code": "parcelone_gls_business",
        "service_name": "GLS Business",
        "currency": "EUR",
    },
    # Hermes services
    {
        "service_code": "parcelone_hermes_standard",
        "service_name": "Hermes Standard",
        "currency": "EUR",
    },
]
