from karrio.core import units
from karrio.core.utils import Enum, Flag
from karrio.core.units import MeasurementOptionsType, PackagePreset
from karrio.core.utils.enum import OptionEnum

PRESET_DEFAULTS = dict(dimension_unit="IN", weight_unit="LB")


class PackagePresets(Flag):
    fedex_envelope_legal_size = PackagePreset(
        **dict(weight=1.0, width=9.5, height=15.5, length=1, packaging_type="envelope"),
        **PRESET_DEFAULTS
    )
    fedex_envelope_without_pouch = PackagePreset(
        **dict(weight=1.0, width=9.5, height=15.5, length=1, packaging_type="envelope"),
        **PRESET_DEFAULTS
    )
    fedex_padded_pak = PackagePreset(
        **dict(weight=2.2, width=11.75, height=14.75, length=1, packaging_type="pak"),
        **PRESET_DEFAULTS
    )
    fedex_polyethylene_pak = PackagePreset(
        **dict(weight=2.2, width=12.0, height=15.5, length=1, packaging_type="pak"),
        **PRESET_DEFAULTS
    )
    fedex_clinical_pak = PackagePreset(
        **dict(weight=2.2, width=13.5, height=18.0, length=1, packaging_type="pak"),
        **PRESET_DEFAULTS
    )
    fedex_un_3373_pak = PackagePreset(
        **dict(weight=2.2, width=13.5, height=18.0, length=1, packaging_type="pak"),
        **PRESET_DEFAULTS
    )
    fedex_small_box = PackagePreset(
        **dict(
            weight=20.0,
            width=12.25,
            height=10.9,
            length=1.5,
            packaging_type="small_box",
        ),
        **PRESET_DEFAULTS
    )
    fedex_medium_box = PackagePreset(
        **dict(
            weight=20.0,
            width=13.25,
            height=11.5,
            length=2.38,
            packaging_type="medium_box",
        ),
        **PRESET_DEFAULTS
    )
    fedex_large_box = PackagePreset(
        **dict(
            weight=20.0,
            width=17.88,
            height=12.38,
            length=3.0,
            packaging_type="large_box",
        ),
        **PRESET_DEFAULTS
    )
    fedex_10_kg_box = PackagePreset(
        **dict(
            weight=10.0,
            width=15.81,
            height=12.94,
            length=10.19,
            packaging_type="medium_box",
        ),
        **PRESET_DEFAULTS
    )
    fedex_25_kg_box = PackagePreset(
        **dict(
            weight=25.0,
            width=21.56,
            height=16.56,
            length=13.19,
            packaging_type="medium_box",
        ),
        **PRESET_DEFAULTS
    )
    fedex_tube = PackagePreset(
        **dict(weight=20.0, width=38.0, height=6.0, length=6.0, packaging_type="tube"),
        **PRESET_DEFAULTS
    )
    fedex_envelope = fedex_envelope_legal_size
    fedex_pak = fedex_padded_pak


MeasurementOptions = MeasurementOptionsType(min_in=1, min_cm=1)


class LabelType(Flag):
    PDF_4x6 = ("PDF", "STOCK_4X6")
    PDF_4x6_75 = ("PDF", "STOCK_4X6.75")
    PDF_4x8 = ("PDF", "STOCK_4X8")
    PDF_4x9 = ("PDF", "STOCK_4X9")
    ZPL_4x6 = ("ZPLII", "STOCK_4X6")
    ZPL_4x6_75 = ("ZPLII", "STOCK_4X6.75")
    ZPL_4x8 = ("ZPLII", "STOCK_4X8")
    ZPL_4x9 = ("ZPLII", "STOCK_4X9")

    """ Unified Label type mapping """
    PDF = PDF_4x6
    ZPL = ZPL_4x6


class Incoterm(Enum):
    DDP = "DDP"
    DDU = "DDU"
    DAP = "DAP"
    DAT = "DAT"
    EXW = "EXW"
    CPT = "CPT"
    C_F = "C&F"
    CIP = "CIP"
    CIF = "CIF"
    FCA = "FCA"
    FOB = "FOB"


