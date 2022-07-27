""" DHL Native Types """

import typing
from karrio.core.utils import Enum, Flag
from karrio.core import units
from karrio.core.utils.enum import OptionEnum

PRESET_DEFAULTS = dict(dimension_unit="CM", weight_unit="KG")


class PackagePresets(Flag):
    dhl_express_envelope = units.PackagePreset(
        **dict(
            weight=0.5, width=35.0, height=27.5, length=1.0, packaging_type="envelope"
        ),
        **PRESET_DEFAULTS
    )
    dhl_express_standard_flyer = units.PackagePreset(
        **dict(weight=2.0, width=40.0, height=30.0, length=1.5, packaging_type="pak"),
        **PRESET_DEFAULTS
    )
    dhl_express_large_flyer = units.PackagePreset(
        **dict(weight=3.0, width=47.5, height=37.5, length=1.5, packaging_type="pak"),
        **PRESET_DEFAULTS
    )
    dhl_express_box_2 = units.PackagePreset(
        **dict(
            weight=1.0,
            width=33.7,
            height=18.2,
            length=10.0,
            packaging_type="medium_box",
        ),
        **PRESET_DEFAULTS
    )
    dhl_express_box_3 = units.PackagePreset(
        **dict(
            weight=2.0, width=33.6, height=32.0, length=5.2, packaging_type="medium_box"
        ),
        **PRESET_DEFAULTS
    )
    dhl_express_box_4 = units.PackagePreset(
        **dict(
            weight=5.0,
            width=33.7,
            height=32.2,
            length=18.0,
            packaging_type="medium_box",
        ),
        **PRESET_DEFAULTS
    )
    dhl_express_box_5 = units.PackagePreset(
        **dict(
            weight=10.0,
            width=33.7,
            height=32.2,
            length=34.5,
            packaging_type="medium_box",
        ),
        **PRESET_DEFAULTS
    )
    dhl_express_box_6 = units.PackagePreset(
        **dict(
            weight=15.0,
            width=41.7,
            height=35.9,
            length=36.9,
            packaging_type="large_box",
        ),
        **PRESET_DEFAULTS
    )
    dhl_express_box_7 = units.PackagePreset(
        **dict(
            weight=20.0,
            width=48.1,
            height=40.4,
            length=38.9,
            packaging_type="large_box",
        ),
        **PRESET_DEFAULTS
    )
    dhl_express_box_8 = units.PackagePreset(
        **dict(
            weight=25.0,
            width=54.2,
            height=44.4,
            length=40.9,
            packaging_type="large_box",
        ),
        **PRESET_DEFAULTS
    )
    dhl_express_tube = units.PackagePreset(
        **dict(weight=5.0, width=96.0, height=15.0, length=15.0, packaging_type="tube"),
        **PRESET_DEFAULTS
    )
    dhl_didgeridoo_box = units.PackagePreset(
        **dict(
            weight=10.0,
            width=13.0,
            height=13.0,
            length=162.0,
            packaging_type="medium_box",
        ),
        **PRESET_DEFAULTS
    )
    dhl_jumbo_box = units.PackagePreset(
        **dict(
            weight=30.0,
            width=45.0,
            height=42.7,
            length=33.0,
            packaging_type="medium_box",
        ),
        **PRESET_DEFAULTS
    )
    dhl_jumbo_box_junior = units.PackagePreset(
        **dict(
            weight=20.0,
            width=39.9,
            height=34.0,
            length=24.1,
            packaging_type="medium_box",
        ),
        **PRESET_DEFAULTS
    )


MeasurementOptions = units.MeasurementOptionsType(min_in=1, min_cm=1)
UNSUPPORTED_PAPERLESS_COUNTRIES = ["JM"]


class LabelType(Flag):
    PDF_6x4 = ("PDF", "6X4_PDF")
    PDF_8x4 = ("PDF", "8X4_PDF")
    PDF_8x4_A4 = ("PDF", "8X4_A4_PDF")
    PDF_6x4_A4 = ("PDF", "6X4_A4_PDF")
    PDF_8x4_CI = ("PDF", "8X4_CI_PDF")
    PDF_8x4_RU_A4 = ("PDF", "8X4_RU_A4_PDF")
    ZPL_8x4 = ("ZPL2", "8X4_thermal")
    ZPL_6x4 = ("ZPL2", "6X4_thermal")
    ZPL_8x4_CI = ("ZPL2", "8X4_CI_thermal")

    """ Unified Label type mapping """
    PDF = PDF_6x4
    ZPL = ZPL_6x4


