""" DHL Native Types """

import typing
import karrio.lib as lib

MeasurementOptions = lib.units.MeasurementOptionsType(min_in=1, min_cm=1)
COUNTRY_PREFERED_UNITS = dict(
    JM=(lib.units.WeightUnit.KG, lib.units.DimensionUnit.CM),
)
PRESET_DEFAULTS = dict(dimension_unit="CM", weight_unit="KG")


class PackagePresets(lib.Enum):
    dhl_express_envelope = lib.units.PackagePreset(
        **dict(
            weight=0.5, width=35.0, height=27.5, length=1.0, packaging_type="envelope"
        ),
        **PRESET_DEFAULTS
    )
    dhl_express_standard_flyer = lib.units.PackagePreset(
        **dict(weight=2.0, width=40.0, height=30.0, length=1.5, packaging_type="pak"),
        **PRESET_DEFAULTS
    )
    dhl_express_large_flyer = lib.units.PackagePreset(
        **dict(weight=3.0, width=47.5, height=37.5, length=1.5, packaging_type="pak"),
        **PRESET_DEFAULTS
    )
    dhl_express_box_2 = lib.units.PackagePreset(
        **dict(
            weight=1.0,
            width=33.7,
            height=18.2,
            length=10.0,
            packaging_type="medium_box",
        ),
        **PRESET_DEFAULTS
    )
    dhl_express_box_3 = lib.units.PackagePreset(
        **dict(
            weight=2.0, width=33.6, height=32.0, length=5.2, packaging_type="medium_box"
        ),
        **PRESET_DEFAULTS
    )
    dhl_express_box_4 = lib.units.PackagePreset(
        **dict(
            weight=5.0,
            width=33.7,
            height=32.2,
            length=18.0,
            packaging_type="medium_box",
        ),
        **PRESET_DEFAULTS
    )
    dhl_express_box_5 = lib.units.PackagePreset(
        **dict(
            weight=10.0,
            width=33.7,
            height=32.2,
            length=34.5,
            packaging_type="medium_box",
        ),
        **PRESET_DEFAULTS
    )
    dhl_express_box_6 = lib.units.PackagePreset(
        **dict(
            weight=15.0,
            width=41.7,
            height=35.9,
            length=36.9,
            packaging_type="large_box",
        ),
        **PRESET_DEFAULTS
    )
    dhl_express_box_7 = lib.units.PackagePreset(
        **dict(
            weight=20.0,
            width=48.1,
            height=40.4,
            length=38.9,
            packaging_type="large_box",
        ),
        **PRESET_DEFAULTS
    )
    dhl_express_box_8 = lib.units.PackagePreset(
        **dict(
            weight=25.0,
            width=54.2,
            height=44.4,
            length=40.9,
            packaging_type="large_box",
        ),
        **PRESET_DEFAULTS
    )
    dhl_express_tube = lib.units.PackagePreset(
        **dict(weight=5.0, width=96.0, height=15.0, length=15.0, packaging_type="tube"),
        **PRESET_DEFAULTS
    )
    dhl_didgeridoo_box = lib.units.PackagePreset(
        **dict(
            weight=10.0,
            width=13.0,
            height=13.0,
            length=162.0,
            packaging_type="medium_box",
        ),
        **PRESET_DEFAULTS
    )
    dhl_jumbo_box = lib.units.PackagePreset(
        **dict(
            weight=30.0,
            width=45.0,
            height=42.7,
            length=33.0,
            packaging_type="medium_box",
        ),
        **PRESET_DEFAULTS
    )
    dhl_jumbo_box_junior = lib.units.PackagePreset(
        **dict(
            weight=20.0,
            width=39.9,
            height=34.0,
            length=24.1,
            packaging_type="medium_box",
        ),
        **PRESET_DEFAULTS
    )


class LabelType(lib.Enum):
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


class Incoterm(lib.Enum):
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


class ExportReasonCode(lib.Enum):
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


class PaymentType(lib.StrEnum):
    sender = "S"
    recipient = "R"
    third_party = "T"


