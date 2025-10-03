import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


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


class CustomsContentType(lib.StrEnum):
    other = "OTHER"
    present = "PRESENT"
    document = "DOCUMENT"
    return_of_goods = "RETURN_OF_GOODS"
    commercial_goods = "COMMERCIAL_GOODS"
    commercial_sample = "COMMERCIAL_SAMPLE"

    """ Unified Content type mapping """
    gift = present
    documents = document
    sample = commercial_sample
    merchandise = commercial_goods
    return_merchandise = return_of_goods


class Incoterm(lib.StrEnum):
    """Carrier specific incoterm"""

    DDU = "DDU"
    DAP = "DAP"
    DDP = "DDP"
    DDX = "DDX"
    DXV = "DXV"


class LabelType(lib.Enum):
    """Carrier specific label type"""

    PDF_A4 = ("PDF", "A4")
    ZPL2_A4 = ("ZPL2", "A4")
    PDF_910_300_700 = ("PDF", "910-300-700")
    ZPL2_910_300_700 = ("ZPL2", "910-300-700")
    PDF_910_300_700_oz = ("PDF", "910-300-700-oz")
    ZPL2_910_300_700_oz = ("ZPL2", "910-300-700-oz")
    PDF_910_300_710 = ("PDF", "910-300-710")
    ZPL2_910_300_710 = ("ZPL2", "910-300-710")
    PDF_910_300_600 = ("PDF", "910-300-600")
    ZPL2_910_300_600 = ("ZPL2", "910-300-600")
    PDF_910_300_610 = ("PDF", "910-300-610")
    ZPL2_910_300_610 = ("ZPL2", "910-300-610")
    PDF_910_300_400 = ("PDF", "910-300-400")
    ZPL2_910_300_400 = ("ZPL2", "910-300-400")
    PDF_910_300_410 = ("PDF", "910-300-410")
    ZPL2_910_300_410 = ("ZPL2", "910-300-410")
    PDF_910_300_300 = ("PDF", "910-300-300")
    ZPL2_910_300_300 = ("ZPL2", "910-300-300")
    PDF_910_300_300_oz = ("PDF", "910-300-300-oz")
    ZPL2_910_300_300_oz = ("ZPL2", "910-300-300-oz")

    """ Unified Label type mapping """
    PDF = PDF_A4
    ZPL = ZPL2_A4
    PNG = PDF_A4


class ConnectionConfig(lib.Enum):
    profile = lib.OptionEnum("profile")
    cost_center = lib.OptionEnum("cost_center")
    creation_software = lib.OptionEnum("creation_software")
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    language = lib.OptionEnum(
        "language",
        lib.units.create_enum("Language", ["de", "en"]),
    )
    label_type = lib.OptionEnum(
        "label_type",
        lib.units.create_enum("LabelType", [_.name for _ in LabelType]),  # type: ignore
    )



