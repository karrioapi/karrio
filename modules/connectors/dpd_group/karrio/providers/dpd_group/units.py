"""Karrio DPD Group units and enums."""

import karrio.lib as lib
import karrio.core.units as units


class PackagingType(lib.StrEnum):
    """DPD Group packaging types"""
    dpd_group_package = "PACKAGE"

    """Unified Packaging type mapping"""
    envelope = dpd_group_package
    pak = dpd_group_package
    small_box = dpd_group_package
    medium_box = dpd_group_package
    your_packaging = dpd_group_package


class ShippingService(lib.StrEnum):
    """DPD Group shipping services"""
    dpd_group_classic = "CL"
    dpd_group_express_10 = "E10"
    dpd_group_express_12 = "E12"
    dpd_group_express_18 = "E18"
    dpd_group_parcelshop = "PS"


class ShippingOption(lib.Enum):
    """DPD Group shipping options"""
    dpd_group_saturday_delivery = lib.OptionEnum("saturdayDelivery", bool)
    dpd_group_insurance = lib.OptionEnum("insurance", float)

    """Unified Option type mapping"""
    saturday_delivery = dpd_group_saturday_delivery
    insurance = dpd_group_insurance


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """Apply default values to the given options."""
    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class TrackingStatus(lib.Enum):
    """DPD Group tracking status codes"""
    delivered = ["DELIVERED"]
    in_transit = ["IN_TRANSIT", "PICKED_UP"]
    out_for_delivery = ["OUT_FOR_DELIVERY"]
    delivery_failed = ["DELIVERY_FAILED"]
    ready_for_pickup = ["READY_FOR_PICKUP"]


class ConnectionConfig(lib.Enum):
    """DPD Group connection configuration options"""
    shipping_account_number = lib.OptionEnum("shipping_account_number")
