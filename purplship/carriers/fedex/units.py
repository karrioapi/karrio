from enum import Enum, Flag
from purplship.core.units import PackagePreset as BasePackagePreset
from dataclasses import dataclass


@dataclass
class PackagePreset(BasePackagePreset):
    dimension_unit: str = "IN"
    weight_unit: str = "LB"
    packaging_type: str = "medium_box"


class PackagePresets(Flag):
    fedex_envelope_legal_size = PackagePreset(weight=1, width=9.5, height=15.5, packaging_type="envelope")
    fedex_envelope_without_pouch = PackagePreset(weight=1, width=9.5, height=15.5, packaging_type="envelope")
    fedex_padded_pak = PackagePreset(weight=2.2, width=11.75, height=14.75, packaging_type="pak")
    fedex_polyethylene_pak = PackagePreset(weight=2.2, width=12, height=15.5, packaging_type="pak")
    fedex_clinical_pak = PackagePreset(weight=2.2, width=13.5, height=18, packaging_type="pak")
    fedex_un_3373_pak = PackagePreset(weight=2.2, width=13.5, height=18, packaging_type="pak")
    fedex_small_box = PackagePreset(weight=20, width=12.25, height=10.9, length=1.5, packaging_type="small_box")
    fedex_medium_box = PackagePreset(weight=20, width=13.25, height=11.5, length=2.38)
    fedex_large_box = PackagePreset(weight=20, width=17.88, height=12.38, length=3, packaging_type="large_box")
    fedex_10_kg_box = PackagePreset(weight=10, width=15.81, height=12.94, length=10.19)
    fedex_25_kg_box = PackagePreset(weight=25, width=21.56, height=16.56, length=13.19)
    fedex_tube = PackagePreset(weight=20, width=38, height=6, length=6, packaging_type="tube")
    fedex_envelope = fedex_envelope_legal_size
    fedex_pak = fedex_padded_pak


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
    sm = envelope
    pc = piece
    pal = pallet


class ServiceType(Enum):
    europe_first_international_priority = "EUROPE_FIRST_INTERNATIONAL_PRIORITY"
    fedex_1_day_freight = "FEDEX_1_DAY_FREIGHT"
    fedex_2_day = "FEDEX_2_DAY"
    fedex_2_day_am = "FEDEX_2_DAY_AM"
    fedex_2_day_freight = "FEDEX_2_DAY_FREIGHT"
    fedex_3_day_freight = "FEDEX_3_DAY_FREIGHT"
    fedex_cargo_airport_to_airport = "FEDEX_CARGO_AIRPORT_TO_AIRPORT"
    fedex_cargo_freight_forwarding = "FEDEX_CARGO_FREIGHT_FORWARDING"
    fedex_cargo_international_express_freight = "FEDEX_CARGO_INTERNATIONAL_EXPRESS_FREIGHT"
    fedex_cargo_international_premium = "FEDEX_CARGO_INTERNATIONAL_PREMIUM"
    fedex_cargo_mail = "FEDEX_CARGO_MAIL"
    fedex_cargo_registered_mail = "FEDEX_CARGO_REGISTERED_MAIL"
    fedex_cargo_surface_mail = "FEDEX_CARGO_SURFACE_MAIL"
    fedex_custom_critical_air_expedite = "FEDEX_CUSTOM_CRITICAL_AIR_EXPEDITE"
    fedex_custom_critical_air_expedite_exclusive_use = "FEDEX_CUSTOM_CRITICAL_AIR_EXPEDITE_EXCLUSIVE_USE"
    fedex_custom_critical_air_expedite_network = "FEDEX_CUSTOM_CRITICAL_AIR_EXPEDITE_NETWORK"
    fedex_custom_critical_charter_air = "FEDEX_CUSTOM_CRITICAL_CHARTER_AIR"
    fedex_custom_critical_point_to_point = "FEDEX_CUSTOM_CRITICAL_POINT_TO_POINT"
    fedex_custom_critical_surface_expedite = "FEDEX_CUSTOM_CRITICAL_SURFACE_EXPEDITE"
    fedex_custom_critical_surface_expedite_exclusive_use = "FEDEX_CUSTOM_CRITICAL_SURFACE_EXPEDITE_EXCLUSIVE_USE"
    fedex_custom_critical_temp_assure_air = "FEDEX_CUSTOM_CRITICAL_TEMP_ASSURE_AIR"
    fedex_custom_critical_temp_assure_validated_air = "FEDEX_CUSTOM_CRITICAL_TEMP_ASSURE_VALIDATED_AIR"
    fedex_custom_critical_white_glove_services = "FEDEX_CUSTOM_CRITICAL_WHITE_GLOVE_SERVICES"
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
    first_overnight = "FIRST_OVERNIGHT"
    ground_home_delivery = "GROUND_HOME_DELIVERY"
    international_distribution_freight = "INTERNATIONAL_DISTRIBUTION_FREIGHT"
    international_economy = "INTERNATIONAL_ECONOMY"
    international_economy_distribution = "INTERNATIONAL_ECONOMY_DISTRIBUTION"
    international_economy_freight = "INTERNATIONAL_ECONOMY_FREIGHT"
    international_first = "INTERNATIONAL_FIRST"
    international_ground = "INTERNATIONAL_GROUND"
    international_priority = "INTERNATIONAL_PRIORITY"
    international_priority_distribution = "INTERNATIONAL_PRIORITY_DISTRIBUTION"
    international_priority_express = "INTERNATIONAL_PRIORITY_EXPRESS"
    international_priority_freight = "INTERNATIONAL_PRIORITY_FREIGHT"
    priority_overnight = "PRIORITY_OVERNIGHT"
    same_day = "SAME_DAY"
    same_day_city = "SAME_DAY_CITY"
    same_day_metro_afternoon = "SAME_DAY_METRO_AFTERNOON"
    same_day_metro_morning = "SAME_DAY_METRO_MORNING"
    same_day_metro_rush = "SAME_DAY_METRO_RUSH"
    smart_post = "SMART_POST"
    standard_overnight = "STANDARD_OVERNIGHT"
    transborder_distribution_consolidation = "TRANSBORDER_DISTRIBUTION_CONSOLIDATION"


