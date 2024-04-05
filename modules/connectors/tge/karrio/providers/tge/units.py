import karrio.lib as lib
import karrio.core.units as units

MeasurementOptions = lib.units.MeasurementOptionsType(
    quant=0.1,
    min_volume=0.1,
)


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type"""

    BAG = "BG"

    """ Unified Packaging type mapping """
    envelope = BAG
    pak = BAG
    tube = BAG
    pallet = BAG
    small_box = BAG
    medium_box = BAG
    your_packaging = BAG


class ConnectionConfig(lib.Enum):
    channel = lib.OptionEnum("channel")
    server_url = lib.OptionEnum("server_url")
    text_color = lib.OptionEnum("text_color")
    brand_color = lib.OptionEnum("brand_color")
    business_id = lib.OptionEnum("business_id")
    freight_mode = lib.OptionEnum("freight_mode")
    message_sender = lib.OptionEnum("message_sender")

    SYSID = lib.OptionEnum("SYSID")

    SHIP_GS1 = lib.OptionEnum("SHIP_GS1")
    SHIP_range_end = lib.OptionEnum("SHIP_range_end", lib.to_int)
    SHIP_range_start = lib.OptionEnum("SHIP_range_start", lib.to_int)

    SSCC_GS1 = lib.OptionEnum("SSCC_GS1")
    SSCC_range_end = lib.OptionEnum("SSCC_range_end", lib.to_int)
    SSCC_range_start = lib.OptionEnum("SSCC_range_start", lib.to_int)


class ShippingService(lib.StrEnum):
    """Carrier specific services"""

    tge_freight_service = "X"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    tge_ssc_ids = lib.OptionEnum("tge_ssc_ids", list)
    tge_shipment_ids = lib.OptionEnum("tge_shipment_ids", list)
    tge_freight_mode = lib.OptionEnum("tge_freight_mode")
    tge_despatch_date = lib.OptionEnum("tge_despatch_date")
    tge_special_instruction = lib.OptionEnum("tge_special_instruction")
    tge_required_delivery_date = lib.OptionEnum("tge_required_delivery_date")

    instructions = tge_special_instruction


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """
    Apply default values to the given options.
    """
    _options = options.copy()

    if package_options is not None:
        _options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(_options, ShippingOption, items_filter=items_filter)