class Incoterm(Enum):
    EXW = "Ex Works"
    FCA = "Free Carrier"
    CPT = "Carriage Paid To"
    CFR = "CFR Cost and Freight"
    CIP = "Carriage and Insurance Paid To"
    CIF = "CIF Cost, Insurance and Freight"
    DAT = "Delivered At Terminal"
    DAP = "Delivered At Place"
    DDP = "Delivered Duty Paid"
    FAS = "FAS Free Alongside Ship"
    FOB = "FOB Free On Board"


class ExportReasonCode(Enum):
    permanent = "P"
    temporary = "T"
    return_for_repair = "R"
    used_exhibition_goods_to_origin = "M"
    intercompany_use = "I"
    commercial_purpose_or_sale = "C"
    personal_belongings_or_personal_use = "E"
    sample = "S"
    gift = "G"
    return_to_origin = "U"
    warranty_replacement = "W"
    diplmatic_goods = "D"
    defenece_material = "F"

    """ Unified Customs Content type mapping """
    other = None
    documents = other
    merchandise = commercial_purpose_or_sale
    return_merchandise = return_to_origin


class PaymentType(Enum):
    sender = "S"
    recipient = "R"
    third_party = "T"


class DimensionUnit(Enum):
    CM = "C"
    IN = "I"


class WeightUnit(Enum):
    KG = "K"
    LB = "L"


class DeliveryType(Enum):
    door_to_door = "DD"
    door_to_airport = "DA"
    airport_to_airport = "AA"
    door_to_door_c = "DC"


class DCTPackageType(Enum):
    dhl_flyer_smalls = "FLY"
    dhl_parcels_conveyables = "COY"
    dhl_non_conveyables = "NCY"
    dhl_pallets = "PAL"
    dhl_double_pallets = "DBL"
    dhl_box = "BOX"

    """ Unified Packaging type mapping """
    envelope = dhl_flyer_smalls
    pak = dhl_flyer_smalls
    tube = dhl_parcels_conveyables
    pallet = dhl_pallets
    small_box = dhl_box
    medium_box = dhl_box
    large_box = dhl_box
    your_packaging = dhl_box


class NetworkType(Enum):
    both_time_and_day_definite = "AL"
    day_definite = "DD"
    time_definite = "TD"


class PackageType(Flag):
    dhl_jumbo_document = "BD"
    dhl_jumbo_parcel = "BP"
    dhl_customer_provided = "CP"
    dhl_document = "DC"
    dhl_flyer = "DF"
    dhl_domestic = "DM"
    dhl_express_document = "ED"
    dhl_express_envelope = "EE"
    dhl_freight = "FR"
    dhl_jumbo_box = "JB"
    dhl_jumbo_junior_document = "JD"
    dhl_junior_jumbo_box = "JJ"
    dhl_jumbo_junior_parcel = "JP"
    dhl_other_dhl_packaging = "OD"
    dhl_parcel = "PA"
    dhl_your_packaging = "YP"

    """ Unified Packaging type mapping """
    envelope = dhl_express_envelope
    pak = dhl_flyer
    tube = dhl_other_dhl_packaging
    pallet = dhl_freight
    small_box = dhl_junior_jumbo_box
    medium_box = dhl_jumbo_box
    large_box = dhl_jumbo_parcel
    your_packaging = dhl_your_packaging


