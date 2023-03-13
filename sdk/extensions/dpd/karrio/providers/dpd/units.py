import karrio.lib as lib
import karrio.core.units as units


class PackagingType(lib.Flag):
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


class Incoterm(lib.Enum):
    DAP = "06"
    DAP_enhanced = "07"


class CustomsContentType(lib.Flag):
    sale = "01"
    return_replacement = "02"
    gift = "03"

    """ Unified Content type mapping """
    sample = sale
    merchandise = sale
    return_merchandise = return_replacement


class ShippingService(lib.Enum):
    """Carrier specific services"""

    dpd_express_10h = "E10"
    dpd_express_12h = "E12"
    dpd_express_18h_guarantee = "E18"
    dpd_express_b2b_predict = "B2B MSG option"
    dpd_cl = "CL"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    dpd_order_type = lib.OptionEnum("orderType")
    dpd_saturday_delivery = lib.OptionEnum("saturdayDelivery")
    dpd_ex_works_delivery = lib.OptionEnum("exWorksDelivery")
    dpd_guarantee = lib.OptionEnum("guarantee")
    dpd_tyres = lib.OptionEnum("tyres")
    dpd_personal_delivery = lib.OptionEnum("personalDelivery")
    dpd_pickup = lib.OptionEnum("pickup")
    dpd_parcel_shop_delivery = lib.OptionEnum("parcelShopDelivery")
    dpd_predict = lib.OptionEnum("predict")
    dpd_personal_delivery_notification = lib.OptionEnum("personalDeliveryNotification")
    dpd_proactive_notification = lib.OptionEnum("proactiveNotification")
    dpd_delivery = lib.OptionEnum("delivery")
    dpd_invoice_address = lib.OptionEnum("invoiceAddress")
    dpd_country_specific_service = lib.OptionEnum("countrySpecificService")


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
    """Carrier tracking status mapping"""

    delivered = ["Delivered"]
    in_transit = ["in_transit"]
    delivery_failed = ["DeliveryFailure"]
    out_for_delivery = ["Courier", "ReturningFromDelivery"]
    ready_for_pickup = ["ParcelShop"]