from purplship.core.utils import Enum, Flag
from purplship.core.units import PackagePreset as BasePackagePreset
from dataclasses import dataclass


@dataclass
class PackagePreset(BasePackagePreset):
    dimension_unit: str = "IN"
    weight_unit: str = "LB"
    packaging_type: str = "medium_box"


class PackagePresets(Flag):
    fedex_envelope_legal_size = PackagePreset(
        weight=1.0, width=9.5, height=15.5, packaging_type="envelope"
    )
    fedex_envelope_without_pouch = PackagePreset(
        weight=1.0, width=9.5, height=15.5, packaging_type="envelope"
    )
    fedex_padded_pak = PackagePreset(
        weight=2.2, width=11.75, height=14.75, packaging_type="pak"
    )
    fedex_polyethylene_pak = PackagePreset(
        weight=2.2, width=12.0, height=15.5, packaging_type="pak"
    )
    fedex_clinical_pak = PackagePreset(
        weight=2.2, width=13.5, height=18.0, packaging_type="pak"
    )
    fedex_un_3373_pak = PackagePreset(
        weight=2.2, width=13.5, height=18.0, packaging_type="pak"
    )
    fedex_small_box = PackagePreset(
        weight=20.0, width=12.25, height=10.9, length=1.5, packaging_type="small_box"
    )
    fedex_medium_box = PackagePreset(weight=20.0, width=13.25, height=11.5, length=2.38)
    fedex_large_box = PackagePreset(
        weight=20.0, width=17.88, height=12.38, length=3.0, packaging_type="large_box"
    )
    fedex_10_kg_box = PackagePreset(
        weight=10.0, width=15.81, height=12.94, length=10.19
    )
    fedex_25_kg_box = PackagePreset(
        weight=25.0, width=21.56, height=16.56, length=13.19
    )
    fedex_tube = PackagePreset(
        weight=20.0, width=38.0, height=6.0, length=6.0, packaging_type="tube"
    )
    fedex_envelope = fedex_envelope_legal_size
    fedex_pak = fedex_padded_pak


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
    fedex_transborder_distribution_consolidation = "TRANSBORDER_DISTRIBUTION_CONSOLIDATION"


