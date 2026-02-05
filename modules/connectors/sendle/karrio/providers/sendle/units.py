import csv
import pathlib

import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


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


class ShippingService(lib.StrEnum):
    """Carrier specific services"""

    sendle_standard_pickup = "STANDARD-PICKUP"
    sendle_standard_dropoff = "STANDARD-DROPOFF"
    sendle_express_pickup = "EXPRESS-PICKUP"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    sendle_hide_pickup_address = lib.OptionEnum("hide_pickup_address", bool, meta=dict(category="DELIVERY_OPTIONS"))
    sendle_first_mile_option = lib.OptionEnum("first_mile_option", bool, meta=dict(category="DELIVERY_OPTIONS"))


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
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class TrackingStatus(lib.Enum):
    on_hold = ["Pickup Attempted", "Delivery Attempted"]
    delivered = ["Delivered"]
    in_transit = ["Pickup", "Drop Off", "Dropped Off", "In Transit"]
    delivery_failed = ["Damaged", "Unable to Deliver"]
    delivery_delayed = ["Card Left"]
    out_for_delivery = ["Out for Delivery", "Local Delivery"]
    ready_for_pickup = ["Left with Agent"]


class TrackingIncidentReason(lib.Enum):
    """Maps Sendle exception codes to normalized TrackingIncidentReason."""

    # Carrier-caused issues
    carrier_damaged_parcel = ["Damaged", "Package Damaged", "Parcel Damaged"]
    carrier_sorting_error = ["Sorting Error", "Misrouted"]
    carrier_address_not_found = ["Address Not Found", "Unable to Locate Address"]
    carrier_parcel_lost = ["Lost", "Missing"]
    carrier_not_enough_time = ["Insufficient Time", "Time Constraint"]
    carrier_vehicle_issue = ["Vehicle Issue", "Transport Issue"]

    # Consignee-caused issues
    consignee_refused = ["Refused", "Delivery Refused", "Recipient Refused"]
    consignee_business_closed = ["Business Closed", "Closed"]
    consignee_not_available = ["Not Available", "Recipient Not Available"]
    consignee_not_home = ["Not Home", "No One Home", "Card Left"]
    consignee_incorrect_address = ["Incorrect Address", "Wrong Address"]
    consignee_access_restricted = ["Access Restricted", "Unable to Access"]

    # Customs-related issues
    customs_delay = ["Customs Delay", "Customs Hold", "Customs Processing"]
    customs_documentation = ["Customs Documentation", "Missing Documents"]
    customs_duties_unpaid = ["Duties Unpaid", "Customs Fees Outstanding"]

    # Weather/Force majeure
    weather_delay = ["Weather Delay", "Weather", "Severe Weather"]
    natural_disaster = ["Natural Disaster", "Emergency Situation"]

    # Delivery exceptions
    delivery_exception_hold = ["Held at Agent", "Left with Agent", "Pickup Attempted", "Delivery Attempted"]
    delivery_exception_undeliverable = ["Unable to Deliver", "Undeliverable"]

    # Other issues
    unknown = []


def load_services_from_csv() -> list:
    csv_path = pathlib.Path(__file__).resolve().parent / "services.csv"
    if not csv_path.exists():
        return []
    services_dict: dict[str, dict] = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            service_code = row["service_code"]
            karrio_service_code = ShippingService.map(service_code).name_or_key
            if karrio_service_code not in services_dict:
                services_dict[karrio_service_code] = {
                    "service_name": row["service_name"],
                    "service_code": karrio_service_code,
                    "currency": row.get("currency", "AUD"),
                    "min_weight": float(row["min_weight"]) if row.get("min_weight") else None,
                    "max_weight": float(row["max_weight"]) if row.get("max_weight") else None,
                    "max_length": float(row["max_length"]) if row.get("max_length") else None,
                    "max_width": float(row["max_width"]) if row.get("max_width") else None,
                    "max_height": float(row["max_height"]) if row.get("max_height") else None,
                    "weight_unit": "KG",
                    "dimension_unit": "CM",
                    "domicile": (row.get("domicile") or "").lower() == "true",
                    "international": True if (row.get("international") or "").lower() == "true" else None,
                    "zones": [],
                }
            country_codes = [c.strip() for c in row.get("country_codes", "").split(",") if c.strip()]
            zone = models.ServiceZone(
                label=row.get("zone_label", "Default Zone"),
                rate=float(row.get("rate", 0.0)),
                min_weight=float(row["min_weight"]) if row.get("min_weight") else None,
                max_weight=float(row["max_weight"]) if row.get("max_weight") else None,
                transit_days=int(row["transit_days"].split("-")[0]) if row.get("transit_days") and row["transit_days"].split("-")[0].isdigit() else None,
                country_codes=country_codes if country_codes else None,
            )
            services_dict[karrio_service_code]["zones"].append(zone)
    return [models.ServiceLevel(**service_data) for service_data in services_dict.values()]


DEFAULT_SERVICES = load_services_from_csv()
