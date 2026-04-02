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

    KG = "KG"  # Kilograms
    LBR = "LBR"  # Pounds


class DimensionUnit(lib.StrEnum):
    """SmartKargo dimension/volume units"""

    CMQ = "CMQ"  # Centimeters
    CFT = "CFT"  # Inches (feet)


class ShippingService(lib.StrEnum):
    """SmartKargo shipping services"""

    smartkargo_express = "EXP"  # eCommerce Express
    smartkargo_priority = "EPR"  # eCommerce Priority
    smartkargo_standard = "EST"  # eCommerce Standard
    smartkargo_economy = "ECL"  # eCommerce Economy (Five Days)


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    smartkargo_insurance = lib.OptionEnum("hasInsurance", bool)
    smartkargo_declared_value = lib.OptionEnum("insuranceAmmount", float)
    smartkargo_delivery_type = lib.OptionEnum("deliveryType", str)
    smartkargo_channel = lib.OptionEnum("channel", str)
    smartkargo_label_ref2 = lib.OptionEnum("labelRef2", str)
    smartkargo_special_handling = lib.OptionEnum("specialHandlingType", str)
    smartkargo_commodity_type = lib.OptionEnum("commodityType", str)
    smartkargo_incoterm = lib.OptionEnum("incoterm", str)
    smartkargo_additional_info_01 = lib.OptionEnum("additionalInfo01", str)
    smartkargo_additional_info_02 = lib.OptionEnum("additionalInfo02", str)
    smartkargo_additional_info_03 = lib.OptionEnum("additionalInfo03", str)
    smartkargo_additional_info_04 = lib.OptionEnum("additionalInfo04", str)

    """ Unified Option type mapping """
    insurance = smartkargo_declared_value


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
    in_transit = ["DEP", "RCF", "INF", "MDL"]  # Departed / Recovered / Info / Arrived at airport
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

    primary_id = lib.OptionEnum("primary_id", str)
    site_id = lib.OptionEnum("site_id", str)
    additional_id = lib.OptionEnum("additional_id", str)
    origin = lib.OptionEnum("origin", str)
    destination = lib.OptionEnum("destination", str)
    shipping_options = lib.OptionEnum("shipping_options", list)
    currency = lib.OptionEnum("currency", str)
    shipping_services = lib.OptionEnum("shipping_services", list)
    partner_tracking_url = lib.OptionEnum("partner_tracking_url", str)
    partner_tracking_api_code = lib.OptionEnum("partner_tracking_api_code", str)
