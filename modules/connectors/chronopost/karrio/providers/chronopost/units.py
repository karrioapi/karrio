import csv
import pathlib
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
from karrio.core.utils.enum import OptionEnum


class WeightUnit(lib.StrEnum):
    KG = "KGM"


class LabelType(lib.StrEnum):
    PDF_LABEL = "PDF"
    PPR_LABEL = "PPR"
    SPD_LABEL = "SPD"
    Z2D_LABEL = "Z2D"
    THE_LABEL = "THE"
    XML_LABEL = "XML"
    XML2D_LABEL = "XML2D"
    THEPSG_LABEL = "THEPSG"
    ZPLPSG_LABEL = "ZPLPSG"
    ZPL300_LABEL = "ZPL300"

    """ Unified Label type mapping """
    PDF = PDF_LABEL
    ZPL = ZPL300_LABEL


class CustomsContentType(lib.StrEnum):
    document = "DOC"
    marchandise = "MAR"

    """ Unified Customs Content Type mapping"""
    documents = document
    merchandise = marchandise


class ShippingService(lib.StrEnum):
    chronopost_retrait_bureau = "0"
    chronopost_13 = "1"
    chronopost_10 = "2"
    chronopost_18 = "16"
    chronopost_relais = "86"
    chronopost_express_international = "17"
    chronopost_premium_international = "37"
    chronopost_classic_international = "44"


class ShippingOption(lib.Enum):
    chronopost_delivery_on_monday = OptionEnum("1", meta=dict(category="DELIVERY_OPTIONS"))
    chronopost_delivery_on_saturday = OptionEnum("6", meta=dict(category="DELIVERY_OPTIONS"))
    chronopost_delivery_normal = OptionEnum("0", meta=dict(category="DELIVERY_OPTIONS"))

    """ Unified Option type mapping """
    saturday_delivery = chronopost_delivery_on_saturday


class TrackingIncidentReason(lib.Enum):
    """Maps Chronopost exception codes to normalized TrackingIncidentReason."""
    carrier_damaged_parcel = ["DMG", "DAMAGE", "DAMAGED"]
    carrier_sorting_error = ["MISROUTE", "TRI"]
    carrier_parcel_lost = ["LOST", "PERDU"]
    carrier_vehicle_issue = ["DELAY", "RETARD"]

    consignee_refused = ["REFUSED", "REF", "REFUSE"]
    consignee_business_closed = ["CLOSED", "FERME"]
    consignee_not_home = ["NOTHOME", "NH", "ABSENT"]
    consignee_incorrect_address = ["BADADDR", "INCORRECT", "ADRESSE"]
    consignee_access_restricted = ["NOACCESS", "ACCES"]

    customs_delay = ["CUSTOMS", "CUSTOMSHOLD", "DOUANE"]
    customs_documentation = ["CUSTOMSDOC", "DOUANE_DOC"]
    customs_duties_unpaid = ["CUSTOMS_UNPAID", "TAXES"]

    weather_delay = ["WEATHER", "METEO"]

    delivery_exception_hold = ["HOLD", "ONHOLD", "RETENU"]
    delivery_exception_undeliverable = ["UNDELIVERABLE", "NON_LIVRABLE"]

    unknown = []


def shipping_options_initializer(
    options: dict,
    package_options: units.Options = None,
) -> units.Options:
    """
    Apply default values to the given options.
    """
    _options = options.copy()

    if package_options is not None:
        _options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(_options, ShippingOption, items_filter=items_filter)


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
                service_name="Chronopost 13",
                service_code="chronopost_13",
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