class PurposeType(Enum):
    gift = "GIFT"
    not_sold = "NOT_SOLD"
    personal_effects = "PERSONAL_EFFECTS"
    repair_and_return = "REPAIR_AND_RETURN"
    sample = "SAMPLE"
    sold = "SOLD"
    other = None

    """ Unified Content type mapping """
    documents = other
    merchandise = sold
    return_merchandise = repair_and_return


class PackagingType(Flag):
    fedex_envelope = "FEDEX_ENVELOPE"
    fedex_pak = "FEDEX_PAK"
    fedex_box = "FEDEX_BOX"
    fedex_10_kg_box = "FEDEX_10KG_BOX"
    fedex_25_kg_box = "FEDEX_25KG_BOX"
    fedex_tube = "FEDEX_TUBE"
    your_packaging = "YOUR_PACKAGING"

    """ Unified Packaging type mapping """
    envelope = fedex_envelope
    pak = fedex_pak
    tube = fedex_tube
    pallet = your_packaging
    small_box = fedex_10_kg_box
    medium_box = fedex_box
    large_box = fedex_25_kg_box


class PhysicalPackagingType(Flag):
    bag = "BAG"
    barrel = "BBL"
    basket = "BSK"
    box = "BOX"
    bucket = "BXT"
    bundle = "BDL"
    carton = "CTN"
    case = "CAS"
    container = "CNT"
    crate = "CRT"
    cylinder = "CYL"
    drum = "DRM"
    envelope = "ENV"
    pail = "PAL"
    pallet = "PLT"
    piece = "PC "
    reel = "REL"
    roll = "ROL"
    skid = "SKD"
    tank = "TNK"
    tube = "TBE"

    """ Unified Packaging type mapping """
    pak = roll
    small_box = box
    medium_box = box
    large_box = carton
    pieces = piece


class FreightPackagingType(Flag):
    fedex_10_kg_box = "FEDEX_10KG_BOX"
    fedex_25_kg_box = "FEDEX_25KG_BOX"
    fedex_box = "FEDEX_BOX"
    fedex_envelope = "FEDEX_ENVELOPE"
    fedex_extra_large_box = "FEDEX_EXTRA_LARGE_BOX"
    fedex_large_box = "FEDEX_LARGE_BOX"
    fedex_medium_box = "FEDEX_MEDIUM_BOX"
    fedex_pak = "FEDEX_PAK"
    fedex_small_box = "FEDEX_SMALL_BOX"
    fedex_tube = "FEDEX_TUBE"
    your_packaging = "YOUR_PACKAGING"

    """ Unified Packaging type mapping """
    envelope = fedex_envelope
    pak = fedex_pak
    tube = fedex_tube
    pallet = fedex_extra_large_box
    small_box = fedex_small_box
    medium_box = fedex_medium_box
    large_box = fedex_large_box


class PaymentType(Flag):
    account = "ACCOUNT"
    collect = "COLLECT"
    recipient = "RECIPIENT"
    sender = "SENDER"
    third_party = "THIRD_PARTY"


