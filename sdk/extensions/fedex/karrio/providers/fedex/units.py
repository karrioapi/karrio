import karrio.core.units as units
import karrio.core.utils as utils

PRESET_DEFAULTS = dict(
    dimension_unit="IN",
    weight_unit="LB",
)
MeasurementOptions = units.MeasurementOptionsType(
    min_in=1,
    min_cm=1,
)
COUNTRY_PREFERED_UNITS = dict(
    US=(units.WeightUnit.LB, units.DimensionUnit.IN),
)


class PackagePresets(utils.Flag):
    fedex_envelope_legal_size = units.PackagePreset(
        **dict(weight=1.0, width=9.5, height=15.5, length=1, packaging_type="envelope"),
        **PRESET_DEFAULTS
    )
    fedex_envelope_without_pouch = units.PackagePreset(
        **dict(weight=1.0, width=9.5, height=15.5, length=1, packaging_type="envelope"),
        **PRESET_DEFAULTS
    )
    fedex_padded_pak = units.PackagePreset(
        **dict(weight=2.2, width=11.75, height=14.75, length=1, packaging_type="pak"),
        **PRESET_DEFAULTS
    )
    fedex_polyethylene_pak = units.PackagePreset(
        **dict(weight=2.2, width=12.0, height=15.5, length=1, packaging_type="pak"),
        **PRESET_DEFAULTS
    )
    fedex_clinical_pak = units.PackagePreset(
        **dict(weight=2.2, width=13.5, height=18.0, length=1, packaging_type="pak"),
        **PRESET_DEFAULTS
    )
    fedex_un_3373_pak = units.PackagePreset(
        **dict(weight=2.2, width=13.5, height=18.0, length=1, packaging_type="pak"),
        **PRESET_DEFAULTS
    )
    fedex_small_box = units.PackagePreset(
        **dict(
            weight=20.0,
            width=12.25,
            height=10.9,
            length=1.5,
            packaging_type="small_box",
        ),
        **PRESET_DEFAULTS
    )
    fedex_medium_box = units.PackagePreset(
        **dict(
            weight=20.0,
            width=13.25,
            height=11.5,
            length=2.38,
            packaging_type="medium_box",
        ),
        **PRESET_DEFAULTS
    )
    fedex_large_box = units.PackagePreset(
        **dict(
            weight=20.0,
            width=17.88,
            height=12.38,
            length=3.0,
            packaging_type="large_box",
        ),
        **PRESET_DEFAULTS
    )
    fedex_extra_large_box = units.PackagePreset(
        **dict(
            weight=20.0,
            width=11.88,
            height=11.00,
            length=10.75,
            packaging_type="extra_large_box",
        ),
        **PRESET_DEFAULTS
    )
    fedex_10_kg_box = units.PackagePreset(
        **dict(
            weight=10.0,
            width=15.81,
            height=12.94,
            length=10.19,
            packaging_type="medium_box",
        ),
        **PRESET_DEFAULTS
    )
    fedex_25_kg_box = units.PackagePreset(
        **dict(
            weight=25.0,
            width=21.56,
            height=16.56,
            length=13.19,
            packaging_type="medium_box",
        ),
        **PRESET_DEFAULTS
    )
    fedex_tube = units.PackagePreset(
        **dict(weight=20.0, width=38.0, height=6.0, length=6.0, packaging_type="tube"),
        **PRESET_DEFAULTS
    )
    fedex_envelope = fedex_envelope_legal_size
    fedex_pak = fedex_padded_pak


class LabelType(utils.Flag):
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


class Incoterm(utils.Enum):
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


class PurposeType(utils.Enum):
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


class PackagingType(utils.Flag):
    fedex_envelope = "FEDEX_ENVELOPE"
    fedex_pak = "FEDEX_PAK"
    fedex_box = "FEDEX_BOX"
    fedex_small_box = "FEDEX_SMALL_BOX"
    fedex_medium_box = "FEDEX_MEDIUM_BOX"
    fedex_large_box = "FEDEX_LARGE_BOX"
    fedex_extra_large_box = "FEDEX_EXTRA_LARGE_BOX"
    fedex_10_kg_box = "FEDEX_10KG_BOX"
    fedex_25_kg_box = "FEDEX_25KG_BOX"
    fedex_tube = "FEDEX_TUBE"
    your_packaging = "YOUR_PACKAGING"

    """ Unified Packaging type mapping """
    envelope = fedex_envelope
    pak = fedex_pak
    tube = fedex_tube
    pallet = your_packaging
    small_box = fedex_small_box
    medium_box = fedex_medium_box
    large_box = fedex_large_box
    extra_large_box = fedex_extra_large_box


