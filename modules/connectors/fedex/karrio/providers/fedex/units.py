import karrio.lib as lib
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


class PackagePresets(lib.Enum):
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


class LabelType(lib.Enum):
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


class Incoterm(lib.Enum):
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


class PurposeType(lib.Enum):
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


class PackagingType(lib.Enum):
    fedex_envelope = "FEDEX_ENVELOPE"
    fedex_box = "FEDEX_BOX"
    fedex_small_box = "FEDEX_SMALL_BOX"
    fedex_medium_box = "FEDEX_MEDIUM_BOX"
    fedex_large_box = "FEDEX_LARGE_BOX"
    fedex_extra_large_box = "FEDEX_EXTRA_LARGE_BOX"
    fedex_10kg_box = "FEDEX_10KG_BOX"
    fedex_25kg_box = "FEDEX_25KG_BOX"
    fedex_pak = "FEDEX_PAK"
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


class SubPackageType(lib.Enum):
    fedex_bag = "BAG"
    fedex_barrel = "BARREL"
    fedex_basket = "BASKET"
    fedex_box = "BOX"
    fedex_bucket = "BUCKET"
    fedex_bundle = "BUNDLE"
    fedex_cage = "CAGE"
    fedex_carton = "CARTON"
    fedex_case = "CASE"
    fedex_chest = "CHEST"
    fedex_container = "CONTAINER"
    fedex_crate = "CRATE"
    fedex_cylinder = "CYLINDER"
    fedex_drum = "DRUM"
    fedex_envelope = "ENVELOPE"
    fedex_hamper = "HAMPER"
    fedex_other = "OTHER"
    fedex_package = "PACKAGE"
    fedex_pail = "PAIL"
    fedex_pallet = "PALLET"
    fedex_parcel = "PARCEL"
    fedex_piece = "PIECE"
    fedex_reel = "REEL"
    fedex_roll = "ROLL"
    fedex_sack = "SACK"
    fedex_shrinkwrapped = "SHRINKWRAPPED"
    fedex_skid = "SKID"
    fedex_tank = "TANK"
    fedex_totebin = "TOTEBIN"
    fedex_tube = "TUBE"
    fedex_unit = "UNIT"

    """ Unified Packaging type mapping """
    envelope = fedex_envelope
    pak = fedex_other
    tube = fedex_tube
    pallet = fedex_pallet
    small_box = fedex_parcel
    medium_box = fedex_parcel
    large_box = fedex_parcel
    extra_large_box = fedex_parcel
    your_packaging = fedex_other


class PaymentType(lib.Enum):
    account = "ACCOUNT"
    collect = "COLLECT"
    recipient = "RECIPIENT"
    sender = "SENDER"
    third_party = "THIRD_PARTY"


class ConnectionConfig(lib.Enum):
    label_type = lib.OptionEnum("label_type", LabelType)
    smart_post_hub_id = lib.OptionEnum("smart_post_hub_id")
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    locale = lib.OptionEnum(
        "locale", lib.units.create_enum("Locale", ["en_US", "fr_CA"])
    )


