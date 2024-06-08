import karrio.lib as lib
import karrio.core.units as units
from karrio.core.utils.enum import OptionEnum


class WeightUnit(lib.StrEnum):
    KG = "KGM"


class LabelType(lib.StrEnum):
    PDF_LABEL = "PDF"
    PPR_LABEL = "PPR"
    SPD_LABEL = "SPD"
    Z2D_LABEL = "Z2D"
    THE_LABEL = "THE"
    XML_LABEL = "XML"
    XML2D_LABEL = "XML2D"
    THEPSG_LABEL = "THEPSG"
    ZPLPSG_LABEL = "ZPLPSG"
    ZPL300_LABEL = "ZPL300"

    """ Unified Label type mapping """
    PDF = PDF_LABEL
    ZPL = ZPL300_LABEL


class CustomsContentType(lib.StrEnum):
    document = "DOC"
    marchandise = "MAR"

    """ Unified Customs Content Type mapping"""
    documents = document
    merchandise = marchandise


class ShippingService(lib.StrEnum):
    chronopost_retrait_bureau = "0"
    chronopost_13 = "1"
    chronopost_10 = "2"
    chronopost_18 = "16"
    chronopost_relais = "86"
    chronopost_express_international = "17"
    chronopost_premium_international = "37"
    chronopost_classic_international = "44"


class ShippingOption(lib.Enum):
    chronopost_delivery_on_monday = OptionEnum("1")
    chronopost_delivery_on_saturday = OptionEnum("6")
    chronopost_delivery_normal = OptionEnum("0")

    """ Unified Option type mapping """
    saturday_delivery = chronopost_delivery_on_saturday


def shipping_options_initializer(
    options: dict,
    package_options: units.Options = None,
) -> units.Options:
    """
    Apply default values to the given options.
    """
    _options = options.copy()

    if package_options is not None:
        _options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(_options, ShippingOption, items_filter=items_filter)
