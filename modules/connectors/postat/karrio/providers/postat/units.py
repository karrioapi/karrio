"""PostAT units and enums."""

import karrio.lib as lib
import karrio.core.units as units


class LabelFormat(lib.StrEnum):
    """Supported label formats."""

    PDF = "pdf"
    ZPL2 = "zpl2"


class LabelSize(lib.StrEnum):
    """Supported label sizes."""

    SIZE_100x150 = "100x150"
    SIZE_100x200 = "100x200"


class PaperLayout(lib.StrEnum):
    """Supported paper layouts for PDF output."""

    LAYOUT_2xA5inA4 = "2xA5inA4"
    LAYOUT_4xA6inA4 = "4xA6inA4"
    LAYOUT_A4 = "A4"


class ConnectionConfig(lib.Enum):
    """PostAT connection configuration options."""

    server_url = lib.OptionEnum("server_url", str)
    label_format = lib.OptionEnum(
        "label_format",
        lib.units.create_enum("LabelFormat", [_.name for _ in LabelFormat]),
    )
    label_size = lib.OptionEnum(
        "label_size",
        lib.units.create_enum("LabelSize", [_.name for _ in LabelSize]),
    )
    paper_layout = lib.OptionEnum(
        "paper_layout",
        lib.units.create_enum("PaperLayout", [_.name for _ in PaperLayout]),
    )
    shipping_services = lib.OptionEnum("shipping_services", list)
    shipping_options = lib.OptionEnum("shipping_options", list)


class ShippingService(lib.StrEnum):
    """PostAT shipping services.

    Note: Service codes (DeliveryServiceThirdPartyID) are configured per account
    by Austrian Post. These are common examples.
    """

    postat_standard_domestic = "10"
    postat_express_domestic = "20"
    postat_international_standard = "30"
    postat_international_express = "40"


class ShippingOption(lib.Enum):
    """PostAT shipping options (Features)."""

    # Label configuration (can be set per-shipment)
    postat_label_size = lib.OptionEnum("label_size", str)
    postat_paper_layout = lib.OptionEnum("paper_layout", str)

    # Cash on Delivery
    postat_cod = lib.OptionEnum("COD", float)
    postat_cod_currency = lib.OptionEnum("COD_CURRENCY", str)

    # Insurance
    postat_insurance = lib.OptionEnum("INS", float)
    postat_insurance_currency = lib.OptionEnum("INS_CURRENCY", str)

    # Signature required
    postat_signature = lib.OptionEnum("SIG", bool)

    # Saturday delivery
    postat_saturday_delivery = lib.OptionEnum("SAT", bool)

    # Email notification
    postat_email_notification = lib.OptionEnum("MAIL", str)

    # SMS notification
    postat_sms_notification = lib.OptionEnum("SMS", str)

    # Age verification (16 or 18)
    postat_age_verification = lib.OptionEnum("AGE", int)

    # Unified option mappings
    cash_on_delivery = postat_cod
    insurance = postat_insurance
    signature_required = postat_signature
    saturday_delivery = postat_saturday_delivery
    email_notification = postat_email_notification


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
    """PostAT tracking status mapping."""

    pending = [
        "REGISTERED",
        "CREATED",
        "DATA_RECEIVED",
        "LABEL_PRINTED",
    ]
    delivered = [
        "DELIVERED",
        "ZUGESTELLT",
        "POD",
    ]
    in_transit = [
        "IN_TRANSIT",
        "UNTERWEGS",
        "DEPARTED",
        "ARRIVED",
    ]
    out_for_delivery = [
        "OUT_FOR_DELIVERY",
        "IN_ZUSTELLUNG",
    ]
    on_hold = [
        "HELD",
        "CUSTOMS",
    ]
    delivery_failed = [
        "FAILED",
        "NOT_DELIVERED",
        "REFUSED",
    ]


DEFAULT_SERVICES = [
    {
        "service_code": "postat_standard_domestic",
        "service_name": "Standard Domestic",
        "currency": "EUR",
    },
    {
        "service_code": "postat_express_domestic",
        "service_name": "Express Domestic",
        "currency": "EUR",
    },
    {
        "service_code": "postat_international_standard",
        "service_name": "International Standard",
        "currency": "EUR",
    },
    {
        "service_code": "postat_international_express",
        "service_name": "International Express",
        "currency": "EUR",
    },
]