class ShippingService(lib.Enum):
    fedex_international_priority_express = "FEDEX_INTERNATIONAL_PRIORITY_EXPRESS"
    fedex_international_first = "INTERNATIONAL_FIRST"
    fedex_international_priority = "FEDEX_INTERNATIONAL_PRIORITY"
    fedex_international_economy = "INTERNATIONAL_ECONOMY"
    fedex_ground = "FEDEX_GROUND"
    fedex_cargo_mail = "FEDEX_CARGO_MAIL"
    fedex_cargo_international_premium = "FEDEX_CARGO_INTERNATIONAL_PREMIUM"
    fedex_first_overnight = "FIRST_OVERNIGHT"
    fedex_first_overnight_freight = "FIRST_OVERNIGHT_FREIGHT"
    fedex_1_day_freight = "FEDEX_1_DAY_FREIGHT"
    fedex_2_day_freight = "FEDEX_2_DAY_FREIGHT"
    fedex_3_day_freight = "FEDEX_3_DAY_FREIGHT"
    fedex_international_priority_freight = "INTERNATIONAL_PRIORITY_FREIGHT"
    fedex_international_economy_freight = "INTERNATIONAL_ECONOMY_FREIGHT"
    fedex_cargo_airport_to_airport = "FEDEX_CARGO_AIRPORT_TO_AIRPORT"
    fedex_international_priority_distribution = "INTERNATIONAL_PRIORITY_DISTRIBUTION"
    fedex_ip_direct_distribution_freight = "FEDEX_IP_DIRECT_DISTRIBUTION_FREIGHT"
    fedex_intl_ground_distribution = "INTL_GROUND_DISTRIBUTION"
    fedex_ground_home_delivery = "GROUND_HOME_DELIVERY"
    fedex_smart_post = "SMART_POST"
    fedex_priority_overnight = "PRIORITY_OVERNIGHT"
    fedex_standard_overnight = "STANDARD_OVERNIGHT"
    fedex_2_day = "FEDEX_2_DAY"
    fedex_2_day_am = "FEDEX_2_DAY_AM"
    fedex_express_saver = "FEDEX_EXPRESS_SAVER"
    fedex_same_day = "SAME_DAY"
    fedex_same_day_city = "SAME_DAY_CITY"
    fedex_one_day_freight = "FEDEX_ONE_DAY_FREIGHT"
    fedex_international_economy_distribution = "INTERNATIONAL_ECONOMY_DISTRIBUTION"
    fedex_international_connect_plus = "FEDEX_INTERNATIONAL_CONNECT_PLUS"
    fedex_international_distribution_freight = "INTERNATIONAL_DISTRIBUTION_FREIGHT"
    fedex_regional_economy = "FEDEX_REGIONAL_ECONOMY"
    fedex_next_day_freight = "FEDEX_NEXT_DAY_FREIGHT"
    fedex_next_day = "FEDEX_NEXT_DAY"
    fedex_next_day_10am = "FEDEX_NEXT_DAY_10AM"
    fedex_next_day_12pm = "FEDEX_NEXT_DAY_12PM"
    fedex_next_day_end_of_day = "FEDEX_NEXT_DAY_END_OF_DAY"
    fedex_distance_deferred = "FEDEX_DISTANCE_DEFERRED"


