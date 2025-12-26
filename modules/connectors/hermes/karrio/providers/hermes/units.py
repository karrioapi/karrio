import karrio.lib as lib
import karrio.core.units as units


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
    """Hermes label formats."""

    PDF = "application/pdf"
    ZPL = "text/vnd.hermes.zpl"
    PNG = "image/png"


class PickupTimeSlot(lib.StrEnum):
    """Hermes pickup time slots."""

    FORENOON = "FORENOON"
    NOON = "NOON"
    AFTERNOON = "AFTERNOON"
    EVENING = "EVENING"
