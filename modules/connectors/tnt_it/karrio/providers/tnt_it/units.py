import karrio.lib as lib
import karrio.core.units as units


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type"""

    colli = "C"
    buste = "S"
    bauletti_piccoli = "B"
    bauletti_grandi = "D"

    """ Unified Packaging type mapping """
    envelope = buste
    pak = buste
    tube = colli
    small_box = bauletti_piccoli
    medium_box = bauletti_grandi
    pallet = bauletti_grandi
    your_packaging = colli


class PaymentType(lib.StrEnum):
    """Carrier specific payment type"""

    sender = "S"
    receiver = "R"
    third_party = "R"


class ShippingServiceCode(lib.Enum):
    """Carrier specific services"""

    tnt_express_doc = ("DOC", "D", "N")
    tnt_express_air_scs_nondoc = ("NONDOC", "D", "A")
    tnt_express_air_scs_doc = ("DOC", "D", "A")
    tnt_economy_express_road_scs_nondoc = ("NONDOC", "D", "N")
    tnt_economy_express_road_scs_doc = tnt_express_doc
    tnt_express_nondoc = ("NONDOC", "G", "15N")
    tnt_9_00_express_doc = ("DOC", "G", "09D")
    tnt_9_00_express_nondoc = ("NONDOC", "G", "09N")
    tnt_10_00_express_doc = ("DOC", "G", "10D")
    tnt_10_00_express_nondoc = ("NONDOC", "G", "10N")
    tnt_12_00_express_doc = ("DOC", "G", "12D")
    tnt_12_00_express_nondoc = ("NONDOC", "G", "12N")
    tnt_10_00_express_nondoc = ("NONDOC", "D", "D")
    tnt_10_00_express_doc = ("DOC", "D", "D")
    tnt_12_00_express_nondoc = ("NONDOC", "D", "T")
    tnt_12_00_express_doc = ("DOC", "D", "T")
    tnt_express_nondoc_N = tnt_economy_express_road_scs_nondoc
    tnt_economy_express_nondoc = ("NONDOC", "G", "48N")
    tnt_12_00_economy_express_nondoc = ("NONDOC", "G", "412")
    tnt_express_doc_15D = ("DOC", "G", "15D")

    @classmethod
    def details(cls, service: str) -> tuple[str, str, str]:
        if service in cls:
            return cls[service]

        return next(
            (_ for _ in cls if _[2] == service),
            (None, None, service),
        )


class ShippingService(lib.StrEnum):
    """Carrier specific services"""

    tnt_express_doc = "tnt_express_doc"
    tnt_express_air_scs_nondoc = "tnt_express_air_scs_nondoc"
    tnt_express_air_scs_doc = "tnt_express_air_scs_doc"
    tnt_economy_express_road_scs_nondoc = "tnt_economy_express_road_scs_nondoc"
    tnt_economy_express_road_scs_doc = "tnt_economy_express_road_scs_doc"
    tnt_express_nondoc = "tnt_express_nondoc"
    tnt_9_00_express_doc = "tnt_9_00_express_doc"
    tnt_9_00_express_nondoc = "tnt_9_00_express_nondoc"
    tnt_10_00_express_doc = "tnt_10_00_express_doc"
    tnt_10_00_express_nondoc = "tnt_10_00_express_nondoc"
    tnt_12_00_express_doc = "tnt_12_00_express_doc"
    tnt_12_00_express_nondoc = "tnt_12_00_express_nondoc"
    tnt_10_00_express_nondoc = "tnt_10_00_express_nondoc"
    tnt_10_00_express_doc = "tnt_10_00_express_doc"
    tnt_12_00_express_nondoc = "tnt_12_00_express_nondoc"
    tnt_12_00_express_doc = "tnt_12_00_express_doc"
    tnt_express_nondoc_N = "tnt_express_nondoc_N"
    tnt_economy_express_nondoc = "tnt_economy_express_nondoc"
    tnt_12_00_economy_express_nondoc = "tnt_12_00_economy_express_nondoc"
    tnt_express_doc_15D = "tnt_express_doc_15D"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    # tnt_it_option = lib.OptionEnum("code")

    """ Unified Option type mapping """
    # insurance = tnt_it_coverage  #  maps unified karrio option to carrier specific

    pass


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
