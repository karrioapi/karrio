import csv
import pathlib
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


class ConnectionConfig(lib.Enum):
    """Carrier connection configuration options."""

    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    label_type = lib.OptionEnum("label_type", str, "PDF")
    language = lib.OptionEnum("language", str, "DE")  # DE or EN


class ParcelClass(lib.StrEnum):
    """Hermes parcel size classes."""

    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"


class ProductType(lib.StrEnum):
    """Hermes product types."""

    BAG = "BAG"
    BIKE = "BIKE"
    LARGE_ITEM = "LARGE_ITEM"
    PARCEL = "PARCEL"


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type."""

    hermes_parcel = "PARCEL"
    hermes_bag = "BAG"
    hermes_bike = "BIKE"
    hermes_large_item = "LARGE_ITEM"

    """Unified Packaging type mapping."""
    envelope = hermes_parcel
    pak = hermes_parcel
    tube = hermes_parcel
    pallet = hermes_large_item
    small_box = hermes_parcel
    medium_box = hermes_parcel
    your_packaging = hermes_parcel


class ShippingService(lib.StrEnum):
    """Carrier specific services."""

    hermes_standard = "hermes_standard"
    hermes_next_day = "hermes_next_day"
    hermes_stated_day = "hermes_stated_day"
    hermes_parcel_shop = "hermes_parcel_shop"
    hermes_international = "hermes_international"


class ShippingOption(lib.Enum):
    """Carrier specific options."""

    # Hermes services as options
    hermes_tan_service = lib.OptionEnum("tanService", bool)
    hermes_limited_quantities = lib.OptionEnum("limitedQuantitiesService", bool)
    hermes_bulk_goods = lib.OptionEnum("bulkGoodService", bool)
    hermes_household_signature = lib.OptionEnum("householdSignatureService", bool)
    hermes_compact_parcel = lib.OptionEnum("compactParcelService", bool)
    hermes_next_day = lib.OptionEnum("nextDayService", bool)
    hermes_signature = lib.OptionEnum("signatureService", bool)
    hermes_redirection_prohibited = lib.OptionEnum("redirectionProhibitedService", bool)
    hermes_exclude_parcel_shop_auth = lib.OptionEnum("excludeParcelShopAuthorization", bool)
    hermes_late_injection = lib.OptionEnum("lateInjectionService", bool)

    # Cash on delivery
    hermes_cod_amount = lib.OptionEnum("codAmount", float)
    hermes_cod_currency = lib.OptionEnum("codCurrency", str)

    # Customer alert service
    hermes_notification_email = lib.OptionEnum("notificationEmail", str)
    hermes_notification_type = lib.OptionEnum("notificationType", str)  # EMAIL, SMS, EMAIL_SMS

    # Stated day service
    hermes_stated_day = lib.OptionEnum("statedDay", str)  # YYYY-MM-DD format

    # Stated time service
    hermes_time_slot = lib.OptionEnum("timeSlot", str)  # FORENOON, NOON, AFTERNOON, EVENING

    # Ident service
    hermes_ident_id = lib.OptionEnum("identID", str)
    hermes_ident_type = lib.OptionEnum("identType", str)  # GERMAN_IDENTITY_CARD, etc.
    hermes_ident_fsk = lib.OptionEnum("identVerifyFsk", str)  # 18
    hermes_ident_birthday = lib.OptionEnum("identVerifyBirthday", str)  # YYYY-MM-DD

    # Parcel shop delivery
    hermes_parcel_shop_id = lib.OptionEnum("psID", str)
    hermes_parcel_shop_selection_rule = lib.OptionEnum("psSelectionRule", str)  # SELECT_BY_ID, SELECT_BY_RECEIVER_ADDRESS
    hermes_parcel_shop_customer_firstname = lib.OptionEnum("psCustomerFirstName", str)
    hermes_parcel_shop_customer_lastname = lib.OptionEnum("psCustomerLastName", str)

    # Multipart service
    hermes_part_number = lib.OptionEnum("partNumber", int)
    hermes_number_of_parts = lib.OptionEnum("numberOfParts", int)
    hermes_parent_shipment_order_id = lib.OptionEnum("parentShipmentOrderID", str)

    """Unified Option type mapping."""
    signature_required = hermes_signature
    cash_on_delivery = hermes_cod_amount


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
    """Hermes tracking status mapping."""

    on_hold = ["on_hold"]
    delivered = ["delivered"]
    in_transit = ["in_transit"]
    delivery_failed = ["delivery_failed"]
    delivery_delayed = ["delivery_delayed"]
    out_for_delivery = ["out_for_delivery"]
    ready_for_pickup = ["ready_for_pickup"]


class LabelType(lib.StrEnum):
    """Hermes label formats - use +json variants for JSON response with base64 label."""

    PDF = "application/shippinglabel-pdf+json"
    ZPL = "application/shippinglabel-zpl+json;dpi=300"
    PNG = "application/shippinglabel-data+json"


class PickupTimeSlot(lib.StrEnum):
    """Hermes pickup time slots per OpenAPI spec."""

    BETWEEN_10_AND_13 = "BETWEEN_10_AND_13"
    BETWEEN_12_AND_15 = "BETWEEN_12_AND_15"
    BETWEEN_14_AND_17 = "BETWEEN_14_AND_17"


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
                service_name="Hermes Standard",
                service_code="hermes_standard",
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