class SpecialServiceType(Flag):
    blind_shipment = "BLIND_SHIPMENT"
    broker_select_option = "BROKER_SELECT_OPTION"
    call_before_delivery = "CALL_BEFORE_DELIVERY"
    cod = "COD"
    cod_remittance = "COD_REMITTANCE"
    custom_delivery_window = "CUSTOM_DELIVERY_WINDOW"
    cut_flowers = "CUT_FLOWERS"
    dangerous_goods = "DANGEROUS_GOODS"
    delivery_on_invoice_acceptance = "DELIVERY_ON_INVOICE_ACCEPTANCE"
    detention = "DETENTION"
    do_not_break_down_pallets = "DO_NOT_BREAK_DOWN_PALLETS"
    do_not_stack_pallets = "DO_NOT_STACK_PALLETS"
    dry_ice = "DRY_ICE"
    east_coast_special = "EAST_COAST_SPECIAL"
    electronic_trade_documents = "ELECTRONIC_TRADE_DOCUMENTS"
    event_notification = "EVENT_NOTIFICATION"
    exclude_from_consolidation = "EXCLUDE_FROM_CONSOLIDATION"
    exclusive_use = "EXCLUSIVE_USE"
    exhibition_delivery = "EXHIBITION_DELIVERY"
    exhibition_pickup = "EXHIBITION_PICKUP"
    expedited_alternate_delivery_route = "EXPEDITED_ALTERNATE_DELIVERY_ROUTE"
    expedited_one_day_earlier = "EXPEDITED_ONE_DAY_EARLIER"
    expedited_service_monitoring_and_delivery = "EXPEDITED_SERVICE_MONITORING_AND_DELIVERY"
    expedited_standard_day_early_delivery = "EXPEDITED_STANDARD_DAY_EARLY_DELIVERY"
    extra_labor = "EXTRA_LABOR"
    extreme_length = "EXTREME_LENGTH"
    fedex_one_rate = "FEDEX_ONE_RATE"
    flatbed_trailer = "FLATBED_TRAILER"
    food = "FOOD"
    freight_guarantee = "FREIGHT_GUARANTEE"
    freight_to_collect = "FREIGHT_TO_COLLECT"
    future_day_shipment = "FUTURE_DAY_SHIPMENT"
    hold_at_location = "HOLD_AT_LOCATION"
    holiday_delivery = "HOLIDAY_DELIVERY"
    holiday_guarantee = "HOLIDAY_GUARANTEE"
    home_delivery_premium = "HOME_DELIVERY_PREMIUM"
    inside_delivery = "INSIDE_DELIVERY"
    inside_pickup = "INSIDE_PICKUP"
    international_controlled_export_service = "INTERNATIONAL_CONTROLLED_EXPORT_SERVICE"
    international_mail_service = "INTERNATIONAL_MAIL_SERVICE"
    international_traffic_in_arms_regulations = "INTERNATIONAL_TRAFFIC_IN_ARMS_REGULATIONS"
    liftgate_delivery = "LIFTGATE_DELIVERY"
    liftgate_pickup = "LIFTGATE_PICKUP"
    limited_access_delivery = "LIMITED_ACCESS_DELIVERY"
    limited_access_pickup = "LIMITED_ACCESS_PICKUP"
    marking_or_tagging = "MARKING_OR_TAGGING"
    non_business_time = "NON_BUSINESS_TIME"
    pallet_shrinkwrap = "PALLET_SHRINKWRAP"
    pallet_weight_allowance = "PALLET_WEIGHT_ALLOWANCE"
    pallets_provided = "PALLETS_PROVIDED"
    pending_complete = "PENDING_COMPLETE"
    pending_shipment = "PENDING_SHIPMENT"
    permit = "PERMIT"
    pharmacy_delivery = "PHARMACY_DELIVERY"
    poison = "POISON"
    port_delivery = "PORT_DELIVERY"
    port_pickup = "PORT_PICKUP"
    pre_delivery_notification = "PRE_DELIVERY_NOTIFICATION"
    pre_eig_processing = "PRE_EIG_PROCESSING"
    pre_multiplier_processing = "PRE_MULTIPLIER_PROCESSING"
    protection_from_freezing = "PROTECTION_FROM_FREEZING"
    regional_mall_delivery = "REGIONAL_MALL_DELIVERY"
    regional_mall_pickup = "REGIONAL_MALL_PICKUP"
    return_shipment = "RETURN_SHIPMENT"
    returns_clearance = "RETURNS_CLEARANCE"
    returns_clearance_special_routing_required = "RETURNS_CLEARANCE_SPECIAL_ROUTING_REQUIRED"
    saturday_delivery = "SATURDAY_DELIVERY"
    saturday_pickup = "SATURDAY_PICKUP"
    shipment_assembly = "SHIPMENT_ASSEMBLY"
    sort_and_segregate = "SORT_AND_SEGREGATE"
    special_delivery = "SPECIAL_DELIVERY"
    special_equipment = "SPECIAL_EQUIPMENT"
    storage = "STORAGE"
    sunday_delivery = "SUNDAY_DELIVERY"
    third_party_consignee = "THIRD_PARTY_CONSIGNEE"
    top_load = "TOP_LOAD"
    usps_delivery = "USPS_DELIVERY"
    usps_pickup = "USPS_PICKUP"
    weighing = "WEIGHING"

    """ Unified Option type mapping """
    notification = event_notification
    cash_on_delivery = cod


class RateType(Enum):
    payor_account_package = "PAYOR_ACCOUNT_PACKAGE"   
    payor_account_shipment = "PAYOR_ACCOUNT_SHIPMENT"  
    payor_list_package = "PAYOR_LIST_PACKAGE"      
    payor_list_shipment = "PAYOR_LIST_SHIPMENT"     
    preferred_account_package = "PREFERRED_ACCOUNT_PACKAGE"
    preferred_account_shipment = "PREFERRED_ACCOUNT_SHIPMENT"
    preferred_list_package = "PREFERRED_LIST_PACKAGE"  
    preferred_list_shipment = "PREFERRED_LIST_SHIPMENT" 