class ServiceType(Enum):
    fedex_europe_first_international_priority = "EUROPE_FIRST_INTERNATIONAL_PRIORITY"
    fedex_1_day_freight = "FEDEX_1_DAY_FREIGHT"
    fedex_2_day = "FEDEX_2_DAY"
    fedex_2_day_am = "FEDEX_2_DAY_AM"
    fedex_2_day_freight = "FEDEX_2_DAY_FREIGHT"
    fedex_3_day_freight = "FEDEX_3_DAY_FREIGHT"
    fedex_cargo_airport_to_airport = "FEDEX_CARGO_AIRPORT_TO_AIRPORT"
    fedex_cargo_freight_forwarding = "FEDEX_CARGO_FREIGHT_FORWARDING"
    fedex_cargo_international_express_freight = (
        "FEDEX_CARGO_INTERNATIONAL_EXPRESS_FREIGHT"
    )
    fedex_cargo_international_premium = "FEDEX_CARGO_INTERNATIONAL_PREMIUM"
    fedex_cargo_mail = "FEDEX_CARGO_MAIL"
    fedex_cargo_registered_mail = "FEDEX_CARGO_REGISTERED_MAIL"
    fedex_cargo_surface_mail = "FEDEX_CARGO_SURFACE_MAIL"
    fedex_custom_critical_air_expedite = "FEDEX_CUSTOM_CRITICAL_AIR_EXPEDITE"
    fedex_custom_critical_air_expedite_exclusive_use = (
        "FEDEX_CUSTOM_CRITICAL_AIR_EXPEDITE_EXCLUSIVE_USE"
    )
    fedex_custom_critical_air_expedite_network = (
        "FEDEX_CUSTOM_CRITICAL_AIR_EXPEDITE_NETWORK"
    )
    fedex_custom_critical_charter_air = "FEDEX_CUSTOM_CRITICAL_CHARTER_AIR"
    fedex_custom_critical_point_to_point = "FEDEX_CUSTOM_CRITICAL_POINT_TO_POINT"
    fedex_custom_critical_surface_expedite = "FEDEX_CUSTOM_CRITICAL_SURFACE_EXPEDITE"
    fedex_custom_critical_surface_expedite_exclusive_use = (
        "FEDEX_CUSTOM_CRITICAL_SURFACE_EXPEDITE_EXCLUSIVE_USE"
    )
    fedex_custom_critical_temp_assure_air = "FEDEX_CUSTOM_CRITICAL_TEMP_ASSURE_AIR"
    fedex_custom_critical_temp_assure_validated_air = (
        "FEDEX_CUSTOM_CRITICAL_TEMP_ASSURE_VALIDATED_AIR"
    )
    fedex_custom_critical_white_glove_services = (
        "FEDEX_CUSTOM_CRITICAL_WHITE_GLOVE_SERVICES"
    )
    fedex_distance_deferred = "FEDEX_DISTANCE_DEFERRED"
    fedex_express_saver = "FEDEX_EXPRESS_SAVER"
    fedex_first_freight = "FEDEX_FIRST_FREIGHT"
    fedex_freight_economy = "FEDEX_FREIGHT_ECONOMY"
    fedex_freight_priority = "FEDEX_FREIGHT_PRIORITY"
    fedex_ground = "FEDEX_GROUND"
    fedex_international_priority_plus = "FEDEX_INTERNATIONAL_PRIORITY_PLUS"
    fedex_next_day_afternoon = "FEDEX_NEXT_DAY_AFTERNOON"
    fedex_next_day_early_morning = "FEDEX_NEXT_DAY_EARLY_MORNING"
    fedex_next_day_end_of_day = "FEDEX_NEXT_DAY_END_OF_DAY"
    fedex_next_day_freight = "FEDEX_NEXT_DAY_FREIGHT"
    fedex_next_day_mid_morning = "FEDEX_NEXT_DAY_MID_MORNING"
    fedex_first_overnight = "FIRST_OVERNIGHT"
    fedex_ground_home_delivery = "GROUND_HOME_DELIVERY"
    fedex_international_distribution_freight = "INTERNATIONAL_DISTRIBUTION_FREIGHT"
    fedex_international_economy = "INTERNATIONAL_ECONOMY"
    fedex_international_economy_distribution = "INTERNATIONAL_ECONOMY_DISTRIBUTION"
    fedex_international_economy_freight = "INTERNATIONAL_ECONOMY_FREIGHT"
    fedex_international_first = "INTERNATIONAL_FIRST"
    fedex_international_ground = "INTERNATIONAL_GROUND"
    fedex_international_priority = "INTERNATIONAL_PRIORITY"
    fedex_international_priority_distribution = "INTERNATIONAL_PRIORITY_DISTRIBUTION"
    fedex_international_priority_express = "INTERNATIONAL_PRIORITY_EXPRESS"
    fedex_international_priority_freight = "INTERNATIONAL_PRIORITY_FREIGHT"
    fedex_priority_overnight = "PRIORITY_OVERNIGHT"
    fedex_same_day = "SAME_DAY"
    fedex_same_day_city = "SAME_DAY_CITY"
    fedex_same_day_metro_afternoon = "SAME_DAY_METRO_AFTERNOON"
    fedex_same_day_metro_morning = "SAME_DAY_METRO_MORNING"
    fedex_same_day_metro_rush = "SAME_DAY_METRO_RUSH"
    fedex_smart_post = "SMART_POST"
    fedex_standard_overnight = "STANDARD_OVERNIGHT"
    fedex_transborder_distribution_consolidation = (
        "TRANSBORDER_DISTRIBUTION_CONSOLIDATION"
    )


