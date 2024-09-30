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
                to_carrier_code(service.get("carrierDTO")),
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


def get_service(search: str, test_mode: bool = False, service_id: str = None) -> str:
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


def get_service_id(search: str, test_mode: bool = False, service_id: str = None) -> str:
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
) -> str:
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
) -> str:
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
) -> str:

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


CARRIER_IDS = {
    "5000001": "aramex",
    "5000002": "canadapost",
    "5000003": "canpar",
    "5000017": "day_ross",
    "5000004": "dhl_express",
    "5000011": "eshipper",
    "5000005": "fedex",
    "8000010": "flashbird",
    "56": "fleet_optics",
    "5000008": "project44",
    "5000007": "purolator",
    "5000047": "pyk",
    "5000014": "sameday",
    "5000048": "skip",
    "5000015": "smartepost_intl",
    "5000010": "ups",
    "5000013": "usps",
}

CARRIER_SERVICES = {
    "56": ["5000458", "5000458", "5000458", "5000458"],
    "5000001": [
        "5000047",
        "5000047",
        "5000046",
        "5000046",
        "5000048",
        "5000048",
        "5000049",
        "5000049",
    ],
    "5000002": [
        "5000181",
        "5000181",
        "5000181",
        "5000028",
        "5000028",
        "5000028",
        "5000029",
        "5000029",
        "5000029",
        "5000025",
        "5000025",
        "5000025",
        "5000031",
        "5000031",
        "5000031",
        "5000035",
        "5000035",
        "5000035",
        "5000034",
        "5000034",
        "5000034",
        "5000033",
        "5000033",
        "5000033",
        "5000027",
        "5000027",
        "5000027",
        "5000024",
        "5000024",
        "5000024",
        "5000032",
        "5000032",
        "5000032",
        "5000026",
        "5000026",
        "5000026",
        "5000030",
        "5000030",
        "5000030",
    ],
    "5000003": [
        "5000134",
        "5000134",
        "5000134",
        "5000133",
        "5000133",
        "5000133",
        "5000132",
        "5000132",
        "5000132",
        "5000125",
        "5000125",
        "5000125",
        "5000128",
        "5000128",
        "5000128",
        "5000127",
        "5000127",
        "5000127",
        "5000126",
        "5000126",
        "5000126",
        "5000135",
        "5000135",
        "5000135",
        "5000184",
        "5000184",
        "5000184",
        "5000131",
        "5000131",
        "5000131",
        "5000130",
        "5000130",
        "5000130",
        "5000129",
        "5000129",
        "5000129",
    ],
    "5000004": [
        "5000020",
        "5000020",
        "5000021",
        "5000021",
        "5000019",
        "5000019",
        "5000015",
        "5000015",
        "5000023",
        "5000023",
        "5000014",
        "5000014",
        "5000180",
        "5000180",
        "5000017",
        "5000017",
        "5000016",
        "5000016",
        "5000018",
        "5000018",
        "5000186",
        "5000186",
        "5000022",
        "5000022",
    ],
    "5000005": [
        "5000172",
        "5000172",
        "5000172",
        "5000169",
        "5000169",
        "5000169",
        "5000175",
        "5000175",
        "5000175",
        "8000023",
        "8000023",
        "8000023",
        "8000022",
        "8000022",
        "8000022",
        "5000176",
        "5000176",
        "5000176",
        "5000179",
        "5000179",
        "5000179",
        "8000018",
        "8000018",
        "8000018",
        "8000017",
        "8000017",
        "8000017",
        "5000183",
        "5000183",
        "5000183",
        "5000171",
        "5000171",
        "5000171",
        "5000170",
        "5000170",
        "5000170",
        "5000174",
        "5000174",
        "5000174",
        "5000173",
        "5000173",
        "5000173",
        "5000178",
        "5000178",
        "5000178",
        "5000177",
        "5000177",
        "5000177",
    ],
    "5000007": [
        "5000008",
        "5000008",
        "5000008",
        "5000009",
        "5000009",
        "5000009",
        "5000007",
        "5000007",
        "5000007",
        "5000005",
        "5000005",
        "5000005",
        "5000006",
        "5000006",
        "5000006",
        "5000004",
        "5000004",
        "5000004",
        "5000012",
        "5000012",
        "5000012",
        "5000013",
        "5000013",
        "5000013",
        "5000010",
        "5000010",
        "5000010",
        "5000011",
        "5000011",
        "5000011",
        "5000002",
        "5000002",
        "5000002",
        "5000003",
        "5000003",
        "5000003",
        "5000001",
        "5000001",
        "5000001",
    ],
    "5000008": [
        "5000056",
        "5000053",
        "5000413",
        "5000109",
        "5000110",
        "5000088",
        "5000065",
        "5000089",
        "5000080",
        "5000055",
        "5000073",
        "5000098",
        "5000097",
        "5000093",
        "5000084",
        "5000082",
        "5000067",
        "5000068",
        "5000052",
        "5000058",
        "5000100",
        "5000094",
        "5000071",
        "5000054",
        "5000063",
        "5000064",
        "5000090",
        "5000087",
        "5000075",
        "5000104",
        "5000074",
        "5000069",
        "5000051",
        "5000096",
        "5000062",
        "5000060",
        "5000106",
        "5000108",
        "5000107",
        "5000059",
        "5000070",
        "5000105",
        "5000077",
        "5000061",
        "5000076",
        "5000078",
        "5000091",
        "5000072",
        "5000101",
        "5000099",
        "5000083",
        "5000057",
        "5000095",
        "5000086",
        "5000085",
        "5000066",
        "5000102",
        "5000079",
        "5000111",
        "5000092",
        "5000081",
        "5000103",
    ],
    "5000010": [
        "5000044",
        "5000044",
        "5000044",
        "5000037",
        "5000037",
        "5000037",
        "5000038",
        "5000038",
        "5000038",
        "5000042",
        "5000042",
        "5000042",
        "5000041",
        "5000041",
        "5000041",
        "5000039",
        "5000039",
        "5000039",
        "5000045",
        "5000045",
        "5000045",
        "5000043",
        "5000043",
        "5000043",
        "5000040",
        "5000040",
        "5000040",
        "5000036",
        "5000036",
        "5000036",
        "5000182",
        "5000182",
        "5000182",
    ],
    "5000011": [
        "5000115",
        "5000113",
        "5000112",
        "5000119",
        "5000114",
        "5000116",
        "5000123",
        "5000117",
        "5000122",
        "5000421",
        "5000419",
        "5000121",
        "5000420",
        "5000118",
        "5000124",
        "5000120",
        "5000414",
    ],
    "5000013": [
        "5000153",
        "5000153",
        "8000003",
        "5000152",
        "5000152",
        "5000151",
        "5000151",
        "5000150",
        "5000150",
        "5000155",
        "5000155",
        "5000154",
        "5000154",
        "5000149",
        "5000149",
        "5000148",
        "5000148",
        "5000147",
        "5000147",
        "8000002",
        "5000146",
    ],
    "5000014": [
        "5000168",
        "5000167",
        "5000166",
        "5000165",
        "5000164",
        "5000163",
        "5000162",
        "5000161",
        "5000160",
        "5000159",
        "5000158",
        "5000157",
        "5000156",
    ],
    "5000015": [
        "5000145",
        "5000145",
        "5000145",
        "5000144",
        "5000144",
        "5000144",
        "5000143",
        "5000143",
        "5000143",
        "5000142",
        "5000142",
        "5000142",
        "5000141",
        "5000141",
        "5000141",
        "5000140",
        "5000140",
        "5000140",
        "5000139",
        "5000139",
        "5000139",
        "5000138",
        "5000138",
        "5000138",
        "5000137",
        "5000137",
        "5000137",
        "8000053",
    ],
    "5000016": ["5000454"],
    "5000017": ["5000457"],
    "5000047": ["5000460", "5000460", "5000459", "5000459"],
    "5000048": ["8000020", "8000019"],
    "8000010": ["8000032"],
}


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
