import karrio.lib as lib
import karrio.core.units as units


class ConnectionConfig(lib.Enum):
    """DHL eCommerce Europe connection configuration options"""
    shipping_services = lib.OptionEnum("shipping_services")


class PackageType(lib.StrEnum):
    """Carrier specific package types"""
    dhl_ecommerce_europe_envelope = "ENVELOPE"
    dhl_ecommerce_europe_package = "PACKAGE"

    """ Unified Package type mapping """
    envelope = dhl_ecommerce_europe_envelope
    pak = dhl_ecommerce_europe_package
    tube = dhl_ecommerce_europe_package
    pallet = dhl_ecommerce_europe_package
    small_box = dhl_ecommerce_europe_package
    medium_box = dhl_ecommerce_europe_package
    your_packaging = dhl_ecommerce_europe_package


class ShippingService(lib.StrEnum):
    """DHL eCommerce Europe specific services"""

    # DHL Parcel Services
    V01PAK = "V01PAK"  # DHL Parcel (DE domestic)
    V02PAK = "V02PAK"  # DHL Parcel International
    V53WPAK = "V53WPAK"  # DHL Europack
    V54EPAK = "V54EPAK"  # DHL Europack (Express)
    V55PAK = "V55PAK"  # DHL Express Easy
    V66WPI = "V66WPI"  # DHL Express International
    
    # Legacy mapping
    dhl_ecommerce_europe_parcel = V01PAK
    dhl_ecommerce_europe_express = V55PAK


class ShippingOption(lib.Enum):
    """DHL eCommerce Europe specific options"""

    pickup_after = lib.OptionEnum("pickup_after")
    delivery_start = lib.OptionEnum("delivery_start")
    delivery_end = lib.OptionEnum("delivery_end")
    declared_value = lib.OptionEnum("declared_value")
    signature_required = lib.OptionEnum("signature_required")
    saturday_delivery = lib.OptionEnum("saturday_delivery")


class TrackingStatus(lib.Enum):
    on_hold = ["on_hold"]
    delivered = ["delivered", "OK"]
    in_transit = ["in_transit", "PU", "pickup"]
    delivery_delayed = ["delivery_delayed"]
    delivery_failed = ["delivery_failed"]
    exception = ["exception"]
    

def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """
    Initialize shipping options for DHL eCommerce Europe.
    """

    _options = options.copy()

    if package_options is not None:
        _options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(_options, ShippingOption, items_filter=items_filter) 