class DimensionUnit(lib.Enum):
    CM = "C"
    IN = "I"


class WeightUnit(lib.Enum):
    KG = "K"
    LB = "L"


class DeliveryType(lib.Enum):
    door_to_door = "DD"
    door_to_airport = "DA"
    airport_to_airport = "AA"
    door_to_door_c = "DC"


class UploadDocumentType(lib.Enum):
    HWB = "HWB"
    INV = "INV"
    PNV = "PNV"
    COO = "COO"
    NAF = "NAF"
    CIN = "CIN"
    DCL = "DCL"

    """ Unified Packaging type mapping """

    certificate_of_origin = COO
    commercial_invoice = CIN
    pro_forma_invoice = PNV
    packing_list = DCL
    other = INV


class DCTPackageType(lib.StrEnum):
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


class NetworkType(lib.Enum):
    both_time_and_day_definite = "AL"
    day_definite = "DD"
    time_definite = "TD"


class PackageType(lib.StrEnum):
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


class ConnectionConfig(lib.Enum):
    label_type = lib.OptionEnum("label_type", LabelType)
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    skip_service_filter = lib.OptionEnum("skip_service_filter", bool)


class ShippingService(lib.Enum):
    dhl_logistics_services = "0"
    dhl_domestic_express_12_00 = "1"
    dhl_express_choice = "2"
    dhl_express_choice_nondoc = "3"
    dhl_jetline = "4"
    dhl_sprintline = "5"
    dhl_air_capacity_sales = "6"
    dhl_express_easy = "7"
    dhl_express_easy_nondoc = "8"
    dhl_parcel_product = "9"
    dhl_accounting = "A"
    dhl_breakbulk_express = "B"
    dhl_medical_express = "C"
    dhl_express_worldwide_doc = "D"
    dhl_express_9_00_nondoc = "E"
    dhl_freight_worldwide_nondoc = "F"
    dhl_economy_select_domestic = "G"
    dhl_economy_select_nondoc = "H"
    dhl_express_domestic_9_00 = "I"
    dhl_jumbo_box_nondoc = "J"
    dhl_express_9_00 = "K"
    dhl_express_10_30 = "L"
    dhl_express_10_30_nondoc = "M"
    dhl_express_domestic = "N"
    dhl_express_domestic_10_30 = "O"
    dhl_express_worldwide_nondoc = "P"
    dhl_medical_express_nondoc = "Q"
    dhl_globalmail = "R"
    dhl_same_day = "S"
    dhl_express_12_00 = "T"
    dhl_express_worldwide = "U"
    dhl_parcel_product_nondoc = "V"
    dhl_economy_select = "W"
    dhl_express_envelope = "X"
    dhl_express_12_00_nondoc = "Y"
    dhl_destination_charges = "Z"
    dhl_express_all = None


def shipping_services_initializer(
    services: typing.List[str],
    is_international: bool = True,
    is_document: bool = False,
    is_envelope: bool = False,
    origin_country: str = None,
) -> lib.units.Services:
    """Apply default product codes to the list of products."""
    _region = CountryRegion.map(origin_country).value
    _services = list(set(services))
    _no_service_provided = (
        any([ShippingService.map(_).key is not None for _ in _services]) is False
    )

    if _no_service_provided and _region == "AM":
        if is_international and is_document:
            _services.append("dhl_express_worldwide_doc")

        if is_international and (is_document is False):
            _services.append("dhl_express_worldwide_nondoc")

        if (is_international is False) and (is_document and is_envelope):
            _services.append("dhl_express_envelope_doc")

        if (is_international is False) and is_document and (is_envelope is False):
            _services.append("dhl_domestic_express_doc")

    elif _region != "AM":
        _services = ["dhl_express_all"]

    return lib.units.Services(_services, ShippingService)