class ProductCode(Enum):
    dhl_logistics_services = "0"
    dhl_domestic_express_12_00_doc = "1"
    dhl_b2_c_doc = "2"
    dhl_b2_c_nondoc = "3"
    dhl_jetline = "4"
    dhl_sprintline = "5"
    dhl_express_easy_doc = "7"
    dhl_express_easy_nondoc = "8"
    dhl_europack_doc = "9"
    dhl_auto_reversals = "A"
    dhl_breakbulk_express_doc = "B"
    dhl_medical_express_doc = "C"
    dhl_express_worldwide_doc = "D"
    dhl_express_9_00_nondoc = "E"
    dhl_freight_worldwide_nondoc = "F"
    dhl_domestic_economy_select_doc = "G"
    dhl_economy_select_nondoc = "H"
    dhl_domestic_express_9_00_doc = "I"
    dhl_jumbo_box_nondoc = "J"
    dhl_express_9_00_doc = "K"
    dhl_express_10_30_doc = "L"
    dhl_express_10_30_nondoc = "M"
    dhl_domestic_express_doc = "N"
    dhl_domestic_express_10_30_doc = "O"
    dhl_express_worldwide_nondoc = "P"
    dhl_medical_express_nondoc = "Q"
    dhl_globalmail_business_doc = "R"
    dhl_same_day_doc = "S"
    dhl_express_12_00_doc = "T"
    dhl_express_worldwide_ecx_doc = "U"
    dhl_europack_nondoc = "V"
    dhl_economy_select_doc = "W"
    dhl_express_envelope_doc = "X"
    dhl_express_12_00_nondoc = "Y"
    dhl_destination_charges = "Z"


def shipping_services_initializer(
    products: typing.List[str],
    is_international: bool = True,
    is_document: bool = False,
    is_envelope: bool = False,
) -> typing.List[str]:
    """
    Apply default product codes to the list of products.
    """
    if not any(_ for _ in products if _ in ProductCode):  # type: ignore
        if is_international and is_document:
            products.append("dhl_express_worldwide_doc")
        elif is_international:
            products.append("dhl_express_worldwide_nondoc")
        elif is_document and is_envelope:
            products.append("dhl_express_envelope_doc")
        elif is_document:
            products.append("dhl_domestic_express_doc")
        else:
            products.append("dhl_express_12_00_nondoc")

    return units.Services(products, ProductCode)


