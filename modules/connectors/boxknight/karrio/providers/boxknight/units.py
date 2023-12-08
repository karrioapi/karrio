import karrio.lib as lib
import karrio.core.units as units


class DimensionUnit(lib.StrEnum):
    CM = "cm"
    IN = "inch"


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

    boxknight_sameday = "SAMEDAY"
    boxknight_nextday = "NEXTDAY"
    boxknight_scheduled = "SCHEDULED"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    boxknight_signature_required = lib.OptionEnum("signatureRequired", bool)
    boxknight_merchant_display_name = lib.OptionEnum("merchantDisplayName")
    boxknight_notes = lib.OptionEnum("notes")

    signature_required = boxknight_signature_required


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
    on_hold = ["CREATED", "GEOCODED"]
    delivered = ["DELIVERY_COMPLETED"]
    in_transit = ["DELIVERY_ASSIGNED", "PICKUP_EN_ROUTE"]
    delivery_delayed = ["delivery_delayed"]
    out_for_delivery = ["PICKUP_COMPLETED", "DELIVERY_EN_ROUTE"]