class ShippingOption(lib.Enum):
    # fmt: off
    fedex_appointment = lib.OptionEnum("APPOINTMENT", bool, meta=dict(category="DELIVERY_OPTIONS"))
    fedex_broker_select_option = lib.OptionEnum("BROKER_SELECT_OPTION", bool)
    fedex_call_before_delivery = lib.OptionEnum("CALL_BEFORE_DELIVERY", bool, meta=dict(category="NOTIFICATION"))
    fedex_cod = lib.OptionEnum("COD", float, meta=dict(category="COD"))
    fedex_custom_delivery_window = lib.OptionEnum("CUSTOM_DELIVERY_WINDOW", bool, meta=dict(category="DELIVERY_OPTIONS"))
    fedex_cut_flowers = lib.OptionEnum("CUT_FLOWERS", bool)
    fedex_do_not_break_down_pallets = lib.OptionEnum("DO_NOT_BREAK_DOWN_PALLETS", bool)
    fedex_do_not_stack_pallets = lib.OptionEnum("DO_NOT_STACK_PALLETS", bool)
    fedex_dry_ice = lib.OptionEnum("DRY_ICE", bool, meta=dict(category="DANGEROUS_GOOD"))
    fedex_east_coast_special = lib.OptionEnum("EAST_COAST_SPECIAL", bool)
    fedex_exclude_from_consolidation = lib.OptionEnum("EXCLUDE_FROM_CONSOLIDATION", bool)
    fedex_extreme_length = lib.OptionEnum("EXTREME_LENGTH", bool)
    fedex_inside_delivery = lib.OptionEnum("INSIDE_DELIVERY", bool)
    fedex_inside_pickup = lib.OptionEnum("INSIDE_PICKUP", bool)
    fedex_international_controlled_export_service = lib.OptionEnum("INTERNATIONAL_CONTROLLED_EXPORT_SERVICE", bool)
    fedex_third_party_consignee = lib.OptionEnum("THIRD_PARTY_CONSIGNEE", bool)
    fedex_electronic_trade_documents = lib.OptionEnum("ELECTRONIC_TRADE_DOCUMENTS", bool, meta=dict(category="PAPERLESS"))
    fedex_food = lib.OptionEnum("FOOD", bool)
    fedex_future_day_shipment = lib.OptionEnum("FUTURE_DAY_SHIPMENT", bool, meta=dict(category="DELIVERY_OPTIONS"))
    fedex_hold_at_location = lib.OptionEnum("HOLD_AT_LOCATION", bool, meta=dict(category="PUDO"))
    fedex_international_traffic_in_arms_regulations = lib.OptionEnum("INTERNATIONAL_TRAFFIC_IN_ARMS_REGULATIONS", bool)
    fedex_liftgate_delivery = lib.OptionEnum("LIFTGATE_DELIVERY", bool)
    fedex_liftgate_pickup = lib.OptionEnum("LIFTGATE_PICKUP", bool)
    fedex_limited_access_delivery = lib.OptionEnum("LIMITED_ACCESS_DELIVERY", bool)
    fedex_limited_access_pickup = lib.OptionEnum("LIMITED_ACCESS_PICKUP", bool)
    fedex_over_length = lib.OptionEnum("OVER_LENGTH", bool)
    fedex_pending_shipment = lib.OptionEnum("PENDING_SHIPMENT", bool)
    fedex_pharmacy_delivery = lib.OptionEnum("PHARMACY_DELIVERY", bool)
    fedex_poison = lib.OptionEnum("POISON", bool, meta=dict(category="DANGEROUS_GOOD"))
    fedex_home_delivery_premium = lib.OptionEnum("HOME_DELIVERY_PREMIUM", bool)
    fedex_protection_from_freezing = lib.OptionEnum("PROTECTION_FROM_FREEZING", bool)
    fedex_returns_clearance = lib.OptionEnum("RETURNS_CLEARANCE", bool, meta=dict(category="RETURN"))
    fedex_return_shipment = lib.OptionEnum("RETURN_SHIPMENT", bool, meta=dict(category="RETURN"))
    fedex_saturday_pickup = lib.OptionEnum("SATURDAY_PICKUP", bool, meta=dict(category="DELIVERY_OPTIONS"))
    fedex_event_notification = lib.OptionEnum("EVENT_NOTIFICATION", bool, meta=dict(category="NOTIFICATION"))
    fedex_delivery_on_invoice_acceptance = lib.OptionEnum("DELIVERY_ON_INVOICE_ACCEPTANCE", bool)
    fedex_top_load = lib.OptionEnum("TOP_LOAD", bool)

    """ Rating Options """
    fedex_one_rate = lib.OptionEnum("FEDEX_ONE_RATE", bool)
    fedex_freight_guarantee = lib.OptionEnum("FREIGHT_GUARANTEE", bool)
    fedex_saturday_delivery = lib.OptionEnum("SATURDAY_DELIVERY", bool, meta=dict(category="DELIVERY_OPTIONS"))
    fedex_smart_post_hub_id = lib.OptionEnum("SMART_POST_HUB_ID")
    fedex_smart_post_allowed_indicia = lib.OptionEnum("SMART_POST_ALLOWED_INDICIA")

    """ Package Options """

    fedex_alcohol = lib.OptionEnum("ALCOHOL", bool, meta=dict(category="DANGEROUS_GOOD"))
    fedex_battery = lib.OptionEnum("BATTERY", bool, meta=dict(category="DANGEROUS_GOOD"))
    fedex_dangerous_goods = lib.OptionEnum("DANGEROUS_GOODS", bool, meta=dict(category="DANGEROUS_GOOD"))
    fedex_priority_alert = lib.OptionEnum("PRIORITY_ALERT", bool, meta=dict(category="NOTIFICATION"))
    fedex_priority_alert_plus = lib.OptionEnum("PRIORITY_ALERT_PLUS", bool, meta=dict(category="NOTIFICATION"))
    fedex_non_standard_container = lib.OptionEnum("NON_STANDARD_CONTAINER", bool)
    fedex_piece_count_verification = lib.OptionEnum("PIECE_COUNT_VERIFICATION", bool)
    fedex_signature_option = lib.OptionEnum("SIGNATURE_OPTION", meta=dict(category="SIGNATURE"))
    fedex_evening = lib.OptionEnum("EVENING", bool, meta=dict(category="DELIVERY_OPTIONS"))
    fedex_date_certain = lib.OptionEnum("DATE_CERTAIN", bool, meta=dict(category="DELIVERY_OPTIONS"))

    """ Unified Option type mapping """
    cash_on_delivery = fedex_cod
    dangerous_good = fedex_dangerous_goods
    notification = fedex_event_notification
    saturday_delivery = fedex_saturday_delivery
    paperless_trade = fedex_electronic_trade_documents
    doc_files = lib.OptionEnum("doc_files", lib.to_dict, meta=dict(category="PAPERLESS"))
    doc_references = lib.OptionEnum("doc_references", lib.to_dict, meta=dict(category="PAPERLESS"))
    shipper_instructions = lib.OptionEnum("shipper_instructions", meta=dict(category="INSTRUCTIONS"))
    recipient_instructions = lib.OptionEnum("recipient_instructions", meta=dict(category="INSTRUCTIONS"))
    # fmt: on


