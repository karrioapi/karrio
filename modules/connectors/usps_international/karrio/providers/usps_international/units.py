import karrio.lib as lib
import karrio.core.units as units


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type"""

    PACKAGE = "PACKAGE"

    """ Unified Packaging type mapping """
    envelope = PACKAGE
    pak = PACKAGE
    tube = PACKAGE
    pallet = PACKAGE
    small_box = PACKAGE
    medium_box = PACKAGE
    your_packaging = PACKAGE


class CustomsContentType(lib.StrEnum):
    merchandise = "MERCHANDISE"
    gift = "GIFT"
    document = "DOCUMENT"
    commercial_sample = "COMMERCIAL_SAMPLE"
    returned_goods = "RETURNED_GOODS"
    other = "OTHER"
    humanitarian_donations = "HUMANITARIAN_DONATIONS"
    dangerous_goods = "DANGEROUS_GOODS"
    cremated_remains = "CREMATED_REMAINS"
    non_negotiable_document = "NON_NEGOTIABLE_DOCUMENT"
    medical_supplies = "MEDICAL_SUPPLIES"
    pharmaceuticals = "PHARMACEUTICALS"

    """ Unified Content type mapping """

    documents = document
    sample = commercial_sample
    return_merchandise = returned_goods


class LabelType(lib.StrEnum):
    """Carrier specific label type"""

    PDF = "PDF"
    TIFF = "TIFF"
    JPG = "JPG"
    SVG = "SVG"
    ZPL203DPI = "ZPL203DPI"
    ZPL300DPI = "ZPL300DPI"
    LABEL_BROKER = "LABEL_BROKER"
    NONE = "NONE"

    """ Unified Label type mapping """
    ZPL = ZPL300DPI
    PNG = JPG


class ShippingService(lib.StrEnum):
    """Carrier specific services"""

    usps_standard_service = "USPS Standard Service"
    usps_parcel_select = "PARCEL_SELECT"
    usps_parcel_select_lightweight = "PARCEL_SELECT_LIGHTWEIGHT"
    usps_priority_mail_express = "PRIORITY_MAIL_EXPRESS"
    usps_priority_mail = "PRIORITY_MAIL"
    usps_first_class_package_service = "FIRST-CLASS_PACKAGE_SERVICE"
    usps_library_mail = "LIBRARY_MAIL"
    usps_media_mail = "MEDIA_MAIL"
    usps_bound_printed_matter = "BOUND_PRINTED_MATTER"
    usps_connect_local = "USPS_CONNECT_LOCAL"
    usps_connect_mail = "USPS_CONNECT_MAIL"
    usps_connect_next_day = "USPS_CONNECT_NEXT_DAY"
    usps_connect_regional = "USPS_CONNECT_REGIONAL"
    usps_connect_same_day = "USPS_CONNECT_SAME_DAY"
    usps_ground_advantage = "USPS_GROUND_ADVANTAGE"
    usps_retail_ground = "USPS_RETAIL_GROUND"
    usps_all = "ALL"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    # fmt: off
    usps_label_delivery_service = lib.OptionEnum("415", bool)
    usps_tracking_plus_6_months = lib.OptionEnum("480", bool)
    usps_tracking_plus_1_year = lib.OptionEnum("481", bool)
    usps_tracking_plus_3_years = lib.OptionEnum("482", bool)
    usps_tracking_plus_5_years = lib.OptionEnum("483", bool)
    usps_tracking_plus_7_years = lib.OptionEnum("484", bool)
    usps_tracking_plus_10_years = lib.OptionEnum("485", bool)
    usps_tracking_plus_signature_3_years = lib.OptionEnum("486", bool)
    usps_tracking_plus_signature_5_years = lib.OptionEnum("487", bool)
    usps_tracking_plus_signature_7_years = lib.OptionEnum("488", bool)
    usps_tracking_plus_signature_10_years = lib.OptionEnum("489", bool)
    usps_hazardous_materials_air_eligible_ethanol = lib.OptionEnum("810", bool)
    usps_hazardous_materials_class_1_toy_propellant_safety_fuse_package = lib.OptionEnum("811", bool)
    usps_hazardous_materials_class_3_flammable_and_combustible_liquids = lib.OptionEnum("812", bool)
    usps_hazardous_materials_class_7_radioactive_materials = lib.OptionEnum("813", bool)
    usps_hazardous_materials_class_8_air_eligible_corrosive_materials = lib.OptionEnum("814", bool)
    usps_hazardous_materials_class_8_nonspillable_wet_batteries = lib.OptionEnum("815", bool)
    usps_hazardous_materials_class_9_lithium_battery_marked_ground_only = lib.OptionEnum("816", bool)
    usps_hazardous_materials_class_9_lithium_battery_returns = lib.OptionEnum("817", bool)
    usps_hazardous_materials_class_9_marked_lithium_batteries = lib.OptionEnum("818", bool)
    usps_hazardous_materials_class_9_dry_ice = lib.OptionEnum("819", bool)
    usps_hazardous_materials_class_9_unmarked_lithium_batteries = lib.OptionEnum("820", bool)
    usps_hazardous_materials_class_9_magnetized_materials = lib.OptionEnum("821", bool)
    usps_hazardous_materials_division_4_1_mailable_flammable_solids_and_safety_matches = lib.OptionEnum("822", bool)
    usps_hazardous_materials_division_5_1_oxidizers = lib.OptionEnum("823", bool)
    usps_hazardous_materials_division_5_2_organic_peroxides = lib.OptionEnum("824", bool)
    usps_hazardous_materials_division_6_1_toxic_materials = lib.OptionEnum("825", bool)
    usps_hazardous_materials_division_6_2_biological_materials = lib.OptionEnum("826", bool)
    usps_hazardous_materials_excepted_quantity_provision = lib.OptionEnum("827", bool)
    usps_hazardous_materials_ground_only_hazardous_materials = lib.OptionEnum("828", bool)
    usps_hazardous_materials_air_eligible_id8000_consumer_commodity = lib.OptionEnum("829", bool)
    usps_hazardous_materials_lighters = lib.OptionEnum("830", bool)
    usps_hazardous_materials_limited_quantity_ground = lib.OptionEnum("831", bool)
    usps_hazardous_materials_small_quantity_provision_markings_required = lib.OptionEnum("832", bool)
    usps_hazardous_materials = lib.OptionEnum("857", bool)
    usps_certified_mail = lib.OptionEnum("910", bool)
    usps_certified_mail_restricted_delivery = lib.OptionEnum("911", bool)
    usps_certified_mail_adult_signature_required = lib.OptionEnum("912", bool)
    usps_certified_mail_adult_signature_restricted_delivery = lib.OptionEnum("913", bool)
    usps_collect_on_delivery = lib.OptionEnum("915", float)
    usps_collect_on_delivery_restricted_delivery = lib.OptionEnum("917", bool)
    usps_tracking_electronic = lib.OptionEnum("920", bool)
    usps_signature_confirmation = lib.OptionEnum("921", bool)
    usps_adult_signature_required = lib.OptionEnum("922", bool)
    usps_adult_signature_restricted_delivery = lib.OptionEnum("923", bool)
    usps_signature_confirmation_restricted_delivery = lib.OptionEnum("924", bool)
    usps_priority_mail_express_merchandise_insurance = lib.OptionEnum("925", bool)
    usps_insurance_bellow_500 = lib.OptionEnum("930", float)
    usps_insurance_above_500 = lib.OptionEnum("931", float)
    usps_insurance_restricted_delivery = lib.OptionEnum("934", bool)
    usps_registered_mail = lib.OptionEnum("940", bool)
    usps_registered_mail_restricted_delivery = lib.OptionEnum("941", bool)
    usps_return_receipt = lib.OptionEnum("955", bool)
    usps_return_receipt_electronic = lib.OptionEnum("957", bool)
    usps_signature_requested_priority_mail_express_only = lib.OptionEnum("981", bool)
    usps_parcel_locker_delivery = lib.OptionEnum("984", bool)
    usps_po_to_addressee_priority_mail_express_only = lib.OptionEnum("986", bool)
    usps_sunday_delivery = lib.OptionEnum("981", bool)
    # fmt: on

    """ Custom Options """
    usps_price_type = lib.OptionEnum("priceType")
    usps_facility_id = lib.OptionEnum("facilityId")
    usps_hold_for_pickup = lib.OptionEnum("holdForPickup", bool)
    usps_rate_indicator = lib.OptionEnum("rateIndicator")
    usps_processing_category = lib.OptionEnum("processingCategory")
    usps_carrier_release = lib.OptionEnum("carrierRelease", bool)
    usps_physical_signature_required = lib.OptionEnum("physicalSignatureRequired", bool)
    usps_restriction_type = lib.OptionEnum("restrictionType")

    """ Unified Option type mapping """
    cash_on_delivery = usps_collect_on_delivery
    signature_confirmation = usps_signature_confirmation
    sunday_delivery = usps_sunday_delivery
    hold_at_location = usps_hold_for_pickup


CUSTOM_OPTIONS = [
    ShippingOption.usps_price_type.name,
    ShippingOption.usps_facility_id.name,
    ShippingOption.usps_hold_for_pickup.name,
    ShippingOption.usps_rate_indicator.name,
    ShippingOption.usps_processing_category.name,
    ShippingOption.usps_carrier_release.name,
    ShippingOption.usps_physical_signature_required.name,
]


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """
    Apply default values to the given options.
    """

    if package_options is not None:
        options.update(package_options.content)

    if "insurance" in options:
        if lib.to_money(options["insurance"]) > 500:
            options[ShippingOption.usps_insurance_above_500.name] = options["insurance"]
        else:
            options[ShippingOption.usps_insurance_bellow_500.name] = options[
                "insurance"
            ]

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class TrackingStatus(lib.Enum):
    on_hold = ["on_hold"]
    delivered = ["delivered"]
    in_transit = ["in_transit"]
    delivery_failed = ["delivery_failed"]
    delivery_delayed = ["delivery_delayed"]
    out_for_delivery = ["out_for_delivery"]
    ready_for_pickup = ["ready_for_pickup"]
