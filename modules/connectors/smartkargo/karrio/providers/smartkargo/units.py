"""SmartKargo carrier units and mappings."""

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


class PaymentMode(lib.StrEnum):
    """SmartKargo payment modes"""

    PX = "PX"  # Billed (typically used)
    PP = "PP"  # Prepaid at the time of tender
    CC = "CC"  # Collected from Consignee at delivery


class WeightUnit(lib.StrEnum):
    """SmartKargo weight units"""

    KG = "KG"   # Kilograms
    LBR = "LBR"  # Pounds


class DimensionUnit(lib.StrEnum):
    """SmartKargo dimension/volume units"""

    CMQ = "CMQ"  # Centimeters
    CFT = "CFT"  # Inches (feet)


class ShippingService(lib.StrEnum):
    """SmartKargo shipping services"""

    smartkargo_express = "EXP"      # eCommerce Express
    smartkargo_priority = "EPR"     # eCommerce Priority
    smartkargo_standard = "EST"     # eCommerce Standard
    smartkargo_economy = "ECL"      # eCommerce Economy (Five Days)


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    smartkargo_insurance = lib.OptionEnum("insuranceRequired", bool)
    smartkargo_declared_value = lib.OptionEnum("declaredValue", float)
    smartkargo_delivery_type = lib.OptionEnum("deliveryType", str)
    smartkargo_channel = lib.OptionEnum("channel", str)
    smartkargo_label_ref2 = lib.OptionEnum("labelRef2", str)
    smartkargo_special_handling = lib.OptionEnum("specialHandlingType", str)
    smartkargo_commodity_type = lib.OptionEnum("commodityType", str)

    """ Unified Option type mapping """
    insurance = smartkargo_insurance
    declared_value = smartkargo_declared_value


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


class TrackingStatus(lib.Enum):
    """Maps SmartKargo tracking event codes to normalized Karrio statuses."""

    pending = ["BKD"]  # Electronic information submitted by shipper
    picked_up = ["RCS"]  # Shipment Picked up by Carrier
    in_transit = ["DEP", "RCF"]  # Departed / Recovered at partner store
    out_for_delivery = ["GDL"]  # Package left partner store for consignee door
    delivered = ["DDL", "DLD"]  # Successfully delivered / Delivered and left at door
    delivery_failed = ["ADL"]  # Delivery attempted but failed
    on_hold = ["RCU"]  # Reminder sent to customer


class TrackingIncidentReason(lib.Enum):
    """Maps SmartKargo exception codes to normalized incident reasons."""

    # Consignee-caused issues
    consignee_not_available = ["ADL"]  # Partner reached address but couldn't deliver

    # Delivery notifications
    delivery_exception_hold = ["RCU"]  # Reminder sent to customer

    # Unknown
    unknown = []


class ConnectionConfig(lib.Enum):
    """SmartKargo connection configuration options."""

    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    label_type = lib.OptionEnum("label_type", str)  # PDF or ZPL
