"""Karrio MyDHL Express units and service mappings.

This module defines all carrier-specific types for the MyDHL Express API integration,
including product codes, value added services, packaging types, and tracking statuses.
All codes are derived from the DHL Express MyDHL API OpenAPI specification v3.1.1.
"""

import karrio.lib as lib
import karrio.core.units as units


class PackagingType(lib.StrEnum):
    """DHL Express packaging types (typeCode values)."""

    # DHL branded packaging
    mydhl_flyer = "FLY"
    mydhl_box_2 = "2BC"
    mydhl_box_3 = "3BX"
    mydhl_box_4 = "4BX"
    mydhl_box_5 = "5BX"
    mydhl_box_6 = "6BX"
    mydhl_box_7 = "7BX"
    mydhl_box_8 = "8BX"
    mydhl_express_envelope = "3"
    mydhl_jumbo_box = "JB"
    mydhl_jumbo_box_junior = "JJ"

    # Customer packaging
    mydhl_customer_packaging = "YP"

    """ Unified Packaging type mapping """
    envelope = mydhl_express_envelope
    pak = mydhl_flyer
    tube = mydhl_box_2
    small_box = mydhl_box_3
    medium_box = mydhl_box_5
    large_box = mydhl_box_8
    your_packaging = mydhl_customer_packaging


class ShippingService(lib.StrEnum):
    """DHL Express Global Product Codes (productCode values).

    These are the main DHL Express shipping services available via the MyDHL API.
    Each service has a 1-2 character product code used in API requests.
    """

    # International Express Services
    mydhl_express_worldwide = "P"
    mydhl_express_12_00 = "T"
    mydhl_express_9_00 = "Y"
    mydhl_express_10_30 = "K"
    mydhl_express_easy = "8"
    mydhl_medical_express = "Q"
    mydhl_jetline = "J"
    mydhl_sprintline = "R"
    mydhl_globalmail = "G"
    mydhl_globalmail_business = "M"

    # Domestic Express Services
    mydhl_express_domestic = "N"
    mydhl_express_domestic_12_00 = "1"
    mydhl_express_domestic_9_00 = "I"
    mydhl_same_day = "S"

    # Economy/Freight Services
    mydhl_economy_select = "W"
    mydhl_europack = "H"
    mydhl_breakbulk_express = "E"
    mydhl_express_freight = "F"

    # Document Services
    mydhl_express_worldwide_doc = "D"
    mydhl_express_envelope = "X"

    # B2C Services
    mydhl_express_worldwide_b2c = "7"
    mydhl_express_easy_b2c = "6"


