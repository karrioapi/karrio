"""Purplship USPS enumerations module"""

from purplship.core.utils import Enum, Flag, Spec


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


class PackagingType(Flag):
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


class FirstClassMailType(Flag):
    flat = "FLAT"
    letter = "LETTER"
    postcard = "POSTCARD"
    package_service = "PACKAGE SERVICE"
    package_service_retail = "PACKAGE SERVICE RETAIL"

    """ Packaging type correspondence """
    variable = package_service
    flat_rate_envelope = flat
    padded_flat_rate_envelope = flat
    legal_flat_rate_envelope = flat
    sm_flat_rate_envelope = flat
    window_flat_rate_envelope = flat
    gift_card_flat_rate_envelope = postcard
    sm_flat_rate_box = package_service
    md_flat_rate_box = package_service
    lg_flat_rate_box = package_service
    cubic_parcels = package_service
    cubic_soft_pack = package_service
    regional_rate_box_a = package_service_retail
    regional_rate_box_b = package_service_retail


class SortLevelType(Flag):
    letter = "LETTER"
    large_envelope = "LARGEENVELOPE"
    package = "PACKAGE"
    flat_rate = "FLATRATE"

    """ Packaging type correspondence """
    variable = package
    sm_flat_rate_box = flat_rate
    md_flat_rate_box = flat_rate
    lg_flat_rate_box = flat_rate
    flat_rate_envelope = flat_rate
    sm_flat_rate_envelope = flat_rate
    legal_flat_rate_envelope = flat_rate
    gift_card_flat_rate_envelope = flat_rate
    padded_flat_rate_envelope = large_envelope
    window_flat_rate_envelope = large_envelope
    cubic_parcels = package
    cubic_soft_pack = package
    regional_rate_box_a = package
    regional_rate_box_b = package


class ShipmentOption(Enum):
    usps_insurance = Spec.asValue("100", float)
    usps_insurance_priority_mail_express = Spec.asValue("101", float)
    usps_return_receipt = Spec.asKey("102")
    usps_collect_on_delivery = Spec.asKey("103")
    usps_certificate_of_mailing_form_3665 = Spec.asKey("104")
    usps_certified_mail = Spec.asKey("105")
    usps_tracking = Spec.asKey("106")
    usps_signature_confirmation = Spec.asKey("108")
    usps_registered_mail = Spec.asKey("109")
    usps_return_receipt_electronic = Spec.asKey("110")
    usps_registered_mail_cod_collection_charge = Spec.asKey("112")
    usps_return_receipt_priority_mail_express = Spec.asKey("118")
    usps_adult_signature_required = Spec.asKey("119")
    usps_adult_signature_restricted_delivery = Spec.asKey("120")
    usps_insurance_priority_mail = Spec.asValue("125", float)
    usps_tracking_electronic = Spec.asKey("155")
    usps_signature_confirmation_electronic = Spec.asKey("156")
    usps_certificate_of_mailing_form_3817 = Spec.asKey("160")
    usps_priority_mail_express_10_30_am_delivery = Spec.asKey("161")
    usps_certified_mail_restricted_delivery = Spec.asKey("170")
    usps_certified_mail_adult_signature_required = Spec.asKey("171")
    usps_certified_mail_adult_signature_restricted_delivery = Spec.asKey("172")
    usps_signature_confirm_restrict_delivery = Spec.asKey("173")
    usps_signature_confirmation_electronic_restricted_delivery = Spec.asKey("174")
    usps_collect_on_delivery_restricted_delivery = Spec.asKey("175")
    usps_registered_mail_restricted_delivery = Spec.asKey("176")
    usps_insurance_restricted_delivery = Spec.asValue("177", float)
    usps_insurance_restrict_delivery_priority_mail = Spec.asValue("179", float)
    usps_insurance_restrict_delivery_priority_mail_express = Spec.asValue("178", float)
    usps_insurance_restrict_delivery_bulk_only = Spec.asValue("180", float)
    usps_scan_retention = Spec.asKey("181")
    usps_scan_signature_retention = Spec.asKey("182")
    usps_special_handling_fragile = Spec.asKey("190")

    """ Non official options """
    usps_option_machinable_item = Spec.asFlag("usps_option_machinable_item")
    usps_option_ground_only = Spec.asFlag("usps_option_ground_only")
    usps_option_return_service_info = Spec.asFlag("usps_option_return_service_info")
    usps_option_ship_info = Spec.asFlag("usps_option_ship_info")

    """ Unified Shipment Option type mapping """
    insurance = usps_insurance


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


