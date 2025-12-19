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
    gls_guaranteed24 = lib.OptionEnum("GUARANTEED24", bool)
    gls_saturday_delivery = lib.OptionEnum("SaturdayService", bool)
    gls_flex_delivery = lib.OptionEnum("FlexDeliveryService", bool)
    gls_deposit_service = lib.OptionEnum("DepositService", bool)
    gls_pick_and_return = lib.OptionEnum("PickAndReturnService", bool)
    gls_shop_delivery = lib.OptionEnum("ShopDeliveryService", bool)
    gls_addressee_only = lib.OptionEnum("AddresseeOnlyService", bool)
    gls_premium = lib.OptionEnum("PremiumService", bool)

    """Standard option mappings"""
    insurance = lib.OptionEnum("insurance", float)
    saturday_delivery = gls_saturday_delivery


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
    """GLS Group tracking status mapping"""
    on_hold = ["ON_HOLD", "EXCEPTION"]
    delivered = ["DELIVERED", "SIGNED"]
    in_transit = ["IN_TRANSIT", "ACCEPTED", "COLLECTED", "IN_DEPOT"]
    delivery_failed = ["DELIVERY_FAILED", "REFUSED", "DAMAGED"]
    out_for_delivery = ["OUT_FOR_DELIVERY"]
    delivery_delayed = ["DELAYED"]
    ready_for_pickup = ["READY_FOR_PICKUP"]


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