RATING_OPTIONS = [
    "FREIGHT_GUARANTEE",
    "SATURDAY_DELIVERY",
    "SMART_POST_ALLOWED_INDICIA",
    "SMART_POST_HUB_ID",
]
PACKAGE_OPTIONS = [
    "ALCOHOL",
    "APPOINTMENT",
    "BATTERY",
    "COD",
    "DANGEROUS_GOODS",
    "DRY_ICE",
    "PRIORITY_ALERT",
    "PRIORITY_ALERT_PLUS",
    "NON_STANDARD_CONTAINER",
    "PIECE_COUNT_VERIFICATION",
    "SIGNATURE_OPTION",
    "EVENING",
    "DATE_CERTAIN",
    "SATURDAY_PICKUP",
]
SHIPMENT_OPTIONS = [
    "APPOINTMENT",
    "BROKER_SELECT_OPTION",
    "CALL_BEFORE_DELIVERY",
    "COD",
    "CUSTOM_DELIVERY_WINDOW",
    "CUT_FLOWERS",
    "DO_NOT_BREAK_DOWN_PALLETS",
    "DO_NOT_STACK_PALLETS",
    "DRY_ICE",
    "EAST_COAST_SPECIAL",
    "EXCLUDE_FROM_CONSOLIDATION",
    "EXTREME_LENGTH",
    "INSIDE_DELIVERY",
    "INSIDE_PICKUP",
    "INTERNATIONAL_CONTROLLED_EXPORT_SERVICE",
    "FEDEX_ONE_RATE",
    "THIRD_PARTY_CONSIGNEE",
    "ELECTRONIC_TRADE_DOCUMENTS",
    "FOOD",
    "HOLD_AT_LOCATION",
    "INTERNATIONAL_TRAFFIC_IN_ARMS_REGULATIONS",
    "LIFTGATE_DELIVERY",
    "LIFTGATE_PICKUP",
    "LIMITED_ACCESS_DELIVERY",
    "LIMITED_ACCESS_PICKUP",
    "OVER_LENGTH",
    "PENDING_SHIPMENT",
    "PHARMACY_DELIVERY",
    "POISON",
    "HOME_DELIVERY_PREMIUM",
    "PROTECTION_FROM_FREEZING",
    "RETURNS_CLEARANCE",
    "RETURN_SHIPMENT",
    "SATURDAY_DELIVERY",
    "SATURDAY_PICKUP",
    "EVENT_NOTIFICATION",
    "DELIVERY_ON_INVOICE_ACCEPTANCE",
    "TOP_LOAD",
    "FREIGHT_GUARANTEE",
]


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

    def items_filter(key: str) -> bool:
        return key in ShippingOption and key not in ["doc_files", "doc_references"]  # type: ignore

    return units.ShippingOptions(_options, ShippingOption, items_filter=items_filter)


