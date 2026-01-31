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


class Incoterm(lib.Enum):
    DAP = "06"
    DAP_enhanced = "07"


class CustomsContentType(lib.StrEnum):
    sale = "01"
    return_replacement = "02"
    gift = "03"

    """ Unified Content type mapping """
    sample = sale
    merchandise = sale
    return_merchandise = return_replacement


class ShippingService(lib.StrEnum):
    """Carrier specific services"""

    dpd_cl = "CL"
    dpd_express_10h = "E10"
    dpd_express_12h = "E12"
    dpd_express_18h_guarantee = "E18"
    dpd_express_b2b_predict = "B2B MSG option"

    dpd_home_europe = dpd_cl
    dpd_shop_europe = dpd_cl
    dpd_express_europe = dpd_cl
    dpd_express_guarantee = dpd_cl
    dpd_express_international = dpd_cl


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    dpd_order_type = lib.OptionEnum("orderType")
    dpd_saturday_delivery = lib.OptionEnum("saturdayDelivery", bool, meta=dict(category="DELIVERY_OPTIONS"))
    dpd_ex_works_delivery = lib.OptionEnum("exWorksDelivery", bool, meta=dict(category="DELIVERY_OPTIONS"))
    # dpd_guarantee = lib.OptionEnum("guarantee", bool)
    dpd_tyres = lib.OptionEnum("tyres", bool)
    # dpd_personal_delivery = lib.OptionEnum("personalDelivery", bool)
    # dpd_pickup = lib.OptionEnum("pickup", bool)
    dpd_parcel_shop_delivery = lib.OptionEnum("parcelShopDelivery", meta=dict(category="PUDO"))
    # dpd_predict = lib.OptionEnum("predict", bool)
    # dpd_personal_delivery_notification = lib.OptionEnum("personalDeliveryNotification", bool)
    # dpd_proactive_notification = lib.OptionEnum("proactiveNotification", bool)
    # dpd_delivery = lib.OptionEnum("delivery", bool)
    # dpd_invoice_address = lib.OptionEnum("invoiceAddress")
    # dpd_country_specific_service = lib.OptionEnum("countrySpecificService")

    """ Unified Option type mapping """
    saturday_delivery = dpd_saturday_delivery


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
    """Carrier tracking status mapping"""

    delivered = ["Delivered"]
    in_transit = ["in_transit"]
    ready_for_pickup = ["ParcelShop"]
    delivery_failed = ["DeliveryFailure"]
    out_for_delivery = ["Courier", "ReturningFromDelivery"]


class TrackingIncidentReason(lib.Enum):
    """Maps DPD exception codes to normalized TrackingIncidentReason."""

    # Carrier-caused issues
    carrier_damaged_parcel = ["DMG", "DAMAGED"]
    carrier_sorting_error = ["MISROUTED"]
    carrier_address_not_found = ["ADDRESS_NOT_FOUND"]
    carrier_parcel_lost = ["LOST"]
    carrier_vehicle_issue = ["VEHICLE_ISSUE"]

    # Consignee-caused issues
    consignee_refused = ["REFUSED", "REJECTED"]
    consignee_business_closed = ["BUSINESS_CLOSED"]
    consignee_not_available = ["NOT_AVAILABLE"]
    consignee_not_home = ["NOT_HOME", "RECIPIENT_ABSENT"]
    consignee_incorrect_address = ["INCORRECT_ADDRESS", "WRONG_ADDRESS"]
    consignee_access_restricted = ["ACCESS_RESTRICTED"]

    # Customs-related issues
    customs_delay = ["CUSTOMS_DELAY", "CUSTOMS_HOLD"]
    customs_documentation = ["CUSTOMS_DOCS"]
    customs_duties_unpaid = ["DUTIES_UNPAID"]

    # Weather/Force majeure
    weather_delay = ["WEATHER"]
    natural_disaster = ["NATURAL_DISASTER"]

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
                service_name="DPD CLASSIC",
                service_code="dpd_cl",
                currency="EUR",
                domicile=True,
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
                min_weight=float(row["min_weight"]) if row.get("min_weight") else None,
                max_weight=float(row["max_weight"]) if row.get("max_weight") else None,
                transit_days=(
                    int(row["transit_days"].split("-")[0]) if row.get("transit_days") and row["transit_days"].split("-")[0].isdigit() else None
                ),
                country_codes=country_codes if country_codes else None,
            )

            services_dict[karrio_service_code]["zones"].append(zone)

    # Convert to ServiceLevel objects
    return [
        models.ServiceLevel(**service_data) for service_data in services_dict.values()
    ]


DEFAULT_SERVICES = load_services_from_csv()


# Legacy Netherlands-specific services (kept for backwards compatibility)
DEFAULT_NL_SERVICES = [
    models.ServiceLevel(
        service_name="DPD CL",
        service_code="dpd_cl",
        currency="EUR",
        max_weight=31.5,
        weight_unit="KG",
        domicile=True,
        international=True,
        zones=[
            # The Netherlands
            models.ServiceZone(
                label="2shop", max_weight=1.00, min_weight=0.00, rate=4.25
            ),
            models.ServiceZone(
                label="2shop", max_weight=10.0, min_weight=1.00, rate=4.40
            ),
            models.ServiceZone(
                label="2shop", max_weight=20.0, min_weight=10.0, rate=9.00
            ),
            models.ServiceZone(
                label="2home", max_weight=1.00, min_weight=0.00, rate=5.25
            ),
            models.ServiceZone(
                label="2home", max_weight=10.0, min_weight=1.00, rate=5.60
            ),
            models.ServiceZone(
                label="2home", max_weight=20.0, min_weight=10.0, rate=9.50
            ),
        ],
    ),
]
