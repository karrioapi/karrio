"""PostAT units and enums."""

import csv
import pathlib
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


class LabelFormat(lib.StrEnum):
    """Supported label formats."""

    PDF = "pdf"
    ZPL2 = "zpl2"


class LabelSize(lib.StrEnum):
    """Supported label sizes."""

    SIZE_100x150 = "100x150"
    SIZE_100x200 = "100x200"


class PaperLayout(lib.StrEnum):
    """Supported paper layouts for PDF output."""

    LAYOUT_2xA5inA4 = "2xA5inA4"
    LAYOUT_4xA6inA4 = "4xA6inA4"
    LAYOUT_A4 = "A4"


class ConnectionConfig(lib.Enum):
    """PostAT connection configuration options."""

    server_url = lib.OptionEnum("server_url", str)
    label_format = lib.OptionEnum(
        "label_format",
        lib.units.create_enum("LabelFormat", [_.name for _ in LabelFormat]),
    )
    label_size = lib.OptionEnum(
        "label_size",
        lib.units.create_enum("LabelSize", [_.name for _ in LabelSize]),
    )
    paper_layout = lib.OptionEnum(
        "paper_layout",
        lib.units.create_enum("PaperLayout", [_.name for _ in PaperLayout]),
    )
    shipping_services = lib.OptionEnum("shipping_services", list)
    shipping_options = lib.OptionEnum("shipping_options", list)


class ShippingService(lib.StrEnum):
    """PostAT shipping services.

    Note: Service codes (DeliveryServiceThirdPartyID) are configured per account
    by Austrian Post. These are common examples.
    """

    postat_standard_domestic = "10"
    postat_express_domestic = "20"
    postat_international_standard = "30"
    postat_international_express = "40"


class ShippingOption(lib.Enum):
    """PostAT shipping options (Features)."""

    # Label configuration (can be set per-shipment)
    postat_label_size = lib.OptionEnum("label_size", str)
    postat_paper_layout = lib.OptionEnum("paper_layout", str)

    # Cash on Delivery
    postat_cod = lib.OptionEnum("COD", float, meta=dict(category="COD"))
    postat_cod_currency = lib.OptionEnum("COD_CURRENCY", str, meta=dict(category="COD"))

    # Insurance
    postat_insurance = lib.OptionEnum("INS", float, meta=dict(category="INSURANCE"))
    postat_insurance_currency = lib.OptionEnum("INS_CURRENCY", str, meta=dict(category="INSURANCE"))

    # Signature required
    postat_signature = lib.OptionEnum("SIG", bool, meta=dict(category="SIGNATURE"))

    # Saturday delivery
    postat_saturday_delivery = lib.OptionEnum("SAT", bool, meta=dict(category="DELIVERY_OPTIONS"))

    # Email notification
    postat_email_notification = lib.OptionEnum("MAIL", str, meta=dict(category="NOTIFICATION"))

    # SMS notification
    postat_sms_notification = lib.OptionEnum("SMS", str, meta=dict(category="NOTIFICATION"))

    # Age verification (16 or 18)
    postat_age_verification = lib.OptionEnum("AGE", int, meta=dict(category="SIGNATURE"))

    # Unified option mappings
    cash_on_delivery = postat_cod
    insurance = postat_insurance
    signature_required = postat_signature
    saturday_delivery = postat_saturday_delivery
    email_notification = postat_email_notification


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
    """PostAT tracking status mapping."""

    pending = [
        "REGISTERED",
        "CREATED",
        "DATA_RECEIVED",
        "LABEL_PRINTED",
    ]
    delivered = [
        "DELIVERED",
        "ZUGESTELLT",
        "POD",
    ]
    in_transit = [
        "IN_TRANSIT",
        "UNTERWEGS",
        "DEPARTED",
        "ARRIVED",
    ]
    out_for_delivery = [
        "OUT_FOR_DELIVERY",
        "IN_ZUSTELLUNG",
    ]
    on_hold = [
        "HELD",
        "CUSTOMS",
    ]
    delivery_failed = [
        "FAILED",
        "NOT_DELIVERED",
        "REFUSED",
    ]


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
                service_name="PostAT Standard Domestic",
                service_code="postat_standard_domestic",
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

            # Parse transit days (handle "1-3" format)
            transit_days = None
            if row.get("transit_days"):
                transit_str = row["transit_days"].split("-")[0]
                if transit_str.isdigit():
                    transit_days = int(transit_str)

            # Create zone
            zone = models.ServiceZone(
                label=row.get("zone_label", "Default Zone"),
                rate=float(row.get("rate", 0.0)),
                transit_days=transit_days,
                country_codes=country_codes if country_codes else None,
            )

            services_dict[karrio_service_code]["zones"].append(zone)

    # Convert to ServiceLevel objects
    return [
        models.ServiceLevel(**service_data) for service_data in services_dict.values()
    ]


DEFAULT_SERVICES = load_services_from_csv()