class ShippingOption(Enum):
    dhl_logistics_services = OptionEnum("0A")
    dhl_mailroom_management = OptionEnum("0B")
    dhl_pallet_administration = OptionEnum("0C")
    dhl_warehousing = OptionEnum("0D")
    dhl_express_logistics_centre = OptionEnum("0E")
    dhl_strategic_parts_centre = OptionEnum("0F")
    dhl_local_distribution_centre = OptionEnum("0G")
    dhl_terminal_handling = OptionEnum("0H")
    dhl_cross_docking = OptionEnum("0I")
    dhl_inventory_management = OptionEnum("0J")
    dhl_loading_unloading = OptionEnum("0K")
    dhl_product_kitting = OptionEnum("0L")
    dhl_priority_account_desk = OptionEnum("0M")
    dhl_document_archiving = OptionEnum("0N")
    dhl_saturday_delivery = OptionEnum("AA")
    dhl_saturday_pickup = OptionEnum("AB")
    dhl_holiday_delivery = OptionEnum("AC")
    dhl_holiday_pickup = OptionEnum("AD")
    dhl_domestic_saturday_delivery = OptionEnum("AG")
    dhl_standard = OptionEnum("BA")
    dhl_globalmail_item = OptionEnum("BB")
    dhl_letter = OptionEnum("BC")
    dhl_packet = OptionEnum("BD")
    dhl_letter_plus = OptionEnum("BE")
    dhl_packet_plus = OptionEnum("BF")
    dhl_elevated_risk = OptionEnum("CA")
    dhl_restricted_destination = OptionEnum("CB")
    dhl_security_validation = OptionEnum("CC")
    dhl_secure_protection = OptionEnum("CD")
    dhl_proof_of_identity = OptionEnum("CE")
    dhl_secure_storage = OptionEnum("CF")
    dhl_diplomatic_material = OptionEnum("CG")
    dhl_smart_sensor = OptionEnum("CH")
    dhl_visa_program = OptionEnum("CI")
    dhl_onboard_courier = OptionEnum("CJ")
    dhl_secure_safebox = OptionEnum("CK")
    dhl_smart_sentry = OptionEnum("CL")
    dhl_split_duties_and_tax = OptionEnum("DC")
    dhl_duties_and_taxes_paid = OptionEnum("DD")
    dhl_receiver_paid = OptionEnum("DE")
    dhl_duties_and_taxes_unpaid = OptionEnum("DS")
    dhl_import_billing = OptionEnum("DT")
    dhl_importer_of_record = OptionEnum("DU")
    dhl_go_green_carbon_neutral = OptionEnum("EA")
    dhl_go_green_carbon_footprint = OptionEnum("EB")
    dhl_go_green_carbon_estimate = OptionEnum("EC")
    dhl_fuel_surcharge_b = OptionEnum("FB")
    dhl_fuel_surcharge_c = OptionEnum("FC")
    dhl_fuel_surcharge_f = OptionEnum("FF")
    dhl_smartphone_box = OptionEnum("GA")
    dhl_laptop_box = OptionEnum("GB")
    dhl_bottle_box = OptionEnum("GC")
    dhl_repacking = OptionEnum("GD")
    dhl_tablet_box = OptionEnum("GE")
    dhl_filler_material = OptionEnum("GF")
    dhl_packaging = OptionEnum("GG")
    dhl_diplomatic_bag = OptionEnum("GH")
    dhl_pallet_box = OptionEnum("GI")
    dhl_lock_box = OptionEnum("GJ")
    dhl_lithium_ion_pi965_section_ii = OptionEnum("HB")
    dhl_dry_ice_un1845 = OptionEnum("HC")
    dhl_lithium_ion_pi965_966_section_ii = OptionEnum("HD")
    dhl_dangerous_goods = OptionEnum("HE")
    dhl_perishable_cargo = OptionEnum("HG")
    dhl_excepted_quantity = OptionEnum("HH")
    dhl_spill_cleaning = OptionEnum("HI")
    dhl_consumer_commodities = OptionEnum("HK")
    dhl_limited_quantities_adr = OptionEnum("HL")
    dhl_lithium_metal_pi969_section_ii = OptionEnum("HM")
    dhl_adr_load_exemption = OptionEnum("HN")
    dhl_lithium_ion_pi967_section_ii = OptionEnum("HV")
    dhl_lithium_metal_pi970_section_ii = OptionEnum("HW")
    dhl_biological_un3373 = OptionEnum("HY")
    dhl_extended_liability = OptionEnum("IB")
    dhl_contract_insurance = OptionEnum("IC")
    dhl_shipment_insurance = OptionEnum("II", float)
    dhl_delivery_notification = OptionEnum("JA")
    dhl_pickup_notification = OptionEnum("JC")
    dhl_proactive_tracking = OptionEnum("JD")
    dhl_performance_reporting = OptionEnum("JE")
    dhl_prealert_notification = OptionEnum("JY")
    dhl_change_of_billing = OptionEnum("KA")
    dhl_cash_on_delivery = OptionEnum("KB", float)
    dhl_printed_invoice = OptionEnum("KD")
    dhl_waybill_copy = OptionEnum("KE")
    dhl_import_paperwork = OptionEnum("KF")
    dhl_payment_on_pickup = OptionEnum("KY")
    dhl_shipment_intercept = OptionEnum("LA")
    dhl_shipment_redirect = OptionEnum("LC")
    dhl_storage_at_facility = OptionEnum("LE")
    dhl_cold_storage = OptionEnum("LG")
    dhl_specific_routing = OptionEnum("LH")
    dhl_service_recovery = OptionEnum("LV")
    dhl_alternative_address = OptionEnum("LW")
    dhl_hold_for_collection = OptionEnum("LX")
    dhl_address_correction_a = OptionEnum("MA")
    dhl_address_correction_b = OptionEnum("MB")
    dhl_neutral_delivery = OptionEnum("NN")
    dhl_remote_area_pickup = OptionEnum("OB")
    dhl_remote_area_delivery_c = OptionEnum("OC")
    dhl_out_of_service_area = OptionEnum("OE")
    dhl_remote_area_delivery_o = OptionEnum("OO")
    dhl_shipment_preparation = OptionEnum("PA")
    dhl_shipment_labeling = OptionEnum("PB")
    dhl_shipment_consolidation = OptionEnum("PC")
    dhl_relabeling_data_entry = OptionEnum("PD")
    dhl_preprinted_waybill = OptionEnum("PE")
    dhl_piece_labelling = OptionEnum("PS")
    dhl_data_staging_03 = OptionEnum("PT")
    dhl_data_staging_06 = OptionEnum("PU")
    dhl_data_staging_12 = OptionEnum("PV")
    dhl_data_staging_24 = OptionEnum("PW")
    dhl_standard_pickup = OptionEnum("PX")
    dhl_scheduled_pickup = OptionEnum("PY")
    dhl_dedicated_pickup = OptionEnum("QA")
    dhl_early_pickup = OptionEnum("QB")
    dhl_late_pickup = OptionEnum("QD")
    dhl_residential_pickup = OptionEnum("QE")
    dhl_loading_waiting = OptionEnum("QF")
    dhl_bypass_injection = OptionEnum("QH")
    dhl_direct_injection = OptionEnum("QI")
    dhl_drop_off_at_facility = OptionEnum("QY")
    dhl_delivery_signature = OptionEnum("SA")
    dhl_content_signature = OptionEnum("SB")
    dhl_named_signature = OptionEnum("SC")
    dhl_adult_signature = OptionEnum("SD")
    dhl_contract_signature = OptionEnum("SE")
    dhl_alternative_signature = OptionEnum("SW")
    dhl_no_signature_required = OptionEnum("SX")
    dhl_dedicated_delivery = OptionEnum("TA")
    dhl_early_delivery = OptionEnum("TB")
    dhl_time_window_delivery = OptionEnum("TC")
    dhl_evening_delivery = OptionEnum("TD")
    dhl_delivery_on_appointment = OptionEnum("TE")
    dhl_return_undeliverable = OptionEnum("TG")
    dhl_swap_delivery = OptionEnum("TH")
    dhl_unloading_waiting = OptionEnum("TJ")
    dhl_residential_delivery = OptionEnum("TK")
    dhl_repeat_delivery = OptionEnum("TN")
    dhl_alternative_date = OptionEnum("TT")
    dhl_no_partial_delivery = OptionEnum("TU")
    dhl_service_point_24_7 = OptionEnum("TV")
    dhl_pre_9_00 = OptionEnum("TW")
    dhl_pre_10_30 = OptionEnum("TX")
    dhl_pre_12_00 = OptionEnum("TY")
    dhl_thermo_packaging = OptionEnum("UA")
    dhl_ambient_vialsafe = OptionEnum("UB")
    dhl_ambient_non_insulated = OptionEnum("UC")
    dhl_ambient_insulated = OptionEnum("UD")
    dhl_ambient_extreme = OptionEnum("UE")
    dhl_chilled_box_s = OptionEnum("UF")
    dhl_chilled_box_m = OptionEnum("UG")
    dhl_chilled_box_l = OptionEnum("UH")
    dhl_frozen_no_ice_s = OptionEnum("UI")
    dhl_frozen_no_ice_m = OptionEnum("UJ")
    dhl_frozen_no_ice_l = OptionEnum("UK")
    dhl_frozen_ice_sticks_s = OptionEnum("UL")
    dhl_frozen_ice_sticks_m = OptionEnum("UM")
    dhl_frozen_ice_sticks_l = OptionEnum("UN")
    dhl_frozen_ice_plates_s = OptionEnum("UO")
    dhl_frozen_ice_plates_m = OptionEnum("UP")
    dhl_frozen_ice_plates_l = OptionEnum("UQ")
    dhl_combination_no_ice = OptionEnum("UR")
    dhl_combination_dry_ice = OptionEnum("US")
    dhl_frozen_ice_sticks_e = OptionEnum("UT")
    dhl_frozen_ice_plates_e = OptionEnum("UV")
    dhl_customer_tcp_1 = OptionEnum("UW")
    dhl_thermo_accessories = OptionEnum("VA")
    dhl_absorbent_sleeve = OptionEnum("VB")
    dhl_cooland_wrap = OptionEnum("VC")
    dhl_dry_ice_supplies = OptionEnum("VD")
    dhl_pressure_bag_s = OptionEnum("VE")
    dhl_pressure_bag_m = OptionEnum("VF")
    dhl_pressure_bag_l = OptionEnum("VG")
    dhl_informal_clearance = OptionEnum("WA")
    dhl_formal_clearance = OptionEnum("WB")
    dhl_payment_deferment = OptionEnum("WC")
    dhl_clearance_authorization = OptionEnum("WD")
    dhl_multiline_entry = OptionEnum("WE")
    dhl_post_clearance_modification = OptionEnum("WF")
    dhl_handover_to_broker = OptionEnum("WG")
    dhl_physical_intervention = OptionEnum("WH")
    dhl_bio_phyto_veterinary_controls = OptionEnum("WI")
    dhl_obtaining_permits_and_licences = OptionEnum("WJ")
    dhl_bonded_storage = OptionEnum("WK")
    dhl_bonded_transit_documents = OptionEnum("WL")
    dhl_temporary_import_export = OptionEnum("WM")
    dhl_under_bond_guarantee = OptionEnum("WN")
    dhl_export_declaration = OptionEnum("WO")
    dhl_exporter_validation = OptionEnum("WP")
    dhl_certificate_of_origin = OptionEnum("WQ")
    dhl_document_translation = OptionEnum("WR")
    dhl_personal_effects = OptionEnum("WS")
    dhl_paperless_trade = OptionEnum("WY")
    dhl_import_export_taxes = OptionEnum("XB")
    dhl_unrecoverable_origin_tax = OptionEnum("XC")
    dhl_quarantine_inspection = OptionEnum("XD")
    dhl_merchandise_process = OptionEnum("XE")
    dhl_domestic_postal_tax = OptionEnum("XF")
    dhl_tier_two_tax = OptionEnum("XG")
    dhl_tier_three_tax = OptionEnum("XH")
    dhl_import_penalty = OptionEnum("XI")
    dhl_cargo_zone_process = OptionEnum("XJ")
    dhl_import_export_duties = OptionEnum("XX")
    dhl_premium_09_00 = OptionEnum("Y1")
    dhl_premium_10_30 = OptionEnum("Y2")
    dhl_premium_12_00 = OptionEnum("Y3")
    dhl_over_sized_piece_b = OptionEnum("YB")
    dhl_over_handled_piece_c = OptionEnum("YC")
    dhl_multipiece_shipment = OptionEnum("YE")
    dhl_over_weight_piece_f = OptionEnum("YF")
    dhl_over_sized_piece_g = OptionEnum("YG")
    dhl_over_handled_piece_h = OptionEnum("YH")
    dhl_premium_9_00_i = OptionEnum("YI")
    dhl_premium_10_30_j = OptionEnum("YJ")
    dhl_premium_12_00_k = OptionEnum("YK")
    dhl_paket_shipment = OptionEnum("YV")
    dhl_breakbulk_mother = OptionEnum("YW")
    dhl_breakbulk_baby = OptionEnum("YX")
    dhl_over_weight_piece_y = OptionEnum("YY")
    dhl_customer_claim = OptionEnum("ZA")
    dhl_damage_compensation = OptionEnum("ZB")
    dhl_loss_compensation = OptionEnum("ZC")
    dhl_customer_rebate = OptionEnum("ZD")
    dhl_e_com_discount = OptionEnum("ZE")

    """ Unified Option type mapping """
    insurance = dhl_shipment_insurance
    cash_on_delivery = dhl_cash_on_delivery