class ServiceClassID(Enum):
    usps_first_class = "0"
    usps_first_class_mail_large_envelope = usps_first_class
    usps_first_class_mail_lt_letter = usps_first_class
    usps_first_class_mail_lt_parcel = usps_first_class
    usps_first_class_mail_postcards = usps_first_class
    usps_priority_mail = "1"
    usps_priority_mail_express_hold_for_pickup = "2"
    usps_priority_mail_express = "3"
    usps_standard_post = "4"
    usps_media_mail = "6"
    usps_library_mail = "7"
    usps_priority_mail_express_flat_rate_envelope = "13"
    usps_first_class_mail_large_postcards = "15"
    usps_priority_mail_flat_rate_envelope = "16"
    usps_priority_mail_medium_flat_rate_box = "17"
    usps_priority_mail_large_flat_rate_box = "22"
    usps_priority_mail_express_sunday_holiday_delivery = "23"
    usps_priority_mail_express_sunday_holiday_delivery_flat_rate_envelope = "25"
    usps_priority_mail_express_flat_rate_envelope_hold_for_pickup = "27"
    usps_priority_mail_small_flat_rate_box = "28"
    usps_priority_mail_padded_flat_rate_envelope = "29"
    usps_priority_mail_express_legal_flat_rate_envelope = "30"
    usps_priority_mail_express_legal_flat_rate_envelope_hold_for_pickup = "31"
    usps_priority_mail_express_sunday_holiday_delivery_legal_flat_rate_envelope = "32"
    usps_priority_mail_hold_for_pickup = "33"
    usps_priority_mail_large_flat_rate_box_hold_for_pickup = "34"
    usps_priority_mail_medium_flat_rate_box_hold_for_pickup = "35"
    usps_priority_mail_small_flat_rate_box_hold_for_pickup = "36"
    usps_priority_mail_flat_rate_envelope_hold_for_pickup = "37"
    usps_priority_mail_gift_card_flat_rate_envelope = "38"
    usps_priority_mail_gift_card_flat_rate_envelope_hold_for_pickup = "39"
    usps_priority_mail_window_flat_rate_envelope = "40"
    usps_priority_mail_window_flat_rate_envelope_hold_for_pickup = "41"
    usps_priority_mail_small_flat_rate_envelope = "42"
    usps_priority_mail_small_flat_rate_envelope_hold_for_pickup = "43"
    usps_priority_mail_legal_flat_rate_envelope = "44"
    usps_priority_mail_legal_flat_rate_envelope_hold_for_pickup = "45"
    usps_priority_mail_padded_flat_rate_envelope_hold_for_pickup = "46"
    usps_priority_mail_regional_rate_box_a = "47"
    usps_priority_mail_regional_rate_box_a_hold_for_pickup = "48"
    usps_priority_mail_regional_rate_box_b = "49"
    usps_priority_mail_regional_rate_box_b_hold_for_pickup = "50"
    usps_first_class_package_service_hold_for_pickup = "53"
    usps_priority_mail_express_flat_rate_boxes = "55"
    usps_priority_mail_express_flat_rate_boxes_hold_for_pickup = "56"
    usps_priority_mail_express_sunday_holiday_delivery_flat_rate_boxes = "57"
    usps_priority_mail_regional_rate_box_c = "58"
    usps_priority_mail_regional_rate_box_c_hold_for_pickup = "59"
    usps_first_class_package_service = "61"
    usps_priority_mail_express_padded_flat_rate_envelope = "62"
    usps_priority_mail_express_padded_flat_rate_envelope_hold_for_pickup = "63"
    usps_priority_mail_express_sunday_holiday_delivery_padded_flat_rate_envelope = "64"


