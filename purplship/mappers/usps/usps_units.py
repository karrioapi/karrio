"""PurplShip USPS enumerations module"""

from enum import Enum


class SortationLevel(Enum):
    Digit_3 = "3D"
    Digit_5 = "5D"
    Basic = "BAS"
    Carrier_Route = "CR"
    Mixed_NDC = "MIX"
    NDC = "NDC"
    Presort = "PST"
    SCG = "SCF"
    EMM_Tray_Box = "TBE"
    Full_Tray_Box = "TBF"
    Half_Tray_Box = "TBH"
    Full_Tub_Tray_Box = "TBT"


class Service(Enum):
    First_Class = "First Class"
    First_Class_Commercial = "First Class Commercial"
    First_Class__HFPCommercial = "First Class HFPCommercial"
    Priority = "Priority"
    Priority_Commercial = "Priority Commercial"
    Priority_Cpp = "Priority Cpp"
    Priority_HFP_Commercial = "Priority HFP Commercial"
    Priority_HFP_CPP = "Priority HFP CPP"
    Priority_Mail_Express = "Priority Mail Express"
    Priority_Mail_Express_Commercial = "Priority Mail Express Commercial"
    Priority_Mail_Express_CPP = "Priority Mail Express CPP"
    Priority_Mail_Express_Sh = "Priority Mail Express Sh"
    Priority_Mail_Express_ShCommercial = "Priority Mail Express ShCommercial"
    Priority_Mail_Express_HFP = "Priority Mail Express HFP"
    Priority_Mail_Express_HFP_Commercial = "Priority Mail Express HFP Commercial"
    Priority_Mail_Express_HFP_CPP = "Priority Mail Express HFP CPP"
    Priority_Mail_Cubic = "Priority Mail Cubic"
    Retail_Ground = "Retail Ground"
    Media = "Media"
    Library = "Library"
    All = "All"
    Online = "Online"
    Plus = "Plus"
    BPM = "BPM"


class FirstClassMailType(Enum):
    LETTER = "LETTER"
    FLAT = "FLAT"
    PACKAGE_SERVICE_RETAIL = "PACKAGE SERVICE RETAIL"
    POSTCARD = "POSTCARD"
    PACKAGE_SERVICE = "PACKAGE SERVICE"

    """ Unified Packaging type mapping """
    SM = LETTER
    BOX = PACKAGE_SERVICE
    PC = POSTCARD
    PAL = PACKAGE_SERVICE_RETAIL


class IntlMailType(Enum):
    ALL = "ALL"
    PACKAGE = "PACKAGE"
    POSTCARDS = "POSTCARDS"
    ENVELOPE = "ENVELOPE"
    LETTER = "LETTER"
    LARGEENVELOPE = "LARGEENVELOPE"
    FLATRATE = "FLATRATE"

    """ Unified Packaging type mapping """
    SM = LETTER
    BOX = PACKAGE
    PC = POSTCARDS
    PAL = ALL


class Container(Enum):
    VARIABLE = "VARIABLE"
    FLAT_RATE_ENVELOPE = "FLAT RATE ENVELOPE"
    PADDED_FLAT_RATE_ENVELOPE = "PADDED FLAT RATE ENVELOPE"
    LEGAL_FLAT_RATE_ENVELOPE = "LEGAL FLAT RATE ENVELOPE"
    SM_FLAT_RATE_ENVELOPE = "SM FLAT RATE ENVELOPE"
    WINDOW_FLAT_RATE_ENVELOPE = "WINDOW FLAT RATE ENVELOPE"
    GIFT_CARD_FLAT_RATE_ENVELOPE = "GIFT CARD FLAT RATE ENVELOPE"
    SM_FLAT_RATE_BOX = "SM FLAT RATE BOX"
    MD_FLAT_RATE_BOX = "MD FLAT RATE BOX"
    LG_FLAT_RATE_BOX = "LG FLAT RATE BOX"
    REGIONALRATEBOXA = "REGIONALRATEBOXA"
    REGIONALRATEBOXB = "REGIONALRATEBOXB"
    RECTANGULAR = "RECTANGULAR"
    NONRECTANGULAR = "NONRECTANGULAR"
    CUBIC_PARCELS = "CUBIC PARCELS"
    CUBIC_SOFT_PACK = "CUBIC SOFT PACK"

    """ Unified Packaging type mapping """
    SM = FLAT_RATE_ENVELOPE
    BOX = SM_FLAT_RATE_BOX
    PC = VARIABLE
    PAL = CUBIC_PARCELS


class IntlContainer(Enum):
    RECTANGULAR = "RECTANGULAR"
    NONRECTANGULAR = "NONRECTANGULAR"

    """ Unified Packaging type mapping """
    SM = NONRECTANGULAR
    BOX = RECTANGULAR
    PC = NONRECTANGULAR
    PAL = RECTANGULAR


class SpecialService(Enum):
    Insurance = "100"
    Insurance_Priority_Mail_Express = "101"
    Return_Receipt = "102"
    Collect_on_Delivery = "103"
    Certificate_of_Mailing_Form_3665 = "104"
    Certified_Mail = "105"
    USPS_Tracking = "106"
    Return_Receipt_for_Merchandise = "107"
    Signature_Confirmation = "108"
    Registered_Mail = "109"
    Return_Receipt_Electronic = "110"
    Registered_mail_COD_collection_Charge = "112"
    Return_Receipt_Priority_Mail_Express = "118"
    Adult_Signature_Required = "119"
    Adult_Signature_Restricted_Delivery = "120"
    Insurance_Priority_Mail = "125"
    USPS_Tracking_Electronic = "155"
    Signature_Confirmation_Electronic = "156"
    Certificate_of_Mailing_Form_3817 = "160"
    Priority_Mail_Express_1030_AM_Delivery = "161"
    Certified_Mail_Restricted_Delivery = "170"
    Certified_Mail_Adult_Signature_Required = "171"
    Certified_Mail_Adult_Signature_Restricted_Delivery = "172"
    Signature_Confirm_Restrict_Delivery = "173"
    Signature_Confirmation_Electronic_Restricted_Delivery = "174"
    Collect_on_Delivery_Restricted_Delivery = "175"
    Registered_Mail_Restricted_Delivery = "176"
    Insurance_Restricted_Delivery = "177"
    Insurance_Restrict_Delivery_Priority_Mail = "179"
    Insurance_Restrict_Delivery_Priority_Mail_Express = "178"
    Insurance_Restrict_Delivery_Bulk_Only = "180"
    Special_Handling_Fragile = "190"


class IntlSpecialService(Enum):
    Registered_Mail = "103"
    Insurance_Global_Express_Guaranteed = "106"
    Insurance_Express_Mail_International = "107"
    Insurance_Priority_Mail_International = "108"
    Return_Receipt = "105"
    Certificate_of_Mailing = "100"
    Electronic_USPS_Delivery_Confirmation_International = "109"


class ContentType(Enum):
    HAZMAT = "HAZMAT"
    CREMATEDREMAINS = "CREMATEDREMAINS"
    FRAGILE = "FRAGILE"
    PERISHABLE = "PERISHABLE"
    PHARMACEUTICALS = "PHARMACEUTICALS"
    MEDICALSUPPLIES = "MEDICALSUPPLIES"
    LIVES = "LIVES"


class IntlContentType(Enum):
    CrematedRemains = "CrematedRemains"
    NonnegotiableDocument = "NonnegotiableDocument"
    Pharmaceuticals = "Pharmaceuticals"
    MedicalSupplies = "MedicalSupplies"
    Documents = "Documents"
