import typing
import karrio.lib as lib
import karrio.core.units as units


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type"""

    usps_3_digit = "3D"
    usps_3_digit_dimensional_rectangular = "3N"
    usps_3_digit_dimensional_nonrectangular = "3R"
    usps_5_digit = "5D"
    usps_basic = "BA"
    usps_mixed_ndc = "BB"
    usps_ndc = "BM"
    usps_cubic_pricing_tier_1 = "C1"
    usps_cubic_pricing_tier_2 = "C2"
    usps_cubic_pricing_tier_3 = "C3"
    usps_cubic_pricing_tier_4 = "C4"
    usps_cubic_pricing_tier_5 = "C5"
    usps_cubic_parcel = "CP"
    usps_connect_local = "CM"
    usps_non_presorted = "NP"
    usps_full_tray_box = "O1"
    usps_half_tray_box = "O2"
    usps_emm_tray_box = "O3"
    usps_flat_tub_tray_box = "O4"
    usps_surface_transported_pallet = "O5"
    usps_half_pallet_box = "O7"
    usps_oversized = "OS"
    usps_cubic_soft_pack_tier_1 = "P5"
    usps_cubic_soft_pack_tier_2 = "P6"
    usps_cubic_soft_pack_tier_3 = "P7"
    usps_cubic_soft_pack_tier_4 = "P8"
    usps_cubic_soft_pack_tier_5 = "P9"
    usps_cubic_soft_pack_tier_6 = "Q6"
    usps_cubic_soft_pack_tier_7 = "Q7"
    usps_cubic_soft_pack_tier_8 = "Q8"
    usps_cubic_soft_pack_tier_9 = "Q9"
    usps_cubic_soft_pack_tier_10 = "Q0"
    usps_priority_mail_express_single_piece = "PA"
    usps_large_flat_rate_box = "PL"
    usps_large_flat_rate_box_apofpo = "PM"
    usps_presorted = "PR"
    usps_small_flat_rate_bag = "SB"
    usps_scf_dimensional_nonrectangular = "SN"
    usps_scf_dimensional_rectangular = "SR"
    usps_single_piece = "SP"

    """ Unified Packaging type mapping """
    envelope = usps_single_piece
    pak = usps_single_piece
    tube = usps_scf_dimensional_nonrectangular
    pallet = usps_large_flat_rate_box
    small_box = usps_single_piece
    medium_box = usps_scf_dimensional_rectangular
    your_packaging = usps_single_piece


class ContentType(lib.StrEnum):
    HAZMAT = "HAZMAT"
    CREMATED_REMAINS = "CREMATED_REMAINS"
    BEES = "BEES"
    DAY_OLD_POULTRY = "DAY_OLD_POULTRY"
    ADULT_BIRDS = "ADULT_BIRDS"
    OTHER_LIVES = "OTHER_LIVES"
    PERISHABLE = "PERISHABLE"
    PHARMACEUTICALS = "PHARMACEUTICALS"
    MEDICAL_SUPPLIES = "MEDICAL_SUPPLIES"
    FRUITS = "FRUITS"
    VEGETABLES = "VEGETABLES"
    LIVE_PLANTS = "LIVE_PLANTS"


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
    ZPL = ZPL203DPI
    PNG = JPG


class ShippingService(lib.StrEnum):
    """Carrier specific services"""

    usps_parcel_select_lightweight = "PARCEL_SELECT_LIGHTWEIGHT"
    usps_parcel_select = "PARCEL_SELECT"
    usps_priority_mail_express = "PRIORITY_MAIL_EXPRESS"
    usps_priority_mail = "PRIORITY_MAIL"
    usps_library_mail = "LIBRARY_MAIL"
    usps_media_mail = "MEDIA_MAIL"
    usps_bound_printed_matter = "BOUND_PRINTED_MATTER"
    usps_connect_local = "USPS_CONNECT_LOCAL"
    usps_connect_mail = "USPS_CONNECT_MAIL"
    usps_connect_next_day = "USPS_CONNECT_NEXT_DAY"
    usps_connect_regional = "USPS_CONNECT_REGIONAL"
    usps_connect_same_day = "USPS_CONNECT_SAME_DAY"
    usps_ground_advantage = "USPS_GROUND_ADVANTAGE"
    usps_domestic_matter_for_the_blind = "DOMESTIC_MATTER_FOR_THE_BLIND"
    usps_all = "ALL"

    @classmethod
    def to_product_code(cls, product_name: str) -> str:
        """Convert product description to product code

        to_product_code("Priority Mail Padded Flat Rate Envelope") -> "usps_priority_mail_padded_flat_rate_envelope"

        Args:
            product_name (str): Product name

        Returns:
            str: Service code
        """
        return lib.to_slug("usps", product_name).replace("usps_usps_", "usps_")

    @classmethod
    def to_product_name(cls, product_code: str) -> str:
        """Convert product code to product name

        to_product_name("usps_priority_mail_padded_flat_rate_envelope") -> "USPS PRIORITY MAIL PADDED FLAT RATE ENVELOPE"

        Args:
            product_code (str): Service code

        Returns:
            str: Product name
        """
        if not product_code:
            return ""

        # Remove the "usps_" prefix if present
        if product_code.startswith("usps_"):
            product_code = product_code[5:]  # Remove "usps_" (5 characters)

        # Replace underscores with spaces and convert to uppercase
        product_name = product_code.replace("_", " ").upper()

        # Add "USPS" prefix
        return f"USPS {product_name}"

    @classmethod
    def to_mail_class(cls, product_code: str) -> typing.Optional['ShippingService']:
        """Convert product code to mail class

        to_mail_class("usps_priority_mail_padded_flat_rate_envelope") -> "PRIORITY_MAIL"

        Args:
            product_code (str): Service code

        Returns:
            str: ShippingService
        """
        return ShippingService.map(
            next((
                service for service in list(cls) if service.name in product_code
            ), None)
        )


INCOMPATIBLE_SERVICES = [
    ShippingService.usps_ground_advantage.name,  # type: ignore
]


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
    usps_insurance_below_500 = lib.OptionEnum("930", float)
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

    """ Custom Options """
    usps_mail_class = lib.OptionEnum("mailClass", ShippingService)
    usps_facility_id = lib.OptionEnum("facilityId")
    usps_machinable_piece = lib.OptionEnum("machinable", bool)
    usps_hold_for_pickup = lib.OptionEnum("holdForPickup", bool)
    usps_processing_category = lib.OptionEnum("processingCategory")
    usps_carrier_release = lib.OptionEnum("carrierRelease", bool)
    usps_physical_signature_required = lib.OptionEnum("physicalSignatureRequired", bool)
    usps_price_type = lib.OptionEnum("priceType", lib.units.create_enum("priceType", ["RETAIL", "COMMERCIAL", "CONTRACT"]))
    usps_destination_entry_facility_type = lib.OptionEnum("destinationEntryFacilityType", lib.units.create_enum("destinationEntryFacilityType", ["NONE", "DESTINATION_NETWORK_DISTRIBUTION_CENTER", "DESTINATION_SECTIONAL_CENTER_FACILITY", "DESTINATION_DELIVERY_UNIT", "DESTINATION_SERVICE_HUB"]))
    usps_extra_services = lib.OptionEnum("extraServices", list)
    usps_shipping_filter = lib.OptionEnum("shippingFilter", lib.units.create_enum("shippingFilter", ["PRICE", "SERVICE_STANDARDS"]))

    """ Unified Option type mapping """
    cash_on_delivery = usps_collect_on_delivery
    signature_confirmation = usps_signature_confirmation
    sunday_delivery = usps_sunday_delivery
    hold_at_location = usps_hold_for_pickup
    # fmt: on


CUSTOM_OPTIONS = [
    ShippingOption.usps_mail_class.name,
    ShippingOption.usps_extra_services.name,
    ShippingOption.usps_facility_id.name,
    ShippingOption.usps_machinable_piece.name,
    ShippingOption.usps_hold_for_pickup.name,
    ShippingOption.usps_processing_category.name,
    ShippingOption.usps_carrier_release.name,
    ShippingOption.usps_physical_signature_required.name,
    ShippingOption.usps_price_type.name,
    ShippingOption.usps_destination_entry_facility_type.name,
    ShippingOption.usps_shipping_filter.name,
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
            options[ShippingOption.usps_insurance_below_500.name] = options["insurance"]

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class TrackingStatus(lib.Enum):
    on_hold = ["on hold"]
    delivered = ["delivered"]
    in_transit = ["in transit"]
    delivery_failed = ["delivery failed"]
    delivery_delayed = ["delivery delayed"]
    out_for_delivery = ["out for delivery"]
    ready_for_pickup = ["ready for pickup"]