class PhysicalPackagingType(utils.Flag):
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


class FreightPackagingType(utils.Flag):
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
    extra_large_box = fedex_extra_large_box


class PaymentType(utils.Flag):
    account = "ACCOUNT"
    collect = "COLLECT"
    recipient = "RECIPIENT"
    sender = "SENDER"
    third_party = "THIRD_PARTY"


class ServiceType(utils.Enum):
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


class RatingOption(utils.Enum):
    fedex_one_rate = utils.OptionEnum("FEDEX_ONE_RATE", bool)
    fedex_freight_guarantee = utils.OptionEnum("FREIGHT_GUARANTEE", bool)
    fedex_saturday_delivery = utils.OptionEnum("SATURDAY_DELIVERY", bool)
    fedex_smart_post_allowed_indicia = utils.OptionEnum(
        "SMART_POST_ALLOWED_INDICIA", bool
    )
    fedex_smart_post_hub_id = utils.OptionEnum("SMART_POST_HUB_ID", bool)


class ShippingOption(utils.Enum):
    fedex_blind_shipment = utils.OptionEnum("BLIND_SHIPMENT", bool)
    fedex_broker_select_option = utils.OptionEnum("BROKER_SELECT_OPTION", bool)
    fedex_call_before_delivery = utils.OptionEnum("CALL_BEFORE_DELIVERY", bool)
    fedex_cod = utils.OptionEnum("COD", float)
    fedex_cod_remittance = utils.OptionEnum("COD_REMITTANCE", float)
    fedex_custom_delivery_window = utils.OptionEnum("CUSTOM_DELIVERY_WINDOW", bool)
    fedex_cut_flowers = utils.OptionEnum("CUT_FLOWERS", bool)
    fedex_dangerous_goods = utils.OptionEnum("DANGEROUS_GOODS", bool)
    fedex_delivery_on_invoice_acceptance = utils.OptionEnum(
        "DELIVERY_ON_INVOICE_ACCEPTANCE", bool
    )
    fedex_detention = utils.OptionEnum("DETENTION", bool)
    fedex_do_not_break_down_pallets = utils.OptionEnum(
        "DO_NOT_BREAK_DOWN_PALLETS", bool
    )
    fedex_do_not_stack_pallets = utils.OptionEnum("DO_NOT_STACK_PALLETS", bool)
    fedex_dry_ice = utils.OptionEnum("DRY_ICE", bool)
    fedex_east_coast_special = utils.OptionEnum("EAST_COAST_SPECIAL", bool)
    fedex_electronic_trade_documents = utils.OptionEnum(
        "ELECTRONIC_TRADE_DOCUMENTS", bool
    )
    fedex_event_notification = utils.OptionEnum("EVENT_NOTIFICATION", bool)
    fedex_exclude_from_consolidation = utils.OptionEnum(
        "EXCLUDE_FROM_CONSOLIDATION", bool
    )
    fedex_exclusive_use = utils.OptionEnum("EXCLUSIVE_USE", bool)
    fedex_exhibition_delivery = utils.OptionEnum("EXHIBITION_DELIVERY", bool)
    fedex_exhibition_pickup = utils.OptionEnum("EXHIBITION_PICKUP", bool)
    fedex_expedited_alternate_delivery_route = utils.OptionEnum(
        "EXPEDITED_ALTERNATE_DELIVERY_ROUTE", bool
    )
    fedex_expedited_one_day_earlier = utils.OptionEnum(
        "EXPEDITED_ONE_DAY_EARLIER", bool
    )
    fedex_expedited_service_monitoring_and_delivery = utils.OptionEnum(
        "EXPEDITED_SERVICE_MONITORING_AND_DELIVERY", bool
    )
    fedex_expedited_standard_day_early_delivery = utils.OptionEnum(
        "EXPEDITED_STANDARD_DAY_EARLY_DELIVERY", bool
    )
    fedex_extra_labor = utils.OptionEnum("EXTRA_LABOR", bool)
    fedex_extreme_length = utils.OptionEnum("EXTREME_LENGTH", bool)
    fedex_one_rate = utils.OptionEnum("FEDEX_ONE_RATE", bool)
    fedex_flatbed_trailer = utils.OptionEnum("FLATBED_TRAILER", bool)
    fedex_food = utils.OptionEnum("FOOD", bool)
    fedex_freight_guarantee = utils.OptionEnum("FREIGHT_GUARANTEE")
    fedex_freight_to_collect = utils.OptionEnum("FREIGHT_TO_COLLECT", float)
    fedex_future_day_shipment = utils.OptionEnum("FUTURE_DAY_SHIPMENT", bool)
    fedex_hold_at_location = utils.OptionEnum("HOLD_AT_LOCATION", bool)
    fedex_holiday_delivery = utils.OptionEnum("HOLIDAY_DELIVERY", bool)
    fedex_holiday_guarantee = utils.OptionEnum("HOLIDAY_GUARANTEE", bool)
    fedex_home_delivery_premium = utils.OptionEnum("HOME_DELIVERY_PREMIUM", bool)
    fedex_inside_delivery = utils.OptionEnum("INSIDE_DELIVERY", bool)
    fedex_inside_pickup = utils.OptionEnum("INSIDE_PICKUP", bool)
    fedex_international_controlled_export_service = utils.OptionEnum(
        "INTERNATIONAL_CONTROLLED_EXPORT_SERVICE", bool
    )
    fedex_international_mail_service = utils.OptionEnum(
        "INTERNATIONAL_MAIL_SERVICE", bool
    )
    fedex_international_traffic_in_arms_regulations = utils.OptionEnum(
        "INTERNATIONAL_TRAFFIC_IN_ARMS_REGULATIONS", bool
    )
    fedex_liftgate_delivery = utils.OptionEnum("LIFTGATE_DELIVERY", bool)
    fedex_liftgate_pickup = utils.OptionEnum("LIFTGATE_PICKUP", bool)
    fedex_limited_access_delivery = utils.OptionEnum("LIMITED_ACCESS_DELIVERY", bool)
    fedex_limited_access_pickup = utils.OptionEnum("LIMITED_ACCESS_PICKUP", bool)
    fedex_marking_or_tagging = utils.OptionEnum("MARKING_OR_TAGGING")
    fedex_non_business_time = utils.OptionEnum("NON_BUSINESS_TIME", bool)
    fedex_pallet_shrinkwrap = utils.OptionEnum("PALLET_SHRINKWRAP", bool)
    fedex_pallet_weight_allowance = utils.OptionEnum("PALLET_WEIGHT_ALLOWANCE", bool)
    fedex_pallets_provided = utils.OptionEnum("PALLETS_PROVIDED", bool)
    fedex_pending_complete = utils.OptionEnum("PENDING_COMPLETE", bool)
    fedex_pending_shipment = utils.OptionEnum("PENDING_SHIPMENT", bool)
    fedex_permit = utils.OptionEnum("PERMIT")
    fedex_pharmacy_delivery = utils.OptionEnum("PHARMACY_DELIVERY", bool)
    fedex_poison = utils.OptionEnum("POISON", bool)
    fedex_port_delivery = utils.OptionEnum("PORT_DELIVERY", bool)
    fedex_port_pickup = utils.OptionEnum("PORT_PICKUP", bool)
    fedex_pre_delivery_notification = utils.OptionEnum(
        "PRE_DELIVERY_NOTIFICATION", bool
    )
    fedex_pre_eig_processing = utils.OptionEnum("PRE_EIG_PROCESSING", bool)
    fedex_pre_multiplier_processing = utils.OptionEnum(
        "PRE_MULTIPLIER_PROCESSING", bool
    )
    fedex_protection_from_freezing = utils.OptionEnum("PROTECTION_FROM_FREEZING", bool)
    fedex_regional_mall_delivery = utils.OptionEnum("REGIONAL_MALL_DELIVERY", bool)
    fedex_regional_mall_pickup = utils.OptionEnum("REGIONAL_MALL_PICKUP", bool)
    fedex_return_shipment = utils.OptionEnum("RETURN_SHIPMENT", bool)
    fedex_returns_clearance = utils.OptionEnum("RETURNS_CLEARANCE", bool)
    fedex_returns_clearance_special_routing_required = utils.OptionEnum(
        "RETURNS_CLEARANCE_SPECIAL_ROUTING_REQUIRED", bool
    )
    fedex_saturday_delivery = utils.OptionEnum("SATURDAY_DELIVERY", bool)
    fedex_saturday_pickup = utils.OptionEnum("SATURDAY_PICKUP", bool)
    fedex_shipment_assembly = utils.OptionEnum("SHIPMENT_ASSEMBLY", bool)
    fedex_sort_and_segregate = utils.OptionEnum("SORT_AND_SEGREGATE", bool)
    fedex_special_delivery = utils.OptionEnum("SPECIAL_DELIVERY", bool)
    fedex_special_equipment = utils.OptionEnum("SPECIAL_EQUIPMENT", bool)
    fedex_storage = utils.OptionEnum("STORAGE", bool)
    fedex_sunday_delivery = utils.OptionEnum("SUNDAY_DELIVERY", bool)
    fedex_third_party_consignee = utils.OptionEnum("THIRD_PARTY_CONSIGNEE", bool)
    fedex_top_load = utils.OptionEnum("TOP_LOAD", bool)
    fedex_usps_delivery = utils.OptionEnum("USPS_DELIVERY", bool)
    fedex_usps_pickup = utils.OptionEnum("USPS_PICKUP", bool)
    fedex_weighing = utils.OptionEnum("WEIGHING", bool)

    """ Unified Option type mapping """
    notification = fedex_event_notification
    cash_on_delivery = fedex_cod
    paperless_trade = fedex_electronic_trade_documents


