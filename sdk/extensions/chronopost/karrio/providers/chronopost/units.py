from karrio.core.utils import Enum, Flag, Spec


class WeightUnit(Flag):
    KG = "KGM"


class LabelType(Flag):
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


class Service(Enum):
    chronopost_retrait_bureau = "00"
    chronopost_13 = "01"
    chronopost_10 = "02"
    chronopost_18 = "16"
    chronopost_relais = "86"
    chronopost_express_international = "17"
    chronopost_premium_international = "37"
    chronopost_classic_international = "44"


class Option(Flag):
    chronopost_delivery_on_monday = Spec.asKey("1")
    chronopost_delivery_on_saturday = Spec.asKey("6")
    chronopost_delivery_normal = Spec.asKey("0")
