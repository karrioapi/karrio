import typing
import pathlib
import karrio.lib as lib
import karrio.core.units as units

METADATA_JSON = lib.to_dict(
    lib.load_file_content(
        pathlib.Path(__file__).resolve().parent / "metadata.json"
    ).replace('"NULL"', "null")
)
KARRIO_CARRIER_MAPPING = {
    "fed_ex": "fedex",
    "e_shipper": "eshipper",
    "tforce_freight": "tforce",
    "federal_express": "fedex",
    "canada_post": "canadapost",
    "e_shipper_ltl": "eshipper",
    "fedex_freight_ltl": "fedex",
    "e_shipper_trucking": "eshipper",
}


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type"""

    Drum = "Drum"
    Boxes = "Boxes"
    Rolls = "Rolls"
    Pipes = "Pipes"
    Bales = "Bales"
    Bags = "Bags"
    Pallet = "Pallet"
    Cylinder = "Cylinder"
    Pails = "Pails"
    Reels = "Reels"
    Crate = "Crate"
    Bucket = "Bucket"
    Bundle = "Bundle"
    Can = "Can"
    Carton = "Carton"
    Case = "Case"
    Coil = "Coil"
    Pieces = "Pieces"
    Skid = "Skid"

    """ Unified Packaging type mapping """
    tube = Cylinder
    pallet = Pallet
    small_box = Boxes
    medium_box = Boxes


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    eshipper_signature_required = lib.OptionEnum("signatureRequired", bool)
    eshipper_insurance_type = lib.OptionEnum("insuranceType")
    eshipper_dangerous_goods_type = lib.OptionEnum("dangerousGoodsType", bool)
    eshipper_cod = lib.OptionEnum("cod", float)
    eshipper_is_saturday_service = lib.OptionEnum("isSaturdayService", bool)
    eshipper_hold_for_pickup_required = lib.OptionEnum("holdForPickupRequired", bool)
    eshipper_special_equipment = lib.OptionEnum("specialEquipment", bool)
    eshipper_inside_delivery = lib.OptionEnum("insideDelivery", bool)
    eshipper_delivery_appointment = lib.OptionEnum("deliveryAppointment", bool)
    eshipper_inside_pickup = lib.OptionEnum("insidePickup", bool)
    eshipper_saturday_pickup_required = lib.OptionEnum("saturdayPickupRequired", bool)
    eshipper_stackable = lib.OptionEnum("stackable", bool)

    """ Unified Option type mapping """
    cash_on_delivery = eshipper_cod
    insurance = eshipper_insurance_type
    signature_confirmation = eshipper_signature_required
    saturday_delivery = eshipper_is_saturday_service
    hold_at_location = eshipper_hold_for_pickup_required
    dangerous_good = eshipper_dangerous_goods_type


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


def to_carrier_code(carrierDTO: typing.Dict[str, str]) -> str:
    _code = lib.to_snake_case((carrierDTO or {}).get("name") or "eshipper")

    # map carrier names to their corresponding Karrio code
    return KARRIO_CARRIER_MAPPING.get(_code, _code)


def to_service_code(service: typing.Dict[str, str]) -> str:
    parts = list(
        dict.fromkeys(
            [
                to_carrier_code(service.get("carrierDTO")),  # type: ignore
                *[
                    _.lower()
                    for _ in (
                        service.get("esServicename") or service.get("name")
                    ).split(" ")
                ],
            ][::-1]
        )
    )[::-1]
    output = (
        lib.to_slug(" ".join(["eshipper", *parts]))
        .replace("_eshipper", "")
        .replace("__", "_")
    )

    return output


def get_service(search: str, test_mode: bool = False, service_id: str = None):
    prod_metadata = METADATA_JSON["PROD_SERVICES"]
    test_metadata = METADATA_JSON["DEV_SERVICES"]
    metadata = lib.identity(
        test_metadata + prod_metadata if test_mode else prod_metadata + test_metadata
    )

    return next(
        (
            service
            for service in metadata
            if to_service_code(service) == search
            or service.get("name") == search
            or str(service.get("id")) == search
            or (service_id and service_id == str(service.get("id")))
        ),
        {},
    )


def get_service_id(search: str, test_mode: bool = False, service_id: str = None):
    return (
        get_service(search, test_mode=test_mode, service_id=service_id).get("id")
        or service_id
    )


def find_service(search: str, test_mode: bool = False, service_id: str = None):

    if ShippingService.map(search).name:
        return ShippingService.map(search)

    service = get_service(search, test_mode=test_mode, service_id=service_id)

    if service:
        return ShippingService.map(to_service_code(service))

    return ShippingService.map(search)


def get_carrier(
    search: str,
    test_mode: bool = False,
    service_search: str = None,
    service_id: str = None,
):
    id_key = "test_id" if test_mode else "prod_id"
    alternate_key = "prod_id" if not test_mode else "test_id"
    service = get_service(service_search, test_mode=test_mode, service_id=service_id)

    return service.get("carrierDTO") or next(
        (
            carrier
            for carrier in ESHIPPER_CARRIER_METADATA.values()
            if search == carrier.get(id_key) or search == carrier.get("name")
        ),
        next(
            (
                carrier
                for carrier in ESHIPPER_CARRIER_METADATA.values()
                if search == carrier.get(alternate_key) or search == carrier.get("name")
            ),
            {},
        ),
    )


def get_carrier_id(
    search: str,
    test_mode: bool = False,
    service_search: str = None,
    service_id: str = None,
):
    return get_carrier(
        search,
        test_mode=test_mode,
        service_search=service_search,
        service_id=service_id,
    ).get("id")


def find_rate_provider(
    search: str,
    test_mode: bool = False,
    service_search: str = None,
    service_id: str = None,
):

    if RateProvider.map(lib.to_snake_case(search)).name:
        return RateProvider.map(lib.to_snake_case(search))

    carrier = get_carrier(
        search,
        test_mode=test_mode,
        service_search=service_search,
        service_id=service_id,
    )

    if carrier and RateProvider.map(to_carrier_code(carrier)).name:
        return RateProvider.map(to_carrier_code(carrier))

    return RateProvider.map(lib.to_snake_case(search))


ESHIPPER_CARRIER_METADATA = {
    lib.to_snake_case(carrier["carrierDTO"]["name"]): {
        **carrier["carrierDTO"],
        "ids": list(
            set(
                [
                    s["carrierDTO"]["id"]
                    for s in METADATA_JSON["PROD_SERVICES"]
                    + METADATA_JSON["DEV_SERVICES"]
                    if s["carrierDTO"]["name"] == carrier["carrierDTO"]["name"]
                ]
            )
        ),
        "prod_id": next(
            (
                s["carrierDTO"]["id"]
                for s in METADATA_JSON["PROD_SERVICES"]
                if s["carrierDTO"]["name"] == carrier["carrierDTO"]["name"]
            ),
            None,
        ),
        "test_id": next(
            (
                s["carrierDTO"]["id"]
                for s in METADATA_JSON["DEV_SERVICES"]
                if s["carrierDTO"]["name"] == carrier["carrierDTO"]["name"]
            ),
            None,
        ),
    }
    for carrier in {
        s["carrierDTO"]["name"]: s
        for s in METADATA_JSON["PROD_SERVICES"] + METADATA_JSON["DEV_SERVICES"]
    }.values()
}

ESHIPPER_SERVICE_METADATA = {
    lib.to_snake_case(service.get("esServicename") or service.get("name")): {
        **service,
        "ids": list(
            set(
                [
                    s["id"]
                    for s in METADATA_JSON["PROD_SERVICES"]
                    + METADATA_JSON["DEV_SERVICES"]
                    if lib.to_snake_case(s["name"])
                    == lib.to_snake_case(service["name"])
                ]
            )
        ),
        "prod_id": next(
            (
                s["id"]
                for s in METADATA_JSON["PROD_SERVICES"]
                if s["name"] == service["name"]
            ),
            None,
        ),
        "test_id": next(
            (
                s["id"]
                for s in METADATA_JSON["DEV_SERVICES"]
                if s["name"] == service["name"]
            ),
            None,
        ),
        "carrier": lib.to_snake_case(service["carrierDTO"]["name"]),
    }
    for service in {
        s["name"]: s
        for s in METADATA_JSON["PROD_SERVICES"] + METADATA_JSON["DEV_SERVICES"]
    }.values()
}


ShippingService = lib.StrEnum(
    "ShippingService",
    {
        to_service_code(service): service["name"]
        for service in ESHIPPER_SERVICE_METADATA.values()
    },
)

RateProvider = lib.StrEnum(
    "RateProvider",
    {
        to_carrier_code(carrier): slug
        for slug, carrier in ESHIPPER_CARRIER_METADATA.items()
    },
)


setattr(ShippingService, "service_id", get_service_id)
setattr(ShippingService, "carrier_id", get_carrier_id)
setattr(ShippingService, "find", find_service)
setattr(RateProvider, "find", find_rate_provider)