class ServiceType(Enum):
    usps_bpm = "BPM"
    usps_media = "MEDIA"
    usps_library = "LIBRARY"
    usps_priority = "PRIORITY"
    usps_first_class = "FIRST CLASS"
    usps_priority_mail_express = "PRIORITY EXPRESS"
    usps_priority_mail_cubic = "PRIORITY MAIL CUBIC"
    usps_parcel_select_ground = "PARCEL SELECT GROUND"

    """ ShipmentService type correspondence """
    usps_first_class_mail_large_envelope = usps_first_class
    usps_first_class_mail_lt_letter = usps_first_class
    usps_first_class_mail_lt_parcel = usps_first_class
    usps_first_class_mail_postcards = usps_first_class
    usps_first_class_mail_large_postcards = usps_first_class
    usps_priority_mail = usps_priority
    usps_priority_mail_express_hold_for_pickup = usps_priority_mail_express
    usps_standard_post = usps_parcel_select_ground
    usps_media_mail = usps_media
    usps_library_mail = usps_library
    usps_priority_mail_express_flat_rate_envelope = usps_priority_mail_express
    usps_priority_mail_flat_rate_envelope = usps_priority
    usps_priority_mail_medium_flat_rate_box = usps_priority_mail_cubic
    usps_priority_mail_large_flat_rate_box = usps_priority_mail_cubic
    usps_priority_mail_express_sunday_holiday_delivery = usps_priority_mail_express
    usps_priority_mail_express_sunday_holiday_delivery_flat_rate_envelope = usps_priority_mail_express
    usps_priority_mail_express_flat_rate_envelope_hold_for_pickup = usps_priority_mail_express
    usps_priority_mail_small_flat_rate_box = usps_priority
    usps_priority_mail_padded_flat_rate_envelope = usps_priority
    usps_priority_mail_express_legal_flat_rate_envelope = usps_priority_mail_express
    usps_priority_mail_express_legal_flat_rate_envelope_hold_for_pickup = usps_priority_mail_express
    usps_priority_mail_express_sunday_holiday_delivery_legal_flat_rate_envelope = usps_priority_mail_express
    usps_priority_mail_hold_for_pickup = usps_priority_mail_cubic
    usps_priority_mail_large_flat_rate_box_hold_for_pickup = usps_priority_mail_cubic
    usps_priority_mail_medium_flat_rate_box_hold_for_pickup = usps_priority_mail_cubic
    usps_priority_mail_small_flat_rate_box_hold_for_pickup = usps_priority_mail_cubic
    usps_priority_mail_flat_rate_envelope_hold_for_pickup = usps_priority
    usps_priority_mail_gift_card_flat_rate_envelope = usps_priority
    usps_priority_mail_gift_card_flat_rate_envelope_hold_for_pickup = usps_priority
    usps_priority_mail_window_flat_rate_envelope = usps_priority
    usps_priority_mail_window_flat_rate_envelope_hold_for_pickup = usps_priority
    usps_priority_mail_small_flat_rate_envelope = usps_priority
    usps_priority_mail_small_flat_rate_envelope_hold_for_pickup = usps_priority
    usps_priority_mail_legal_flat_rate_envelope = usps_priority
    usps_priority_mail_legal_flat_rate_envelope_hold_for_pickup = usps_priority
    usps_priority_mail_padded_flat_rate_envelope_hold_for_pickup = usps_priority
    usps_priority_mail_regional_rate_box_a = usps_priority_mail_cubic
    usps_priority_mail_regional_rate_box_a_hold_for_pickup = usps_priority_mail_cubic
    usps_priority_mail_regional_rate_box_b = usps_priority_mail_cubic
    usps_priority_mail_regional_rate_box_b_hold_for_pickup = usps_priority_mail_cubic
    usps_first_class_package_service_hold_for_pickup = usps_first_class
    usps_priority_mail_express_flat_rate_boxes = usps_priority_mail_express
    usps_priority_mail_express_flat_rate_boxes_hold_for_pickup = usps_priority_mail_express
    usps_priority_mail_express_sunday_holiday_delivery_flat_rate_boxes = usps_priority_mail_express
    usps_priority_mail_regional_rate_box_c = usps_priority_mail_cubic
    usps_priority_mail_regional_rate_box_c_hold_for_pickup = usps_priority_mail_cubic
    usps_first_class_package_service = usps_first_class
    usps_priority_mail_express_padded_flat_rate_envelope = usps_priority_mail_express
    usps_priority_mail_express_padded_flat_rate_envelope_hold_for_pickup = usps_priority_mail_express
    usps_priority_mail_express_sunday_holiday_delivery_padded_flat_rate_envelope = usps_priority_mail_express
