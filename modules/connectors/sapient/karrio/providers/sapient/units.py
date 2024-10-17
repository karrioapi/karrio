import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


class LabelType(lib.StrEnum):
    """Carrier specific label type"""

    PDF = "PDF"
    PNG = "PNG"
    ZPL203DPI = "ZPL203DPI"
    ZPL300DPI = "ZPL300DPI"

    """ Unified Label type mapping """

    ZPL = ZPL300DPI


class CustomsContentType(lib.StrEnum):
    gift = "Gift"
    commercial_sample = "Commercial Sample"
    documents = "Documents"
    sale_of_goods = "Sale of Goods"
    return_of_goods = "Return of Goods"
    mixed_content = "Mixed Content"
    other = "Other"

    """ Unified Customs content type mapping """

    sample = commercial_sample
    merchandise = sale_of_goods
    return_merchandise = return_of_goods


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type"""

    Letter = "Letter"
    LargeLetter = "LargeLetter"
    Parcel = "Parcel"
    PrintedPapers = "PrintedPapers"

    """ Unified Packaging type mapping """
    envelope = Letter
    pak = LargeLetter
    tube = Parcel
    pallet = Parcel
    small_box = Parcel
    medium_box = Parcel
    your_packaging = Parcel


class ShippingService(lib.StrEnum):
    """Carrier specific services"""

    # fmt: off
    sapient_royal_mail_hm_forces_mail = "BF1"
    sapient_royal_mail_hm_forces_signed_for = "BF2"
    sapient_royal_mail_hm_forces_special_delivery_500 = "BF7"
    sapient_royal_mail_hm_forces_special_delivery_1000 = "BF8"
    sapient_royal_mail_hm_forces_special_delivery_2500 = "BF9"
    sapient_royal_mail_international_business_personal_correspondence_max_sort_residue_ll = "BG1"
    sapient_royal_mail_international_business_mail_ll_max_sort_residue_standard = "BG2"
    sapient_royal_mail_international_business_personal_correspondence_max_sort_residue_l = "BP1"
    sapient_royal_mail_international_business_mail_l_max_sort_residue_standard = "BP2"
    sapient_royal_mail_international_business_printed_matter_packet = "BPI"
    sapient_royal_mail_1st_class = "BPL1"
    sapient_royal_mail_2nd_class = "BPL2"
    sapient_royal_mail_1st_class_signed_for = "BPR1"
    sapient_royal_mail_2nd_class_signed_for = "BPR2"
    sapient_royal_mail_international_business_parcel_priority_country_priced_boxable = "BXB"
    sapient_royal_mail_international_business_parcel_tracked_country_priced_boxable_extra_comp = "BXC"
    sapient_royal_mail_international_business_parcel_priority_country_priced_boxable_ddp = "BXD"
    sapient_royal_mail_international_business_parcel_tracked_country_priced_boxable_ddp = "BXE"
    sapient_royal_mail_international_business_parcel_tracked_country_priced_boxable = "BXF"
    sapient_royal_mail_24_standard_signed_for_parcel_daily_rate_service = "CRL1"
    sapient_royal_mail_48_standard_signed_for_parcel_daily_rate_service = "CRL2"
    sapient_royal_mail_international_business_parcels_zero_sort_priority = "DE4"
    sapient_royal_mail_international_business_parcels_zero_sort_priority_DE = "DE6"
    sapient_royal_mail_de_import_standard_24_parcel = "DEA"
    sapient_royal_mail_de_import_standard_24_parcel_DE = "DEB"
    sapient_royal_mail_de_import_standard_24_ll = "DEC"
    sapient_royal_mail_de_import_standard_48_ll = "DED"
    sapient_royal_mail_de_import_to_eu_tracked_signed_ll = "DEE"
    sapient_royal_mail_de_import_to_eu_max_sort_ll = "DEG"
    sapient_royal_mail_de_import_to_eu_tracked_parcel = "DEI"
    sapient_royal_mail_de_import_to_eu_tracked_signed_parcel = "DEJ"
    sapient_royal_mail_de_import_to_eu_tracked_high_vol_ll = "DEK"
    sapient_royal_mail_de_import_to_eu_max_sort_parcel = "DEM"
    sapient_royal_mail_international_business_mail_ll_country_priced_priority = "DG4"
    sapient_royal_mail_international_business_personal_correspondence_l_priority_untracked = "DP3"
    sapient_royal_mail_international_business_mail_ll_country_sort_priority = "DP6"
    sapient_royal_mail_international_business_parcels = "DW1"
    sapient_royal_mail_international_business_parcels_tracked_country_priced_extra_territorial_office_of_exchange = "ETA"
    sapient_royal_mail_international_business_parcels_tracked_signed_country_priced_extra_territorial_office_of_exchange = "ETB"
    sapient_royal_mail_international_business_parcels_zero_sort_priority_extra_territorial_office_of_exchange = "ETC"
    sapient_royal_mail_international_business_mail_tracked_ll_country_priced_extra_territorial_office_of_exchange = "ETD"
    sapient_royal_mail_international_business_mail_tracked_signed_ll_country_priced_extra_territorial_office_of_exchange = "ETE"
    sapient_royal_mail_international_business_mail_ll_country_priced_priority_extra_territorial_office_of_exchange = "ETF"
    sapient_royal_mail_international_tracked_parcels_0_30kg_extra_territorial_office_of_exchange_e = "ETG"
    sapient_royal_mail_international_tracked_parcels_0_30kg_extra_comp_extra_territorial_office_of_exchange_e = "ETH"
    sapient_royal_mail_international_tracked_parcels_0_30kg_extra_territorial_office_of_exchange_c = "ETI"
    sapient_royal_mail_international_tracked_parcels_0_30kg_extra_comp_extra_territorial_office_of_exchange_c = "ETJ"
    sapient_royal_mail_international_business_personal_correspondence_l_priority_untracked_extra_territorial_office_of_exchange = "ETK"
    sapient_royal_mail_international_business_personal_correspondence_l_tracked_high_vol_country_priced_extra_territorial_office_of_exchange = "ETL"
    sapient_royal_mail_international_business_personal_correspondence_l_tracked_signed_high_vol_country_priced_extra_territorial_office_of_exchange = "ETM"
    sapient_royal_mail_international_business_personal_correspondence_signed_l_high_vol_country_priced_extra_territorial_office_of_exchange = "ETN"
    sapient_royal_mail_international_business_personal_correspondence_ll_country_sort_priority_extra_territorial_office_of_exchange = "ETO"
    sapient_royal_mail_international_business_personal_correspondence_tracked_ll_high_vol_extra_comp_country_priced_extra_territorial_office_of_exchange = "ETP"
    sapient_royal_mail_international_business_personal_correspondence_tracked_signed_ll_high_vol_extra_comp_country_priced_extra_territorial_office_of_exchange = "ETQ"
    sapient_royal_mail_international_business_personal_correspondence_signed_ll_extra_compensation_country_priced_extra_territorial_office_of_exchange = "ETR"
    sapient_royal_mail_24_standard_signed_for_large_letter_flat_rate_service = "FS1"
    sapient_royal_mail_48_standard_signed_for_large_letter_flat_rate_service = "FS2"
    sapient_royal_mail_24_presorted_ll = "FS7"
    sapient_royal_mail_48_presorted_ll = "FS8"
    sapient_royal_mail_international_tracked_parcels_0_30kg = "HVB"
    sapient_royal_mail_international_business_tracked_express_npc = "HVD"
    sapient_royal_mail_international_tracked_parcels_0_30kg_extra_comp = "HVE"
    sapient_royal_mail_international_tracked_parcels_0_30kg_c_prio = "HVK"
    sapient_royal_mail_international_tracked_parcels_0_30kg_xcomp_c_prio = "HVL"
    sapient_royal_mail_international_business_parcels_zone_sort_priority_service = "IE1"
    sapient_royal_mail_international_business_mail_large_letter_zone_sort_priority = "IG1"
    sapient_royal_mail_international_business_mail_large_letter_zone_sort_priority_machine = "IG4"
    sapient_royal_mail_international_business_mail_letters_zone_sort_priority = "IP1"
    sapient_royal_mail_import_de_tracked_returns_24 = "ITA"
    sapient_royal_mail_import_de_tracked_returns_48 = "ITB"
    sapient_royal_mail_import_de_tracked_24_letter_boxable_high_volume = "ITC"
    sapient_royal_mail_import_de_tracked_48_letter_boxable_high_volume = "ITD"
    sapient_royal_mail_import_de_tracked_48_letter_boxable = "ITE"
    sapient_royal_mail_import_de_tracked_24_letter_boxable = "ITF"
    sapient_royal_mail_import_de_tracked_48_high_volume = "ITL"
    sapient_royal_mail_import_de_tracked_24_high_volume = "ITM"
    sapient_royal_mail_import_de_tracked_24 = "ITN"
    sapient_royal_mail_de_import_to_eu_signed_parcel = "ITR"
    sapient_royal_mail_import_de_tracked_48 = "ITS"
    sapient_royal_mail_international_business_parcels_print_direct_priority = "MB1"
    sapient_royal_mail_international_business_parcels_print_direct_standard = "MB2"
    sapient_royal_mail_international_business_parcels_signed_extra_compensation_country_priced = "MP0"
    sapient_royal_mail_international_business_parcels_tracked_zone_sort = "MP1"
    sapient_royal_mail_international_business_parcels_tracked_extra_comp_zone_sort = "MP4"
    sapient_royal_mail_international_business_parcels_signed_zone_sort = "MP5"
    sapient_royal_mail_international_business_parcels_signed_extra_compensation_zone_sort = "MP6"
    sapient_royal_mail_international_business_parcels_tracked_country_priced = "MP7"
    sapient_royal_mail_international_business_parcels_tracked_extra_comp_country_priced = "MP8"
    sapient_royal_mail_international_business_parcels_signed_country_priced = "MP9"
    sapient_royal_mail_international_business_mail_tracked_high_vol_country_priced = "MPL"
    sapient_royal_mail_international_business_mail_tracked_signed_high_vol_country_priced = "MPM"
    sapient_royal_mail_international_business_mail_signed_high_vol_country_priced = "MPN"
    sapient_royal_mail_international_business_mail_tracked_high_vol_extra_comp_country_priced = "MPO"
    sapient_royal_mail_international_business_mail_tracked_signed_high_vol_extra_comp_country_priced = "MPP"
    sapient_royal_mail_international_business_parcel_tracked_boxable_country_priced = "MPR"
    sapient_royal_mail_international_business_parcels_tracked_signed_zone_sort = "MTA"
    sapient_royal_mail_international_business_parcels_tracked_signed_extra_compensation_zone_sort = "MTB"
    sapient_royal_mail_international_business_mail_tracked_signed_zone_sort = "MTC"
    sapient_royal_mail_international_business_parcels_tracked_signed_country_priced = "MTE"
    sapient_royal_mail_international_business_parcels_tracked_signed_extra_compensation_country_priced = "MTF"
    sapient_royal_mail_international_business_mail_tracked_signed_country_priced = "MTG"
    sapient_royal_mail_international_business_mail_tracked_zone_sort = "MTI"
    sapient_royal_mail_international_business_mail_tracked_country_priced = "MTK"
    sapient_royal_mail_international_business_mail_signed_zone_sort = "MTM"
    sapient_royal_mail_international_business_mail_signed_country_priced = "MTO"
    sapient_royal_mail_international_business_mail_signed_extra_compensation_country_priced = "MTP"
    sapient_royal_mail_international_business_parcels_tracked_direct_ireland_country = "MTS"
    sapient_royal_mail_international_business_parcels_tracked_signed_ddp = "MTV"
    sapient_royal_mail_international_standard_on_account = "OLA"
    sapient_royal_mail_international_economy_on_account = "OLS"
    sapient_royal_mail_international_signed_on_account = "OSA"
    sapient_royal_mail_international_signed_on_account_extra_comp = "OSB"
    sapient_royal_mail_international_tracked_on_account = "OTA"
    sapient_royal_mail_international_tracked_on_account_extra_comp = "OTB"
    sapient_royal_mail_international_tracked_signed_on_account = "OTC"
    sapient_royal_mail_international_tracked_signed_on_account_extra_comp = "OTD"
    sapient_royal_mail_48_ll_flat_rate = "PK0"
    sapient_royal_mail_24_standard_signed_for_parcel_sort8_flat_rate_service = "PK1"
    sapient_royal_mail_48_standard_signed_for_parcel_sort8_flat_rate_service = "PK2"
    sapient_royal_mail_24_standard_signed_for_parcel_sort8_daily_rate_service = "PK3"
    sapient_royal_mail_48_standard_signed_for_parcel_sort8_daily_rate_service = "PK4"
    sapient_royal_mail_24_presorted_p = "PK7"
    sapient_royal_mail_48_presorted_p = "PK8"
    sapient_royal_mail_24_ll_flat_rate = "PK9"
    sapient_royal_mail_rm24_presorted_p_annual_flat_rate = "PKB"
    sapient_royal_mail_rm48_presorted_p_annual_flat_rate = "PKD"
    sapient_royal_mail_rm48_presorted_ll_annual_flat_rate = "PKK"
    sapient_royal_mail_rm24_presorted_ll_annual_flat_rate = "PKM"
    sapient_royal_mail_24_standard_signed_for_packetpost_flat_rate_service = "PPF1"
    sapient_royal_mail_48_standard_signed_for_packetpost_flat_rate_service = "PPF2"
    sapient_royal_mail_parcelpost_flat_rate_annual = "PPJ1"
    sapient_royal_mail_parcelpost_flat_rate_annual_PPJ = "PPJ2"
    sapient_royal_mail_rm24_ll_annual_flat_rate = "PPS"
    sapient_royal_mail_rm48_ll_annual_flat_rate = "PPT"
    sapient_royal_mail_international_business_personal_correspondence_max_sort_l = "PS5"
    sapient_royal_mail_international_business_mail_large_letter_max_sort_priority_service = "PS7"
    sapient_royal_mail_international_business_mail_letters_max_sort_standard = "PSA"
    sapient_royal_mail_international_business_mail_large_letter_max_sort_standard_service = "PSB"
    sapient_royal_mail_48_sort8p_annual_flat_rate = "RM0"
    sapient_royal_mail_24_ll_daily_rate = "RM1"
    sapient_royal_mail_24_p_daily_rate = "RM2"
    sapient_royal_mail_48_ll_daily_rate = "RM3"
    sapient_royal_mail_48_p_daily_rate = "RM4"
    sapient_royal_mail_24_p_flat_rate = "RM5"
    sapient_royal_mail_48_p_flat_rate = "RM6"
    sapient_royal_mail_24_sort8_ll_annual_flat_rate = "RM7"
    sapient_royal_mail_24_sort8_p_annual_flat_rate = "RM8"
    sapient_royal_mail_48_sort8_ll_annual_flat_rate = "RM9"
    sapient_royal_mail_special_delivery_guaranteed_by_1pm_750 = "SD1"
    sapient_royal_mail_special_delivery_guaranteed_by_1pm_1000 = "SD2"
    sapient_royal_mail_special_delivery_guaranteed_by_1pm_2500 = "SD3"
    sapient_royal_mail_special_delivery_guaranteed_by_9am_750 = "SD4"
    sapient_royal_mail_special_delivery_guaranteed_by_9am_1000 = "SD5"
    sapient_royal_mail_special_delivery_guaranteed_by_9am_2500 = "SD6"
    sapient_royal_mail_special_delivery_guaranteed_by_1pm_id_750 = "SDA"
    sapient_royal_mail_special_delivery_guaranteed_by_1pm_id_1000 = "SDB"
    sapient_royal_mail_special_delivery_guaranteed_by_1pm_id_2500 = "SDC"
    sapient_royal_mail_special_delivery_guaranteed_by_9am_id_750 = "SDE"
    sapient_royal_mail_special_delivery_guaranteed_by_9am_id_1000 = "SDF"
    sapient_royal_mail_special_delivery_guaranteed_by_9am_id_2500 = "SDG"
    sapient_royal_mail_special_delivery_guaranteed_by_1pm_age_750 = "SDH"
    sapient_royal_mail_special_delivery_guaranteed_by_1pm_age_1000 = "SDJ"
    sapient_royal_mail_special_delivery_guaranteed_by_1pm_age_2500 = "SDK"
    sapient_royal_mail_special_delivery_guaranteed_by_9am_age_750 = "SDM"
    sapient_royal_mail_special_delivery_guaranteed_by_9am_age_1000 = "SDN"
    sapient_royal_mail_special_delivery_guaranteed_by_9am_age_2500 = "SDQ"
    sapient_royal_mail_special_delivery_guaranteed_age_750 = "SDV"
    sapient_royal_mail_special_delivery_guaranteed_age_1000 = "SDW"
    sapient_royal_mail_special_delivery_guaranteed_age_2500 = "SDX"
    sapient_royal_mail_special_delivery_guaranteed_id_750 = "SDY"
    sapient_royal_mail_special_delivery_guaranteed_id_1000 = "SDZ"
    sapient_royal_mail_special_delivery_guaranteed_id_2500 = "SEA"
    sapient_royal_mail_special_delivery_guaranteed_750 = "SEB"
    sapient_royal_mail_special_delivery_guaranteed_1000 = "SEC"
    sapient_royal_mail_special_delivery_guaranteed_2500 = "SED"
    sapient_royal_mail_1st_class_standard_signed_for_letters_daily_rate_service = "STL1"
    sapient_royal_mail_2nd_class_standard_signed_for_letters_daily_rate_service = "STL2"
    sapient_royal_mail_tracked_24_high_volume_signature_age = "TPA"
    sapient_royal_mail_tracked_48_high_volume_signature_age = "TPB"
    sapient_royal_mail_tracked_24_signature_age = "TPC"
    sapient_royal_mail_tracked_48_signature_age = "TPD"
    sapient_royal_mail_tracked_48_high_volume_signature_no_signature = "TPL"
    sapient_royal_mail_tracked_24_high_volume_signature_no_signature = "TPM"
    sapient_royal_mail_tracked_24_signature_no_signature = "TPN"
    sapient_royal_mail_tracked_48_signature_no_signature = "TPS"
    sapient_royal_mail_tracked_letter_boxable_48_high_volume_signature_no_signature = "TRL"
    sapient_royal_mail_tracked_letter_boxable_24_high_volume_signature_no_signature = "TRM"
    sapient_royal_mail_tracked_letter_boxable_24_signature_no_signature = "TRN"
    sapient_royal_mail_tracked_letter_boxable_48_signature_no_signature = "TRS"
    sapient_royal_mail_tracked_returns_24 = "TSN"
    sapient_royal_mail_tracked_returns_48 = "TSS"
    sapient_royal_mail_international_business_parcels_zero_sort_priority_WE = "WE1"
    sapient_royal_mail_international_business_mail_large_letter_zero_sort_priority = "WG1"
    sapient_royal_mail_international_business_mail_large_letter_zero_sort_priority_machine = "WG4"
    sapient_royal_mail_international_business_mail_letters_zero_sort_priority = "WP1"
    # fmt: on

    @classmethod
    def carrier(cls, value: str) -> dict:
        return next((_ for _ in SAPIENT_CARRIERS if _["alias"] in value), None)

    @classmethod
    def carrier_code(cls, value: str) -> str:
        return (cls.carrier(value) or {}).get("CarrierCode")

    @classmethod
    def carrier_alias(cls, value: str) -> str:
        return (cls.carrier(value) or {}).get("alias")


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    # sapient_option = lib.OptionEnum("code")
    sapient_CL1 = lib.OptionEnum("CL1", float)
    sapient_CL2 = lib.OptionEnum("CL2", float)
    sapient_CL3 = lib.OptionEnum("CL3", float)
    sapient_CL4 = lib.OptionEnum("CL4", float)
    sapient_CL5 = lib.OptionEnum("CL5", float)
    sapient_signed = lib.OptionEnum("Signed", bool)
    sapient_SMS = lib.OptionEnum("SMS", bool)
    sapient_email = lib.OptionEnum("Email", bool)
    sapient_localcollect = lib.OptionEnum("LocalCollect", bool)
    sapient_customs_email = lib.OptionEnum("CustomsEmail")
    sapient_customs_phone = lib.OptionEnum("CustomsPhone")
    sapient_safeplace_location = lib.OptionEnum("Safeplace")

    """ Custom options """
    sapient_ebay_vtn = lib.OptionEnum("EbayVtn")
    sapient_container_id = lib.OptionEnum("ContainerId")
    sapient_business_transaction_type = lib.OptionEnum("BusinessTransactionType")

    """ Unified Option type mapping """
    insurance = sapient_CL1
    signature_confirmation = sapient_signed
    hold_at_location = sapient_localcollect


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
    on_hold = ["on_hold"]
    delivered = ["delivered"]
    in_transit = ["in_transit"]
    delivery_failed = ["delivery_failed"]
    delivery_delayed = ["delivery_delayed"]
    out_for_delivery = ["out_for_delivery"]
    ready_for_pickup = ["ready_for_pickup"]


SAPIENT_CARRIERS = [
    {
        "CarrierCode": "DX",
        "Name": "DX",
        "Description": "DX – provides create shipment, print labels, print manifest, and view item tracking sent via the DX network.",
        "alias": "dx",
    },
    {
        "CarrierCode": "EVRI",
        "Name": "EVRi",
        "Description": "Produces labels for shipments sent via the Evri network.",
        "alias": "evri",
    },
    {
        "CarrierCode": "RM",
        "Name": "Royal Mail",
        "Description": "Produces labels, required documentation, billing management for shipments sent via the Royal Mail network.",
        "alias": "royalmail",
    },
    {
        "CarrierCode": "UPS",
        "Name": "UPS",
        "Description": "Provides shipping labels, tracking services, and comprehensive shipping solutions for shipments sent via the UPS network.",
        "alias": "ups",
    },
    {
        "CarrierCode": "YODEL",
        "Name": "Yodel",
        "Description": "Produces labels, PDF manifests, Pre-advice files for shipments sent via the Yodel network.",
        "alias": "yodel",
    },
]

CUSTOM_OPTIONS = [
    ShippingOption.sapient_ebay_vtn.name,
    ShippingOption.sapient_container_id.name,
    ShippingOption.sapient_business_transaction_type.name,
]

SERVICES_DATA = [
    ["BF1", "HM Forces Mail"],
    ["BF2", "HM Forces Signed For"],
    ["BF7", "HM Forces Special Delivery (£500)"],
    ["BF8", "HM Forces Special Delivery (£1000)"],
    ["BF9", "HM Forces Special Delivery (£2500)"],
    ["BG1", "International Business Personal Correspondence Max Sort Residue (LL)"],
    ["BG2", "International Business Mail (LL) Max Sort Residue Standard"],
    ["BP1", "International Business Personal Correspondence Max Sort Residue (L)"],
    ["BP2", "International Business Mail (L) Max Sort Residue Standard"],
    ["BPI", "International Business Printed Matter Packet"],
    ["BPL1", "Royal Mail 1st Class"],
    ["BPL2", "Royal Mail 2nd Class"],
    ["BPR1", "Royal Mail 1st Class Signed For"],
    ["BPR2", "Royal Mail 2nd Class Signed For"],
    ["BXB", "International Business Parcel Priority Country Priced Boxable"],
    ["BXC", "International Business Parcel Tracked Country Priced Boxable Extra Comp"],
    ["BXD", "International Business Parcel Priority Country Priced Boxable DDP "],
    ["BXE", "International Business Parcel Tracked Country Priced Boxable DDP"],
    ["BXF", "International Business Parcel Tracked Country Priced Boxable"],
    ["CRL1", "Royal Mail 24 Standard/Signed For (Parcel - Daily Rate Service)"],
    ["CRL2", "Royal Mail 48 Standard/Signed For (Parcel - Daily Rate Service)"],
    ["DE4", "International Business Parcels Zero Sort Priority"],
    ["DE6", "International Business Parcels Zero Sort Priority"],
    ["DEA", "DE Import Standard 24 Parcel"],
    ["DEB", "DE Import Standard 24 Parcel"],
    ["DEC", "DE Import Standard 24 (LL)"],
    ["DED", "DE Import Standard 48 (LL)"],
    ["DEE", "DE Import to EU Tracked & Signed (LL)"],
    ["DEG", "DE Import to EU Max Sort (LL)"],
    ["DEI", "DE Import to EU Tracked Parcel"],
    ["DEJ", "DE Import to EU Tracked & Signed Parcel"],
    ["DEK", "DE Import to EU Tracked High Vol (LL)"],
    ["DEM", "DE Import to EU Max Sort Parcel"],
    ["DG4", "International Business Mail (LL) Country Priced Priority"],
    ["DP3", "International Business Personal Correspondence (L) Priority Untracked"],
    ["DP6", "International Business Mail (LL) Country Sort Priority"],
    ["DW1", "International Business Parcels"],
    [
        "ETA",
        "International Business Parcels Tracked Country Priced Extra-Territorial Office of Exchange",
    ],
    [
        "ETB",
        "International Business Parcels Tracked & Signed Country Priced Extra-Territorial Office of Exchange",
    ],
    [
        "ETC",
        "International Business Parcels Zero Sort Priority Extra-Territorial Office of Exchange",
    ],
    [
        "ETD",
        "International Business Mail Tracked (LL) Country Priced Extra-Territorial Office of Exchange",
    ],
    [
        "ETE",
        "International Business Mail Tracked & Signed (LL) Country Priced Extra-Territorial Office of Exchange",
    ],
    [
        "ETF",
        "International Business Mail (LL) Country Priced Priority Extra-Territorial Office of Exchange",
    ],
    [
        "ETG",
        "International Tracked Parcels 0-30kg Extra-Territorial Office of Exchange - E",
    ],
    [
        "ETH",
        "International Tracked Parcels 0-30kg Extra Comp Extra-Territorial Office of Exchange E",
    ],
    [
        "ETI",
        "International Tracked Parcels 0-30kg Extra-Territorial Office of Exchange - C",
    ],
    [
        "ETJ",
        "International Tracked Parcels 0-30kg Extra Comp Extra-Territorial Office of Exchange C",
    ],
    [
        "ETK",
        "International Business Personal Correspondence (L) Priority Untracked Extra-Territorial Office of Exchange",
    ],
    [
        "ETL",
        "International Business Personal Correspondence (L) Tracked High Vol. Country Priced Extra-Territorial Office of Exchange",
    ],
    [
        "ETM",
        "International Business Personal Correspondence (L) Tracked & Signed High Vol. Country Priced Extra-Territorial Office of Exchange",
    ],
    [
        "ETN",
        "International Business Personal Correspondence Signed (L) High Vol. Country Priced Extra-Territorial Office of Exchange",
    ],
    [
        "ETO",
        "International Business Personal Correspondence (LL) Country Sort Priority Extra-Territorial Office of Exchange",
    ],
    [
        "ETP",
        "International Business Personal Correspondence Tracked (LL) High Vol. Extra Comp Country Priced Extra-Territorial Office of Exchange",
    ],
    [
        "ETQ",
        "International Business Personal Correspondence Tracked & Signed (LL) High Vol. Extra Comp Country Priced Extra-Territorial Office of Exchange",
    ],
    [
        "ETR",
        "International Business Personal Correspondence Signed (LL) Extra Compensation Country Priced Extra-Territorial Office of Exchange",
    ],
    ["FS1", "Royal Mail 24 Standard/Signed For Large Letter (Flat Rate Service)"],
    ["FS2", "Royal Mail 48 Standard/Signed For Large Letter (Flat Rate Service)"],
    ["FS7", "Royal Mail 24 (Presorted) (LL)"],
    ["FS8", "Royal Mail 48 (Presorted) (LL)"],
    ["HVB", "International Tracked Parcels 0-30kg"],
    ["HVD", "International Business Tracked Express NPC"],
    ["HVE", "International Tracked Parcels 0-30kg Extra Comp"],
    ["HVK", "International Tracked Parcels 0-30kg C Prio"],
    ["HVL", "International Tracked Parcels 0-30kg XComp C Prio"],
    ["IE1", "International Business Parcels Zone Sort Priority Service"],
    ["IG1", "International Business Mail Large Letter Zone Sort Priority"],
    ["IG4", "International Business Mail Large Letter Zone Sort Priority Machine"],
    ["IP1", "International Business Mail Letters Zone Sort Priority"],
    ["ITA", "Import DE Tracked Returns 24"],
    ["ITB", "Import DE Tracked Returns 48"],
    ["ITC", "Import DE Tracked 24 Letter-boxable High Volume"],
    ["ITD", "Import DE Tracked 48 Letter-boxable High Volume"],
    ["ITE", "Import DE Tracked 48 Letter-boxable"],
    ["ITF", "Import DE Tracked 24 Letter-boxable"],
    ["ITL", "Import DE Tracked 48 High Volume"],
    ["ITM", "Import DE Tracked 24 High Volume"],
    ["ITN", "Import DE Tracked 24"],
    ["ITR", "DE Import to EU Signed Parcel"],
    ["ITS", "Import DE Tracked 48"],
    ["MB1", "International Business Parcels Print Direct Priority"],
    ["MB2", "International Business Parcels Print Direct Standard"],
    ["MP0", "International Business Parcels Signed Extra Compensation Country Priced"],
    ["MP1", "International Business Parcels Tracked Zone Sort"],
    ["MP4", "International Business Parcels Tracked Extra Comp Zone Sort"],
    ["MP5", "International Business Parcels Signed  Zone Sort"],
    ["MP6", "International Business Parcels Signed Extra Compensation  Zone Sort"],
    ["MP7", "International Business Parcels Tracked Country Priced"],
    ["MP8", "International Business Parcels Tracked Extra Comp Country Priced"],
    ["MP9", "International Business Parcels Signed Country Priced"],
    ["MPL", "International Business Mail Tracked High Vol. Country Priced"],
    ["MPM", "International Business Mail Tracked & Signed High Vol. Country Priced"],
    ["MPN", "International Business Mail Signed High Vol. Country Priced"],
    ["MPO", "International Business Mail Tracked High Vol. Extra Comp Country Priced"],
    [
        "MPP",
        "International Business Mail Tracked & Signed High Vol. Extra Comp Country Priced",
    ],
    ["MPR", "International Business Parcel Tracked Boxable Country Priced"],
    ["MTA", "International Business Parcels Tracked & Signed Zone Sort"],
    [
        "MTB",
        "International Business Parcels Tracked & Signed Extra Compensation Zone Sort",
    ],
    ["MTC", "International Business Mail Tracked & Signed Zone Sort"],
    ["MTE", "International Business Parcels Tracked & Signed Country Priced"],
    [
        "MTF",
        "International Business Parcels Tracked & Signed Extra Compensation Country Priced",
    ],
    ["MTG", "International Business Mail Tracked & Signed Country Priced"],
    ["MTI", "International Business Mail Tracked Zone Sort"],
    ["MTK", "International Business Mail Tracked Country Priced"],
    ["MTM", "International Business Mail Signed Zone Sort"],
    ["MTO", "International Business Mail Signed Country Priced"],
    ["MTP", "International Business Mail Signed Extra Compensation Country Priced"],
    ["MTS", "International Business Parcels Tracked Direct Ireland Country"],
    ["MTV", "International Business Parcels Tracked & Signed DDP"],
    ["OLA", "International Standard On Account"],
    ["OLS", "International Economy On Account"],
    ["OSA", "International Signed On Account"],
    ["OSB", "International Signed On Account Extra Comp"],
    ["OTA", "International Tracked On Account"],
    ["OTB", "International Tracked On Account Extra Comp"],
    ["OTC", "International Tracked & Signed On Account"],
    ["OTD", "International Tracked & Signed On Account Extra Comp"],
    ["PK0", "Royal Mail 48 (LL) Flat Rate"],
    ["PK1", "Royal Mail 24 Standard/Signed For (Parcel - Sort8 - Flat Rate Service)"],
    ["PK2", "Royal Mail 48 Standard/Signed For (Parcel - Sort8 - Flat Rate Service)"],
    ["PK3", "Royal Mail 24 Standard/Signed For (Parcel - Sort8 - Daily Rate Service)"],
    ["PK4", "Royal Mail 48 Standard/Signed For (Parcel - Sort8 - Daily Rate Service)"],
    ["PK7", "Royal Mail 24 (Presorted) (P)"],
    ["PK8", "Royal Mail 48 (Presorted) (P)"],
    ["PK9", "Royal Mail 24 (LL) Flat Rate"],
    ["PKB", "RM24 (Presorted) (P) Annual Flat Rate"],
    ["PKD", "RM48 (Presorted) (P) Annual Flat Rate"],
    ["PKK", "RM48 (Presorted) (LL) Annual Flat Rate"],
    ["PKM", "RM24 (Presorted) (LL) Annual Flat Rate"],
    ["PPF1", "Royal Mail 24 Standard/Signed For (Packetpost- Flat Rate Service)"],
    ["PPF2", "Royal Mail 48 Standard/Signed For (Packetpost- Flat Rate Service)"],
    ["PPJ1", "Parcelpost Flat Rate (Annual)"],
    ["PPJ2", "Parcelpost Flat Rate (Annual)"],
    ["PPS", "RM24 (LL) Annual Flat Rate"],
    ["PPT", "RM48 (LL) Annual Flat Rate"],
    ["PS5", "International Business Personal Correspondence Max Sort (L)"],
    ["PS7", "International Business Mail Large Letter Max Sort Priority Service"],
    ["PSA", "International Business Mail Letters Max Sort Standard"],
    ["PSB", "International Business Mail Large Letter Max Sort Standard Service"],
    ["RM0", "Royal Mail 48 (Sort8)(P) Annual Flat Rate"],
    ["RM1", "Royal Mail 24 (LL) Daily Rate"],
    ["RM2", "Royal Mail 24 (P) Daily Rate"],
    ["RM3", "Royal Mail 48 (LL) Daily Rate"],
    ["RM4", "Royal Mail 48 (P) Daily Rate"],
    ["RM5", "Royal Mail 24 (P) Flat Rate"],
    ["RM6", "Royal Mail 48 (P) Flat Rate"],
    ["RM7", "Royal Mail 24 (SORT8) (LL) Annual Flat Rate"],
    ["RM8", "Royal Mail 24 (SORT8) (P) Annual Flat Rate"],
    ["RM9", "Royal Mail 48 (SORT8) (LL) Annual Flat Rate"],
    ["SD1", "Special Delivery Guaranteed By 1PM (£750)"],
    ["SD2", "Special Delivery Guaranteed By 1PM (£1000)"],
    ["SD3", "Special Delivery Guaranteed By 1PM (£2500)"],
    ["SD4", "Special Delivery Guaranteed By 9AM (£750)"],
    ["SD5", "Special Delivery Guaranteed By 9AM (£1000)"],
    ["SD6", "Special Delivery Guaranteed By 9AM (£2500)"],
    ["SDA", "Special Delivery Guaranteed By 1PM (ID) (£750)"],
    ["SDB", "Special Delivery Guaranteed By 1PM (ID) (£1000)"],
    ["SDC", "Special Delivery Guaranteed By 1PM (ID) (£2500)"],
    ["SDE", "Special Delivery Guaranteed By 9AM (ID) (£750)"],
    ["SDF", "Special Delivery Guaranteed By 9AM (ID) (£1000)"],
    ["SDG", "Special Delivery Guaranteed By 9AM (ID) (£2500)"],
    ["SDH", "Special Delivery Guaranteed By 1PM (AGE) (£750)"],
    ["SDJ", "Special Delivery Guaranteed By 1PM (AGE) (£1000)"],
    ["SDK", "Special Delivery Guaranteed By 1PM (AGE) (£2500)"],
    ["SDM", "Special Delivery Guaranteed By 9AM (AGE) (£750)"],
    ["SDN", "Special Delivery Guaranteed By 9AM (AGE) (£1000)"],
    ["SDQ", "Special Delivery Guaranteed By 9AM (AGE) (£2500)"],
    ["SDV", "Special Delivery Guaranteed (AGE) (£750)"],
    ["SDW", "Special Delivery Guaranteed (AGE) (£1000)"],
    ["SDX", "Special Delivery Guaranteed (AGE) (£2500)"],
    ["SDY", "Special Delivery Guaranteed (ID) (£750)"],
    ["SDZ", "Special Delivery Guaranteed (ID) (£1000)"],
    ["SEA", "Special Delivery Guaranteed (ID) (£2500)"],
    ["SEB", "Special Delivery Guaranteed (£750)"],
    ["SEC", "Special Delivery Guaranteed (£1000)"],
    ["SED", "Special Delivery Guaranteed (£2500)"],
    ["STL1", "Royal Mail 1st Class Standard/Signed For (Letters - Daily Rate service)"],
    ["STL2", "Royal Mail 2nd Class Standard/Signed For (Letters - Daily Rate service)"],
    ["TPA", "Tracked 24 High Volume Signature (AGE)"],
    ["TPB", "Tracked 48 High Volume Signature (AGE)"],
    ["TPC", "Tracked 24 Signature (AGE)"],
    ["TPD", "Tracked 48 Signature (AGE)"],
    ["TPL", "Tracked 48 High Volume Signature / No Signature"],
    ["TPM", "Tracked 24 High Volume Signature / No Signature"],
    ["TPN", "Tracked 24 Signature / No Signature"],
    ["TPS", "Tracked 48 Signature / No Signature"],
    ["TRL", "Tracked Letter-Boxable 48 High Volume Signature / No Signature"],
    ["TRM", "Tracked Letter-Boxable 24 High Volume Signature / No Signature"],
    ["TRN", "Tracked Letter-Boxable 24 Signature / No Signature"],
    ["TRS", "Tracked Letter-Boxable 48 Signature / No Signature"],
    ["TSN", "Tracked Returns 24"],
    ["TSS", "Tracked Returns 48"],
    ["WE1", "International Business Parcels Zero Sort Priority"],
    ["WG1", "International Business Mail Large Letter Zero Sort Priority"],
    ["WG4", "International Business Mail Large Letter Zero Sort Priority Machine"],
    ["WP1", "International Business Mail Letters Zero Sort Priority"],
]

DEFAULT_SERVICES = [
    models.ServiceLevel(
        service_name=__,
        service_code=ShippingService.map(_).name_or_key,
        carrier_service_code=_,
        currency="GBP",
        domicile=not "International" in __,
        international="International" in __,
        zones=[models.ServiceZone(rate=2.80)],
    )
    for _, __ in SERVICES_DATA
]

ShippingCarrier = lib.Enum(
    "ShippingCarrier",
    {carrier["alias"]: carrier["CarrierCode"] for carrier in SAPIENT_CARRIERS},
)
