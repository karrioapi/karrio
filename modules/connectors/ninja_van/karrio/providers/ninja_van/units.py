
import karrio.lib as lib
import karrio.core.units as units


class PackagingType(lib.StrEnum):
    """ Carrier specific packaging type """
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
    """ Carrier specific services """
    ninja_van_standard_service = "Ninja Van Standard Service"


class ShippingOption(lib.Enum):
    """ Carrier specific options """
    # ninja_van_option = lib.OptionEnum("code")

    """ Unified Option type mapping """
    # insurance = ninja_van_coverage  #  maps unified karrio option to carrier specific

    pass


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
    on_hold = ["Pending Pickup","Delivery Attempted"]
    delivered = ["Delivered", "Delivered, Received by Customer", ]
    in_transit = ["Pickup", "Drop Off", "Dropped Off", "In Transit", "Arrived at Origin Hub"]
    delivery_failed = ["Unable to Deliver"]
    delivery_delayed = ["delivery_delayed"]
    out_for_delivery = ["Out for Delivery"]
    ready_for_pickup = ["ready_for_pickup"]
