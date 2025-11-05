import karrio.lib as lib
import karrio.core.units as units


class PackagingType(lib.StrEnum):
    """GLS Group specific packaging types"""
    gls_parcel = "PARCEL"
    gls_envelope = "ENVELOPE"
    gls_pallet = "PALLET"

    """Unified Packaging type mapping"""
    envelope = gls_envelope
    pak = gls_parcel
    small_box = gls_parcel
    medium_box = gls_parcel
    your_packaging = gls_parcel
    pallet = gls_pallet


class ShippingService(lib.StrEnum):
    """GLS Group specific services"""
    gls_parcel = "PARCEL"
    gls_express = "EXPRESS"
    gls_guaranteed24 = "GUARANTEED24"
    gls_business_parcel = "BUSINESSPARCEL"
    gls_euro_business_parcel = "EUROBUSINESSPARCEL"


class ShippingOption(lib.Enum):
    """GLS Group specific options"""
    gls_guaranteed24 = lib.OptionEnum("GUARANTEED24", bool)
    gls_saturday_delivery = lib.OptionEnum("SaturdayService", bool)
    gls_flex_delivery = lib.OptionEnum("FlexDeliveryService", bool)
    gls_deposit_service = lib.OptionEnum("DepositService", bool)
    gls_pick_and_return = lib.OptionEnum("PickAndReturnService", bool)
    gls_shop_delivery = lib.OptionEnum("ShopDeliveryService", bool)
    gls_addressee_only = lib.OptionEnum("AddresseeOnlyService", bool)
    gls_premium = lib.OptionEnum("PremiumService", bool)

    """Standard option mappings"""
    insurance = lib.OptionEnum("insurance", float)
    saturday_delivery = gls_saturday_delivery


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
    """GLS Group tracking status mapping"""
    on_hold = ["ON_HOLD", "EXCEPTION"]
    delivered = ["DELIVERED", "SIGNED"]
    in_transit = ["IN_TRANSIT", "ACCEPTED", "COLLECTED", "IN_DEPOT"]
    delivery_failed = ["DELIVERY_FAILED", "REFUSED", "DAMAGED"]
    out_for_delivery = ["OUT_FOR_DELIVERY"]
    delivery_delayed = ["DELAYED"]
    ready_for_pickup = ["READY_FOR_PICKUP"]


class WeightUnit(lib.StrEnum):
    """Weight unit mapping"""
    KG = "kg"
    LB = "lb"


class DimensionUnit(lib.StrEnum):
    """Dimension unit mapping"""
    CM = "cm"
    IN = "in"
