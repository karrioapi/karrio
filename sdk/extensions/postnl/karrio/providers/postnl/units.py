import karrio.lib as lib
import karrio.core.units as units


class PackagingType(lib.Flag):
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


class ConnectionConfig(lib.Enum):
    language = lib.OptionEnum("language")
    cost_center = lib.OptionEnum("cost_center")
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)


class ShippingService(lib.Enum):
    """Carrier specific services"""

    postnl_standard_service = "Post NL Standard Service"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    # postnl_option = lib.OptionEnum("code")

    """ Unified Option type mapping """
    # insurance = postnl_coverage  #  maps unified karrio option to carrier specific

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
    on_hold = ["9"]
    delivered = ["11"]
    in_transit = ["1"]
    delivery_failed = ["15", "18", "19"]
    delivery_delayed = ["16", "8", "17"]
    out_for_delivery = ["7"]
    ready_for_pickup = ["12"]
