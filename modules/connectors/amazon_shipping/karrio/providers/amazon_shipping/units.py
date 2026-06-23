"""Karrio Amazon Shipping units and enums."""

import karrio.lib as lib


class WeightUnit(lib.StrEnum):
    """Amazon Shipping weight units."""

    GRAM = "GRAM"
    KILOGRAM = "KILOGRAM"
    OUNCE = "OUNCE"
    POUND = "POUND"


class DimensionUnit(lib.StrEnum):
    """Amazon Shipping dimension units."""

    INCH = "INCH"
    CENTIMETER = "CENTIMETER"


class LabelFormat(lib.StrEnum):
    """Amazon Shipping label formats."""

    PNG = "PNG"
    PDF = "PDF"
    ZPL = "ZPL"


class ShippingBusinessId(lib.StrEnum):
    """Amazon Shipping business IDs."""

    AmazonShipping_US = "AmazonShipping_US"
    AmazonShipping_UK = "AmazonShipping_UK"
    AmazonShipping_IN = "AmazonShipping_IN"
    AmazonShipping_IT = "AmazonShipping_IT"
    AmazonShipping_ES = "AmazonShipping_ES"
    AmazonShipping_FR = "AmazonShipping_FR"


class ShippingService(lib.StrEnum):
    """Amazon Shipping services.

    Service IDs are dynamic and returned by the getRates API.
    These are common service patterns.
    """

    # US services
    amazon_shipping_standard = "AMZN_US_STD"
    amazon_shipping_premium = "AMZN_US_PREM"
    amazon_shipping_ground = "AMZN_US_GND"

    # UK services
    amazon_shipping_uk_standard = "AMZN_UK_STD"
    amazon_shipping_uk_premium = "AMZN_UK_PREM"

    # Generic fallback
    amazon_shipping = "AMZN"


class PackagingType(lib.StrEnum):
    """Amazon Shipping packaging types."""

    PACKAGE = "PACKAGE"

    # Unified packaging type mapping
    envelope = PACKAGE
    pak = PACKAGE
    tube = PACKAGE
    pallet = PACKAGE
    small_box = PACKAGE
    medium_box = PACKAGE
    your_packaging = PACKAGE


class ChannelType(lib.StrEnum):
    """Amazon Shipping channel types."""

    AMAZON = "AMAZON"
    EXTERNAL = "EXTERNAL"


class ShippingOption(lib.Enum):
    """Amazon Shipping options."""

    amazon_shipping_channel_type = lib.OptionEnum("channel_type", str)
    amazon_shipping_label_format = lib.OptionEnum("label_format", str)
    amazon_shipping_label_size = lib.OptionEnum("label_size", str)


def shipping_options_initializer(
    options: dict,
    package_options: lib.units.Options = None,
) -> lib.units.Options:
    """Initialize Amazon Shipping options."""
    _options = options.copy()

    if package_options is not None:
        _options.update(package_options.content)

    return lib.units.ShippingOptions(_options, ShippingOption)


class TrackingStatus(lib.Enum):
    """Maps Amazon Shipping tracking event codes to karrio normalized status.

    Amazon Shipping v2 uses specific event codes for tracking.
    """

    pending = ["LabelCreated", "PickedUp", "Manifested"]
    in_transit = [
        "InTransit",
        "ArrivedAtCarrierFacility",
        "DepartedCarrierFacility",
        "ArrivedAtDeliveryStation",
        "ArrivedAtLocalFacility",
    ]
    out_for_delivery = ["OutForDelivery"]
    delivered = ["Delivered"]
    on_hold = ["Delayed", "OnHold", "PaymentNotReady"]
    delivery_failed = [
        "DeliveryAttempted",
        "Undeliverable",
        "AddressNotFound",
        "BusinessClosed",
        "CustomerUnavailable",
        "UnableToAccess",
        "UnableToContactRecipient",
    ]
    delivery_delayed = ["Delayed", "WeatherDelay"]
    return_initiated = ["ReturnInitiated", "Rejected", "CancelledByRecipient"]


class TrackingIncidentReason(lib.Enum):
    """Maps Amazon Shipping exception codes to normalized TrackingIncidentReason."""

    carrier_damaged_parcel = ["Damaged"]
    consignee_refused = [
        "Rejected",
        "RejectedByRecipientWithVerification",
        "IncorrectItems",
        "NotRequired",
    ]
    consignee_not_home = ["CustomerUnavailable", "BusinessClosed"]
    wrong_address = ["AddressNotFound"]
    unable_to_access = ["UnableToAccess", "UnableToContactRecipient"]
    payment_issue = ["PaymentNotReady", "OtpNotAvailable"]
    hazmat = ["HazmatShipment"]
    unknown = []