class ShippingOption(lib.Enum):
    """DHL Express Value Added Services (serviceCode values).

    These are additional services that can be added to shipments.
    All codes are from the MyDHL API specification reference data.
    """

    # Delivery Services
    mydhl_saturday_delivery = lib.OptionEnum("AA", bool, meta=dict(category="DELIVERY_OPTIONS"))
    mydhl_hold_for_collection = lib.OptionEnum("LX", bool, meta=dict(category="PUDO"))
    mydhl_neutral_delivery = lib.OptionEnum("NN", bool, meta=dict(category="DELIVERY_OPTIONS"))
    mydhl_residential_delivery = lib.OptionEnum("TK", bool, meta=dict(category="DELIVERY_OPTIONS"))
    mydhl_scheduled_delivery = lib.OptionEnum("TT", bool, meta=dict(category="DELIVERY_OPTIONS"))
    mydhl_collect_from_service_point = lib.OptionEnum("TV", bool, meta=dict(category="PUDO"))
    mydhl_verified_delivery = lib.OptionEnum("TF", bool, meta=dict(category="SIGNATURE"))

    # Signature Services
    mydhl_direct_signature = lib.OptionEnum("SF", bool, meta=dict(category="SIGNATURE"))
    mydhl_signature_release = lib.OptionEnum("SX", bool, meta=dict(category="SIGNATURE"))

    # Billing/Payment Services
    mydhl_duty_tax_paid = lib.OptionEnum("DD", bool)
    mydhl_receiver_paid = lib.OptionEnum("DE", bool)
    mydhl_import_billing = lib.OptionEnum("DT", bool)
    mydhl_duty_tax_importer = lib.OptionEnum("DU", bool)

    # Insurance/Protection
    mydhl_shipment_insurance = lib.OptionEnum("II", float, meta=dict(category="INSURANCE"))

    # Dangerous Goods
    mydhl_dangerous_goods = lib.OptionEnum("HE", bool, meta=dict(category="DANGEROUS_GOOD"))
    mydhl_dry_ice = lib.OptionEnum("HC", bool, meta=dict(category="DANGEROUS_GOOD"))
    mydhl_lithium_ion_pi966_section_ii = lib.OptionEnum("HD", bool, meta=dict(category="DANGEROUS_GOOD"))
    mydhl_lithium_ion_pi967_section_ii = lib.OptionEnum("HV", bool, meta=dict(category="DANGEROUS_GOOD"))
    mydhl_lithium_metal_pi969_section_ii = lib.OptionEnum("HM", bool, meta=dict(category="DANGEROUS_GOOD"))
    mydhl_lithium_metal_pi970_section_ii = lib.OptionEnum("HW", bool, meta=dict(category="DANGEROUS_GOOD"))
    mydhl_excepted_quantities = lib.OptionEnum("HH", bool, meta=dict(category="DANGEROUS_GOOD"))
    mydhl_consumer_commodities = lib.OptionEnum("HK", bool, meta=dict(category="DANGEROUS_GOOD"))
    mydhl_magnetized_material = lib.OptionEnum("HX", bool, meta=dict(category="DANGEROUS_GOOD"))
    mydhl_not_restricted_dangerous_goods = lib.OptionEnum("HU", bool, meta=dict(category="DANGEROUS_GOOD"))
    mydhl_active_data_logger = lib.OptionEnum("HT", bool, meta=dict(category="DANGEROUS_GOOD"))

    # Environmental Services
    mydhl_gogreen_climate_neutral = lib.OptionEnum("EE", bool)
    mydhl_gogreen_plus_carbon_reduced = lib.OptionEnum("FE", bool)

    # Notification Services
    mydhl_verbal_notification = lib.OptionEnum("JA", bool, meta=dict(category="NOTIFICATION"))
    mydhl_verbal_notification_alternative = lib.OptionEnum("JD", bool, meta=dict(category="NOTIFICATION"))
    mydhl_broker_notification = lib.OptionEnum("WG", bool, meta=dict(category="NOTIFICATION"))

    # Special Handling
    mydhl_emergency_situation = lib.OptionEnum("CR", bool)
    mydhl_diplomatic_mail = lib.OptionEnum("CG", bool)
    mydhl_cold_storage = lib.OptionEnum("LG", bool)
    mydhl_sanctions_routing = lib.OptionEnum("LU", bool)
    mydhl_courier_time_window = lib.OptionEnum("JY", bool, meta=dict(category="DELIVERY_OPTIONS"))
    mydhl_dedicated_pickup = lib.OptionEnum("QA", bool)
    mydhl_non_stackable_pallet = lib.OptionEnum("YC", bool)

    # Customs/Clearance Services
    mydhl_paperless_trade = lib.OptionEnum("WY", bool, meta=dict(category="PAPERLESS"))
    mydhl_export_declaration = lib.OptionEnum("WO", bool, meta=dict(category="PAPERLESS"))
    mydhl_clearance_authorization = lib.OptionEnum("WD", bool)
    mydhl_clearance_data_modification = lib.OptionEnum("WF", bool)
    mydhl_bonded_storage = lib.OptionEnum("WK", bool)
    mydhl_bonded_transit = lib.OptionEnum("WL", bool)
    mydhl_temporary_import_export = lib.OptionEnum("WM", bool)
    mydhl_non_routine_entry = lib.OptionEnum("WB", bool)
    mydhl_multiline_entry = lib.OptionEnum("WE", bool)
    mydhl_physical_intervention = lib.OptionEnum("WH", bool)
    mydhl_other_government_agency = lib.OptionEnum("WI", bool)
    mydhl_obtaining_permits_licences = lib.OptionEnum("WJ", bool)
    mydhl_post_clearance_modification = lib.OptionEnum("WS", bool)
    mydhl_sale_in_transit = lib.OptionEnum("WT", bool)

    # Data/Label Services
    mydhl_data_entry = lib.OptionEnum("PD", bool)
    mydhl_label_free = lib.OptionEnum("PZ", bool)
    mydhl_personally_identifiable_data = lib.OptionEnum("PQ", bool)
    mydhl_neutral_description_label = lib.OptionEnum("PP", bool)

    # Returns/Redirect
    mydhl_return_to_seller = lib.OptionEnum("PH", bool, meta=dict(category="RETURN"))
    mydhl_return_to_origin = lib.OptionEnum("PR", bool, meta=dict(category="RETURN"))

    # Surcharges (for reference, typically auto-applied)
    mydhl_fuel_surcharge = lib.OptionEnum("FF", bool)
    mydhl_remote_area_delivery = lib.OptionEnum("OO", bool, meta=dict(category="DELIVERY_OPTIONS"))
    mydhl_address_correction = lib.OptionEnum("MA", bool)

    # Packaging
    mydhl_packaging = lib.OptionEnum("GG", bool)

    # Import/Export Taxes
    mydhl_import_export_taxes = lib.OptionEnum("XB", bool)
    mydhl_import_export_duties = lib.OptionEnum("XX", bool)
    mydhl_merchandise_process = lib.OptionEnum("XE", bool)
    mydhl_trade_zone_process = lib.OptionEnum("XJ", bool)
    mydhl_regulatory_charges = lib.OptionEnum("XK", bool)

    # Data Staging
    mydhl_data_staging_03 = lib.OptionEnum("PT", bool)
    mydhl_data_staging_06 = lib.OptionEnum("PU", bool)
    mydhl_data_staging_12 = lib.OptionEnum("PV", bool)
    mydhl_data_staging_24 = lib.OptionEnum("PW", bool)

    # Other Services
    mydhl_shipment_preparation = lib.OptionEnum("PA", bool)
    mydhl_automated_digital_imaging = lib.OptionEnum("PJ", bool)
    mydhl_plt_images_pending = lib.OptionEnum("PK", bool)
    mydhl_optical_character_recognition = lib.OptionEnum("PL", bool)
    mydhl_commercial_invoice_data_merge = lib.OptionEnum("PM", bool)
    mydhl_comat = lib.OptionEnum("PO", bool)
    mydhl_import_billing_account = lib.OptionEnum("30", bool)

    """ Unified Option type mapping """
    insurance = mydhl_shipment_insurance
    signature_confirmation = mydhl_direct_signature
    hold_for_pickup = mydhl_hold_for_collection
    saturday_delivery = mydhl_saturday_delivery
    dangerous_goods = mydhl_dangerous_goods
    email_notification = mydhl_verbal_notification
    dry_ice = mydhl_dry_ice
    hold_at_location = mydhl_hold_for_collection

    """ Document upload options """
    doc_files = lib.OptionEnum("doc_files", lib.to_dict, meta=dict(category="PAPERLESS"))


