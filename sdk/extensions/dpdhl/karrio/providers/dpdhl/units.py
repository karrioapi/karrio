import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


class PackagingType(lib.Flag):
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


class LabelType(lib.Flag):
    B_64 = "B64"
    ZPL_2 = "ZPL2"

    """ Unified Label type mapping """
    PDF = B_64
    ZPL = ZPL_2


class CustomsContentType(lib.Flag):
    OTHER = "OTHER"
    PRESENT = "PRESENT"
    COMMERCIAL_SAMPLE = "COMMERCIAL_SAMPLE"
    DOCUMENT = "DOCUMENT"
    RETURN_OF_GOODS = "RETURN_OF_GOODS"
    COMMERCIAL_GOODS = "COMMERCIAL_GOODS"

    """ Unified Content type mapping """
    gift = PRESENT
    other = OTHER
    documents = DOCUMENT
    sample = COMMERCIAL_SAMPLE
    merchandise = COMMERCIAL_GOODS
    return_merchandise = RETURN_OF_GOODS


class Incoterm(lib.Enum):
    DXV = "Delivery Duty Paid (excl. VAT)"
    DAP = "Delivery Duty Paid"
    DDX = "Delivery Duty Paid (excl. Duties, taxes and VAT"

    """ Unified Incoterm mapping """

    CFR = "Cost and Freight"
    CIF = "Cost Insurance and Freight"
    CIP = "Carriage and Insurance Paid"
    CPT = "Carriage Paid To"
    DAF = "Delivered at Frontier"
    DDP = DAP
    DDU = "Delivery Duty Unpaid"
    DEQ = "Delivered Ex Quay"
    DES = "Delivered Ex Ship"
    EXW = "Ex Works"
    FAS = "Free Alongside Ship"
    FCA = "Free Carrier"
    FOB = "Free On Board"


class ShippingService(lib.Enum):
    """Carrier specific services"""

    dpdhl_paket = "V01PAK"
    dpdhl_paket_international = "V53WPAK"
    dpdhl_europaket = "V54EPAK"
    dpdhl_paket_connect = "V55PAK"
    dpdhl_warenpost = "V62WP"
    dpdhl_warenpost_international = "V66WPI"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    dpdhl_individual_sender_requirement = lib.OptionEnum(
        "IndividualSenderRequirement", bool
    )
    dpdhl_packaging_return = lib.OptionEnum("PackagingReturn", bool)
    dpdhl_return_receipt = lib.OptionEnum("ReturnReceipt", bool)
    dpdhl_preferred_neighbour = lib.OptionEnum("PreferredNeighbour")
    dpdhl_preferred_location = lib.OptionEnum("PreferredLocation")
    dpdhl_visual_check_of_age = lib.OptionEnum("VisualCheckOfAge", bool)
    dpdhl_named_person_only = lib.OptionEnum("NamedPersonOnly", bool)
    dpdhl_identcheck = lib.OptionEnum("code", lib.to_dict)
    dpdhl_no_neighbour_delivery = lib.OptionEnum("NoNeighbourDelivery", bool)
    dpdhl_preferred_day = lib.OptionEnum("PreferredDay")
    dpdhl_endorsement = lib.OptionEnum("Endorsement", bool)
    dpdhl_go_green = lib.OptionEnum("GoGreen", bool)
    dpdhl_additional_insurance = lib.OptionEnum("AdditionalInsurance", float)
    dpdhl_bulky_goods = lib.OptionEnum("BulkyGoods", bool)
    dpdhl_cash_on_delivery = lib.OptionEnum("CashOnDelivery", float)
    dpdhl_premium = lib.OptionEnum("Premium", bool)
    dpdhl_parcel_outlet_routing = lib.OptionEnum("ParcelOutletRouting", bool)

    """ Unified Option type mapping """
    insurance = dpdhl_additional_insurance


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
        service_name="DHL Paket",
        service_code="dpdhl_paket",
        cost="0.00",
        currency="EUR",
        domicile=True,
    ),
    models.ServiceLevel(
        service_name="DHL Paket International",
        service_code="dpdhl_paket_international",
        cost="0.00",
        currency="EUR",
        international=True,
    ),
    models.ServiceLevel(
        service_name="DHL EuroPaket",
        service_code="dpdhl_europaket",
        cost="0.00",
        currency="EUR",
        international=True,
    ),
    models.ServiceLevel(
        service_name="DHL Paket Connect",
        service_code="dpdhl_paket_connect",
        cost="0.00",
        currency="EUR",
        international=True,
    ),
    models.ServiceLevel(
        service_name="DHL Warenpost",
        service_code="dpdhl_warenpost",
        cost="0.00",
        currency="EUR",
        domicile=True,
    ),
    models.ServiceLevel(
        service_name="DHL Warenpost International",
        service_code="dpdhl_warenpost_international",
        cost="0.00",
        currency="EUR",
        international=True,
    ),
]
