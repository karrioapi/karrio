""" DHL Native Types """

from purplship.core.utils import Enum, Flag, Spec
from purplship.core.units import PackagePreset

PRESET_DEFAULTS = dict(dimension_unit="IN", weight_unit="LB")


class PackagePresets(Flag):
    dhl_express_envelope = PackagePreset(
        **dict(weight=0.5, width=35.0, height=27.5, length=1.0, packaging_type="envelope"),
        **PRESET_DEFAULTS
    )
    dhl_express_standard_flyer = PackagePreset(
        **dict(weight=2.0, width=40.0, height=30.0, length=1.5, packaging_type="pak"),
        **PRESET_DEFAULTS
    )
    dhl_express_large_flyer = PackagePreset(
        **dict(weight=3.0, width=47.5, height=37.5, length=1.5, packaging_type="pak"),
        **PRESET_DEFAULTS
    )
    dhl_express_box_2 = PackagePreset(
        **dict(weight=1.0, width=33.7, height=18.2, length=10.0, packaging_type="medium_box"),
        **PRESET_DEFAULTS
    )
    dhl_express_box_3 = PackagePreset(
        **dict(weight=2.0, width=33.6, height=32.0, length=5.2, packaging_type="medium_box"),
        **PRESET_DEFAULTS
    )
    dhl_express_box_4 = PackagePreset(
        **dict(weight=5.0, width=33.7, height=32.2, length=18.0, packaging_type="medium_box"),
        **PRESET_DEFAULTS
    )
    dhl_express_box_5 = PackagePreset(
        **dict(weight=10.0, width=33.7, height=32.2, length=34.5, packaging_type="medium_box"),
        **PRESET_DEFAULTS
    )
    dhl_express_box_6 = PackagePreset(
        **dict(weight=15.0, width=41.7, height=35.9, length=36.9, packaging_type="large_box"),
        **PRESET_DEFAULTS
    )
    dhl_express_box_7 = PackagePreset(
        **dict(weight=20.0, width=48.1, height=40.4, length=38.9, packaging_type="large_box"),
        **PRESET_DEFAULTS
    )
    dhl_express_box_8 = PackagePreset(
        **dict(weight=25.0, width=54.2, height=44.4, length=40.9, packaging_type="large_box"),
        **PRESET_DEFAULTS
    )
    dhl_express_tube = PackagePreset(
        **dict(weight=5.0, width=96.0, height=15.0, length=15.0, packaging_type="tube"),
        **PRESET_DEFAULTS
    )
    dhl_didgeridoo_box = PackagePreset(
        **dict(weight=10.0, width=13.0, height=13.0, length=162.0, packaging_type="medium_box"),
        **PRESET_DEFAULTS
    )
    dhl_jumbo_box = PackagePreset(
        **dict(weight=30.0, width=45.0, height=42.7, length=33.0, packaging_type="medium_box"),
        **PRESET_DEFAULTS
    )
    dhl_jumbo_box_junior = PackagePreset(
        **dict(weight=20.0, width=39.9, height=34.0, length=24.1, packaging_type="medium_box"),
        **PRESET_DEFAULTS
    )


class LabelType(Flag):
    PDF_6x4 = ('PDF', '6X4_PDF')
    PDF_8x4 = ('PDF', '8X4_PDF')
    PDF_8x4_A4 = ('PDF', '8X4_A4_PDF')
    PDF_6x4_A4 = ('PDF', '6X4_A4_PDF')
    PDF_8x4_CI = ('PDF', '8X4_CI_PDF')
    PDF_8x4_RU_A4 = ('PDF', '8X4_RU_A4_PDF')
    ZPL_8x4 = ('ZPL2', '8X4_thermal')
    ZPL_6x4 = ('ZPL2', '6X4_thermal')
    ZPL_8x4_CI = ('ZPL2', '8X4_CI_thermal')

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


class PaymentType(Enum):
    sender = "S"
    recipient = "R"
    third_party = "T"


class Dimension(Enum):
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


