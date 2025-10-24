import karrio.lib as lib
import karrio.core.units as units


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

    sendle_standard_pickup = "STANDARD-PICKUP"
    sendle_standard_dropoff = "STANDARD-DROPOFF"
    sendle_express_pickup = "EXPRESS-PICKUP"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    sendle_hide_pickup_address = lib.OptionEnum("hide_pickup_address", bool)
    sendle_first_mile_option = lib.OptionEnum("first_mile_option", bool)


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
    on_hold = ["Pickup Attempted", "Delivery Attempted"]
    delivered = ["Delivered"]
    in_transit = ["Pickup", "Drop Off", "Dropped Off", "In Transit"]
    delivery_failed = ["Damaged", "Unable to Deliver"]
    delivery_delayed = ["Card Left"]
    out_for_delivery = ["Out for Delivery", "Local Delivery"]
    ready_for_pickup = ["Left with Agent"]
