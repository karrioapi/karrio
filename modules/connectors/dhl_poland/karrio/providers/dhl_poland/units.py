import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


class CustomsContentType(lib.StrEnum):
    other = "9"
    sale_of_goods = "11"
    return_of_goods = "21"
    gifts = "31"
    samples_of_goods = "32"
    documents = "91"

    """ Unified Content type mapping """
    gift = gifts
    sample = samples_of_goods
    merchandise = sale_of_goods
    return_merchandise = return_of_goods


class LabelType(lib.StrEnum):
    BLP_LABEL = "BLP"
    LBLP_LABEL_A4_PDF = "LBLP"
    ZBLP_LABEL_ZPL = "ZBLP"

    """ Unified Label type mapping """
    PDF = BLP_LABEL
    ZPL = ZBLP_LABEL_ZPL


class PaymentType(lib.StrEnum):
    shipper = "SHIPPER"
    receiver = "RECEIVER"
    user = "USER"

    """ Unified Payment type mapping """
    sender = shipper
    recipient = receiver
    third_party = user


class PackagingType(lib.StrEnum):
    dhl_poland_envelope = "ENVELOPE"
    dhl_poland_package = "PACKAGE"
    dhl_poland_pallet = "PALLET"

    """ Unified Packaging type mapping """
    envelope = dhl_poland_envelope
    pak = dhl_poland_package
    tube = dhl_poland_package
    pallet = dhl_poland_pallet
    small_box = dhl_poland_package
    medium_box = dhl_poland_package
    large_box = dhl_poland_package
    your_packaging = dhl_poland_package


class Service(lib.Enum):
    dhl_poland_premium = "PR"
    dhl_poland_polska = "AH"
    dhl_poland_09 = "09"
    dhl_poland_12 = "12"
    dhl_poland_connect = "EK"
    dhl_poland_international = "PI"


class ShippingOption(lib.Enum):
    dhl_poland_delivery_in_18_22_hours = lib.OptionEnum("1722", bool)
    dhl_poland_delivery_on_saturday = lib.OptionEnum("SATURDAY", bool)
    dhl_poland_pickup_on_staturday = lib.OptionEnum("NAD_SOBOTA", bool)
    dhl_poland_insuration = lib.OptionEnum("UBEZP", float)
    dhl_poland_collect_on_delivery = lib.OptionEnum("COD", float)
    dhl_poland_information_to_receiver = lib.OptionEnum("PDI")
    dhl_poland_return_of_document = lib.OptionEnum("ROD", bool)
    dhl_poland_proof_of_delivery = lib.OptionEnum("POD", bool)
    dhl_poland_delivery_to_neighbour = lib.OptionEnum("SAS", bool)
    dhl_poland_self_collect = lib.OptionEnum("ODB", bool)

    """ Unified Option type mapping """
    insurance = dhl_poland_insuration
    cash_on_delivery = dhl_poland_collect_on_delivery
    saturday_delivery = dhl_poland_delivery_on_saturday


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


DEFAULT_SERVICES = [
    models.ServiceLevel(
        service_name="DHL Poland Premium",
        service_code="dhl_poland_premium",
        currency="EUR",
        domicile=True,
        zones=[models.ServiceZone(label="Zone 1", rate=0.0)],
    ),
    models.ServiceLevel(
        service_name="DHL Poland Polska",
        service_code="dhl_poland_polska",
        currency="EUR",
        domicile=True,
        zones=[models.ServiceZone(label="Zone 1", rate=0.0)],
    ),
    models.ServiceLevel(
        service_name="DHL Poland 09",
        service_code="dhl_poland_09",
        currency="EUR",
        domicile=True,
        zones=[models.ServiceZone(label="Zone 1", rate=0.0)],
    ),
    models.ServiceLevel(
        service_name="DHL Poland 12",
        service_code="dhl_poland_12",
        currency="EUR",
        domicile=True,
        zones=[models.ServiceZone(label="Zone 1", rate=0.0)],
    ),
    models.ServiceLevel(
        service_name="DHL Poland Connect",
        service_code="dhl_poland_connect",
        currency="EUR",
        international=True,
        zones=[models.ServiceZone(label="Zone 1", rate=0.0)],
    ),
    models.ServiceLevel(
        service_name="DHL Poland International",
        service_code="dhl_poland_international",
        currency="EUR",
        international=True,
        zones=[models.ServiceZone(label="Zone 1", rate=0.0)],
    ),
]
