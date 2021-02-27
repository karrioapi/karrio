"""Purplship USPS International units module"""

import typing
from purplship.core.utils import Enum, Spec
from purplship.core.models import Address


class Incoterm(Enum):
    CPT = "CPT"
    CIP = "CIP"
    DAF = "DAF"
    DDU = "DDU"
    OTHER = "OTHER"

    """ Unified Incoterm type mapping """
    CFR = OTHER
    CIF = OTHER
    DDP = OTHER
    DEQ = OTHER
    DES = OTHER
    EXW = OTHER
    FAS = OTHER
    FCA = OTHER
    FOB = OTHER


class ContentType(Enum):
    cremated_remains = "CREMATEDREMAINS"
    merchandise = "MERCHANDISE"
    sample = "SAMPLE"
    gift = "GIFT"
    documents = "DOCUMENTS"
    return_merchandise = "RETURN"
    humanitarian = "HUMANITARIAN"
    dangerousgoods = "DANGEROUSGOODS"
    nonnegotiabledocument = "NONNEGOTIABLEDOCUMENT"
    pharmacuticals = "PHARMACUTICALS"
    medicalsupplies = "MEDICALSUPPLIES"
    other = "OTHER"


class LabelFormat(Enum):
    usps_barcode_only = "BARCODE ONLY"
    usps_crop = "CROP"
    usps_4_x_6_label = "4X6LABEL"
    usps_4_x_6_label_l = "4X6LABELL"
    usps_6_x_4_label = "6X4LABEL"
    usps_4_x_6_label_p = "4X6LABELP"
    usps_4_x_6_label_p_page = "4X6LABELP PAGE"
    usps_4_x_6_zpl_203_dpi = "4X6ZPL203DPI"
    usps_4_x_6_zpl_300_dpi = "4X6ZPL300DPI"
    usps_separate_continue_page = "SEPARATECONTINUEPAGE"

    """ Unified Label type mapping """
    PDF = usps_6_x_4_label
    ZPL = usps_4_x_6_zpl_203_dpi


class PackagingType(Enum):
    all = "ALL"
    package = "PACKAGE"
    postcards = "POSTCARDS"
    envelope = "ENVELOPE"
    letter = "LETTER"
    large_envelope = "LARGEENVELOPE"
    flat_rate = "FLATRATE"
    variable = "VARIABLE"
    legalenvelope = "LEGALENVELOPE"
    uspsgxgenvelope = "USPSGXGENVELOPE"
    uspsgxglegalenvelope = "USPSGXGLEGALENVELOPE"
    uspsgxgtyvekenvelope = "USPSGXGTYVEKENVELOPE"

    """ Unified Packaging type mapping """
    pak = large_envelope
    tube = package
    pallet = package
    small_box = package
    medium_box = package
    your_packaging = package


class ServiceAlias(Enum):
    usps_gxg = "GXG"
    usps_airmail_m_bags = "Airmail M-Bags"
    usps_usps_retail_ground = "USPS International Retail Ground"
    usps_media_mail = "Media Mail"
    usps_priority_mail = "Priority Mail"
    usps_priority_mail_express = "Priority Mail Express"
    usps_first_class_mail = "First-Class Mail"
    usps_priority_mail_international = "Priority Mail International"
    usps_priority_mail_express_international = "Priority Mail Express International"
    usps_first_class_package_service = "First-Class Package Service"
    usps_first_class_mail_international = "First-Class Mail International"
    usps_first_class_package_international_service = "First-Class Package International Service"

    @staticmethod
    def find(service: str) -> 'ServiceAlias':
        return next(reversed(sorted(
            [s for s in list(typing.cast(Enum, ServiceAlias)) if s.value in service],
            key=lambda s: len(s.value)
        )))


class ShipmentService(Enum):
    usps_first_class = "First Class"
    usps_first_class_commercial = "First Class Commercial"
    usps_first_class_hfp_commercial = "First Class HFPCommercial"
    usps_priority = "Priority"
    usps_priority_commercial = "Priority Commercial"
    usps_priority_cpp = "Priority Cpp"
    usps_priority_hfp_commercial = "Priority HFP Commercial"
    usps_priority_hfp_cpp = "Priority HFP CPP"
    usps_priority_mail_express = "Priority Mail Express"
    usps_priority_mail_express_commercial = "Priority Mail Express Commercial"
    usps_priority_mail_express_cpp = "Priority Mail Express CPP"
    usps_priority_mail_express_sh = "Priority Mail Express Sh"
    usps_priority_mail_express_sh_commercial = "Priority Mail Express ShCommercial"
    usps_priority_mail_express_hfp = "Priority Mail Express HFP"
    usps_priority_mail_express_hfp_commercial = "Priority Mail Express HFP Commercial"
    usps_priority_mail_express_hfp_cpp = "Priority Mail Express HFP CPP"
    usps_priority_mail_cubic = "Priority Mail Cubic"
    usps_retail_ground = "Retail Ground"
    usps_media = "Media"
    usps_library = "Library"
    usps_all = "All"
    usps_online = "Online"
    usps_plus = "Plus"
    usps_bpm = "BPM"


class ShipmentOption(Enum):
    usps_registered_mail = Spec.asKey("103")
    usps_insurance_global_express_guaranteed = Spec.asValue("106")
    usps_insurance_express_mail_international = Spec.asValue("107")
    usps_insurance_priority_mail_international = Spec.asValue("108")
    usps_return_receipt = Spec.asKey("105")
    usps_certificate_of_mailing = Spec.asKey("100")
    usps_electronic_usps_delivery_confirmation_international = Spec.asKey("109")

    """ Non official options """
    usps_option_machinable_item = Spec.asFlag("usps_option_machinable_item")
    usps_option_abandon_non_delivery = Spec.asKey("ABANDON")
    usps_option_return_non_delivery = Spec.asKey("RETURN")
    usps_option_redirect_non_delivery = Spec.asValue("REDIRECT", Address)