class RateType(lib.Enum):
    payor_account_package = "PAYOR_ACCOUNT_PACKAGE"
    payor_account_shipment = "PAYOR_ACCOUNT_SHIPMENT"
    payor_list_package = "PAYOR_LIST_PACKAGE"
    payor_list_shipment = "PAYOR_LIST_SHIPMENT"
    preferred_account_package = "PREFERRED_ACCOUNT_PACKAGE"
    preferred_account_shipment = "PREFERRED_ACCOUNT_SHIPMENT"
    preferred_list_package = "PREFERRED_LIST_PACKAGE"
    preferred_list_shipment = "PREFERRED_LIST_SHIPMENT"


class SignatureOptionType(lib.Enum):
    adult = "ADULT"
    direct = "DIRECT"
    indirect = "INDIRECT"
    no_signature_required = "NO_SIGNATURE_REQUIRED"
    service_default = "SERVICE_DEFAULT"


class UploadDocumentType(lib.Enum):
    fedex_usmca_commercial_invoice_certification_of_origin = (
        "USMCA_COMMERCIAL_INVOICE_CERTIFICATION_OF_ORIGIN"
    )
    fedex_usmca_certification_of_origin = "USMCA_CERTIFICATION_OF_ORIGIN"
    fedex_certificate_of_origin = "CERTIFICATE_OF_ORIGIN"
    fedex_commercial_invoice = "COMMERCIAL_INVOICE"
    fedex_pro_forma_invoice = "PRO_FORMA_INVOICE"
    fedex_net_rate_sheet = "NET_RATE_SHEET"
    fedex_etd_label = "ETD_LABEL"
    fedex_other = "OTHER"

    """ Unified upload document type mapping """
    certificate_of_origin = fedex_certificate_of_origin
    commercial_invoice = fedex_commercial_invoice
    pro_forma_invoice = fedex_pro_forma_invoice
    packing_list = fedex_other
    other = fedex_other


class DocumentUploadOption(lib.Enum):
    fedex_carrier_code = lib.OptionEnum("carrierCode", str)
    pre_shipment = lib.OptionEnum("pre_shipment", bool)