class ShippingOption(lib.Enum):
    dhl_logistics_services = lib.OptionEnum("0A", bool)
    dhl_mailroom_management = lib.OptionEnum("0B", bool)
    dhl_pallet_administration = lib.OptionEnum("0C", bool)
    dhl_warehousing = lib.OptionEnum("0D", bool)
    dhl_express_logistics_centre = lib.OptionEnum("0E", bool)
    dhl_strategic_parts_centre = lib.OptionEnum("0F", bool)
    dhl_local_distribution_centre = lib.OptionEnum("0G", bool)
    dhl_terminal_handling = lib.OptionEnum("0H", bool)
    dhl_cross_docking = lib.OptionEnum("0I", bool)
    dhl_inventory_management = lib.OptionEnum("0J", bool)
    dhl_loading_unloading = lib.OptionEnum("0K", bool)
    dhl_product_kitting = lib.OptionEnum("0L", bool)
    dhl_priority_account_desk = lib.OptionEnum("0M", bool)
    dhl_document_archiving = lib.OptionEnum("0N", bool)
    dhl_saturday_delivery = lib.OptionEnum("AA", bool)
    dhl_saturday_pickup = lib.OptionEnum("AB", bool)
    dhl_holiday_delivery = lib.OptionEnum("AC", bool)
    dhl_holiday_pickup = lib.OptionEnum("AD", bool)
    dhl_domestic_saturday_delivery = lib.OptionEnum("AG", bool)
    dhl_standard = lib.OptionEnum("BA", bool)
    dhl_globalmail_item = lib.OptionEnum("BB", bool)
    dhl_letter = lib.OptionEnum("BC", bool)
    dhl_packet = lib.OptionEnum("BD", bool)
    dhl_letter_plus = lib.OptionEnum("BE", bool)
    dhl_packet_plus = lib.OptionEnum("BF", bool)
    dhl_elevated_risk = lib.OptionEnum("CA", bool)
    dhl_restricted_destination = lib.OptionEnum("CB", bool)
    dhl_security_validation = lib.OptionEnum("CC", bool)
    dhl_secure_protection = lib.OptionEnum("CD", bool)
    dhl_proof_of_identity = lib.OptionEnum("CE", bool)
    dhl_secure_storage = lib.OptionEnum("CF", bool)
    dhl_diplomatic_material = lib.OptionEnum("CG", bool)
    dhl_smart_sensor = lib.OptionEnum("CH", bool)
    dhl_visa_program = lib.OptionEnum("CI", bool)
    dhl_onboard_courier = lib.OptionEnum("CJ", bool)
    dhl_secure_safebox = lib.OptionEnum("CK", bool)
    dhl_smart_sentry = lib.OptionEnum("CL", bool)
    dhl_split_duties_and_tax = lib.OptionEnum("DC", bool)
    dhl_duties_and_taxes_paid = lib.OptionEnum("DD", bool)
    dhl_receiver_paid = lib.OptionEnum("DE", bool)
    dhl_duties_and_taxes_unpaid = lib.OptionEnum("DS", bool)
    dhl_import_billing = lib.OptionEnum("DT", bool)
    dhl_importer_of_record = lib.OptionEnum("DU", bool)
    dhl_go_green_carbon_neutral = lib.OptionEnum("EA", bool)
    dhl_go_green_carbon_footprint = lib.OptionEnum("EB", bool)
    dhl_go_green_carbon_estimate = lib.OptionEnum("EC", bool)
    dhl_fuel_surcharge_b = lib.OptionEnum("FB", bool)
    dhl_fuel_surcharge_c = lib.OptionEnum("FC", bool)
    dhl_fuel_surcharge_f = lib.OptionEnum("FF", bool)
    dhl_smartphone_box = lib.OptionEnum("GA", bool)
    dhl_laptop_box = lib.OptionEnum("GB", bool)
    dhl_bottle_box = lib.OptionEnum("GC", bool)
    dhl_repacking = lib.OptionEnum("GD", bool)
    dhl_tablet_box = lib.OptionEnum("GE", bool)
    dhl_filler_material = lib.OptionEnum("GF", bool)
    dhl_packaging = lib.OptionEnum("GG", bool)
    dhl_diplomatic_bag = lib.OptionEnum("GH", bool)
    dhl_pallet_box = lib.OptionEnum("GI", bool)
    dhl_lock_box = lib.OptionEnum("GJ", bool)
    dhl_lithium_ion_pi965_section_ii = lib.OptionEnum("HB", bool)
    dhl_dry_ice_un1845 = lib.OptionEnum("HC", bool)
    dhl_lithium_ion_pi965_966_section_ii = lib.OptionEnum("HD", bool)
    dhl_dangerous_goods = lib.OptionEnum("HE", bool)
    dhl_perishable_cargo = lib.OptionEnum("HG", bool)
    dhl_excepted_quantity = lib.OptionEnum("HH", bool)
    dhl_spill_cleaning = lib.OptionEnum("HI", bool)
    dhl_consumer_commodities = lib.OptionEnum("HK", bool)
    dhl_limited_quantities_adr = lib.OptionEnum("HL", bool)
    dhl_lithium_metal_pi969_section_ii = lib.OptionEnum("HM", bool)
    dhl_adr_load_exemption = lib.OptionEnum("HN", bool)
    dhl_lithium_ion_pi967_section_ii = lib.OptionEnum("HV", bool)
    dhl_lithium_metal_pi970_section_ii = lib.OptionEnum("HW", bool)
    dhl_biological_un3373 = lib.OptionEnum("HY", bool)
    dhl_extended_liability = lib.OptionEnum("IB", bool)
    dhl_contract_insurance = lib.OptionEnum("IC", float)
    dhl_shipment_insurance = lib.OptionEnum("II", float)
    dhl_delivery_notification = lib.OptionEnum("JA", bool)
    dhl_pickup_notification = lib.OptionEnum("JC", bool)
    dhl_proactive_tracking = lib.OptionEnum("JD", bool)
    dhl_performance_reporting = lib.OptionEnum("JE", bool)
    dhl_prealert_notification = lib.OptionEnum("JY", bool)
    dhl_change_of_billing = lib.OptionEnum("KA", bool)
    dhl_cash_on_delivery = lib.OptionEnum("KB", float)
    dhl_printed_invoice = lib.OptionEnum("KD", bool)
    dhl_waybill_copy = lib.OptionEnum("KE", bool)
    dhl_import_paperwork = lib.OptionEnum("KF", bool)
    dhl_payment_on_pickup = lib.OptionEnum("KY", bool)
    dhl_shipment_intercept = lib.OptionEnum("LA", bool)
    dhl_shipment_redirect = lib.OptionEnum("LC", bool)
    dhl_storage_at_facility = lib.OptionEnum("LE", bool)
    dhl_cold_storage = lib.OptionEnum("LG", bool)
    dhl_specific_routing = lib.OptionEnum("LH", bool)
    dhl_service_recovery = lib.OptionEnum("LV", bool)
    dhl_alternative_address = lib.OptionEnum("LW", bool)
    dhl_hold_for_collection = lib.OptionEnum("LX", bool)
    dhl_address_correction_a = lib.OptionEnum("MA", bool)
    dhl_address_correction_b = lib.OptionEnum("MB", bool)
    dhl_neutral_delivery = lib.OptionEnum("NN", bool)
    dhl_remote_area_pickup = lib.OptionEnum("OB", bool)
    dhl_remote_area_delivery_c = lib.OptionEnum("OC", bool)
    dhl_out_of_service_area = lib.OptionEnum("OE", bool)
    dhl_remote_area_delivery_o = lib.OptionEnum("OO", bool)
    dhl_shipment_preparation = lib.OptionEnum("PA", bool)
    dhl_shipment_labeling = lib.OptionEnum("PB", bool)
    dhl_shipment_consolidation = lib.OptionEnum("PC", bool)
    dhl_relabeling_data_entry = lib.OptionEnum("PD", bool)
    dhl_preprinted_waybill = lib.OptionEnum("PE", bool)
    dhl_piece_labelling = lib.OptionEnum("PS", bool)
    dhl_data_staging_03 = lib.OptionEnum("PT", bool)
    dhl_data_staging_06 = lib.OptionEnum("PU", bool)
    dhl_data_staging_12 = lib.OptionEnum("PV", bool)
    dhl_data_staging_24 = lib.OptionEnum("PW", bool)
    dhl_standard_pickup = lib.OptionEnum("PX", bool)
    dhl_scheduled_pickup = lib.OptionEnum("PY", bool)
    dhl_dedicated_pickup = lib.OptionEnum("QA", bool)
    dhl_early_pickup = lib.OptionEnum("QB", bool)
    dhl_late_pickup = lib.OptionEnum("QD", bool)
    dhl_residential_pickup = lib.OptionEnum("QE", bool)
    dhl_loading_waiting = lib.OptionEnum("QF", bool)
    dhl_bypass_injection = lib.OptionEnum("QH", bool)
    dhl_direct_injection = lib.OptionEnum("QI", bool)
    dhl_drop_off_at_facility = lib.OptionEnum("QY", bool)
    dhl_delivery_signature = lib.OptionEnum("SA", bool)
    dhl_content_signature = lib.OptionEnum("SB", bool)
    dhl_named_signature = lib.OptionEnum("SC", bool)
    dhl_adult_signature = lib.OptionEnum("SD", bool)
    dhl_contract_signature = lib.OptionEnum("SE", bool)
    dhl_alternative_signature = lib.OptionEnum("SW", bool)
    dhl_no_signature_required = lib.OptionEnum("SX", bool)
    dhl_dedicated_delivery = lib.OptionEnum("TA", bool)
    dhl_early_delivery = lib.OptionEnum("TB", bool)
    dhl_time_window_delivery = lib.OptionEnum("TC", bool)
    dhl_evening_delivery = lib.OptionEnum("TD", bool)
    dhl_delivery_on_appointment = lib.OptionEnum("TE", bool)
    dhl_return_undeliverable = lib.OptionEnum("TG", bool)
    dhl_swap_delivery = lib.OptionEnum("TH", bool)
    dhl_unloading_waiting = lib.OptionEnum("TJ", bool)
    dhl_residential_delivery = lib.OptionEnum("TK", bool)
    dhl_repeat_delivery = lib.OptionEnum("TN", bool)
    dhl_alternative_date = lib.OptionEnum("TT", bool)
    dhl_no_partial_delivery = lib.OptionEnum("TU", bool)
    dhl_service_point_24_7 = lib.OptionEnum("TV", bool)
    dhl_pre_9_00 = lib.OptionEnum("TW", bool)
    dhl_pre_10_30 = lib.OptionEnum("TX", bool)
    dhl_pre_12_00 = lib.OptionEnum("TY", bool)
    dhl_thermo_packaging = lib.OptionEnum("UA", bool)
    dhl_ambient_vialsafe = lib.OptionEnum("UB", bool)
    dhl_ambient_non_insulated = lib.OptionEnum("UC", bool)
    dhl_ambient_insulated = lib.OptionEnum("UD", bool)
    dhl_ambient_extreme = lib.OptionEnum("UE", bool)
    dhl_chilled_box_s = lib.OptionEnum("UF", bool)
    dhl_chilled_box_m = lib.OptionEnum("UG", bool)
    dhl_chilled_box_l = lib.OptionEnum("UH", bool)
    dhl_frozen_no_ice_s = lib.OptionEnum("UI", bool)
    dhl_frozen_no_ice_m = lib.OptionEnum("UJ", bool)
    dhl_frozen_no_ice_l = lib.OptionEnum("UK", bool)
    dhl_frozen_ice_sticks_s = lib.OptionEnum("UL", bool)
    dhl_frozen_ice_sticks_m = lib.OptionEnum("UM", bool)
    dhl_frozen_ice_sticks_l = lib.OptionEnum("UN", bool)
    dhl_frozen_ice_plates_s = lib.OptionEnum("UO", bool)
    dhl_frozen_ice_plates_m = lib.OptionEnum("UP", bool)
    dhl_frozen_ice_plates_l = lib.OptionEnum("UQ", bool)
    dhl_combination_no_ice = lib.OptionEnum("UR", bool)
    dhl_combination_dry_ice = lib.OptionEnum("US", bool)
    dhl_frozen_ice_sticks_e = lib.OptionEnum("UT", bool)
    dhl_frozen_ice_plates_e = lib.OptionEnum("UV", bool)
    dhl_customer_tcp_1 = lib.OptionEnum("UW", bool)
    dhl_thermo_accessories = lib.OptionEnum("VA", bool)
    dhl_absorbent_sleeve = lib.OptionEnum("VB", bool)
    dhl_cooland_wrap = lib.OptionEnum("VC", bool)
    dhl_dry_ice_supplies = lib.OptionEnum("VD", bool)
    dhl_pressure_bag_s = lib.OptionEnum("VE", bool)
    dhl_pressure_bag_m = lib.OptionEnum("VF", bool)
    dhl_pressure_bag_l = lib.OptionEnum("VG", bool)
    dhl_informal_clearance = lib.OptionEnum("WA", bool)
    dhl_formal_clearance = lib.OptionEnum("WB", bool)
    dhl_payment_deferment = lib.OptionEnum("WC", bool)
    dhl_clearance_authorization = lib.OptionEnum("WD", bool)
    dhl_multiline_entry = lib.OptionEnum("WE", bool)
    dhl_post_clearance_modification = lib.OptionEnum("WF", bool)
    dhl_handover_to_broker = lib.OptionEnum("WG", bool)
    dhl_physical_intervention = lib.OptionEnum("WH", bool)
    dhl_bio_phyto_veterinary_controls = lib.OptionEnum("WI", bool)
    dhl_obtaining_permits_and_licences = lib.OptionEnum("WJ", bool)
    dhl_bonded_storage = lib.OptionEnum("WK", bool)
    dhl_bonded_transit_documents = lib.OptionEnum("WL", bool)
    dhl_temporary_import_export = lib.OptionEnum("WM", bool)
    dhl_under_bond_guarantee = lib.OptionEnum("WN", bool)
    dhl_export_declaration = lib.OptionEnum("WO", bool)
    dhl_exporter_validation = lib.OptionEnum("WP", bool)
    dhl_certificate_of_origin = lib.OptionEnum("WQ", bool)
    dhl_document_translation = lib.OptionEnum("WR", bool)
    dhl_personal_effects = lib.OptionEnum("WS", bool)
    dhl_paperless_trade = lib.OptionEnum("WY", bool)
    dhl_import_export_taxes = lib.OptionEnum("XB", bool)
    dhl_unrecoverable_origin_tax = lib.OptionEnum("XC", bool)
    dhl_quarantine_inspection = lib.OptionEnum("XD", bool)
    dhl_merchandise_process = lib.OptionEnum("XE", bool)
    dhl_domestic_postal_tax = lib.OptionEnum("XF", bool)
    dhl_tier_two_tax = lib.OptionEnum("XG", bool)
    dhl_tier_three_tax = lib.OptionEnum("XH", bool)
    dhl_import_penalty = lib.OptionEnum("XI", bool)
    dhl_cargo_zone_process = lib.OptionEnum("XJ", bool)
    dhl_import_export_duties = lib.OptionEnum("XX", bool)
    dhl_premium_09_00 = lib.OptionEnum("Y1", bool)
    dhl_premium_10_30 = lib.OptionEnum("Y2", bool)
    dhl_premium_12_00 = lib.OptionEnum("Y3", bool)
    dhl_over_sized_piece_b = lib.OptionEnum("YB", bool)
    dhl_over_handled_piece_c = lib.OptionEnum("YC", bool)
    dhl_multipiece_shipment = lib.OptionEnum("YE", bool)
    dhl_over_weight_piece_f = lib.OptionEnum("YF", bool)
    dhl_over_sized_piece_g = lib.OptionEnum("YG", bool)
    dhl_over_handled_piece_h = lib.OptionEnum("YH", bool)
    dhl_premium_9_00_i = lib.OptionEnum("YI", bool)
    dhl_premium_10_30_j = lib.OptionEnum("YJ", bool)
    dhl_premium_12_00_k = lib.OptionEnum("YK", bool)
    dhl_paket_shipment = lib.OptionEnum("YV", bool)
    dhl_breakbulk_mother = lib.OptionEnum("YW", bool)
    dhl_breakbulk_baby = lib.OptionEnum("YX", bool)
    dhl_over_weight_piece_y = lib.OptionEnum("YY", bool)
    dhl_customer_claim = lib.OptionEnum("ZA", bool)
    dhl_damage_compensation = lib.OptionEnum("ZB", bool)
    dhl_loss_compensation = lib.OptionEnum("ZC", bool)
    dhl_customer_rebate = lib.OptionEnum("ZD", bool)
    dhl_e_com_discount = lib.OptionEnum("ZE", bool)

    """ Custom Options """
    dhl_shipment_content = lib.OptionEnum("content")

    """ Unified Option type mapping """
    insurance = dhl_shipment_insurance
    paperless_trade = dhl_paperless_trade
    cash_on_delivery = dhl_cash_on_delivery
    saturday_delivery = dhl_saturday_delivery


