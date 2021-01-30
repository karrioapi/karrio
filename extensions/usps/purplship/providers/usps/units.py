"""Purplship USPS enumerations module"""

import typing
from purplship.core.utils import Enum


class ContentType(Enum):
    hazmat = "HAZMAT"
    cremated_remains = "CREMATEDREMAINS"
    fragile = "FRAGILE"
    perishable = "PERISHABLE"
    pharmaceuticals = "PHARMACEUTICALS"
    medical_supplies = "MEDICAL SUPPLIES"
    lives = "LIVES"


class Incoterm(Enum):
    CPT = "CPT"
    CIP = "CIP"
    DAF = "DAF"
    DDU = "DDU"
    OTHER = "OTHER"


class IntlContentType(Enum):
    cremated_remains = "CrematedRemains"
    non_negotiable_document = "NonnegotiableDocument"
    pharmaceuticals = "Pharmaceuticals"
    medical_supplies = "MedicalSupplies"
    documents = "Documents"


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


class Size(Enum):
    regular = "REGULAR"
    large = "LARGE"


class Container(Enum):
    variable = "VARIABLE"
    flat_rate_envelope = "FLAT RATE ENVELOPE"
    padded_flat_rate_envelope = "PADDED FLAT RATE ENVELOPE"
    legal_flat_rate_envelope = "LEGAL FLAT RATE ENVELOPE"
    sm_flat_rate_envelope = "SM FLAT RATE ENVELOPE"
    window_flat_rate_envelope = "WINDOW FLAT RATE ENVELOPE"
    gift_card_flat_rate_envelope = "GIFT CARD FLAT RATE ENVELOPE"
    sm_flat_rate_box = "SM FLAT RATE BOX"
    md_flat_rate_box = "MD FLAT RATE BOX"
    lg_flat_rate_box = "LG FLAT RATE BOX"
    regional_rate_box_a = "REGIONALRATEBOXA"
    regional_rate_box_b = "REGIONALRATEBOXB"
    cubic_parcels = "CUBIC PARCELS"
    cubic_soft_pack = "CUBIC SOFT PACK"

    """ Unified Packaging type mapping """
    envelope = flat_rate_envelope
    pak = padded_flat_rate_envelope
    pallet = cubic_parcels
    small_box = sm_flat_rate_box
    medium_box = md_flat_rate_box
    tube = variable
    your_packaging = variable


class FirstClassMailType(Enum):
    flat = "FLAT"
    letter = "LETTER"
    package_service_retail = "PACKAGE SERVICE RETAIL"
    package_service = "PACKAGE SERVICE"
    postcard = "POSTCARD"

    """ Unified Packaging type mapping """
    envelope = letter
    medium_box = package_service
    pak = flat
    pallet = package_service_retail
    small_box = package_service
    tube = package_service
    your_packaging = package_service


class IntlPackageType(Enum):
    all = "ALL"
    package = "PACKAGE"
    postcards = "POSTCARDS"
    envelope = "ENVELOPE"
    letter = "LETTER"
    large_envelope = "LARGEENVELOPE"
    flat_rate = "FLATRATE"

    """ Unified Packaging type mapping """
    pak = large_envelope
    tube = package
    pallet = package
    small_box = package
    medium_box = package
    your_packaging = package


class SortationLevel(Enum):
    digit_3 = "3D"
    digit_5 = "5D"
    basic = "BAS"
    carrier_route = "CR"
    mixed_ndc = "MIX"
    ndc = "NDC"
    presort = "PST"
    scg = "SCF"
    emm_tray_box = "TBE"
    full_tray_box = "TBF"
    half_tray_box = "TBH"
    full_tub_tray_box = "TBT"


class Service(Enum):
    usps_gxg = "GXG"
    usps_airmail_m_bags = "Airmail M-Bags"
    usps_usps_retail_ground = "USPS Retail Ground"
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
    def find(service: str) -> 'Service':
        return next(reversed(sorted(
            [s for s in list(typing.cast(Enum, Service)) if s.value in service],
            key=lambda s: len(s.value)
        )))


class RateService(Enum):
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


class ExtraService(Enum):
    usps_registered_mail = "103"
    usps_insurance_global_express_guaranteed = "106"
    usps_insurance_express_mail_international = "107"
    usps_insurance_priority_mail_international = "108"
    usps_return_receipt = "105"
    usps_certificate_of_mailing = "100"
    usps_electronic_usps_delivery_confirmation_international = "109"

    usps_machinable = "001"


class SpecialService(Enum):
    usps_insurance = "100"
    usps_insurance_priority_mail_express = "101"
    usps_return_receipt = "102"
    usps_collect_on_delivery = "103"
    usps_certificate_of_mailing_form_3665 = "104"
    usps_certified_mail = "105"
    usps_tracking = "106"
    usps_signature_confirmation = "108"
    usps_registered_mail = "109"
    usps_return_receipt_electronic = "110"
    usps_registered_mail_cod_collection_charge = "112"
    usps_return_receipt_priority_mail_express = "118"
    usps_adult_signature_required = "119"
    usps_adult_signature_restricted_delivery = "120"
    usps_insurance_priority_mail = "125"
    usps_tracking_electronic = "155"
    usps_signature_confirmation_electronic = "156"
    usps_certificate_of_mailing_form_3817 = "160"
    usps_priority_mail_express_1030_am_delivery = "161"
    usps_certified_mail_restricted_delivery = "170"
    usps_certified_mail_adult_signature_required = "171"
    usps_certified_mail_adult_signature_restricted_delivery = "172"
    usps_signature_confirm_restrict_delivery = "173"
    usps_signature_confirmation_electronic_restricted_delivery = "174"
    usps_collect_on_delivery_restricted_delivery = "175"
    usps_registered_mail_restricted_delivery = "176"
    usps_insurance_restricted_delivery = "177"
    usps_insurance_restrict_delivery_priority_mail = "179"
    usps_insurance_restrict_delivery_priority_mail_express = "178"
    usps_insurance_restrict_delivery_bulk_only = "180"
    usps_scan_retention = "181"
    usps_scan_signature_retention = "182"
    usps_special_handling_fragile = "190"

    usps_machinable = "001"
