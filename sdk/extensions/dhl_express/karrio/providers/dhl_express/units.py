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

    """ Mapp from DCT package type """
    dhl_flyer_smalls = dhl_flyer
    dhl_parcels_conveyables = dhl_other_dhl_packaging
    dhl_non_conveyables = dhl_other_dhl_packaging
    dhl_pallets = dhl_freight
    dhl_double_pallets = dhl_freight
    dhl_box = dhl_jumbo_box

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
    
    if is_international and is_document:
        products.append("dhl_express_worldwide_doc")

    if is_international and (is_document is False):
        products.append("dhl_express_worldwide_nondoc")

    if (is_international is False) and (is_document and is_envelope):
        products.append("dhl_express_envelope_doc")

    if (is_international is False) and is_document and (is_envelope is False):
        products.append("dhl_domestic_express_doc")

    return units.Services(list(set(products)), ProductCode)


class ShippingOption(Enum):
    dhl_logistics_services = OptionEnum("0A", bool)
    dhl_mailroom_management = OptionEnum("0B", bool)
    dhl_pallet_administration = OptionEnum("0C", bool)
    dhl_warehousing = OptionEnum("0D", bool)
    dhl_express_logistics_centre = OptionEnum("0E", bool)
    dhl_strategic_parts_centre = OptionEnum("0F", bool)
    dhl_local_distribution_centre = OptionEnum("0G", bool)
    dhl_terminal_handling = OptionEnum("0H", bool)
    dhl_cross_docking = OptionEnum("0I", bool)
    dhl_inventory_management = OptionEnum("0J", bool)
    dhl_loading_unloading = OptionEnum("0K", bool)
    dhl_product_kitting = OptionEnum("0L", bool)
    dhl_priority_account_desk = OptionEnum("0M", bool)
    dhl_document_archiving = OptionEnum("0N", bool)
    dhl_saturday_delivery = OptionEnum("AA", bool)
    dhl_saturday_pickup = OptionEnum("AB", bool)
    dhl_holiday_delivery = OptionEnum("AC", bool)
    dhl_holiday_pickup = OptionEnum("AD", bool)
    dhl_domestic_saturday_delivery = OptionEnum("AG", bool)
    dhl_standard = OptionEnum("BA", bool)
    dhl_globalmail_item = OptionEnum("BB", bool)
    dhl_letter = OptionEnum("BC", bool)
    dhl_packet = OptionEnum("BD", bool)
    dhl_letter_plus = OptionEnum("BE", bool)
    dhl_packet_plus = OptionEnum("BF", bool)
    dhl_elevated_risk = OptionEnum("CA", bool)
    dhl_restricted_destination = OptionEnum("CB", bool)
    dhl_security_validation = OptionEnum("CC", bool)
    dhl_secure_protection = OptionEnum("CD", bool)
    dhl_proof_of_identity = OptionEnum("CE", bool)
    dhl_secure_storage = OptionEnum("CF", bool)
    dhl_diplomatic_material = OptionEnum("CG", bool)
    dhl_smart_sensor = OptionEnum("CH", bool)
    dhl_visa_program = OptionEnum("CI", bool)
    dhl_onboard_courier = OptionEnum("CJ", bool)
    dhl_secure_safebox = OptionEnum("CK", bool)
    dhl_smart_sentry = OptionEnum("CL", bool)
    dhl_split_duties_and_tax = OptionEnum("DC", bool)
    dhl_duties_and_taxes_paid = OptionEnum("DD", bool)
    dhl_receiver_paid = OptionEnum("DE", bool)
    dhl_duties_and_taxes_unpaid = OptionEnum("DS", bool)
    dhl_import_billing = OptionEnum("DT", bool)
    dhl_importer_of_record = OptionEnum("DU", bool)
    dhl_go_green_carbon_neutral = OptionEnum("EA", bool)
    dhl_go_green_carbon_footprint = OptionEnum("EB", bool)
    dhl_go_green_carbon_estimate = OptionEnum("EC", bool)
    dhl_fuel_surcharge_b = OptionEnum("FB", bool)
    dhl_fuel_surcharge_c = OptionEnum("FC", bool)
    dhl_fuel_surcharge_f = OptionEnum("FF", bool)
    dhl_smartphone_box = OptionEnum("GA", bool)
    dhl_laptop_box = OptionEnum("GB", bool)
    dhl_bottle_box = OptionEnum("GC", bool)
    dhl_repacking = OptionEnum("GD", bool)
    dhl_tablet_box = OptionEnum("GE", bool)
    dhl_filler_material = OptionEnum("GF", bool)
    dhl_packaging = OptionEnum("GG", bool)
    dhl_diplomatic_bag = OptionEnum("GH", bool)
    dhl_pallet_box = OptionEnum("GI", bool)
    dhl_lock_box = OptionEnum("GJ", bool)
    dhl_lithium_ion_pi965_section_ii = OptionEnum("HB", bool)
    dhl_dry_ice_un1845 = OptionEnum("HC", bool)
    dhl_lithium_ion_pi965_966_section_ii = OptionEnum("HD", bool)
    dhl_dangerous_goods = OptionEnum("HE", bool)
    dhl_perishable_cargo = OptionEnum("HG", bool)
    dhl_excepted_quantity = OptionEnum("HH", bool)
    dhl_spill_cleaning = OptionEnum("HI", bool)
    dhl_consumer_commodities = OptionEnum("HK", bool)
    dhl_limited_quantities_adr = OptionEnum("HL", bool)
    dhl_lithium_metal_pi969_section_ii = OptionEnum("HM", bool)
    dhl_adr_load_exemption = OptionEnum("HN", bool)
    dhl_lithium_ion_pi967_section_ii = OptionEnum("HV", bool)
    dhl_lithium_metal_pi970_section_ii = OptionEnum("HW", bool)
    dhl_biological_un3373 = OptionEnum("HY", bool)
    dhl_extended_liability = OptionEnum("IB", bool)
    dhl_contract_insurance = OptionEnum("IC", float)
    dhl_shipment_insurance = OptionEnum("II", float)
    dhl_delivery_notification = OptionEnum("JA", bool)
    dhl_pickup_notification = OptionEnum("JC", bool)
    dhl_proactive_tracking = OptionEnum("JD", bool)
    dhl_performance_reporting = OptionEnum("JE", bool)
    dhl_prealert_notification = OptionEnum("JY", bool)
    dhl_change_of_billing = OptionEnum("KA", bool)
    dhl_cash_on_delivery = OptionEnum("KB", float)
    dhl_printed_invoice = OptionEnum("KD", bool)
    dhl_waybill_copy = OptionEnum("KE", bool)
    dhl_import_paperwork = OptionEnum("KF", bool)
    dhl_payment_on_pickup = OptionEnum("KY", bool)
    dhl_shipment_intercept = OptionEnum("LA", bool)
    dhl_shipment_redirect = OptionEnum("LC", bool)
    dhl_storage_at_facility = OptionEnum("LE", bool)
    dhl_cold_storage = OptionEnum("LG", bool)
    dhl_specific_routing = OptionEnum("LH", bool)
    dhl_service_recovery = OptionEnum("LV", bool)
    dhl_alternative_address = OptionEnum("LW", bool)
    dhl_hold_for_collection = OptionEnum("LX", bool)
    dhl_address_correction_a = OptionEnum("MA", bool)
    dhl_address_correction_b = OptionEnum("MB", bool)
    dhl_neutral_delivery = OptionEnum("NN", bool)
    dhl_remote_area_pickup = OptionEnum("OB", bool)
    dhl_remote_area_delivery_c = OptionEnum("OC", bool)
    dhl_out_of_service_area = OptionEnum("OE", bool)
    dhl_remote_area_delivery_o = OptionEnum("OO", bool)
    dhl_shipment_preparation = OptionEnum("PA", bool)
    dhl_shipment_labeling = OptionEnum("PB", bool)
    dhl_shipment_consolidation = OptionEnum("PC", bool)
    dhl_relabeling_data_entry = OptionEnum("PD", bool)
    dhl_preprinted_waybill = OptionEnum("PE", bool)
    dhl_piece_labelling = OptionEnum("PS", bool)
    dhl_data_staging_03 = OptionEnum("PT", bool)
    dhl_data_staging_06 = OptionEnum("PU", bool)
    dhl_data_staging_12 = OptionEnum("PV", bool)
    dhl_data_staging_24 = OptionEnum("PW", bool)
    dhl_standard_pickup = OptionEnum("PX", bool)
    dhl_scheduled_pickup = OptionEnum("PY", bool)
    dhl_dedicated_pickup = OptionEnum("QA", bool)
    dhl_early_pickup = OptionEnum("QB", bool)
    dhl_late_pickup = OptionEnum("QD", bool)
    dhl_residential_pickup = OptionEnum("QE", bool)
    dhl_loading_waiting = OptionEnum("QF", bool)
    dhl_bypass_injection = OptionEnum("QH", bool)
    dhl_direct_injection = OptionEnum("QI", bool)
    dhl_drop_off_at_facility = OptionEnum("QY", bool)
    dhl_delivery_signature = OptionEnum("SA", bool)
    dhl_content_signature = OptionEnum("SB", bool)
    dhl_named_signature = OptionEnum("SC", bool)
    dhl_adult_signature = OptionEnum("SD", bool)
    dhl_contract_signature = OptionEnum("SE", bool)
    dhl_alternative_signature = OptionEnum("SW", bool)
    dhl_no_signature_required = OptionEnum("SX", bool)
    dhl_dedicated_delivery = OptionEnum("TA", bool)
    dhl_early_delivery = OptionEnum("TB", bool)
    dhl_time_window_delivery = OptionEnum("TC", bool)
    dhl_evening_delivery = OptionEnum("TD", bool)
    dhl_delivery_on_appointment = OptionEnum("TE", bool)
    dhl_return_undeliverable = OptionEnum("TG", bool)
    dhl_swap_delivery = OptionEnum("TH", bool)
    dhl_unloading_waiting = OptionEnum("TJ", bool)
    dhl_residential_delivery = OptionEnum("TK", bool)
    dhl_repeat_delivery = OptionEnum("TN", bool)
    dhl_alternative_date = OptionEnum("TT", bool)
    dhl_no_partial_delivery = OptionEnum("TU", bool)
    dhl_service_point_24_7 = OptionEnum("TV", bool)
    dhl_pre_9_00 = OptionEnum("TW", bool)
    dhl_pre_10_30 = OptionEnum("TX", bool)
    dhl_pre_12_00 = OptionEnum("TY", bool)
    dhl_thermo_packaging = OptionEnum("UA", bool)
    dhl_ambient_vialsafe = OptionEnum("UB", bool)
    dhl_ambient_non_insulated = OptionEnum("UC", bool)
    dhl_ambient_insulated = OptionEnum("UD", bool)
    dhl_ambient_extreme = OptionEnum("UE", bool)
    dhl_chilled_box_s = OptionEnum("UF", bool)
    dhl_chilled_box_m = OptionEnum("UG", bool)
    dhl_chilled_box_l = OptionEnum("UH", bool)
    dhl_frozen_no_ice_s = OptionEnum("UI", bool)
    dhl_frozen_no_ice_m = OptionEnum("UJ", bool)
    dhl_frozen_no_ice_l = OptionEnum("UK", bool)
    dhl_frozen_ice_sticks_s = OptionEnum("UL", bool)
    dhl_frozen_ice_sticks_m = OptionEnum("UM", bool)
    dhl_frozen_ice_sticks_l = OptionEnum("UN", bool)
    dhl_frozen_ice_plates_s = OptionEnum("UO", bool)
    dhl_frozen_ice_plates_m = OptionEnum("UP", bool)
    dhl_frozen_ice_plates_l = OptionEnum("UQ", bool)
    dhl_combination_no_ice = OptionEnum("UR", bool)
    dhl_combination_dry_ice = OptionEnum("US", bool)
    dhl_frozen_ice_sticks_e = OptionEnum("UT", bool)
    dhl_frozen_ice_plates_e = OptionEnum("UV", bool)
    dhl_customer_tcp_1 = OptionEnum("UW", bool)
    dhl_thermo_accessories = OptionEnum("VA", bool)
    dhl_absorbent_sleeve = OptionEnum("VB", bool)
    dhl_cooland_wrap = OptionEnum("VC", bool)
    dhl_dry_ice_supplies = OptionEnum("VD", bool)
    dhl_pressure_bag_s = OptionEnum("VE", bool)
    dhl_pressure_bag_m = OptionEnum("VF", bool)
    dhl_pressure_bag_l = OptionEnum("VG", bool)
    dhl_informal_clearance = OptionEnum("WA", bool)
    dhl_formal_clearance = OptionEnum("WB", bool)
    dhl_payment_deferment = OptionEnum("WC", bool)
    dhl_clearance_authorization = OptionEnum("WD", bool)
    dhl_multiline_entry = OptionEnum("WE", bool)
    dhl_post_clearance_modification = OptionEnum("WF", bool)
    dhl_handover_to_broker = OptionEnum("WG", bool)
    dhl_physical_intervention = OptionEnum("WH", bool)
    dhl_bio_phyto_veterinary_controls = OptionEnum("WI", bool)
    dhl_obtaining_permits_and_licences = OptionEnum("WJ", bool)
    dhl_bonded_storage = OptionEnum("WK", bool)
    dhl_bonded_transit_documents = OptionEnum("WL", bool)
    dhl_temporary_import_export = OptionEnum("WM", bool)
    dhl_under_bond_guarantee = OptionEnum("WN", bool)
    dhl_export_declaration = OptionEnum("WO", bool)
    dhl_exporter_validation = OptionEnum("WP", bool)
    dhl_certificate_of_origin = OptionEnum("WQ", bool)
    dhl_document_translation = OptionEnum("WR", bool)
    dhl_personal_effects = OptionEnum("WS", bool)
    dhl_paperless_trade = OptionEnum("WY", bool, bool)
    dhl_import_export_taxes = OptionEnum("XB", bool)
    dhl_unrecoverable_origin_tax = OptionEnum("XC", bool)
    dhl_quarantine_inspection = OptionEnum("XD", bool)
    dhl_merchandise_process = OptionEnum("XE", bool)
    dhl_domestic_postal_tax = OptionEnum("XF", bool)
    dhl_tier_two_tax = OptionEnum("XG", bool)
    dhl_tier_three_tax = OptionEnum("XH", bool)
    dhl_import_penalty = OptionEnum("XI", bool)
    dhl_cargo_zone_process = OptionEnum("XJ", bool)
    dhl_import_export_duties = OptionEnum("XX", bool)
    dhl_premium_09_00 = OptionEnum("Y1", bool)
    dhl_premium_10_30 = OptionEnum("Y2", bool)
    dhl_premium_12_00 = OptionEnum("Y3", bool)
    dhl_over_sized_piece_b = OptionEnum("YB", bool)
    dhl_over_handled_piece_c = OptionEnum("YC", bool)
    dhl_multipiece_shipment = OptionEnum("YE", bool)
    dhl_over_weight_piece_f = OptionEnum("YF", bool)
    dhl_over_sized_piece_g = OptionEnum("YG", bool)
    dhl_over_handled_piece_h = OptionEnum("YH", bool)
    dhl_premium_9_00_i = OptionEnum("YI", bool)
    dhl_premium_10_30_j = OptionEnum("YJ", bool)
    dhl_premium_12_00_k = OptionEnum("YK", bool)
    dhl_paket_shipment = OptionEnum("YV", bool)
    dhl_breakbulk_mother = OptionEnum("YW", bool)
    dhl_breakbulk_baby = OptionEnum("YX", bool)
    dhl_over_weight_piece_y = OptionEnum("YY", bool)
    dhl_customer_claim = OptionEnum("ZA", bool)
    dhl_damage_compensation = OptionEnum("ZB", bool)
    dhl_loss_compensation = OptionEnum("ZC", bool)
    dhl_customer_rebate = OptionEnum("ZD", bool)
    dhl_e_com_discount = OptionEnum("ZE", bool)

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
    _options = options.copy()

    if (
        is_international
        and is_dutiable
        and ShippingOption.dhl_paperless_trade.name not in options
        and shipper_country not in UNSUPPORTED_PAPERLESS_COUNTRIES
    ):
        _options.update({ShippingOption.dhl_paperless_trade.name: True})

    if package_options is not None:
        _options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(_options, ShippingOption, items_filter=items_filter)


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
