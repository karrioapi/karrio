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

    roadie_local_delivery = "Roadie Local Delivery"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    pickup_after = lib.OptionEnum("pickup_after")
    deliver_start = lib.OptionEnum("delivery_start")
    deliver_end = lib.OptionEnum("delivery_end")
    roadie_signature_required = lib.OptionEnum("signature_required", bool)
    roadie_notifications_enabled = lib.OptionEnum("notifications_enabled", bool)
    roadie_over_21_required = lib.OptionEnum("over_21_required", bool)
    roadie_extra_compensation = lib.OptionEnum("extra_compensation", float)
    roadie_trailer_required = lib.OptionEnum("trailer_required", bool)
    roadie_decline_insurance = lib.OptionEnum("decline_insurance", bool)

    """ Unified Option type mapping """
    signature_required = roadie_signature_required
    email_notification = roadie_notifications_enabled


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
    delivered = ["delivery_confirmed"]
    in_transit = ["at_pickup", "pickup_confirmed"]
    out_for_delivery = [
        "en_route_to_delivery",
        "at_delivery",
        "driver_approaching_delivery",
    ]
    delivery_failed = ["delivery_attempted", "returned", "canceled"]
