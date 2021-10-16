""" Asendia US Native Types """

from purplship.core.utils import Enum, Flag, Spec


class ProcessingLocation(Enum):
    SFO = "SFO"
    MIA = "MIA"
    JFK = "JFK"
    PHL = "PHL"
    ORD = "ORD" 
    LAX = "LAX"


class LabelType(Enum):
    ANY = "ANY"
    PDF = "PDF"
    PNG = "PNG"
    ZPL = "ZPL"


class Service(Flag):
    asendia_us_all = "*"
    asendia_us_ecom_tracked_ddp = 19
    asendia_us_fully_tracked = 65
    asendia_us_country_tracked = 66


class Option(Flag):
    asendia_sub_account_number = Spec.asValue("asendia_sub_account_number")
    asendia_processing_location = Spec.asValue("asendia_processing_location")
