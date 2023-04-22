import typing
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

    DDP = DAP
    CFR = "Cost and Freight"
    CIF = "Cost Insurance and Freight"
    CIP = "Carriage and Insurance Paid"
    CPT = "Carriage Paid To"
    DAF = "Delivered at Frontier"
    DDU = "Delivery Duty Unpaid"
    DEQ = "Delivered Ex Quay"
    DES = "Delivered Ex Ship"
    EXW = "Ex Works"
    FAS = "Free Alongside Ship"
    FCA = "Free Carrier"
    FOB = "Free On Board"


class ConnectionConfig(lib.Enum):
    language_code = lib.OptionEnum("language_code")
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)


class ShippingService(lib.Enum):
    """Carrier specific services"""

    dpdhl_paket = "V01PAK"
    dpdhl_paket_international = "V53WPAK"
    dpdhl_europaket = "V54EPAK"
    dpdhl_paket_connect = "V55PAK"
    dpdhl_warenpost = "V62WP"
    dpdhl_warenpost_international = "V66WPI"
    dpdhl_retoure = ""


class ServicePrefix(lib.Enum):
    V01PAK = "01"
    V53WPAK = "53"
    V54EPAK = "54"
    V55PAK = "55"
    V62WP = "62"
    V66WPI = "66"

    @classmethod
    def account_suffix(
        cls: lib.Enum,
        account: str,
        service: str,
        options: units.Options,
        is_international: bool = None,
    ):
        if len(account) > 10:
            return account

        _prefix = cls[service].value
        _suffix = "01"

        if service == cls.V01PAK.name and (
            options.dpdhl_additional_insurance.state is not None
            or options.dpdhl_cash_on_delivery.state is not None
        ):
            _suffix = "03"

        if (
            service == cls.V53WPAK.name
            and is_international
            and options.dpdhl_additional_insurance.state is None
            and options.dpdhl_cash_on_delivery.state is None
            and options.dpdhl_premium.state is None
        ):
            _suffix = "02"

        if service == cls.V54EPAK.name and options.dpdhl_go_green.state is None:
            _suffix = "02"
        if service == cls.V54EPAK.name and (
            options.dpdhl_bulky_goods.state is not None
        ):
            _suffix = "03"

        if (
            service == cls.V55PAK.name
            and options.dpdhl_additional_insurance.state is None
            and options.dpdhl_bulky_goods.state is None
            and options.dpdhl_go_green.state is None
        ):
            _suffix = "02"

        if service == cls.V62WP.name:
            _suffix = "01"

        if (
            service == cls.V66WPI.name
            and options.dpdhl_go_green.state is None
            and options.dpdhl_premium.state is None
        ):
            _suffix = "03"
        if service == cls.V66WPI.name and (
            options.dpdhl_go_green.state is not None
            and options.dpdhl_premium.state is not None
        ):
            _suffix = "04"

        return f"{account}{_prefix}{_suffix}"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    dpdhl_individual_sender_requirement = lib.OptionEnum(
        "IndividualSenderRequirement", bool
    )
    dpdhl_packaging_return = lib.OptionEnum("PackagingReturn", bool)
    dpdhl_return_receipt = lib.OptionEnum("ReturnReceipt", bool)
    dpdhl_preferred_neighbour = lib.OptionEnum("PreferredNeighbour")
    dpdhl_preferred_location = lib.OptionEnum("PreferredLocation")
    dpdhl_notification = lib.OptionEnum("Notification")
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
    cash_on_dlivery = dpdhl_cash_on_delivery
    email_notification = dpdhl_notification


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


class TrackingStatus(lib.Enum):
    in_transit = [""]
    on_hold = ["EXPHD"]
    delivered = ["DLVRD"]
    delivery_delayed = ["FWDCF"]
    ready_for_pickup = ["CNRFC", "HLDCC", "PCKDU"]
    delivery_failed = ["DLVRF", "DSPSD", "NTDEL", "RETRN"]
    out_for_delivery = ["MVARR", "MVARR", "MVDEX", "MVDPT", "MVTEX", "ULFMV"]


DEFAULT_SERVICES = [
    models.ServiceLevel(
        service_name="DHL Paket",
        service_code="dpdhl_paket",
        currency="EUR",
        domicile=True,
        zones=[models.ServiceZone(rate=0.0)],
    ),
    models.ServiceLevel(
        service_name="DHL Paket International",
        service_code="dpdhl_paket_international",
        currency="EUR",
        international=True,
        zones=[models.ServiceZone(rate=0.0)],
    ),
    models.ServiceLevel(
        service_name="DHL EuroPaket",
        service_code="dpdhl_europaket",
        currency="EUR",
        international=True,
        zones=[models.ServiceZone(rate=0.0)],
    ),
    models.ServiceLevel(
        service_name="DHL Paket Connect",
        service_code="dpdhl_paket_connect",
        currency="EUR",
        international=True,
        zones=[models.ServiceZone(rate=0.0)],
    ),
    models.ServiceLevel(
        service_name="DHL Warenpost",
        service_code="dpdhl_warenpost",
        currency="EUR",
        domicile=True,
        zones=[models.ServiceZone(rate=0.0)],
    ),
    models.ServiceLevel(
        service_name="DHL Warenpost International",
        service_code="dpdhl_warenpost_international",
        currency="EUR",
        international=True,
        zones=[models.ServiceZone(rate=0.0)],
    ),
]