def shipping_options_initializer(
    options: dict,
    is_international: bool = True,
    is_dutiable: bool = True,
    package_options: units.Options = None,
    shipper_country: str = "",
) -> units.Options:
    """
    Apply default values to the given options.
    """

    if (
        is_international
        and is_dutiable
        and ShippingOption.dhl_paperless_trade.name not in options
        and shipper_country not in UNSUPPORTED_PAPERLESS_COUNTRIES
    ):
        options.update({ShippingOption.dhl_paperless_trade.name: True})

    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.Options(options, ShippingOption, items_filter=items_filter)


COUNTRY_PREFERED_UNITS = dict(
    JM=(units.WeightUnit.KG, units.DimensionUnit.CM),
)


class CountryRegion(Enum):
    AD = "EU"
    AE = "AP"
    AF = "AP"
    AG = "AM"
    AI = "AM"
    AL = "AP"
    AM = "AP"
    AN = "AM"
    AO = "AP"
    AR = "AM"
    AS = "AM"
    AT = "EU"
    AU = "AP"
    AW = "AM"
    AZ = "AM"
    BA = "AP"
    BB = "AM"
    BD = "AP"
    BE = "EU"
    BF = "AP"
    BG = "EU"
    BH = "AP"
    BI = "AP"
    BJ = "AP"
    BM = "AM"
    BN = "AP"
    BO = "AM"
    BR = "AM"
    BS = "AM"
    BT = "AP"
    BW = "AP"
    BY = "AP"
    BZ = "AM"
    CA = "AM"
    CD = "AP"
    CF = "AP"
    CG = "AP"
    CH = "EU"
    CI = "AP"
    CK = "AP"
    CL = "AM"
    CM = "AP"
    CN = "AP"
    CO = "AM"
    CR = "AM"
    CU = "AM"
    CV = "AP"
    CY = "AP"
    CZ = "EU"
    DE = "EU"
    DJ = "AP"
    DK = "EU"
    DM = "AM"
    DO = "AM"
    DZ = "AP"
    EC = "AM"
    EE = "EU"
    EG = "AP"
    ER = "AP"
    ES = "EU"
    ET = "AP"
    FI = "EU"
    FJ = "AP"
    FK = "EU"
    FM = "AM"
    FO = "AM"
    FR = "EU"
    GA = "AP"
    GB = "EU"
    GD = "AM"
    GE = "AM"
    GF = "AM"
    GG = "EU"
    GH = "AP"
    GI = "EU"
    GL = "AM"
    GM = "AP"
    GN = "AP"
    GP = "AM"
    GQ = "AP"
    GR = "EU"
    GT = "AM"
    GU = "AM"
    GW = "AP"
    GY = "AP"
    HK = "AP"
    HN = "AM"
    HR = "AP"
    HT = "AM"
    HU = "EU"
    IC = "EU"
    ID = "AP"
    IE = "EU"
    IL = "AP"
    IN = "AP"
    IQ = "AP"
    IR = "AP"
    IS = "EU"
    IT = "EU"
    JE = "EU"
    JM = "AM"
    JO = "AP"
    JP = "AP"
    KE = "AP"
    KG = "AP"
    KH = "AP"
    KI = "AP"
    KM = "AP"
    KN = "AM"
    KP = "AP"
    KR = "AP"
    KV = "AM"
    KW = "AP"
    KY = "AM"
    KZ = "AP"
    LA = "AP"
    LB = "AP"
    LC = "AM"
    LI = "AM"
    LK = "AP"
    LR = "AP"
    LS = "AP"
    LT = "EU"
    LU = "EU"
    LV = "EU"
    LY = "AP"
    MA = "AP"
    MC = "AM"
    MD = "AP"
    ME = "AM"
    MG = "AP"
    MH = "AM"
    MK = "AP"
    ML = "AP"
    MM = "AP"
    MN = "AP"
    MO = "AP"
    MP = "AM"
    MQ = "AM"
    MR = "AP"
    MS = "AM"
    MT = "AP"
    MU = "AP"
    MV = "AP"
    MW = "AP"
    MX = "AM"
    MY = "AP"
    MZ = "AP"
    NA = "AP"
    NC = "AP"
    NE = "AP"
    NG = "AP"
    NI = "AM"
    NL = "EU"
    NO = "EU"
    NP = "AP"
    NR = "AP"
    NU = "AP"
    NZ = "AP"
    OM = "AP"
    PA = "AM"
    PE = "AM"
    PF = "AP"
    PG = "AP"
    PH = "AP"
    PK = "AP"
    PL = "EU"
    PR = "AM"
    PT = "EU"
    PW = "AM"
    PY = "AM"
    QA = "AP"
    RE = "AP"
    RO = "EU"
    RS = "AP"
    RU = "AP"
    RW = "AP"
    SA = "AP"
    SB = "AP"
    SC = "AP"
    SD = "AP"
    SE = "EU"
    SG = "AP"
    SH = "AP"
    SI = "EU"
    SK = "EU"
    SL = "AP"
    SM = "EU"
    SN = "AP"
    SO = "AM"
    SR = "AM"
    SS = "AP"
    ST = "AP"
    SV = "AM"
    SY = "AP"
    SZ = "AP"
    TC = "AM"
    TD = "AP"
    TG = "AP"
    TH = "AP"
    TJ = "AP"
    TL = "AP"
    TN = "AP"
    TO = "AP"
    TR = "AP"
    TT = "AM"
    TV = "AP"
    TW = "AP"
    TZ = "AP"
    UA = "AP"
    UG = "AP"
    US = "AM"
    UY = "AM"
    UZ = "AP"
    VA = ""
    VC = "AM"
    VE = "AM"
    VG = "AM"
    VI = "AM"
    VN = "AP"
    VU = "AP"
    WS = "AP"
    XB = "AM"
    XC = "AM"
    XE = "AM"
    XM = "AM"
    XN = "AM"
    XS = "AP"
    XY = "AM"
    YE = "AP"
    YT = "AP"
    ZA = "AP"
    ZM = "AP"
    ZW = "AP"
