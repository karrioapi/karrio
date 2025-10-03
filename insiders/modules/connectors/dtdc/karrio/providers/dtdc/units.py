import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


class LoadType(lib.StrEnum):
    """DTDC Load Types"""

    DOCUMENT = "DOCUMENT"
    NON_DOCUMENT = "NON-DOCUMENT"


class LabelFormat(lib.StrEnum):
    """DTDC Label Formats"""

    PDF = "pdf"
    BASE64 = "base64"


class LabelType(lib.StrEnum):
    """DTDC Label Types"""

    SHIP_LABEL_A4 = "SHIP_LABEL_A4"
    SHIP_LABEL_A6 = "SHIP_LABEL_A6"
    SHIP_LABEL_POD = "SHIP_LABEL_POD"
    SHIP_LABEL_4X6 = "SHIP_LABEL_4X6"
    ROUTE_LABEL_A4 = "ROUTE_LABEL_A4"
    ROUTE_LABEL_4X4 = "ROUTE_LABEL_4X4"
    ADDR_LABEL_A4 = "ADDR_LABEL_A4"
    ADDR_LABEL_4X2 = "ADDR_LABEL_4X2"

    """Unified Label type mapping"""
    PDF = SHIP_LABEL_4X6
    ZPL = SHIP_LABEL_4X6


class PackagingType(lib.StrEnum):
    """DTDC specific packaging types"""

    dtdc_document = DOCUMENT = "DOCUMENT"
    dtdc_non_document = NON_DOCUMENT = "NON-DOCUMENT"

    """Unified Packaging type mapping"""
    envelope = DOCUMENT
    pak = NON_DOCUMENT
    tube = NON_DOCUMENT
    pallet = NON_DOCUMENT
    small_box = NON_DOCUMENT
    medium_box = NON_DOCUMENT
    large_box = NON_DOCUMENT
    your_packaging = NON_DOCUMENT


class ConnectionConfig(lib.Enum):
    """DTDC connection configuration options."""

    label_type = lib.OptionEnum("label_type", LabelType)
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)


class ShippingService(lib.StrEnum):
    """DTDC specific services"""

    dtdc_b2c_priority = "B2C PRIORITY"
    dtdc_b2c_economy = "B2C SMART EXPRESS"
    dtdc_b2c_express = "B2C PREMIUM"
    dtdc_b2c_ground = "B2C GROUND ECONOMY"
    dtdc_priority = "PRIORITY"
    dtdc_ground_express = "GROUND EXPRESS"
    dtdc_premium = "PREMIUM"
    dtdc_economy_ground = "GEC"
    dtdc_standard_express = "STD EXP-A"


class ShippingOption(lib.Enum):
    """DTDC specific options"""

    # fmt: off
    dtdc_is_risk_surcharge_applicable = lib.OptionEnum("is_risk_surcharge_applicable", bool)
    dtdc_invoice_number = lib.OptionEnum("invoice_number", str)
    dtdc_invoice_date = lib.OptionEnum("invoice_date", str)
    dtdc_commodity_id = lib.OptionEnum("commodity_id", str)
    dtdc_cod_amount = lib.OptionEnum("cod_amount", float)
    dtdc_eway_bill = lib.OptionEnum("eway_bill", str)
    dtdc_cod_collection_mode = lib.OptionEnum("cod_collection_mode", lib.units.create_enum("CodCollectionMode", ["CASH", "CHEQUE"]))
    # fmt: on

    """Unified Option type mapping"""
    cash_on_delivery = dtdc_cod_amount
    invoice_number = dtdc_invoice_number
    invoice_date = dtdc_invoice_date


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """
    Apply default values to the given options.
    """
    if package_options is not None:
        options.update(package_options.content)

    # If COD amount is not provided, set COD collection mode to CASH
    if lib.to_money(options.get("dtdc_cod_amount")) is None:
        options.update(
            {
                "dtdc_cod_collection_mode": options.get("dtdc_cod_collection_mode")
                or "CASH"
            }
        )

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class TrackingStatus(lib.Enum):
    """Map DTDC tracking status codes to unified statuses"""

    # Pickup and booking statuses
    pending = ["BKD", "BOOKED"]

    # In transit statuses
    in_transit = [
        "DISPATCHED",
        "CDOUT",
        "CDIN",
        "OBMD",
        "IBMD",
        "OPMF",
        "IPMF",
        "OMBM",
        "In Transit",
        "IN TRANSIT",
        "inscan",
        "RECEIVED",
    ]

    # Out for delivery
    out_for_delivery = ["OUTDLV", "OUT FOR DELIVERY"]

    # Delivered
    delivered = ["DLV", "DELIVERED", "Delivered"]

    # Failed/Not delivered
    delivery_failed = ["NOT DELIVERED", "ATTEMPTED"]

    # Held up
    on_hold = ["HELDUP", "HELD UP", "HELDUP AT CUSTOMS"]

    # Return
    delivery_delayed = ["RTO", "CONSIGNMENT HAS RETURNED"]

    # Other statuses
    ready_for_pickup = ["CONSIGNMENT RELEASED", "ARRIVAL AT AIRPORT", "CUSTOMS CLEARED"]


DEFAULT_SERVICES = [
    models.ServiceLevel(
        service_name=f"DTDC {service.value}",
        service_code=service.name,
        currency="INR",
        zones=[models.ServiceZone(label="Zone 1", rate=0.0)],
    )
    for service in ShippingService
]
