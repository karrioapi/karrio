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

    laposte_standard_service = "La Poste Standard Service"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    # laposte_option = lib.OptionEnum("code")

    """ Unified Option type mapping """
    # insurance = laposte_coverage  #  maps unified karrio option to carrier specific

    pass


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
    delivered = ["DI1"]
    in_transit = [""]
    out_for_delivery = ["MD2", "ET1"]


class TrackingIncidentReason(lib.Enum):
    """Maps La Poste exception codes to normalized TrackingIncidentReason."""

    # Carrier-caused issues
    carrier_damaged_parcel = []
    carrier_sorting_error = []
    carrier_address_not_found = ["AN1"]
    carrier_parcel_lost = []
    carrier_vehicle_issue = []

    # Consignee-caused issues
    consignee_refused = ["RE1"]
    consignee_business_closed = []
    consignee_not_available = ["ND1", "AG1"]
    consignee_not_home = ["ND1"]
    consignee_incorrect_address = ["AN1"]
    consignee_access_restricted = []

    # Customs-related issues
    customs_delay = ["DO1"]
    customs_documentation = []
    customs_duties_unpaid = []

    # Weather/Force majeure
    weather_delay = []
    natural_disaster = []

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
                    "currency": row.get("currency", "EUR"),
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
