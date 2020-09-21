"""Purplship USPS enumerations module"""

from enum import Enum


class Size(Enum):
    regular = "REGULAR"
    large = "LARGE"


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
    first_class = "First Class"
    first_class_commercial = "First Class Commercial"
    first_class_hfp_commercial = "First Class HFPCommercial"
    priority = "Priority"
    priority_commercial = "Priority Commercial"
    priority_cpp = "Priority Cpp"
    priority_hfp_commercial = "Priority HFP Commercial"
    priority_hfp_cpp = "Priority HFP CPP"
    priority_mail_express = "Priority Mail Express"
    priority_mail_express_commercial = "Priority Mail Express Commercial"
    priority_mail_express_cpp = "Priority Mail Express CPP"
    priority_mail_express_sh = "Priority Mail Express Sh"
    priority_mail_express_sh_commercial = "Priority Mail Express ShCommercial"
    priority_mail_express_hfp = "Priority Mail Express HFP"
    priority_mail_express_hfp_commercial = "Priority Mail Express HFP Commercial"
    priority_mail_express_hfp_cpp = "Priority Mail Express HFP CPP"
    priority_mail_cubic = "Priority Mail Cubic"
    retail_ground = "Retail Ground"
    media = "Media"
    library = "Library"
    all = "All"
    online = "Online"
    plus = "Plus"
    bpm = "BPM"


class FirstClassMailType(Enum):
    letter = "LETTER"
    flat = "FLAT"
    package_service_retail = "PACKAGE SERVICE RETAIL"
    postcard = "POSTCARD"
    package_service = "PACKAGE SERVICE"

    """ Unified Packaging type mapping """
    sm = letter
    box = package_service
    pc = postcard
    pal = package_service_retail


class IntlMailType(Enum):
    all = "ALL"
    package = "PACKAGE"
    postcards = "POSTCARDS"
    envelope = "ENVELOPE"
    letter = "LETTER"
    largeenvelope = "LARGEENVELOPE"
    flatrate = "FLATRATE"

    """ Unified Packaging type mapping """
    sm = envelope
    box = package
    pc = postcards
    pal = all


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
    regionalrateboxa = "REGIONALRATEBOXA"
    regionalrateboxb = "REGIONALRATEBOXB"
    rectangular = "RECTANGULAR"
    nonrectangular = "NONRECTANGULAR"
    cubic_parcels = "CUBIC PARCELS"
    cubic_soft_pack = "CUBIC SOFT PACK"

    """ Unified Packaging type mapping """
    sm = sm_flat_rate_envelope
    box = sm_flat_rate_box
    pc = variable
    pal = cubic_parcels


class IntlContainer(Enum):
    rectangular = "RECTANGULAR"
    nonrectangular = "NONRECTANGULAR"

    """ Unified Packaging type mapping """
    sm = nonrectangular
    box = rectangular
    pc = nonrectangular
    pal = rectangular


class SpecialService(Enum):
    insurance = "100"
    insurance_priority_mail_express = "101"
    return_receipt = "102"
    collect_on_delivery = "103"
    certificate_of_mailing_form_3665 = "104"
    certified_mail = "105"
    usps_tracking = "106"
    return_receipt_for_merchandise = "107"
    signature_confirmation = "108"
    registered_mail = "109"
    return_receipt_electronic = "110"
    registered_mail_cod_collection_charge = "112"
    return_receipt_priority_mail_express = "118"
    adult_signature_required = "119"
    adult_signature_restricted_delivery = "120"
    insurance_priority_mail = "125"
    usps_tracking_electronic = "155"
    signature_confirmation_electronic = "156"
    certificate_of_mailing_form_3817 = "160"
    priority_mail_express_1030_am_delivery = "161"
    certified_mail_restricted_delivery = "170"
    certified_mail_adult_signature_required = "171"
    certified_mail_adult_signature_restricted_delivery = "172"
    signature_confirm_restrict_delivery = "173"
    signature_confirmation_electronic_restricted_delivery = "174"
    collect_on_delivery_restricted_delivery = "175"
    registered_mail_restricted_delivery = "176"
    insurance_restricted_delivery = "177"
    insurance_restrict_delivery_priority_mail = "179"
    insurance_restrict_delivery_priority_mail_express = "178"
    insurance_restrict_delivery_bulk_only = "180"
    special_handling_fragile = "190"


class ExtraService(Enum):
    registered_mail = "103"
    insurance_global_express_guaranteed = "106"
    insurance_express_mail_international = "107"
    insurance_priority_mail_international = "108"
    return_receipt = "105"
    certificate_of_mailing = "100"
    electronic_usps_delivery_confirmation_international = "109"


class ContentType(Enum):
    hazmat = "HAZMAT"
    crematedremains = "CREMATEDREMAINS"
    fragile = "FRAGILE"
    perishable = "PERISHABLE"
    pharmaceuticals = "PHARMACEUTICALS"
    medicalsupplies = "MEDICALSUPPLIES"
    lives = "LIVES"


class IntlContentType(Enum):
    cremated_remains = "CrematedRemains"
    nonnegotiable_document = "NonnegotiableDocument"
    pharmaceuticals = "Pharmaceuticals"
    medical_supplies = "MedicalSupplies"
    documents = "Documents"
