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


class ShippingService(lib.StrEnum):
    """Carrier specific services"""

    allied_road_service = "R"
    allied_parcel_service = "P"
    allied_standard_pallet_service = "PT"
    allied_oversized_pallet_service = "PT2"


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


class TrackingStatus(lib.Enum):
    on_hold = ["Other", "DAMAGED"]
    delivered = ["Freight has been delivered"]
    in_transit = ["IN TRANSIT TO"]
    delivery_failed = ["RETURN TO SENDER"]
    delivery_delayed = ["RETURN TO DEPOT", "CARD LEFT", "LEFT IN DEPOT"]
    out_for_delivery = ["It's on board with driver"]
    ready_for_pickup = ["IN AGENT"]
