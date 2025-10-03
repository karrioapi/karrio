import typing
import karrio.lib as lib
import karrio.core.units as units


PriceTypeEnum = lib.units.create_enum(
    "priceType",
    ["RETAIL", "COMMERCIAL", "COMMERCIAL_BASE", "COMMERCIAL_PLUS", "CONTRACT"],
)


class RateIndicator(lib.StrEnum):
    """Rate indicator types for USPS International"""

    E4 = "Priority Mail Express Flat Rate Envelope - Post Office To Addressee"
    E6 = "Priority Mail Express Legal Flat Rate Envelope"
    FA = "Legal Flat Rate Envelope"
    FB = "Medium Flat Rate Box/Large Flat Rate Bag"
    FE = "Flat Rate Envelope"
    FP = "Padded Flat Rate Envelope"
    FS = "Small Flat Rate Box"
    PA = "Priority Mail Express International Single Piece"
    PL = "Large Flat Rate Box"
    SP = "Single Piece"
    EP = "ECOMPRO Single Piece"
    HA = "ECOMPRO Legal Flat Rate Envelope"
    HB = "ECOMPRO Medium Flat Rate Box"
    HE = "ECOMPRO Flat Rate Envelope"
    HL = "ECOMPRO Large Flat Rate Box"
    HP = "ECOMPRO Padded Flat Rate Envelope"
    HS = "ECOMPRO Small Flat Rate Box"
    LE = "Single-piece parcel"


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type"""

    usps_priority_mail_express_international_flat_rate_envelope = "E4"
    usps_priority_mail_express_legal_flat_rate_envelope = "E6"
    usps_legal_flat_rate_envelope = "FA"
    usps_medium_flat_rate_box_large_flat_rate_bag = "FB"
    usps_flat_rate_envelope = "FE"
    usps_padded_flat_rate_envelope = "FP"
    usps_small_flat_rate_box = "FS"
    usps_priority_mail_express_international_single_piece = "PA"
    usps_large_flat_rate_box = "PL"
    usps_single_piece = "SP"
    usps_ecomp_single_piece = "EP"
    usps_ecomp_legal_flat_rate_envelope = "HA"
    usps_ecomp_medium_flat_rate_box = "HB"
    usps_ecomp_flat_rate_envelope = "HE"
    usps_ecomp_large_flat_rate_box = "HL"
    usps_ecomp_padded_flat_rate_envelope = "HP"
    usps_ecomp_small_flat_rate_box = "HS"
    usps_single_piece_parcel = "LE"

    """ Unified Packaging type mapping """
    envelope = usps_priority_mail_express_international_flat_rate_envelope
    pak = usps_single_piece
    tube = usps_single_piece
    pallet = usps_large_flat_rate_box
    small_box = usps_small_flat_rate_box
    medium_box = usps_medium_flat_rate_box_large_flat_rate_bag
    your_packaging = usps_single_piece_parcel


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

    # fmt: off
    usps_first_class_package_international_service = "FIRST-CLASS_PACKAGE_INTERNATIONAL_SERVICE"
    usps_priority_mail_international = "PRIORITY_MAIL_INTERNATIONAL"
    usps_priority_mail_express_international = "PRIORITY_MAIL_EXPRESS_INTERNATIONAL"
    usps_global_express_guaranteed = "GLOBAL_EXPRESS_GUARANTEED"
    usps_all = "ALL"
    # fmt: on

    @classmethod
    def to_product_code(cls, product_name: str) -> str:
        """Convert product description to product code

        to_product_code("Priority Mail Padded Flat Rate Envelope") -> "usps_priority_mail_padded_flat_rate_envelope"

        Args:
            product_name (str): Product name

        Returns:
            str: Service code
        """
        return lib.to_slug("usps", product_name)

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


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    # fmt: off
    usps_hazardous_materials_class_7_radioactive_materials = lib.OptionEnum("813", bool)
    usps_hazardous_materials_class_9_unmarked_lithium_batteries = lib.OptionEnum("820", bool)
    usps_hazardous_materials_division_6_2_biological_materials = lib.OptionEnum("826", bool)
    usps_hazardous_materials = lib.OptionEnum("857", bool)
    usps_insurance_below_500 = lib.OptionEnum("930", float)
    usps_insurance_above_500 = lib.OptionEnum("931", float)
    usps_return_receipt = lib.OptionEnum("955", bool)
    # fmt: on

    """ Custom Options """
    usps_mail_class = lib.OptionEnum("mailClass", ShippingService)
    usps_facility_id = lib.OptionEnum("facilityId")
    usps_machinable_piece = lib.OptionEnum("machinable", bool)
    usps_price_type = lib.OptionEnum("priceType", PriceTypeEnum)
    usps_hold_for_pickup = lib.OptionEnum("holdForPickup", bool)
    usps_carrier_release = lib.OptionEnum("carrierRelease", bool)
    usps_processing_category = lib.OptionEnum("processingCategory")
    usps_rate_indicator = lib.OptionEnum("rateIndicator", RateIndicator)
    usps_physical_signature_required = lib.OptionEnum("physicalSignatureRequired", bool)
    usps_extra_services = lib.OptionEnum("extraServices", list)
    usps_shipping_filter = lib.OptionEnum("shippingFilter", lib.units.create_enum("shippingFilter", ["PRICE"]))

    """ Unified Option type mapping """
    insurance = usps_insurance_below_500
    hold_at_location = usps_hold_for_pickup


CUSTOM_OPTIONS = [
    ShippingOption.usps_mail_class.name,
    ShippingOption.usps_extra_services.name,
    ShippingOption.usps_facility_id.name,
    ShippingOption.usps_machinable_piece.name,
    ShippingOption.usps_hold_for_pickup.name,
    ShippingOption.usps_processing_category.name,
    ShippingOption.usps_carrier_release.name,
    ShippingOption.usps_physical_signature_required.name,
    ShippingOption.usps_rate_indicator.name,
    ShippingOption.usps_price_type.name,
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
