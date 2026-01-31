"""Karrio Asendia unit definitions."""

import csv
import pathlib
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


class ConnectionConfig(lib.Enum):
    """Asendia connection configuration options."""

    label_type = lib.OptionEnum("label_type", str)
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)


class LabelType(lib.StrEnum):
    """Asendia label format types."""

    PDF = "PDF"
    PNG = "PNG"
    ZPL = "Zebra"


class ProductCode(lib.StrEnum):
    """Asendia product codes."""

    # e-PAQ products
    asendia_epaq_standard = "EPAQSTD"
    asendia_epaq_plus = "EPAQPLUS"
    asendia_epaq_elite = "EPAQELITE"
    asendia_epaq_returns = "EPAQRET"

    # Country Road products
    asendia_country_road = "CROAD"
    asendia_country_road_plus = "CROADPLUS"

    # Priority products
    asendia_priority = "PRIORITY"
    asendia_priority_tracked = "PRIORITYTRK"


class ServiceCode(lib.StrEnum):
    """Asendia service codes."""

    # Common service codes
    asendia_cup = "CUP"  # Collection/Pickup
    asendia_std = "STD"  # Standard
    asendia_exp = "EXP"  # Express


class ShippingService(lib.StrEnum):
    """Asendia shipping services (product + service combination)."""

    # e-PAQ Standard services
    asendia_epaq_standard = "EPAQSTD"
    asendia_epaq_standard_cup = "EPAQSTD_CUP"

    # e-PAQ Plus services
    asendia_epaq_plus = "EPAQPLUS"
    asendia_epaq_plus_cup = "EPAQPLUS_CUP"

    # e-PAQ Elite services
    asendia_epaq_elite = "EPAQELITE"
    asendia_epaq_elite_cup = "EPAQELITE_CUP"

    # e-PAQ Returns
    asendia_epaq_returns = "EPAQRET"
    asendia_epaq_returns_domestic = "EPAQRETDOM"

    # Country Road services
    asendia_country_road = "CROAD"
    asendia_country_road_plus = "CROADPLUS"

    # Priority services
    asendia_priority = "PRIORITY"
    asendia_priority_tracked = "PRIORITYTRK"


class PackagingType(lib.StrEnum):
    """Asendia format/packaging types."""

    # Asendia format codes
    asendia_packet = "B"  # Standard packet format
    asendia_parcel = "P"  # Parcel format

    # Unified Packaging type mapping
    envelope = asendia_packet
    pak = asendia_packet
    tube = asendia_parcel
    pallet = asendia_parcel
    small_box = asendia_packet
    medium_box = asendia_parcel
    your_packaging = asendia_packet


class InsuranceOption(lib.StrEnum):
    """Asendia insurance options."""

    asendia_el150 = "EL150"
    asendia_el500 = "EL500"
    asendia_el1000 = "EL1000"
    asendia_el2500 = "EL2500"


class ReturnLabelType(lib.StrEnum):
    """Asendia return label types."""

    asendia_epaq_return_domestic = "EPAQRETDOM"


class ReturnPaymentType(lib.StrEnum):
    """Asendia return label payment types."""

    asendia_prepaid = "RETPP"  # Return prepaid


class ShippingOption(lib.Enum):
    """Asendia shipping options."""

    # Asendia specific options
    asendia_insurance = lib.OptionEnum("insurance", str)
    asendia_return_label = lib.OptionEnum("return_label", bool)
    asendia_return_label_type = lib.OptionEnum("return_label_type", str)
    asendia_return_label_payment = lib.OptionEnum("return_label_payment", str)
    asendia_sender_eori = lib.OptionEnum("sender_eori", str)
    asendia_seller_eori = lib.OptionEnum("seller_eori", str)
    asendia_sender_tax_id = lib.OptionEnum("sender_tax_id", str)
    asendia_receiver_tax_id = lib.OptionEnum("receiver_tax_id", str)

    # Unified Option type mapping
    insurance = asendia_insurance


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
    """Maps Asendia tracking status codes to normalized Karrio statuses."""

    pending = ["PENDING", "CREATED", "ACCEPTED", "LABEL_PRINTED"]
    picked_up = ["PICKED_UP", "COLLECTED", "COLLECTION", "PU"]
    in_transit = [
        "IN_TRANSIT",
        "IT",
        "TRANSIT",
        "DEPARTED",
        "ARRIVED",
        "PROCESSED",
        "CUSTOMS",
        "CLEARED",
    ]
    out_for_delivery = ["OUT_FOR_DELIVERY", "OFD", "WITH_COURIER"]
    delivered = ["DELIVERED", "DL", "DELIVERY_CONFIRMED"]
    ready_for_pickup = ["READY_FOR_PICKUP", "PICKUP", "AT_LOCATION"]
    on_hold = ["ON_HOLD", "HELD", "AWAITING"]
    delivery_delayed = ["DELAYED", "DELAY", "RESCHEDULED"]
    delivery_failed = [
        "DELIVERY_FAILED",
        "FAILED",
        "UNDELIVERABLE",
        "RETURNED",
        "RTS",
    ]


class TrackingIncidentReason(lib.Enum):
    """Maps carrier exception codes to normalized incident reasons.

    IMPORTANT: This enum is required for tracking implementations.
    It maps carrier-specific exception/status codes to standardized
    incident reasons for tracking events. The reason field helps
    identify why a delivery exception occurred.

    Categories of reasons:
    - carrier_*: Issues caused by the carrier
    - consignee_*: Issues caused by the recipient
    - customs_*: Customs-related delays
    - weather_*: Weather/force majeure events
    """

    # Carrier-caused issues
    carrier_damaged_parcel = ["DAMAGED", "DMG"]
    carrier_sorting_error = ["MISROUTED", "MSR"]
    carrier_address_not_found = ["ADDRESS_NOT_FOUND", "ANF"]
    carrier_parcel_lost = ["LOST", "LP"]
    carrier_not_enough_time = ["LATE", "NO_TIME"]
    carrier_vehicle_issue = ["VEHICLE_BREAKDOWN", "VB"]

    # Consignee-caused issues
    consignee_refused = ["REFUSED", "RJ"]
    consignee_business_closed = ["BUSINESS_CLOSED", "BC"]
    consignee_not_available = ["NOT_AVAILABLE", "NA"]
    consignee_not_home = ["NOT_HOME", "NH"]
    consignee_incorrect_address = ["WRONG_ADDRESS", "IA"]
    consignee_access_restricted = ["ACCESS_RESTRICTED", "AR"]

    # Customs-related issues
    customs_delay = ["CUSTOMS_DELAY", "CD"]
    customs_documentation = ["CUSTOMS_DOCS", "CM"]
    customs_duties_unpaid = ["DUTIES_UNPAID", "DU"]

    # Weather/Force majeure
    weather_delay = ["WEATHER", "WE"]
    natural_disaster = ["NATURAL_DISASTER", "ND"]

    # Unknown
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
                service_name="Asendia e-PAQ Standard",
                service_code="asendia_epaq_standard",
                currency="EUR",
                international=True,
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
                    "domicile": (row.get("domicile") or "").lower() == "true",
                    "international": (
                        True if (row.get("international") or "").lower() == "true" else None
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