class SpecialServiceCode(Enum):
    dhl_logistics_services = Spec.asKey("0A")
    dhl_mailroom_management = Spec.asKey("0B")
    dhl_pallet_administration = Spec.asKey("0C")
    dhl_warehousing = Spec.asKey("0D")
    dhl_express_logistics_centre = Spec.asKey("0E")
    dhl_strategic_parts_centre = Spec.asKey("0F")
    dhl_local_distribution_centre = Spec.asKey("0G")
    dhl_terminal_handling = Spec.asKey("0H")
    dhl_cross_docking = Spec.asKey("0I")
    dhl_inventory_management = Spec.asKey("0J")
    dhl_loading_unloading = Spec.asKey("0K")
    dhl_product_kitting = Spec.asKey("0L")
    dhl_priority_account_desk = Spec.asKey("0M")
    dhl_document_archiving = Spec.asKey("0N")
    dhl_saturday_delivery = Spec.asKey("AA")
    dhl_saturday_pickup = Spec.asKey("AB")
    dhl_holiday_delivery = Spec.asKey("AC")
    dhl_holiday_pickup = Spec.asKey("AD")
    dhl_domestic_saturday_delivery = Spec.asKey("AG")
    dhl_standard = Spec.asKey("BA")
    dhl_globalmail_item = Spec.asKey("BB")
    dhl_letter = Spec.asKey("BC")
    dhl_packet = Spec.asKey("BD")
    dhl_letter_plus = Spec.asKey("BE")
    dhl_packet_plus = Spec.asKey("BF")
    dhl_elevated_risk = Spec.asKey("CA")
    dhl_restricted_destination = Spec.asKey("CB")
    dhl_security_validation = Spec.asKey("CC")
    dhl_secure_protection = Spec.asKey("CD")
    dhl_proof_of_identity = Spec.asKey("CE")
    dhl_secure_storage = Spec.asKey("CF")
    dhl_diplomatic_material = Spec.asKey("CG")
    dhl_smart_sensor = Spec.asKey("CH")
    dhl_visa_program = Spec.asKey("CI")
    dhl_onboard_courier = Spec.asKey("CJ")
    dhl_secure_safebox = Spec.asKey("CK")
    dhl_smart_sentry = Spec.asKey("CL")
    dhl_split_duties_and_tax = Spec.asKey("DC")
    dhl_duties_and_taxes_paid = Spec.asKey("DD")
    dhl_receiver_paid = Spec.asKey("DE")
    dhl_duties_and_taxes_unpaid = Spec.asKey("DS")
    dhl_import_billing = Spec.asKey("DT")
    dhl_importer_of_record = Spec.asKey("DU")
    dhl_go_green_carbon_neutral = Spec.asKey("EA")
    dhl_go_green_carbon_footprint = Spec.asKey("EB")
    dhl_go_green_carbon_estimate = Spec.asKey("EC")
    dhl_fuel_surcharge_b = Spec.asKey("FB")
    dhl_fuel_surcharge_c = Spec.asKey("FC")
    dhl_fuel_surcharge_f = Spec.asKey("FF")
    dhl_smartphone_box = Spec.asKey("GA")
    dhl_laptop_box = Spec.asKey("GB")
    dhl_bottle_box = Spec.asKey("GC")
    dhl_repacking = Spec.asKey("GD")
    dhl_tablet_box = Spec.asKey("GE")
    dhl_filler_material = Spec.asKey("GF")
    dhl_packaging = Spec.asKey("GG")
    dhl_diplomatic_bag = Spec.asKey("GH")
    dhl_pallet_box = Spec.asKey("GI")
    dhl_lock_box = Spec.asKey("GJ")
    dhl_lithium_ion_pi965_section_ii = Spec.asKey("HB")
    dhl_dry_ice_un1845 = Spec.asKey("HC")
    dhl_lithium_ion_pi965_966_section_ii = Spec.asKey("HD")
    dhl_dangerous_goods = Spec.asKey("HE")
    dhl_perishable_cargo = Spec.asKey("HG")
    dhl_excepted_quantity = Spec.asKey("HH")
    dhl_spill_cleaning = Spec.asKey("HI")
    dhl_consumer_commodities = Spec.asKey("HK")
    dhl_limited_quantities_adr = Spec.asKey("HL")
    dhl_lithium_metal_pi969_section_ii = Spec.asKey("HM")
    dhl_adr_load_exemption = Spec.asKey("HN")
    dhl_lithium_ion_pi967_section_ii = Spec.asKey("HV")
    dhl_lithium_metal_pi970_section_ii = Spec.asKey("HW")
    dhl_biological_un3373 = Spec.asKey("HY")
    dhl_extended_liability = Spec.asKey("IB")
    dhl_contract_insurance = Spec.asKey("IC")
    dhl_shipment_insurance = Spec.asKeyVal("II", float)
    dhl_delivery_notification = Spec.asKeyVal("JA")
    dhl_pickup_notification = Spec.asKey("JC")
    dhl_proactive_tracking = Spec.asKey("JD")
    dhl_performance_reporting = Spec.asKey("JE")
    dhl_prealert_notification = Spec.asKey("JY")
    dhl_change_of_billing = Spec.asKey("KA")
    dhl_cash_on_delivery = Spec.asKey("KB")
    dhl_printed_invoice = Spec.asKey("KD")
    dhl_waybill_copy = Spec.asKey("KE")
    dhl_import_paperwork = Spec.asKey("KF")
    dhl_payment_on_pickup = Spec.asKey("KY")
    dhl_shipment_intercept = Spec.asKey("LA")
    dhl_shipment_redirect = Spec.asKey("LC")
    dhl_storage_at_facility = Spec.asKey("LE")
    dhl_cold_storage = Spec.asKey("LG")
    dhl_specific_routing = Spec.asKey("LH")
    dhl_service_recovery = Spec.asKey("LV")
    dhl_alternative_address = Spec.asKey("LW")
    dhl_hold_for_collection = Spec.asKey("LX")
    dhl_address_correction_a = Spec.asKey("MA")
    dhl_address_correction_b = Spec.asKey("MB")
    dhl_neutral_delivery = Spec.asKey("NN")
    dhl_remote_area_pickup = Spec.asKey("OB")
    dhl_remote_area_delivery_c = Spec.asKey("OC")
    dhl_out_of_service_area = Spec.asKey("OE")
    dhl_remote_area_delivery_o = Spec.asKey("OO")
    dhl_shipment_preparation = Spec.asKey("PA")
    dhl_shipment_labeling = Spec.asKey("PB")
    dhl_shipment_consolidation = Spec.asKey("PC")
    dhl_relabeling_data_entry = Spec.asKey("PD")
    dhl_preprinted_waybill = Spec.asKey("PE")
    dhl_piece_labelling = Spec.asKey("PS")
    dhl_data_staging_03 = Spec.asKey("PT")
    dhl_data_staging_06 = Spec.asKey("PU")
    dhl_data_staging_12 = Spec.asKey("PV")
    dhl_data_staging_24 = Spec.asKey("PW")
    dhl_standard_pickup = Spec.asKey("PX")
    dhl_scheduled_pickup = Spec.asKey("PY")
    dhl_dedicated_pickup = Spec.asKey("QA")
    dhl_early_pickup = Spec.asKey("QB")
    dhl_late_pickup = Spec.asKey("QD")
    dhl_residential_pickup = Spec.asKey("QE")
    dhl_loading_waiting = Spec.asKey("QF")
    dhl_bypass_injection = Spec.asKey("QH")
    dhl_direct_injection = Spec.asKey("QI")
    dhl_drop_off_at_facility = Spec.asKey("QY")
    dhl_delivery_signature = Spec.asKey("SA")
    dhl_content_signature = Spec.asKey("SB")
    dhl_named_signature = Spec.asKey("SC")
    dhl_adult_signature = Spec.asKey("SD")
    dhl_contract_signature = Spec.asKey("SE")
    dhl_alternative_signature = Spec.asKey("SW")
    dhl_no_signature_required = Spec.asKey("SX")
    dhl_dedicated_delivery = Spec.asKey("TA")
    dhl_early_delivery = Spec.asKey("TB")
    dhl_time_window_delivery = Spec.asKey("TC")
    dhl_evening_delivery = Spec.asKey("TD")
    dhl_delivery_on_appointment = Spec.asKey("TE")
    dhl_return_undeliverable = Spec.asKey("TG")
    dhl_swap_delivery = Spec.asKey("TH")
    dhl_unloading_waiting = Spec.asKey("TJ")
    dhl_residential_delivery = Spec.asKey("TK")
    dhl_repeat_delivery = Spec.asKey("TN")
    dhl_alternative_date = Spec.asKey("TT")
    dhl_no_partial_delivery = Spec.asKey("TU")
    dhl_service_point_24_7 = Spec.asKey("TV")
    dhl_pre_9_00 = Spec.asKey("TW")
    dhl_pre_10_30 = Spec.asKey("TX")
    dhl_pre_12_00 = Spec.asKey("TY")
    dhl_thermo_packaging = Spec.asKey("UA")
    dhl_ambient_vialsafe = Spec.asKey("UB")
    dhl_ambient_non_insulated = Spec.asKey("UC")
    dhl_ambient_insulated = Spec.asKey("UD")
    dhl_ambient_extreme = Spec.asKey("UE")
    dhl_chilled_box_s = Spec.asKey("UF")
    dhl_chilled_box_m = Spec.asKey("UG")
    dhl_chilled_box_l = Spec.asKey("UH")
    dhl_frozen_no_ice_s = Spec.asKey("UI")
    dhl_frozen_no_ice_m = Spec.asKey("UJ")
    dhl_frozen_no_ice_l = Spec.asKey("UK")
    dhl_frozen_ice_sticks_s = Spec.asKey("UL")
    dhl_frozen_ice_sticks_m = Spec.asKey("UM")
    dhl_frozen_ice_sticks_l = Spec.asKey("UN")
    dhl_frozen_ice_plates_s = Spec.asKey("UO")
    dhl_frozen_ice_plates_m = Spec.asKey("UP")
    dhl_frozen_ice_plates_l = Spec.asKey("UQ")
    dhl_combination_no_ice = Spec.asKey("UR")
    dhl_combination_dry_ice = Spec.asKey("US")
    dhl_frozen_ice_sticks_e = Spec.asKey("UT")
    dhl_frozen_ice_plates_e = Spec.asKey("UV")
    dhl_customer_tcp_1 = Spec.asKey("UW")
    dhl_thermo_accessories = Spec.asKey("VA")
    dhl_absorbent_sleeve = Spec.asKey("VB")
    dhl_cooland_wrap = Spec.asKey("VC")
    dhl_dry_ice_supplies = Spec.asKey("VD")
    dhl_pressure_bag_s = Spec.asKey("VE")
    dhl_pressure_bag_m = Spec.asKey("VF")
    dhl_pressure_bag_l = Spec.asKey("VG")
    dhl_informal_clearance = Spec.asKey("WA")
    dhl_formal_clearance = Spec.asKey("WB")
    dhl_payment_deferment = Spec.asKey("WC")
    dhl_clearance_authorization = Spec.asKey("WD")
    dhl_multiline_entry = Spec.asKey("WE")
    dhl_post_clearance_modification = Spec.asKey("WF")
    dhl_handover_to_broker = Spec.asKey("WG")
    dhl_physical_intervention = Spec.asKey("WH")
    dhl_bio_phyto_veterinary_controls = Spec.asKey("WI")
    dhl_obtaining_permits_and_licences = Spec.asKey("WJ")
    dhl_bonded_storage = Spec.asKey("WK")
    dhl_bonded_transit_documents = Spec.asKey("WL")
    dhl_temporary_import_export = Spec.asKey("WM")
    dhl_under_bond_guarantee = Spec.asKey("WN")
    dhl_export_declaration = Spec.asKey("WO")
    dhl_exporter_validation = Spec.asKey("WP")
    dhl_certificate_of_origin = Spec.asKey("WQ")
    dhl_document_translation = Spec.asKey("WR")
    dhl_personal_effects = Spec.asKey("WS")
    dhl_paperless_trade = Spec.asKey("WY")
    dhl_import_export_taxes = Spec.asKey("XB")
    dhl_unrecoverable_origin_tax = Spec.asKey("XC")
    dhl_quarantine_inspection = Spec.asKey("XD")
    dhl_merchandise_process = Spec.asKey("XE")
    dhl_domestic_postal_tax = Spec.asKey("XF")
    dhl_tier_two_tax = Spec.asKey("XG")
    dhl_tier_three_tax = Spec.asKey("XH")
    dhl_import_penalty = Spec.asKey("XI")
    dhl_cargo_zone_process = Spec.asKey("XJ")
    dhl_import_export_duties = Spec.asKey("XX")
    dhl_premium_09_00 = Spec.asKey("Y1")
    dhl_premium_10_30 = Spec.asKey("Y2")
    dhl_premium_12_00 = Spec.asKey("Y3")
    dhl_over_sized_piece_b = Spec.asKey("YB")
    dhl_over_handled_piece_c = Spec.asKey("YC")
    dhl_multipiece_shipment = Spec.asKey("YE")
    dhl_over_weight_piece_f = Spec.asKey("YF")
    dhl_over_sized_piece_g = Spec.asKey("YG")
    dhl_over_handled_piece_h = Spec.asKey("YH")
    dhl_premium_9_00_i = Spec.asKey("YI")
    dhl_premium_10_30_j = Spec.asKey("YJ")
    dhl_premium_12_00_k = Spec.asKey("YK")
    dhl_paket_shipment = Spec.asKey("YV")
    dhl_breakbulk_mother = Spec.asKey("YW")
    dhl_breakbulk_baby = Spec.asKey("YX")
    dhl_over_weight_piece_y = Spec.asKey("YY")
    dhl_customer_claim = Spec.asKey("ZA")
    dhl_damage_compensation = Spec.asKey("ZB")
    dhl_loss_compensation = Spec.asKey("ZC")
    dhl_customer_rebate = Spec.asKey("ZD")
    dhl_e_com_discount = Spec.asKey("ZE")

    """ Unified Option type mapping """
    insurance = dhl_shipment_insurance


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