class ShippingService(lib.Enum):
    """Carrier specific services"""

    dhl_parcel_de_paket = "V01PAK"
    dhl_parcel_de_warenpost = "V62WP"
    dhl_parcel_de_europaket = "V54EPAK"
    dhl_parcel_de_paket_international = "V53WPAK"
    dhl_parcel_de_warenpost_international = "V66WPI"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    # fmt: off
    dhl_parcel_de_preferred_neighbour = lib.OptionEnum("preferredNeighbour")
    dhl_parcel_de_preferred_location = lib.OptionEnum("preferredLocation")
    dhl_parcel_de_visual_check_of_age = lib.OptionEnum("visualCheckOfAge")
    dhl_parcel_de_named_person_only = lib.OptionEnum("namedPersonOnly", bool)
    # dhl_parcel_de_ident_check = lib.OptionEnum("identCheck")
    dhl_parcel_de_signed_for_by_recipient = lib.OptionEnum("signedForByRecipient", bool)
    dhl_parcel_de_endorsement = lib.OptionEnum("endorsement")
    dhl_parcel_de_preferred_day = lib.OptionEnum("preferredDay")
    dhl_parcel_de_no_neighbour_delivery = lib.OptionEnum("noNeighbourDelivery", bool)
    dhl_parcel_de_additional_insurance = lib.OptionEnum("additionalInsurance", float)
    dhl_parcel_de_bulky_goods = lib.OptionEnum("bulkyGoods", bool)
    dhl_parcel_de_cash_on_delivery = lib.OptionEnum("cashOnDelivery", float)
    dhl_parcel_de_individual_sender_requirement = lib.OptionEnum("individualSenderRequirement")
    dhl_parcel_de_premium = lib.OptionEnum("premium", bool)
    dhl_parcel_de_closest_drop_point = lib.OptionEnum("closestDropPoint", bool)
    dhl_parcel_de_parcel_outlet_routing = lib.OptionEnum("parcelOutletRouting")
    # dhl_parcel_de_dhl_retoure = lib.OptionEnum("dhlRetoure")
    dhl_parcel_de_postal_delivery_duty_paid = lib.OptionEnum("postalDeliveryDutyPaid", bool)

    """ Unified Option type mapping """
    insurance = dhl_parcel_de_additional_insurance
    cash_on_delivery = dhl_parcel_de_cash_on_delivery
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


class CustomsOption(lib.Enum):
    mrn = lib.OptionEnum("MRN")
    permit_number = lib.OptionEnum("permitNo")
    attestation_number = lib.OptionEnum("attestationNo")
    shipper_customs_ref = lib.OptionEnum("shipperCustomsRef")
    consignee_customs_ref = lib.OptionEnum("consigneeCustomsRef")
    electronic_export_notification = lib.OptionEnum("electronicExportNotification")


class TrackingStatus(lib.Enum):
    delivered = ["delivered"]
    in_transit = ["transit"]
    delivery_failed = ["failure"]
    delivery_delayed = ["unknown"]


DEFAULT_SERVICES = [
    models.ServiceLevel(
        service_name="DHL Paket",
        service_code="dhl_parcel_de_paket",
        currency="EUR",
        domicile=True,
        min_weight=0.01,
        max_weight=31.5,
        max_length=120,
        max_width=60,
        max_height=60,
        weight_unit="KG",
        dimension_unit="CM",
        zones=[models.ServiceZone(rate=0.0)],
    ),
    models.ServiceLevel(
        service_name="DHL Paket International",
        service_code="dhl_parcel_de_paket_international",
        currency="EUR",
        domicile=False,
        international=True,
        min_weight=0.01,
        max_weight=31.5,
        max_length=120,
        max_width=60,
        max_height=60,
        weight_unit="KG",
        dimension_unit="CM",
        zones=[models.ServiceZone(rate=0.0)],
    ),
    models.ServiceLevel(
        service_name="DHL EuroPaket",
        service_code="dhl_parcel_de_europaket",
        currency="EUR",
        domicile=False,
        international=True,
        min_weight=0.01,
        max_weight=31.5,
        max_length=120,
        max_width=60,
        max_height=60,
        weight_unit="KG",
        dimension_unit="CM",
        zones=[models.ServiceZone(rate=0.0)],
    ),
    models.ServiceLevel(
        service_name="DHL Warenpost",
        service_code="dhl_parcel_de_warenpost",
        currency="EUR",
        domicile=True,
        international=False,
        min_weight=0.01,
        max_weight=1,
        max_length=35,
        max_width=7,
        max_height=5,
        weight_unit="KG",
        dimension_unit="CM",
        zones=[models.ServiceZone(rate=0.0)],
    ),
    models.ServiceLevel(
        service_name="DHL Warenpost International",
        service_code="dhl_parcel_de_warenpost_international",
        currency="EUR",
        domicile=False,
        international=True,
        min_weight=0.01,
        max_weight=1,
        max_length=35.3,
        max_width=9,
        max_height=10,
        weight_unit="KG",
        dimension_unit="CM",
        zones=[models.ServiceZone(rate=0.0)],
    ),
]