class SpecialServiceType(Flag):
    fedex_blind_shipment = "BLIND_SHIPMENT"
    fedex_broker_select_option = "BROKER_SELECT_OPTION"
    fedex_call_before_delivery = "CALL_BEFORE_DELIVERY"
    fedex_cod = "COD"
    fedex_cod_remittance = "COD_REMITTANCE"
    fedex_custom_delivery_window = "CUSTOM_DELIVERY_WINDOW"
    fedex_cut_flowers = "CUT_FLOWERS"
    fedex_dangerous_goods = "DANGEROUS_GOODS"
    fedex_delivery_on_invoice_acceptance = "DELIVERY_ON_INVOICE_ACCEPTANCE"
    fedex_detention = "DETENTION"
    fedex_do_not_break_down_pallets = "DO_NOT_BREAK_DOWN_PALLETS"
    fedex_do_not_stack_pallets = "DO_NOT_STACK_PALLETS"
    fedex_dry_ice = "DRY_ICE"
    fedex_east_coast_special = "EAST_COAST_SPECIAL"
    fedex_electronic_trade_documents = "ELECTRONIC_TRADE_DOCUMENTS"
    fedex_event_notification = "EVENT_NOTIFICATION"
    fedex_exclude_from_consolidation = "EXCLUDE_FROM_CONSOLIDATION"
    fedex_exclusive_use = "EXCLUSIVE_USE"
    fedex_exhibition_delivery = "EXHIBITION_DELIVERY"
    fedex_exhibition_pickup = "EXHIBITION_PICKUP"
    fedex_expedited_alternate_delivery_route = "EXPEDITED_ALTERNATE_DELIVERY_ROUTE"
    fedex_expedited_one_day_earlier = "EXPEDITED_ONE_DAY_EARLIER"
    fedex_expedited_service_monitoring_and_delivery = (
        "EXPEDITED_SERVICE_MONITORING_AND_DELIVERY"
    )
    fedex_expedited_standard_day_early_delivery = "EXPEDITED_STANDARD_DAY_EARLY_DELIVERY"
    fedex_extra_labor = "EXTRA_LABOR"
    fedex_extreme_length = "EXTREME_LENGTH"
    fedex_one_rate = "FEDEX_ONE_RATE"
    fedex_flatbed_trailer = "FLATBED_TRAILER"
    fedex_food = "FOOD"
    fedex_freight_guarantee = "FREIGHT_GUARANTEE"
    fedex_freight_to_collect = "FREIGHT_TO_COLLECT"
    fedex_future_day_shipment = "FUTURE_DAY_SHIPMENT"
    fedex_hold_at_location = "HOLD_AT_LOCATION"
    fedex_holiday_delivery = "HOLIDAY_DELIVERY"
    fedex_holiday_guarantee = "HOLIDAY_GUARANTEE"
    fedex_home_delivery_premium = "HOME_DELIVERY_PREMIUM"
    fedex_inside_delivery = "INSIDE_DELIVERY"
    fedex_inside_pickup = "INSIDE_PICKUP"
    fedex_international_controlled_export_service = "INTERNATIONAL_CONTROLLED_EXPORT_SERVICE"
    fedex_international_mail_service = "INTERNATIONAL_MAIL_SERVICE"
    fedex_international_traffic_in_arms_regulations = (
        "INTERNATIONAL_TRAFFIC_IN_ARMS_REGULATIONS"
    )
    fedex_liftgate_delivery = "LIFTGATE_DELIVERY"
    fedex_liftgate_pickup = "LIFTGATE_PICKUP"
    fedex_limited_access_delivery = "LIMITED_ACCESS_DELIVERY"
    fedex_limited_access_pickup = "LIMITED_ACCESS_PICKUP"
    fedex_marking_or_tagging = "MARKING_OR_TAGGING"
    fedex_non_business_time = "NON_BUSINESS_TIME"
    fedex_pallet_shrinkwrap = "PALLET_SHRINKWRAP"
    fedex_pallet_weight_allowance = "PALLET_WEIGHT_ALLOWANCE"
    fedex_pallets_provided = "PALLETS_PROVIDED"
    fedex_pending_complete = "PENDING_COMPLETE"
    fedex_pending_shipment = "PENDING_SHIPMENT"
    fedex_permit = "PERMIT"
    fedex_pharmacy_delivery = "PHARMACY_DELIVERY"
    fedex_poison = "POISON"
    fedex_port_delivery = "PORT_DELIVERY"
    fedex_port_pickup = "PORT_PICKUP"
    fedex_pre_delivery_notification = "PRE_DELIVERY_NOTIFICATION"
    fedex_pre_eig_processing = "PRE_EIG_PROCESSING"
    fedex_pre_multiplier_processing = "PRE_MULTIPLIER_PROCESSING"
    fedex_protection_from_freezing = "PROTECTION_FROM_FREEZING"
    fedex_regional_mall_delivery = "REGIONAL_MALL_DELIVERY"
    fedex_regional_mall_pickup = "REGIONAL_MALL_PICKUP"
    fedex_return_shipment = "RETURN_SHIPMENT"
    fedex_returns_clearance = "RETURNS_CLEARANCE"
    fedex_returns_clearance_special_routing_required = (
        "RETURNS_CLEARANCE_SPECIAL_ROUTING_REQUIRED"
    )
    fedex_saturday_delivery = "SATURDAY_DELIVERY"
    fedex_saturday_pickup = "SATURDAY_PICKUP"
    fedex_shipment_assembly = "SHIPMENT_ASSEMBLY"
    fedex_sort_and_segregate = "SORT_AND_SEGREGATE"
    fedex_special_delivery = "SPECIAL_DELIVERY"
    fedex_special_equipment = "SPECIAL_EQUIPMENT"
    fedex_storage = "STORAGE"
    fedex_sunday_delivery = "SUNDAY_DELIVERY"
    fedex_third_party_consignee = "THIRD_PARTY_CONSIGNEE"
    fedex_top_load = "TOP_LOAD"
    fedex_usps_delivery = "USPS_DELIVERY"
    fedex_usps_pickup = "USPS_PICKUP"
    fedex_weighing = "WEIGHING"

    """ Unified Option type mapping """
    notification = fedex_event_notification
    cash_on_delivery = fedex_cod


class RateType(Enum):
    payor_account_package = "PAYOR_ACCOUNT_PACKAGE"
    payor_account_shipment = "PAYOR_ACCOUNT_SHIPMENT"
    payor_list_package = "PAYOR_LIST_PACKAGE"
    payor_list_shipment = "PAYOR_LIST_SHIPMENT"
    preferred_account_package = "PREFERRED_ACCOUNT_PACKAGE"
    preferred_account_shipment = "PREFERRED_ACCOUNT_SHIPMENT"
    preferred_list_package = "PREFERRED_LIST_PACKAGE"
    preferred_list_shipment = "PREFERRED_LIST_SHIPMENT"
