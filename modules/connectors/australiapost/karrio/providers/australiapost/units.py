import karrio.lib as lib
import karrio.core.units as units


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type"""

    box = "BOX"
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
    small_box = box
    medium_box = box
    your_packaging = box


class LabelType(lib.Enum):
    PDF_A4_1pp = ("PDF", "A4-1pp")
    ZPL_A4_1pp = ("ZPL", "A4-1pp")
    PDF_A4_3pp = ("PDF", "A4-3pp")
    ZPL_A4_3pp = ("ZPL", "A4-3pp")
    PDF_A4_4pp = ("PDF", "A4-4pp")
    ZPL_A4_4pp = ("ZPL", "A4-4pp")
    PDF_A6_1pp = ("PDF", "A6-1pp")
    ZPL_A6_1pp = ("ZPL", "A6-1pp")
    PDF_A4_2pp = ("PDF", "A4-2pp")
    ZPL_A4_2pp = ("ZPL", "A4-2pp")
    PDF_A4_1pp_landscape = ("PDF", "A4-1pp landscape")
    ZPL_A4_1pp_landscape = ("ZPL", "A4-1pp landscape")
    PDF_A4_2pp_landscape = ("PDF", "A4-2pp landscape")
    ZPL_A4_2pp_landscape = ("ZPL", "A4-2pp landscape")

    """ Unified Label type mapping """
    PDF = PDF_A4_1pp
    ZPL = PDF_A4_1pp
    PNG = PDF_A4_1pp


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


class ServiceLabelGroup(lib.StrEnum):
    """Carrier specific services"""

    australiapost_parcel_post = "Parcel Post"
    australiapost_express_post = "Express Post"
    australiapost_startrack_courier = "Startrack Courier"
    australiapost_startrack = "StarTrack"
    australiapost_on_demand = "On Demand"
    australiapost_international = "International"
    australiapost_commercial = "Commercial"


class ShippingService(lib.StrEnum):
    """Carrier specific services"""

    australiapost_parcel_post = "T28"
    australiapost_express_post = "E34"
    australiapost_parcel_post_signature = "3D55"
    australiapost_express_post_signature = "3J55"
    australiapost_intl_standard_pack_track = "PTI8"
    australiapost_intl_standard_with_signature = "PTI7"
    australiapost_intl_express_merch = "ECM8"
    australiapost_intl_express_docs = "ECD8"
    australiapost_eparcel_post_returns = "PR"
    australiapost_express_eparcel_post_returns = "XPR"

    # australiapost_parcel_post = "PARCEL POST"
    # australiapost_express_post = "EXPRESS POST"
    # australiapost_parcel_post_signature = "PARCEL POST + SIGNATURE"
    # australiapost_express_post_signature = "EXPRESS POST + SIGNATURE"
    # australiapost_intl_standard_pack_track = "INTL STANDARD/PACK & TRACK"
    # australiapost_intl_standard_with_signature = "INT'L STANDARD WITH SIGNATURE"
    # australiapost_intl_express_merch = "INTL EXPRESS MERCH"
    # australiapost_intl_express_docs = "INTL EXPRESS DOCS"
    # australiapost_eparcel_post_returns = "EPARCEL POST RETURNS"
    # australiapost_express_eparcel_post_returns = "EXPRESS EPARCEL POST RETURNS"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    # fmt: off
    australiapost_delivery_date = lib.OptionEnum("DELIVERY_DATE")
    australiapost_delivery_time_start = lib.OptionEnum("DELIVERY_TIMES")
    australiapost_delivery_time_end = lib.OptionEnum("DELIVERY_TIMES")
    australiapost_pickup_date = lib.OptionEnum("PICKUP_DATE")
    australiapost_pickup_time = lib.OptionEnum("PICKUP_TIME")
    australiapost_identity_on_delivery = lib.OptionEnum("IDENTITY_ON_DELIVERY")
    australiapost_print_at_depot = lib.OptionEnum("PRINT_AT_DEPOT", bool)
    australiapost_transit_cover = lib.OptionEnum("TRANSIT_COVER", float)
    australiapost_sameday_identity_on_delivery = lib.OptionEnum("SAMEDAY_IDENTITY_ON_DELIVERY")

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
