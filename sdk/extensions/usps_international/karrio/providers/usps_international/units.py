"""Karrio USPS International units module"""

import typing
from karrio.core import units
from karrio.core.utils import Enum
from karrio.core.models import Address
from karrio.core.utils.enum import OptionEnum


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
    legal_envelope = "LEGALENVELOPE"
    usps_gxg_envelope = "USPSGXGENVELOPE"
    usps_gxg_legal_envelope = "USPSGXGLEGALENVELOPE"
    usps_gxg_tyvek_envelope = "USPSGXGTYVEKENVELOPE"

    """ Unified Packaging type mapping """
    pak = large_envelope
    tube = package
    pallet = package
    small_box = package
    medium_box = package
    your_packaging = package


class ShippingOption(Enum):
    usps_registered_mail = OptionEnum("103")
    usps_insurance_global_express_guaranteed = OptionEnum("106", float)
    usps_insurance_express_mail_international = OptionEnum("107", float)
    usps_insurance_priority_mail_international = OptionEnum("108", float)
    usps_return_receipt = OptionEnum("105")
    usps_certificate_of_mailing = OptionEnum("100")
    usps_electronic_usps_delivery_confirmation_international = OptionEnum("109")

    """ Non official options """
    usps_option_machinable_item = OptionEnum("usps_option_machinable_item", bool)
    usps_option_abandon_non_delivery = OptionEnum("ABANDON")
    usps_option_return_non_delivery = OptionEnum("RETURN")
    usps_option_redirect_non_delivery = OptionEnum("REDIRECT", Address)

    @classmethod
    def insurance_from(
        cls, options: units.Options, service_key: str
    ) -> typing.Optional[float]:
        return next(
            (
                value.state
                for key, value in options
                if "usps_insurance" in key and service_key in key
            ),
            options.insurance.state,
        )

    @classmethod
    def non_delivery_from(cls, options: units.Options) -> typing.Optional[str]:
        # Gets the first provided non delivery option or default to "RETURN"
        return next(
            (value.state for name, value in options if "non_delivery" in name),
            "RETURN",
        )


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

    def items_filter(code: str) -> bool:
        return code in ShippingOption and "usps_option" not in code  # type: ignore

    return units.ShippingOptions(_options, ShippingOption, items_filter=items_filter)


class ShippingService(Enum):
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
    usps_priority_mail_express_international = "1"
    usps_priority_mail_international = "2"
    usps_global_express_guaranteed_gxg = "4"
    usps_global_express_guaranteed_document = "5"
    usps_global_express_guaranteed_non_document_rectangular = "6"
    usps_global_express_guaranteed_non_document_non_rectangular = "7"
    usps_priority_mail_international_flat_rate_envelope = "8"
    usps_priority_mail_international_medium_flat_rate_box = "9"
    usps_priority_mail_express_international_flat_rate_envelope = "10"
    usps_priority_mail_international_large_flat_rate_box = "11"
    usps_global_express_guaranteed_envelopes = "12"
    usps_first_class_mail_international_letter = "13"
    usps_first_class_mail_international_large_envelope = "14"
    usps_first_class_package_international_service = "15"
    usps_priority_mail_international_small_flat_rate_box = "16"
    usps_priority_mail_express_international_legal_flat_rate_envelope = "17"
    usps_priority_mail_international_gift_card_flat_rate_envelope = "18"
    usps_priority_mail_international_window_flat_rate_envelope = "19"
    usps_priority_mail_international_small_flat_rate_envelope = "20"
    usps_first_class_mail_international_postcard = "21"
    usps_priority_mail_international_legal_flat_rate_envelope = "22"
    usps_priority_mail_international_padded_flat_rate_envelope = "23"
    usps_priority_mail_international_dvd_flat_rate_priced_box = "24"
    usps_priority_mail_international_large_video_flat_rate_priced_box = "25"
    usps_priority_mail_express_international_padded_flat_rate_envelope = "27"


class ServiceType(Enum):
    usps_global_express_guaranteed = "GXG"
    usps_first_class_mail_international = "First-Class Mail International"
    usps_priority_mail_international = "Priority Mail International"
    usps_priority_mail_express_international = "Priority Mail Express International"

    """ ShipmentService type correspondence """
    usps_global_express_guaranteed_gxg = usps_global_express_guaranteed
    usps_global_express_guaranteed_document = usps_global_express_guaranteed
    usps_global_express_guaranteed_envelopes = usps_global_express_guaranteed
    usps_global_express_guaranteed_non_document_rectangular = (
        usps_global_express_guaranteed
    )
    usps_global_express_guaranteed_non_document_non_rectangular = (
        usps_global_express_guaranteed
    )
    usps_priority_mail_international_flat_rate_envelope = (
        usps_priority_mail_international
    )
    usps_priority_mail_international_medium_flat_rate_box = (
        usps_priority_mail_international
    )
    usps_priority_mail_express_international_flat_rate_envelope = (
        usps_priority_mail_express_international
    )
    usps_priority_mail_international_large_flat_rate_box = (
        usps_priority_mail_international
    )
    usps_first_class_mail_international_letter = usps_first_class_mail_international
    usps_first_class_mail_international_large_envelope = (
        usps_first_class_mail_international
    )
    usps_first_class_package_international_service = usps_first_class_mail_international
    usps_priority_mail_international_small_flat_rate_box = (
        usps_priority_mail_international
    )
    usps_priority_mail_express_international_legal_flat_rate_envelope = (
        usps_priority_mail_express_international
    )
    usps_priority_mail_international_gift_card_flat_rate_envelope = (
        usps_priority_mail_international
    )
    usps_priority_mail_international_window_flat_rate_envelope = (
        usps_priority_mail_international
    )
    usps_priority_mail_international_small_flat_rate_envelope = (
        usps_priority_mail_international
    )
    usps_first_class_mail_international_postcard = usps_first_class_mail_international
    usps_priority_mail_international_legal_flat_rate_envelope = (
        usps_priority_mail_international
    )
    usps_priority_mail_international_padded_flat_rate_envelope = (
        usps_priority_mail_international
    )
    usps_priority_mail_international_dvd_flat_rate_priced_box = (
        usps_priority_mail_international
    )
    usps_priority_mail_international_large_video_flat_rate_priced_box = (
        usps_priority_mail_international
    )
    usps_priority_mail_express_international_padded_flat_rate_envelope = (
        usps_priority_mail_express_international
    )
