
import karrio.lib as lib
import karrio.core.units as units


class ConnectionConfig(lib.Enum):
    """Carrier connection configuration options."""

    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    label_type = lib.OptionEnum("label_type", str, "PDF")
    label_format = lib.OptionEnum("label_format", str, "PDF")


class LabelFormat(lib.StrEnum):
    """DPD label format options."""
    PDF = "PDF"
    EPL = "EPL"
    ZPL = "ZPL"
    TIFF = "TIFF"
    PNG = "PNG"


class LabelPaperFormat(lib.StrEnum):
    """DPD label paper size options."""
    A4 = "A4"
    A5 = "A5"
    A6 = "A6"
    A7 = "A7"


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type"""
    PACKAGE = "PACKAGE"

    """Unified Packaging type mapping"""
    envelope = PACKAGE
    pak = PACKAGE
    tube = PACKAGE
    pallet = PACKAGE
    small_box = PACKAGE
    medium_box = PACKAGE
    your_packaging = PACKAGE


class ShippingService(lib.StrEnum):
    """DPD META-API product codes"""
    dpd_group_classic = "101"
    dpd_group_express_10 = "E10"
    dpd_group_express_12 = "E12"
    dpd_group_express_18 = "E18"
    dpd_group_parcel_shop = "PS"


class ShippingOption(lib.Enum):
    """Carrier specific options"""
    dpd_group_saturday_delivery = lib.OptionEnum("saturday_delivery", bool)
    dpd_group_label_format = lib.OptionEnum("label_format", str)
    dpd_group_label_paper_format = lib.OptionEnum("label_paper_format", str)
    dpd_group_dropoff_type = lib.OptionEnum("dropoff_type", str)
    dpd_group_simulate = lib.OptionEnum("simulate", bool)

    """Unified Option type mapping"""
    saturday_delivery = dpd_group_saturday_delivery


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
    on_hold = ["on_hold"]
    delivered = ["delivered"]
    in_transit = ["in_transit"]
    delivery_failed = ["delivery_failed"]
    delivery_delayed = ["delivery_delayed"]
    out_for_delivery = ["out_for_delivery"]
    ready_for_pickup = ["ready_for_pickup"]
