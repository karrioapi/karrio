import karrio.lib as lib
import karrio.core.units as units

MeasurementOptions = lib.units.MeasurementOptionsType(
    quant=0.1,
    min_volume=0.1,
)


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


class ConnectionConfig(lib.Enum):
    app_name = lib.OptionEnum("app_name")
    server_url = lib.OptionEnum("server_url")
    text_color = lib.OptionEnum("text_color")
    brand_color = lib.OptionEnum("brand_color")
    freight_mode = lib.OptionEnum("freight_mode")


class ShippingService(lib.StrEnum):
    """Carrier specific services"""

    allied_road_service = "R"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    instructions = lib.OptionEnum("instructions")
    dangerous_good = lib.OptionEnum("dangerous_good", bool)


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