class MeasurementUnit(lib.StrEnum):
    """Unit of measurement for weight and dimensions."""

    metric = "metric"
    imperial = "imperial"

    KG = metric
    LB = imperial
    CM = metric
    IN = imperial


class WeightUnit(lib.StrEnum):
    """Weight unit codes."""

    KG = "kg"
    LB = "lb"

    metric = KG
    imperial = LB


class DimensionUnit(lib.StrEnum):
    """Dimension unit codes."""

    CM = "cm"
    IN = "in"

    metric = CM
    imperial = IN


class LabelFormat(lib.StrEnum):
    """Supported label encoding formats."""

    PDF = "pdf"
    ZPL = "zpl"
    LP2 = "lp2"
    EPL = "epl"


class LabelTemplate(lib.StrEnum):
    """Common DHL Express label templates."""

    ECOM26_84_001 = "ECOM26_84_001"
    ECOM26_84_A4_001 = "ECOM26_84_A4_001"
    ECOM_TC_A4 = "ECOM_TC_A4"
    ECOM26_A6_002 = "ECOM26_A6_002"
    ECOM26_84CI_001 = "ECOM26_84CI_001"


class InvoiceType(lib.StrEnum):
    """Customs invoice types."""

    commercial = "commercial"
    proforma = "proforma"
    returns = "returns"


