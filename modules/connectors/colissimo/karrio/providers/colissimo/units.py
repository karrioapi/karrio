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


class LabelType(lib.Enum):
    ZPL_10x15_203dpi = "ZPL_10x15_203dpi"
    ZPL_10x15_300dpi = "ZPL_10x15_300dpi"
    DPL_10x15_203dpi = "DPL_10x15_203dpi"
    DPL_10x15_300dpi = "DPL_10x15_300dpi"
    PDF_10x15_300dpi = "PDF_10x15_300dpi"
    PDF_A4_300dpi = "PDF_A4_300dpi"
    ZPL_10x10_203dpi = "ZPL_10x10_203dpi"
    ZPL_10x10_300dpi = "ZPL_10x10_300dpi"
    DPL_10x10_203dpi = "DPL_10x10_203dpi"
    DPL_10x10_300dpi = "DPL_10x10_300dpi"
    PDF_10x10_300dpi = "PDF_10x10_300dpi"
    PDF_10x12_300dpi = "PDF_10x12_300dpi"
    ZPL_10x15_203dpi_UL = "ZPL_10x15_203dpi_UL"
    ZPL_10x15_300dpi_UL = "ZPL_10x15_300dpi_UL"
    DPL_10x15_203dpi_UL = "DPL_10x15_203dpi_UL"
    DPL_10x15_300dpi_UL = "DPL_10x15_300dpi_UL"
    PDF_10x15_300dpi_UL = "PDF_10x15_300dpi_UL"
    PDF_A4_300dpi_UL = "PDF_A4_300dpi_UL"

    """ Unified Label type mapping """
    PDF = PDF_10x15_300dpi
    ZPL = ZPL_10x10_300dpi


class ConnectionConfig(lib.Enum):
    lang = lib.OptionEnum("lang", lib.units.create_enum("Lang", ["FR", "EN"]))


class ServiceName(lib.Enum):
    """Carrier specific services"""

    colissimo_home_without_signature = "Colissimo Home - without signature"
    colissimo_home_with_signature = "Colissimo Home - with signature"
    colissimo_eco_france = "Colissimo Eco France"
    colissimo_return_france = "Colissimo Return France CORE 8R***"
    colissimo_flash_without_signature = "Colissimo Flash – without signature"
    colissimo_flash_with_signature = "Colissimo Flash – with signature"
    colissimo_oversea_home_without_signature = "Colissimo Home OM - without signature"
    colissimo_oversea_home_with_signature = "Colissimo Home OM - with signature"
    colissimo_eco_om_without_signature = "Colissimo Eco OM - without signature"
    colissimo_eco_om_with_signature = "Colissimo Eco OM - with signature"
    colissimo_retour_om = "Colissimo Retour OM"
    colissimo_home_international_without_signature = (
        "Colissimo Home International - without signature***"
    )
    colissimo_home_international_with_signature = (
        "Colissimo Home International - with signature***"
    )
    colissimo_return_international_to_france = (
        "Colissimo Return International – Foreign country to France"
    )
    colissimo_return_international_from_france = (
        "Colissimo Return International – France to foreign cournty"
    )
    colissimo_economical_big_export_offer = (
        "Economical Big Export offer (test offer for China for a pilot customer)"
    )
    colissimo_out_of_home_national_international = (
        "Colissimo Out Of Home National and International : **"
    )
    colissimo_out_of_home_post_office = "Colissimo - Out Of Home – at Post Office"
    colissimo_out_of_home_pickup_points_station_lockers = (
        "Colissimo - Out Of Home – at Pickup points or Pickup Station lockers"
    )
    colissimo_out_of_home_pickup_point = "Colissimo - Out Of Home – at pickup point"
    colissimo_out_of_home_pickup_station_lockers = (
        "Colissimo - Out Of Home – at Pickup Station lockers"
    )


class ShippingService(lib.StrEnum):
    """Carrier specific services"""

    colissimo_home_without_signature = "DOM"
    colissimo_home_with_signature = "DOS"
    colissimo_eco_france = "CECO"
    colissimo_return_france = "CORE"
    colissimo_flash_without_signature = "COLR"
    colissimo_flash_with_signature = "J+1"
    colissimo_oversea_home_without_signature = "COM"
    colissimo_oversea_home_with_signature = "CDS"
    colissimo_eco_om_without_signature = "ECO"
    colissimo_eco_om_with_signature = "ECOS"
    colissimo_retour_om = "CORI"
    colissimo_home_international_without_signature = colissimo_home_without_signature
    colissimo_home_international_with_signature = colissimo_home_with_signature
    colissimo_return_international_to_france = colissimo_retour_om
    colissimo_return_international_from_france = "CORF"
    colissimo_economical_big_export_offer = "ACCI"
    colissimo_out_of_home_national_international = "HD"
    colissimo_out_of_home_post_office = colissimo_out_of_home_national_international
    colissimo_out_of_home_pickup_points_station_lockers = (
        colissimo_out_of_home_national_international
    )
    colissimo_out_of_home_pickup_point = colissimo_out_of_home_national_international
    colissimo_out_of_home_pickup_station_lockers = (
        colissimo_out_of_home_national_international
    )


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    colissimo_insurance_value = lib.OptionEnum("insuranceValue", lib.to_money)
    colissimo_cod_amount = lib.OptionEnum("CODAmount", lib.to_money)
    colissimo_return_receipt = lib.OptionEnum("returnReceipt", bool)
    colissimo_ftd = lib.OptionEnum("ftd", bool)
    colissimo_non_machinable = lib.OptionEnum("nonMachinable", bool)
    colissimo_ddp = lib.OptionEnum("ddp", bool)
    colissimo_instructions = lib.OptionEnum("instructions")

    """ Unified Option type mapping """
    insurance = colissimo_insurance_value
    cash_on_delivery = colissimo_cod_amount


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
    delivered = ["DI1"]
    in_transit = [""]
    out_for_delivery = ["MD2", "ET1"]


DEFAULT_SERVICES = [
    models.ServiceLevel(
        service_name="Colissimo Home - without signature",
        service_code="colissimo_home_without_signature",
        currency="EUR",
        domicile=True,
        zones=[models.ServiceZone(label="Zone 1", rate=0.0)],
    ),
]
