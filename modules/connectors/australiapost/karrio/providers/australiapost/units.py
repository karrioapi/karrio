import karrio.lib as lib
import karrio.core.units as units


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type"""

    carton = "CTN"
    pallet = "PAL"
    satchel = "SAT"
    bag = "BAG"
    envelope = "ENV"
    item = "ITM"
    jiffy_bag = "JIF"
    skid = "SKI"

    """ Unified Packaging type mapping """
    pak = satchel
    tube = item
    pallet = pallet
    small_box = carton
    medium_box = carton
    your_packaging = carton


class CustomsContentType(lib.StrEnum):
    """Carrier specific customs content type"""

    document = "DOCUMENT"
    gift = "GIFT"
    sample = "SAMPLE"
    other = "OTHER"
    return_of_goods = "RETURN"
    sale_of_goods = "SALE_OF_GOODS"

    """ Unified Content type mapping """
    documents = document
    merchandise = sale_of_goods
    return_merchandise = return_of_goods


class ShippingService(lib.StrEnum):
    """Carrier specific services"""

    australiapost_express_post = "E34"
    australiapost_express_post_signature = "E34S"
    australiapost_parcel_post_signature = "T28S"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    # fmt: off
    australiapost_delivery_date = lib.OptionEnum("DELIVERY_DATE")
    australiapost_delivery_times = lib.OptionEnum("DELIVERY_TIMES")
    australiapost_pickup_date = lib.OptionEnum("PICKUP_DATE")
    australiapost_pickup_time = lib.OptionEnum("PICKUP_TIME")
    australiapost_commercial_clearance = lib.OptionEnum("COMMERCIAL_CLEARANCE")
    australiapost_identity_on_delivery = lib.OptionEnum("IDENTITY_ON_DELIVERY")
    australiapost_print_at_depot = lib.OptionEnum("PRINT_AT_DEPOT")
    australiapost_transit_warranty = lib.OptionEnum("TRANSIT_WARRANTY")
    australiapost_transit_cover = lib.OptionEnum("TRANSIT_COVER", float)

    australiapost_authority_to_leave = lib.OptionEnum("authority_to_leave", bool)
    australiapost_allow_partial_delivery = lib.OptionEnum("allow_partial_delivery", bool)
    australiapost_contains_dangerous_goods = lib.OptionEnum("contains_dangerous_goods", bool)

    """ Unified Option type mapping """

    insurance = australiapost_transit_cover
    # fmt: on


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
        return key in ShippingOption and key not in [  # type: ignore
            "australiapost_authority_to_leave",
            "australiapost_allow_partial_delivery",
            "australiapost_contains_dangerous_goods",
        ]

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class TrackingStatus(lib.Enum):
    on_hold = ["Possible delay", "Held by courier"]
    delivered = ["Delivered", "Delivered in Full"]
    in_transit = ["In transit"]
    delivery_failed = [
        "Article damaged",
        "Cancelled",
        "Cannot be delivered",
        "Unsuccessful Delivery",
    ]
    delivery_delayed = ["Possible delay", "To be Re-Delivered"]
    out_for_delivery = ["On Board for Delivery"]
    ready_for_pickup = ["Awaiting collection", "Ready for Pickup"]
