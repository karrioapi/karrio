"""ParcelOne units and enums."""

import csv
import pathlib
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


class LabelFormat(lib.StrEnum):
    """Supported label formats."""

    PDF = "PDF"
    ZPL = "ZPL"
    PNG = "PNG"


class LabelSize(lib.StrEnum):
    """Supported label sizes."""

    A6 = "A6"
    A4 = "A4"


class WeightUnit(lib.StrEnum):
    """Supported weight units."""

    kg = "kg"
    g = "g"


class CEP(lib.StrEnum):
    """Available carriers through ParcelOne (CEP = Courier, Express, Parcel)."""

    PA1 = "PA1"  # Parcel.One
    DHL = "DHL"
    UPS = "UPS"


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

    cep_id = lib.OptionEnum("cep_id", str, "PA1")  # Default carrier (PA1, DHL, UPS)
    product_id = lib.OptionEnum("product_id", str, "eco")  # Default product code
    label_format = lib.OptionEnum("label_format", LabelFormat)
    label_size = lib.OptionEnum("label_size", LabelSize)
    shipping_services = lib.OptionEnum("shipping_services", list)
    shipping_options = lib.OptionEnum("shipping_options", list)


class ShippingService(lib.StrEnum):
    """ParcelOne shipping services.

    Format: parcelone_{cep}_{product}
    The service code maps to CEPID and ProductID internally.
    """

    # Parcel.One (PA1) services
    parcelone_pa1_basic = "PA1_basic"
    parcelone_pa1_eco = "PA1_eco"
    parcelone_pa1_premium = "PA1_premium"
    parcelone_pa1_express = "PA1_express"

    # DHL services (via ParcelOne)
    parcelone_dhl_paket = "DHL_PAKET"
    parcelone_dhl_paket_international = "DHL_PAKETINT"
    parcelone_dhl_express = "DHL_EXPRESS"
    parcelone_dhl_retoure = "DHL_RETOURE"

    # UPS services (via ParcelOne)
    parcelone_ups_standard = "UPS_STANDARD"
    parcelone_ups_express = "UPS_EXPRESS"
    parcelone_ups_express_saver = "UPS_EXPSAVER"


def parse_service_code(service_code: str) -> typing.Tuple[str, str]:
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
    """Carrier specific shipping options.

    ParcelOne ServiceID values that can be added to shipments or packages.
    """

    # Delivery options
    parcelone_saturday_delivery = lib.OptionEnum("SDO", bool, meta=dict(category="DELIVERY_OPTIONS"))  # Saturday delivery only
    parcelone_return_label = lib.OptionEnum("SRL", bool, meta=dict(category="RETURN"))  # Return label

    # Payment services
    parcelone_cod = lib.OptionEnum("COD", float, meta=dict(category="COD"))  # Cash on delivery
    parcelone_cod_currency = lib.OptionEnum("COD_CURRENCY", meta=dict(category="COD"))
    parcelone_insurance = lib.OptionEnum("INS", float, meta=dict(category="INSURANCE"))  # Insurance
    parcelone_insurance_currency = lib.OptionEnum("INS_CURRENCY", meta=dict(category="INSURANCE"))

    # Notification services
    parcelone_notification_email = lib.OptionEnum("MAIL", meta=dict(category="NOTIFICATION"))  # Email notification
    parcelone_notification_sms = lib.OptionEnum("SMS", meta=dict(category="NOTIFICATION"))  # SMS notification

    # Delivery confirmation
    parcelone_signature = lib.OptionEnum("SIG", bool, meta=dict(category="SIGNATURE"))  # Signature required
    parcelone_ident_check = lib.OptionEnum("IDENT", bool, meta=dict(category="SIGNATURE"))  # Identity check
    parcelone_age_check = lib.OptionEnum("AGE", int, meta=dict(category="SIGNATURE"))  # Age verification (16, 18)
    parcelone_personally = lib.OptionEnum("PERS", bool, meta=dict(category="SIGNATURE"))  # Personal delivery only

    # Delivery location options
    parcelone_neighbor_delivery = lib.OptionEnum("NEIGHBOR", bool, meta=dict(category="DELIVERY_OPTIONS"))
    parcelone_no_neighbor = lib.OptionEnum("NONEIGHBOR", bool, meta=dict(category="DELIVERY_OPTIONS"))
    parcelone_drop_off_point = lib.OptionEnum("DROP", meta=dict(category="PUDO"))  # Parcel shop delivery (PUDO ID)

    # Premium services
    parcelone_premium = lib.OptionEnum("PREMIUM", bool)
    parcelone_bulky_goods = lib.OptionEnum("BULKY", bool)

    # Unified option mappings
    cash_on_delivery = parcelone_cod
    insurance = parcelone_insurance
    signature_required = parcelone_signature
    saturday_delivery = parcelone_saturday_delivery
    email_notification = parcelone_notification_email


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

    Maps ParcelOne/last-mile-carrier tracking status codes to Karrio unified status.
    """

    pending = [
        "CREATED",
        "REGISTERED",
        "DATA_RECEIVED",
        "LABEL_PRINTED",
        "0",
        "1",
    ]
    delivered = [
        "DELIVERED",
        "POD",
        "DELIVERED_NEIGHBOR",
        "DELIVERED_SAFE_PLACE",
        "DELIVERED_PARCELSHOP",
        "90",
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
        "SHIPPED",
        "10",
        "20",
        "30",
    ]
    out_for_delivery = [
        "OUT_FOR_DELIVERY",
        "ON_DELIVERY_VEHICLE",
        "DELIVERY_IN_PROGRESS",
        "80",
    ]
    on_hold = [
        "HELD",
        "CUSTOMS",
        "CUSTOMS_CLEARANCE",
        "PAYMENT_REQUIRED",
        "AWAITING_PICKUP",
        "40",
    ]
    delivery_failed = [
        "FAILED",
        "EXCEPTION",
        "NOT_DELIVERED",
        "REFUSED",
        "ADDRESSEE_NOT_FOUND",
        "WRONG_ADDRESS",
        "99",
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
        "70",
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
                service_name="Parcel.One Eco",
                service_code="parcelone_pa1_eco",
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