class ShippingOption(Enum):
    fedex_blind_shipment = OptionEnum("BLIND_SHIPMENT")
    fedex_broker_select_option = OptionEnum("BROKER_SELECT_OPTION")
    fedex_call_before_delivery = OptionEnum("CALL_BEFORE_DELIVERY")
    fedex_cod = OptionEnum("COD", float)
    fedex_cod_remittance = OptionEnum("COD_REMITTANCE")
    fedex_custom_delivery_window = OptionEnum("CUSTOM_DELIVERY_WINDOW")
    fedex_cut_flowers = OptionEnum("CUT_FLOWERS")
    fedex_dangerous_goods = OptionEnum("DANGEROUS_GOODS")
    fedex_delivery_on_invoice_acceptance = OptionEnum("DELIVERY_ON_INVOICE_ACCEPTANCE")
    fedex_detention = OptionEnum("DETENTION")
    fedex_do_not_break_down_pallets = OptionEnum("DO_NOT_BREAK_DOWN_PALLETS")
    fedex_do_not_stack_pallets = OptionEnum("DO_NOT_STACK_PALLETS")
    fedex_dry_ice = OptionEnum("DRY_ICE")
    fedex_east_coast_special = OptionEnum("EAST_COAST_SPECIAL")
    fedex_electronic_trade_documents = OptionEnum("ELECTRONIC_TRADE_DOCUMENTS")
    fedex_event_notification = OptionEnum("EVENT_NOTIFICATION")
    fedex_exclude_from_consolidation = OptionEnum("EXCLUDE_FROM_CONSOLIDATION")
    fedex_exclusive_use = OptionEnum("EXCLUSIVE_USE")
    fedex_exhibition_delivery = OptionEnum("EXHIBITION_DELIVERY")
    fedex_exhibition_pickup = OptionEnum("EXHIBITION_PICKUP")
    fedex_expedited_alternate_delivery_route = OptionEnum(
        "EXPEDITED_ALTERNATE_DELIVERY_ROUTE"
    )
    fedex_expedited_one_day_earlier = OptionEnum("EXPEDITED_ONE_DAY_EARLIER")
    fedex_expedited_service_monitoring_and_delivery = OptionEnum(
        "EXPEDITED_SERVICE_MONITORING_AND_DELIVERY"
    )
    fedex_expedited_standard_day_early_delivery = OptionEnum(
        "EXPEDITED_STANDARD_DAY_EARLY_DELIVERY"
    )
    fedex_extra_labor = OptionEnum("EXTRA_LABOR")
    fedex_extreme_length = OptionEnum("EXTREME_LENGTH")
    fedex_one_rate = OptionEnum("FEDEX_ONE_RATE")
    fedex_flatbed_trailer = OptionEnum("FLATBED_TRAILER")
    fedex_food = OptionEnum("FOOD")
    fedex_freight_guarantee = OptionEnum("FREIGHT_GUARANTEE")
    fedex_freight_to_collect = OptionEnum("FREIGHT_TO_COLLECT")
    fedex_future_day_shipment = OptionEnum("FUTURE_DAY_SHIPMENT")
    fedex_hold_at_location = OptionEnum("HOLD_AT_LOCATION")
    fedex_holiday_delivery = OptionEnum("HOLIDAY_DELIVERY")
    fedex_holiday_guarantee = OptionEnum("HOLIDAY_GUARANTEE")
    fedex_home_delivery_premium = OptionEnum("HOME_DELIVERY_PREMIUM")
    fedex_inside_delivery = OptionEnum("INSIDE_DELIVERY")
    fedex_inside_pickup = OptionEnum("INSIDE_PICKUP")
    fedex_international_controlled_export_service = OptionEnum(
        "INTERNATIONAL_CONTROLLED_EXPORT_SERVICE"
    )
    fedex_international_mail_service = OptionEnum("INTERNATIONAL_MAIL_SERVICE")
    fedex_international_traffic_in_arms_regulations = OptionEnum(
        "INTERNATIONAL_TRAFFIC_IN_ARMS_REGULATIONS"
    )
    fedex_liftgate_delivery = OptionEnum("LIFTGATE_DELIVERY")
    fedex_liftgate_pickup = OptionEnum("LIFTGATE_PICKUP")
    fedex_limited_access_delivery = OptionEnum("LIMITED_ACCESS_DELIVERY")
    fedex_limited_access_pickup = OptionEnum("LIMITED_ACCESS_PICKUP")
    fedex_marking_or_tagging = OptionEnum("MARKING_OR_TAGGING")
    fedex_non_business_time = OptionEnum("NON_BUSINESS_TIME")
    fedex_pallet_shrinkwrap = OptionEnum("PALLET_SHRINKWRAP")
    fedex_pallet_weight_allowance = OptionEnum("PALLET_WEIGHT_ALLOWANCE")
    fedex_pallets_provided = OptionEnum("PALLETS_PROVIDED")
    fedex_pending_complete = OptionEnum("PENDING_COMPLETE")
    fedex_pending_shipment = OptionEnum("PENDING_SHIPMENT")
    fedex_permit = OptionEnum("PERMIT")
    fedex_pharmacy_delivery = OptionEnum("PHARMACY_DELIVERY")
    fedex_poison = OptionEnum("POISON")
    fedex_port_delivery = OptionEnum("PORT_DELIVERY")
    fedex_port_pickup = OptionEnum("PORT_PICKUP")
    fedex_pre_delivery_notification = OptionEnum("PRE_DELIVERY_NOTIFICATION")
    fedex_pre_eig_processing = OptionEnum("PRE_EIG_PROCESSING")
    fedex_pre_multiplier_processing = OptionEnum("PRE_MULTIPLIER_PROCESSING")
    fedex_protection_from_freezing = OptionEnum("PROTECTION_FROM_FREEZING")
    fedex_regional_mall_delivery = OptionEnum("REGIONAL_MALL_DELIVERY")
    fedex_regional_mall_pickup = OptionEnum("REGIONAL_MALL_PICKUP")
    fedex_return_shipment = OptionEnum("RETURN_SHIPMENT")
    fedex_returns_clearance = OptionEnum("RETURNS_CLEARANCE")
    fedex_returns_clearance_special_routing_required = OptionEnum(
        "RETURNS_CLEARANCE_SPECIAL_ROUTING_REQUIRED"
    )
    fedex_saturday_delivery = OptionEnum("SATURDAY_DELIVERY")
    fedex_saturday_pickup = OptionEnum("SATURDAY_PICKUP")
    fedex_shipment_assembly = OptionEnum("SHIPMENT_ASSEMBLY")
    fedex_sort_and_segregate = OptionEnum("SORT_AND_SEGREGATE")
    fedex_special_delivery = OptionEnum("SPECIAL_DELIVERY")
    fedex_special_equipment = OptionEnum("SPECIAL_EQUIPMENT")
    fedex_storage = OptionEnum("STORAGE")
    fedex_sunday_delivery = OptionEnum("SUNDAY_DELIVERY")
    fedex_third_party_consignee = OptionEnum("THIRD_PARTY_CONSIGNEE")
    fedex_top_load = OptionEnum("TOP_LOAD")
    fedex_usps_delivery = OptionEnum("USPS_DELIVERY")
    fedex_usps_pickup = OptionEnum("USPS_PICKUP")
    fedex_weighing = OptionEnum("WEIGHING")

    """ Unified Option type mapping """
    notification = fedex_event_notification
    cash_on_delivery = fedex_cod


def shipping_options_initializer(
    options: dict,
    package_options: units.Options = None,
) -> units.Options:
    """
    Apply default values to the given options.
    """

    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.Options(options, ShippingOption, items_filter=items_filter)


class RateType(Enum):
    payor_account_package = "PAYOR_ACCOUNT_PACKAGE"
    payor_account_shipment = "PAYOR_ACCOUNT_SHIPMENT"
    payor_list_package = "PAYOR_LIST_PACKAGE"
    payor_list_shipment = "PAYOR_LIST_SHIPMENT"
    preferred_account_package = "PREFERRED_ACCOUNT_PACKAGE"
    preferred_account_shipment = "PREFERRED_ACCOUNT_SHIPMENT"
    preferred_list_package = "PREFERRED_LIST_PACKAGE"
    preferred_list_shipment = "PREFERRED_LIST_SHIPMENT"
