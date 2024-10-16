import karrio.lib as lib
import karrio.core.units as units


class LabelType(lib.Enum):
    LABEL_PDF = ("PDF", "LABEL_PDF")
    LABEL_PNG_100X150 = ("PNG", "LABEL_PNG_100X150")
    LABEL_PNG_100X175 = ("PNG", "LABEL_PNG_100X175")
    LABEL_PDF_100X175 = ("PDF", "LABEL_PDF_100X175")
    LABEL_PDF_100X150 = ("PDF", "LABEL_PDF_100X150")
    LABEL_ZPL_100X175 = ("ZPL", "LABEL_ZPL_100X175")
    LABEL_ZPL_100X150 = ("ZPL", "LABEL_ZPL_100X150")

    """ Unified Label type mapping """
    PDF = LABEL_PDF_100X150
    ZPL = LABEL_ZPL_100X150
    PNG = LABEL_PNG_100X150


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type"""

    Bag = "Bag"
    Box = "Box"
    Carton = "Carton"
    Container = "Container"
    Crate = "Crate"
    Envelope = "Envelope"
    Pail = "Pail"
    Pallet = "Pallet"
    Satchel = "Satchel"
    Tube = "Tube"
    Custom = "Custom"

    """ Unified Packaging type mapping """
    envelope = Envelope
    pak = Satchel
    tube = Tube
    pallet = Pallet
    small_box = Box
    medium_box = Carton
    your_packaging = Custom


class ShippingService(lib.StrEnum):
    """Carrier specific services"""

    seko_ecommerce_standard_tracked = "eCommerce Standard Tracked"
    seko_ecommerce_express_tracked = "eCommerce Express Tracked"
    seko_domestic_express = "Domestic Express"
    seko_domestic_standard = "Domestic Standard"
    seko_domestic_large_parcel = "Domestic Large Parcel"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    seko_carrier = lib.OptionEnum("Carrier")
    seko_package_id = lib.OptionEnum("PackageId")
    seko_destination_id = lib.OptionEnum("DestinationId")
    origin_instructions = lib.OptionEnum("OriginInstructions")
    destination_instructions = lib.OptionEnum("DestinationInstructions")
    seko_is_saturday_delivery = lib.OptionEnum("IsSaturdayDelivery", bool)
    seko_is_signature_required = lib.OptionEnum("IsSignatureRequired", bool)
    seko_send_tracking_email = lib.OptionEnum("SendTrackingEmail", bool)
    seko_amount_collected = lib.OptionEnum("AmountCollected", float)
    seko_tax_collected = lib.OptionEnum("TaxCollected", bool)
    seko_cod_amount = lib.OptionEnum("CODAmount", float)
    seko_reference_2 = lib.OptionEnum("Reference2")
    seko_reference_3 = lib.OptionEnum("Reference3")

    """ Unified Option type mapping """
    saturday_delivery = seko_is_saturday_delivery
    signature_required = seko_is_signature_required
    email_notification = seko_send_tracking_email


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """
    Apply default values to the given options.
    """

    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class CustomsOption(lib.Enum):
    XIEORINumber = lib.OptionEnum("XIEORINumber")
    IOSSNUMBER = lib.OptionEnum("IOSSNUMBER")
    GBEORINUMBER = lib.OptionEnum("GBEORINUMBER")
    VOECNUMBER = lib.OptionEnum("VOECNUMBER")
    VATNUMBER = lib.OptionEnum("VATNUMBER")
    VENDORID = lib.OptionEnum("VENDORID")
    NZIRDNUMBER = lib.OptionEnum("NZIRDNUMBER")
    SWISS_VAT = lib.OptionEnum("SWISS VAT")
    OVRNUMBER = lib.OptionEnum("OVRNUMBER")
    EUEORINumber = lib.OptionEnum("EUEORINumber")
    EUVATNumber = lib.OptionEnum("EUVATNumber")
    LVGRegistrationNumber = lib.OptionEnum("LVGRegistrationNumber")

    """ Unified Customs Identifier type mapping """

    ioss = IOSSNUMBER
    nip_number = VATNUMBER
    eori_number = EUEORINumber


class TrackingStatus(lib.Enum):
    on_hold = ["on_hold"]
    delivered = ["delivered"]
    in_transit = ["in_transit"]
    delivery_failed = ["delivery_failed"]
    delivery_delayed = ["delivery_delayed"]
    out_for_delivery = ["out_for_delivery"]
    ready_for_pickup = ["ready_for_pickup"]
