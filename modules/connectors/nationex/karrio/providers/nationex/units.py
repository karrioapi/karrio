import typing
import karrio.lib as lib
import karrio.core.units as units


MeasurementOptions = lib.units.MeasurementOptionsType(
    max_lb=99,
)


class MeasurementUnit(lib.StrEnum):
    CM = "KC"
    IN = "LI"
    KG = "KC"
    LB = "LI"


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


class ShippingService(lib.StrEnum):
    """Carrier specific services"""

    nationex_delivery = "Delivery"


def shipping_services_initializer(
    services: typing.List[str],
) -> lib.units.Services:
    """Apply default product codes to the list of products."""

    _services = list(set(services))
    _no_service_provided = (
        any([ShippingService.map(_).key is not None for _ in _services]) is False
    )

    if _no_service_provided:
        _services.append("nationex_delivery")

    return lib.units.Services(_services, ShippingService)


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    nationex_insurance_amount = lib.OptionEnum("InsuranceAmount", lib.to_money)
    nationex_frozen_protection = lib.OptionEnum("FrozenProtection", bool)
    nationex_dangerous_goods = lib.OptionEnum("DangerousGoods", bool)
    nationex_email_notification = lib.OptionEnum("EmailNotification", bool)
    nationex_sms_notification = lib.OptionEnum("SMSNotification", bool)
    nationex_snr = lib.OptionEnum("SNR", bool)
    nationex_note = lib.OptionEnum("Note")

    """ Unified Option type mapping """
    shipment_note = nationex_note
    insurance = nationex_insurance_amount
    dangerous_good = nationex_dangerous_goods
    sms_notification = nationex_sms_notification
    email_notification = nationex_email_notification


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
    on_hold = ["OnHold", "Attention"]
    delivered = ["Delivered"]
    in_transit = ["Pickup", "Transit"]
    delivery_failed = ["ReturnToSender", "RefusedDelivery"]
    out_for_delivery = ["OutForDelivery", "PartiallyOutForDelivery"]