class TrackingStatus(utils.Enum):
    # Based on FedEx API event/status codes.
    # https://developer.fedex.com/api/en-us/guides/api-reference.html#trackingstatuscodes

    # Pending/manifest statuses - shipment info received, awaiting pickup
    pending = ["OC", "OX", "EP", "MD"]
    # OC = Order Created,  OX = Shipment info sent to USPS, EP = Enroute to Pickup, MD = Manifest Data

    # Picked up - package physically picked up by carrier (NEW)
    picked_up = ["PU", "PX", "OF", "AP"]
    # PU = Picked Up, PX = Picked Up (see details), OF = At FedEx origin facility, AP = At Pickup

    # Delivered statuses
    delivered = ["DL"]
    # DL = Delivered

    # In-transit/processing statuses
    in_transit = ["IT", "IX", "AA", "AC", "AF", "AR", "AX", "DP", "EA", "EO", "FD", "LO", "Ow", "PF", "PL", "PM", "SF", "TR"]
    # IT = In Transit, IX = In Transit (see details), AA = At Airport, AC = At Canada Post facility
    # AF = At local FedEx facility, AR = Arrived at FedEx location, AX = At USPS facility, DP = Departed
    # EA = Enroute to Airport, EO = Enroute to Origin Airport, FD = At FedEx destination, LO = Left Origin
    # Ow = On the way, PF = Plane in Flight, PL = Plane Landed, PM = In Progress, SF = At Sort Facility
    # TR = Transfer

    # Out for delivery
    out_for_delivery = ["AD", "ED", "OD"]
    # AD = At Delivery, ED = Enroute to Delivery, OD = Out for Delivery

    # On hold/exception statuses
    on_hold = ["CD", "SE", "HA"]
    # SE = Shipment Exception, CD = Customs Delay, HA = Hold at Location Requested
    
    # Delivery failed/returned statuses
    delivery_failed = ["DE"]
    # I assume these get a DE status
    # DE = Delivery Exception

    # Cancelled/void statuses
    cancelled = ["CA", "RD"]
    # CA = Shipment Cancelled, RD = Return label link expired

    # Ready for pickup
    ready_for_pickup = ["HL", "HP"]
    # HL = Hold at Location, HP = Ready for Recipient Pickup

    # Delivery delayed
    delivery_delayed = ["DY", "DD", "PY"]
    # DY = Delay, DD = Delivery Delay, PY = Pickup Delay

    # Return to sender
    return_to_sender = ["RS", "RT"]
    # RS = Return to Shipper, RT = Return to Shipper Requested

    # Unknown/unrecognized statuses
    unknown = []  # For any unrecognized status codes


class TrackingIncidentReason(utils.Enum):
    """Maps FedEx exception codes to normalized TrackingIncidentReason.

    Based on FedEx API exception/status codes.
    """
    # Carrier-caused issues
    carrier_damaged_parcel = []  # Damaged
    carrier_sorting_error = ["MR", "MSR"]  # Misrouted
    carrier_address_not_found = ["NA", "ANF"]  # Address not found
    carrier_parcel_lost = []  # Lost
    carrier_not_enough_time = []  # No time
    carrier_vehicle_issue = ["DR"]  # Mechanical, vehicle breakdown

    # Consignee-caused issues
    consignee_refused = ["RF", "RJ", "RE"]  # Refused
    consignee_business_closed = ["BC", "CL"]  # Business closed
    consignee_not_available = ["NA1", "NI"]  # Not available
    consignee_not_home = ["NH", "NAH"]  # Not home
    consignee_incorrect_address = ["IA", "WA", "BA"]  # Incorrect/wrong/bad address
    consignee_access_restricted = ["NS", "SC"]  # No safe location, security issue

    # Customs-related issues
    customs_delay = ["CD", "CP"]  # Customs delay/hold/inspection
    customs_documentation = []  # Customs missing docs, paperwork
    customs_duties_unpaid = []  # Customs unpaid, duties unpaid

    # Weather/Force majeure
    weather_delay = ["WE", "WD", "PMX"]  # Weather
    natural_disaster = ["ND", "EM"]  # Natural disaster, emergency

    # Delivery exceptions
    delivery_exception_hold = ["SEC", "HD"]  # Customer-requested hold, hold at depot
    delivery_exception_undeliverable = ["PD", "UD"]  # Problem with delivery, undeliverable

    # Other issues
    unknown = []  # Unrecognized codes


class ShippingDocumentCategory(lib.StrEnum):
    """FedEx document category mapping to karrio unified categories."""

    commercial_invoice = "COMMERCIAL_INVOICE"
    return_label = "RETURN"
    customs_document = "CUSTOMS"
    dangerous_goods_document = "DANGEROUS_GOODS"
    certificate_of_origin = "CERTIFICATE_OF_ORIGIN"
    etd_document = "ETD"
    packing_list = "PACKING_LIST"
    shipping_label = "LABEL"
    other = "OTHER"