def shipping_options_initializer(
    options: dict,
    package_options: units.Options = None,
    option_type: utils.Enum = ShippingOption,
) -> units.Options:
    """
    Apply default values to the given options.
    """
    _options = options.copy()
    _add_signature = "fedex_signature_option" not in options

    if package_options is not None:
        _options.update(package_options.content)

    if _add_signature:
        _options.update(
            dict(
                fedex_signature_option=(
                    "ADULT"
                    if _options.get("signature_confirmation")
                    else "SERVICE_DEFAULT"
                )
            )
        )

    def items_filter(key: str) -> bool:
        return key in option_type  # type: ignore

    return units.ShippingOptions(_options, option_type, items_filter=items_filter)


class RateType(utils.Enum):
    payor_account_package = "PAYOR_ACCOUNT_PACKAGE"
    payor_account_shipment = "PAYOR_ACCOUNT_SHIPMENT"
    payor_list_package = "PAYOR_LIST_PACKAGE"
    payor_list_shipment = "PAYOR_LIST_SHIPMENT"
    preferred_account_package = "PREFERRED_ACCOUNT_PACKAGE"
    preferred_account_shipment = "PREFERRED_ACCOUNT_SHIPMENT"
    preferred_list_package = "PREFERRED_LIST_PACKAGE"
    preferred_list_shipment = "PREFERRED_LIST_SHIPMENT"


class UploadDocumentType(utils.Flag):
    fedex_certificate_of_origin = "CERTIFICATE_OF_ORIGIN"
    fedex_commercial_invoice = "COMMERCIAL_INVOICE"
    fedex_etd_label = "ETD_LABEL"
    fedex_nafta_certificate_of_origin = "NAFTA_CERTIFICATE_OF_ORIGIN"
    fedex_net_rate_sheet = "NET_RATE_SHEET"
    fedex_other = "OTHER"
    fedex_pro_forma_invoice = "PRO_FORMA_INVOICE"

    """ Unified upload document type mapping """
    certificate_of_origin = fedex_certificate_of_origin
    commercial_invoice = fedex_commercial_invoice
    pro_forma_invoice = fedex_pro_forma_invoice
    packing_list = fedex_other
    other = fedex_other


class DocumentUploadOption(utils.Enum):
    fedex_document_producer = utils.OptionEnum("fedex_document_producer")
    fedex_expiration_date = utils.OptionEnum("fedex_expiration_date")