class ExportReasonType(lib.StrEnum):
    """Export declaration reason types."""

    permanent = "permanent"
    temporary = "temporary"
    returns = "return"


class PartyRoleType(lib.StrEnum):
    """Business party role types."""

    business = "business"
    direct_consumer = "direct_consumer"
    government = "government"
    other = "other"
    private = "private"
    reseller = "reseller"


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """Apply default values to the given options."""
    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class TrackingStatus(lib.Enum):
    """DHL Express tracking status mappings.

    Maps DHL event type codes to standardized Karrio tracking statuses.
    """

    pending = ["PU", "PL", "RW"]
    on_hold = ["OH", "HP", "HN", "HX"]
    delivered = ["OK", "DD", "DL", "PD"]
    in_transit = [
        "DF",
        "AF",
        "AR",
        "CC",
        "CD",
        "CI",
        "CR",
        "CS",
        "CU",
        "DS",
        "FD",
        "HP",
        "MC",
        "OF",
        "PA",
        "PF",
        "PO",
        "RD",
        "RR",
        "RT",
        "SA",
        "SC",
        "SS",
        "TD",
        "TP",
        "TR",
        "UD",
        "WC",
    ]
    delivery_failed = ["BA", "BN", "CA", "CD", "CM", "CR", "MS", "NH", "SS"]
    delivery_delayed = ["AD", "DY", "HI", "HO", "HW", "RD", "SM", "WX"]
    out_for_delivery = ["WC", "OO"]
    ready_for_pickup = ["HP", "LX"]


class TrackingIncidentReason(lib.Enum):
    """Maps MyDHL exception codes to normalized TrackingIncidentReason."""

    # Carrier-caused issues
    carrier_damaged_parcel = ["BN", "DMG"]  # Damaged parcel
    carrier_parcel_lost = ["LO", "LP"]  # Lost parcel
    carrier_sorting_error = ["MS"]  # Missorted
    carrier_delay = ["DY", "SM"]  # Delay

    # Consignee-caused issues
    consignee_refused = ["RF", "CR"]  # Refused by consignee
    consignee_not_home = ["NH", "NA"]  # Not home, Not available
    consignee_business_closed = ["BC", "CL"]  # Business closed
    consignee_incorrect_address = ["IA", "BA", "CA"]  # Incorrect/bad/changed address
    consignee_access_restricted = ["AR"]  # Access restricted

    # Customs-related issues
    customs_delay = ["CC", "CI", "CD", "CM", "CU"]  # Customs clearance/delay/inspection/missing docs/unpaid

    # Weather/Force majeure
    weather_delay = ["WX", "HW"]  # Weather delay

    # Delivery exceptions
    delivery_exception_hold = ["OH", "HP", "HN", "HX"]  # On hold variations
    delivery_exception_undeliverable = ["UD"]  # Undeliverable

    # Other delays
    delivery_delayed = ["AD", "HI", "HO", "RD"]  # Address delay, holiday, other delays

    # Unknown/Other
    unknown = []
