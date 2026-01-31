import csv
import pathlib
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


class PackagingType(lib.StrEnum):
    """GLS Group specific packaging types"""
    gls_parcel = "PARCEL"
    gls_envelope = "ENVELOPE"
    gls_pallet = "PALLET"

    """Unified Packaging type mapping"""
    envelope = gls_envelope
    pak = gls_parcel
    small_box = gls_parcel
    medium_box = gls_parcel
    your_packaging = gls_parcel
    pallet = gls_pallet


class ShippingService(lib.StrEnum):
    """GLS Group specific services"""
    gls_parcel = "PARCEL"
    gls_express = "EXPRESS"
    gls_guaranteed24 = "GUARANTEED24"
    gls_business_parcel = "BUSINESSPARCEL"
    gls_euro_business_parcel = "EUROBUSINESSPARCEL"


class ShippingOption(lib.Enum):
    """GLS Group specific options"""

    # Delivery Options (Zustelloptionen tab)
    gls_guaranteed24 = lib.OptionEnum(
        "GUARANTEED24", bool,
        help="Guaranteed next-day delivery service",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True)
    )
    gls_saturday_delivery = lib.OptionEnum(
        "SaturdayService", bool,
        help="Enable Saturday delivery",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True)
    )
    gls_flex_delivery = lib.OptionEnum(
        "FlexDeliveryService", bool,
        help="Notify recipient about delivery options",
        meta=dict(category="NOTIFICATION", configurable=True)
    )
    gls_deposit_service = lib.OptionEnum(
        "DepositService", bool,
        help="Enable delivery to a predefined deposit location",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True)
    )
    gls_deposit_description = lib.OptionEnum(
        "DepositDescription", str,
        help="Description of the deposit location (e.g., 'Behind the garage')",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True)
    )
    gls_deposit_contact = lib.OptionEnum(
        "DepositContact", str,
        help="Contact person at the deposit location",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True)
    )
    gls_express_parcel = lib.OptionEnum(
        "ExpressParcel", bool,
        help="Enable express shipping",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True)
    )
    gls_time_definite_service = lib.OptionEnum(
        "TimeDefiniteService", str,
        help="Set specific delivery time (before 8 AM, 9 AM, 10 AM, 12 PM)",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True)
    )

    # PUDO Options (Parcel Shop)
    gls_shop_delivery = lib.OptionEnum(
        "ShopDeliveryService", bool,
        help="Delivery to a GLS ParcelShop",
        meta=dict(category="PUDO", configurable=True)
    )
    gls_shop_id = lib.OptionEnum(
        "ShopID", str,
        help="GLS ParcelShop ID for delivery",
        meta=dict(category="PUDO", configurable=True)
    )
    gls_shop_auto_determine = lib.OptionEnum(
        "ShopAutoSelect", bool,
        help="Automatically determine nearest GLS ParcelShop based on recipient address",
        meta=dict(category="PUDO", configurable=True)
    )

    # Signature Options
    gls_addressee_only = lib.OptionEnum(
        "AddresseeOnlyService", bool,
        help="Delivery only to the addressee (no neighbor delivery)",
        meta=dict(category="SIGNATURE", configurable=True)
    )
    gls_signature_service = lib.OptionEnum(
        "SignatureService", bool,
        help="Require signature upon delivery",
        meta=dict(category="SIGNATURE", configurable=True)
    )
    gls_ident_pin_service = lib.OptionEnum(
        "IdentPINService", bool,
        help="Identification via PIN code at delivery",
        meta=dict(category="SIGNATURE", configurable=True)
    )

    # Insurance Options
    gls_add_on_liability = lib.OptionEnum(
        "AddOnLiabilityService", bool,
        help="Add extra liability coverage for shipments",
        meta=dict(category="INSURANCE", configurable=True)
    )

    # Return Options
    gls_pick_and_return = lib.OptionEnum(
        "PickAndReturnService", bool,
        help="Enable pick and return service",
        meta=dict(category="RETURN", configurable=True)
    )
    gls_shop_return = lib.OptionEnum(
        "ShopReturnService", bool,
        help="Add a pre-printed return label inside the package",
        meta=dict(category="RETURN", configurable=True)
    )
    gls_return_enabled = lib.OptionEnum(
        "ReturnService", bool,
        help="Enable return label generation for this shipment",
        meta=dict(category="RETURN", configurable=True)
    )

    # Dangerous Goods
    gls_limited_quantity = lib.OptionEnum(
        "LimitedQuantity", bool,
        help="Mark shipment as containing limited quantity hazardous materials",
        meta=dict(category="DANGEROUS_GOOD", configurable=True)
    )
    gls_limited_quantity_weight = lib.OptionEnum(
        "LimitedQuantityWeight", float,
        help="Weight of limited quantity hazardous material in kg",
        meta=dict(category="DANGEROUS_GOOD", configurable=True)
    )

    # COD Options (Cash on Delivery)
    gls_cod_reference = lib.OptionEnum(
        "CODReference", str,
        help="Reference number for cash on delivery payment",
        meta=dict(category="COD", configurable=True)
    )

    # Premium/Other
    gls_premium = lib.OptionEnum(
        "PremiumService", bool,
        help="Enable premium service",
        meta=dict(configurable=True)
    )

    """Standard option mappings"""
    insurance = lib.OptionEnum(
        "insurance", float,
        help="Insurance value for the shipment",
        meta=dict(category="INSURANCE", configurable=True)
    )
    saturday_delivery = gls_saturday_delivery
    dangerous_good = gls_limited_quantity


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """Apply default values to the given options."""
    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class TrackingStatus(lib.Enum):
    """GLS Group tracking status mapping - based on ecitrackandtrace.yaml ParcelDTO.status enum."""
    pending = ["PLANNEDPICKUP", "INPICKUP", "PREADVICE"]
    in_transit = ["INTRANSIT", "INWAREHOUSE"]
    out_for_delivery = ["INDELIVERY"]
    delivered = ["DELIVERED", "DELIVEREDPS", "FINAL"]
    delivery_failed = ["NOTPICKEDUP", "NOTDELIVERED"]
    cancelled = ["CANCELED"]
    ready_for_pickup = ["DELIVEREDPS"]


class WeightUnit(lib.StrEnum):
    """Weight unit mapping"""
    KG = "kg"
    LB = "lb"


class DimensionUnit(lib.StrEnum):
    """Dimension unit mapping"""
    CM = "cm"
    IN = "in"


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
                service_name="GLS Parcel",
                service_code="gls_parcel",
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