def shipping_options_initializer(
    options: dict,
    package_options: lib.units.Options = None,
    origin_country: str = None,
) -> lib.units.Options:
    """
    Apply default values to the given options.
    """
    _options = options.copy()

    if origin_country in UNSUPPORTED_PAPERLESS_COUNTRIES:
        _options.update({"dhl_paperless_trade": False})

    if package_options is not None:
        _options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption and key != "dhl_shipment_content"  # type: ignore

    return lib.units.ShippingOptions(
        _options, ShippingOption, items_filter=items_filter
    )


class TrackingStatus(lib.Enum):
    on_hold = ["BA", "HP", "OH"]
    delivered = ["OK"]
    in_transit = [""]
    delivery_failed = ["CM", "DM", "DP", "DS", "NH", "RD", "RT", "SS", "ST"]
    delivery_delayed = ["IR", "MD", "TD", "UD"]
    out_for_delivery = ["WC"]


class CountryRegion(lib.Enum):
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


UNSUPPORTED_PAPERLESS_COUNTRIES = [
    "AF",  # N
    "AG",  # N
    "AI",  # N
    "AM",  # N
    "AN",  # N
    "AR",  # N
    "AW",  # N
    "AZ",  # N
    "BB",  # N
    "BD",  # N
    "BR",  # N
    "BS",  # N
    "BY",  # N
    "BZ",  # N
    "CR",  # N
    "CU",  # N
    "DM",  # N
    "DZ",  # N
    "GD",  # N
    "GE",  # N
    "GY",  # N
    "HT",  # N
    "IQ",  # N
    "IR",  # N
    "JM",  # N
    "KG",  # N
    "KH",  # N
    "KN",  # N
    "KP",  # N
    "KV",  # N
    "KY",  # N
    "KZ",  # N
    "LC",  # N
    "LR",  # N
    "LS",  # N
    "MA",  # N
    "MD",  # N
    "ME",  # N
    "MK",  # N
    "ML",  # N
    "MM",  # N
    "MQ",  # N
    "MS",  # N
    "MT",  # N
    "NC",  # N
    "NI",  # N
    "NP",  # N
    "NR",  # N
    "NU",  # N
    "PK",  # N
    "PW",  # N
    "PY",  # N
    "RS",  # N
    "RW",  # N
    "SB",  # N
    "SC",  # N
    "SD",  # N
    "SH",  # N
    "SL",  # N
    "SM",  # N
    "SN",  # N
    "SO",  # N
    "SR",  # N
    "SS",  # N
    "ST",  # N
    "SZ",  # N
    "TC",  # N
    "TD",  # N
    "TG",  # N
    "TJ",  # N
    "TL",  # N
    "TN",  # N
    "TO",  # N
    "TT",  # N
    "TV",  # N
    "UA",  # N
    "UG",  # N
    "UZ",  # N
    "VA",  # N
    "VC",  # N
    "VE",  # N
    "VG",  # N
    "XB",  # N
    "XC",  # N
    "XE",  # N
    "XM",  # N
    "XN",  # N
    "XS",  # N
    "XY",  # N
    "YE",  # N
    "YT",  # N
]
