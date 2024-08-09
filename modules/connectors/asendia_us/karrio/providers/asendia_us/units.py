import karrio.lib as lib
import karrio.core.units as units


class WeightUnit(lib.Enum):
    KG = "Kg"
    LB = "Lb"


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

    asendia_us_e_com_tracked_ddp = "19"
    asendia_us_fully_tracked = "65"
    asendia_us_country_tracked = "66"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    asendia_us_processing_location = lib.OptionEnum("asendia_us_processing_location")


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
    on_hold = ["Hold"]
    delivered = ["Delivered"]
    in_transit = ["Transit"]
    delivery_failed = ["Failed"]
    out_for_delivery = ["Out"]
