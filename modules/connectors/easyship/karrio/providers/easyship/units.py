import typing
import pathlib
import karrio.lib as lib
import karrio.core.units as units

METADATA_JSON = lib.load_json(pathlib.Path(__file__).resolve().parent / "metadata.json")
EASYSHIP_CARRIER_METADATA = [_ for sublist in METADATA_JSON for _ in sublist]
KARRIO_CARRIER_MAPPING = {
    "canada_post": "canadapost",
    "dhl": "dhl_express",
}


class LabelFormat(lib.StrEnum):
    """Carrier specific label format"""

    pdf = "pdf"
    png = "png"
    zpl = "zpl"
    url = "url"

    PDF = pdf
    PNG = png
    ZPL = zpl


class Incoterms(lib.StrEnum):
    """Carrier specific incoterms"""

    DDU = "DDU"
    DDP = "DDP"


class DimensionUnit(lib.StrEnum):
    """Carrier specific dimension unit"""

    CM = "cm"
    IN = "in"


class WeightUnit(lib.StrEnum):
    """Carrier specific weight unit"""

    LB = "lb"
    KG = "kg"


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


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    # fmt: off
    easyship_box_slug = lib.OptionEnum("box_slug")
    easyship_courier_id = lib.OptionEnum("courier_id")
    easyship_eei_reference = lib.OptionEnum("eei_reference")
    easyship_incoterms = lib.OptionEnum("incoterms", Incoterms)
    easyship_apply_shipping_rules = lib.OptionEnum("apply_shipping_rules", bool)
    easyship_show_courier_logo_url = lib.OptionEnum("show_courier_logo_url", bool)
    easyship_allow_courier_fallback = lib.OptionEnum("allow_courier_fallback", bool)
    easyship_list_unavailable_couriers = lib.OptionEnum("list_unavailable_couriers", bool)
    easyship_buyer_notes = lib.OptionEnum("buyer_notes")
    easyship_seller_notes = lib.OptionEnum("seller_notes")
    easyship_sender_address_id = lib.OptionEnum("sender_address_id")
    easyship_return_address_id = lib.OptionEnum("return_address_id")
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
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class TrackingStatus(lib.Enum):
    on_hold = ["on_hold"]
    delivered = ["delivered"]
    in_transit = ["in_transit"]
    delivery_failed = ["delivery_failed"]
    delivery_delayed = ["delivery_delayed"]
    out_for_delivery = ["out_for_delivery"]
    ready_for_pickup = ["ready_for_pickup"]


def to_service_code(service: typing.Dict[str, str]) -> str:
    return lib.to_slug(
        f'easyship_{to_carrier_code(service)}_{lib.to_snake_case(service["service_name"])}'
    )


def to_carrier_code(service: typing.Dict[str, str]) -> str:
    code = lib.to_slug(service["umbrella_name"])
    return KARRIO_CARRIER_MAPPING.get(code, code)


def find_courier(search: str):
    courier: dict = next(
        (
            item
            for item in EASYSHIP_CARRIER_METADATA
            if item["name"] == search
            or item["id"] == search
            or item["umbrella_name"] == search
            or to_service_code(item) == search
            or to_carrier_code(item) == search
        ),
        {},
    )
    if courier:
        return ShippingCourierID.map(to_carrier_code(courier))

    return ShippingCourierID.map(search)


ShippingService = lib.StrEnum(
    "ShippingService",
    {
        to_service_code(service): service["service_name"]
        for service in EASYSHIP_CARRIER_METADATA
    },
)

ShippingServiceID = lib.StrEnum(
    "ShippingServiceID",
    {service["id"]: to_service_code(service) for service in EASYSHIP_CARRIER_METADATA},
)

ShippingCourierID = lib.StrEnum(
    "ShippingCourierID",
    {
        to_carrier_code(courier): courier["name"]
        for courier in {
            _["umbrella_name"]: _ for _ in EASYSHIP_CARRIER_METADATA
        }.values()
    },
)

setattr(ShippingCourierID, "find", find_courier)
