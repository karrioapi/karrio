import karrio.lib as lib
import karrio.core.units as units


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type"""

    teleship_parcel = "parcel"
    teleship_envelope = "envelope"
    teleship_document = "document"

    """ Unified Packaging type mapping """
    envelope = teleship_envelope
    pak = teleship_envelope
    small_box = teleship_parcel
    medium_box = teleship_parcel
    your_packaging = teleship_parcel


class ShippingService(lib.StrEnum):
    """Carrier specific services"""

    teleship_expedited_pickup = "TELESHIP-EXPEDITED-PICKUP"
    teleship_expedited_dropoff = "TELESHIP-EXPEDITED-DROPOFF"
    teleship_standard_dropoff = "TELESHIP-STANDARD-DROPOFF"
    teleship_standard_pickup = "TELESHIP-STANDARD-PICKUP"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    teleship_customer_reference = lib.OptionEnum("customerReference")
    teleship_order_tracking_reference = lib.OptionEnum("orderTrackingReference")
    teleship_include_first_mile = lib.OptionEnum("includeFirstMile", bool)
    teleship_label_format = lib.OptionEnum("labelFormat")
    teleship_service_code = lib.OptionEnum("serviceCode")

    """ Unified Option type mapping """
    insurance = lib.OptionEnum("insurance", float)
    signature_required = lib.OptionEnum("signature", bool)


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
    """Teleship customs identifiers"""

    EORI = lib.OptionEnum("EORI")
    IOSS = lib.OptionEnum("IOSS")
    VAT = lib.OptionEnum("VAT")

    """ Unified Customs Identifier type mapping """

    ioss = IOSS
    eori_number = EORI
    vat_registration_number = VAT


class TrackingStatus(lib.Enum):
    """Teleship tracking statuses"""

    delivered = ["delivered"]
    in_transit = [
        "in_transit",
        "collected",
        "in_hub",
        "out_for_delivery",
        "customs_cleared",
    ]
    out_for_delivery = ["out_for_delivery"]
    delivery_failed = ["delivery_failed", "returned", "cancelled"]
    pending = ["pending", "created", "label_created"]
