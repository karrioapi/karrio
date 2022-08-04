import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


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


class ShippingService(lib.Enum):
    """Carrier specific services"""

    dpdhl_paket = "V01PAK"
    dpdhl_paket_international = "V53WPAK"
    dpdhl_europaket = "V54EPAK"
    dpdhl_paket_connect = "V55PAK"
    dpdhl_warenpost = "V62WP"
    dpdhl_warenpost_international = "V66WPI"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    dpdhl_preferred_neighbour = lib.OptionEnum("code")
    dpdhl_preferred_location = lib.OptionEnum("code")
    dpdhl_notification = lib.OptionEnum("code", bool)
    dpdhl_visual_check_of_age = lib.OptionEnum("code", bool)
    dpdhl_named_person_only = lib.OptionEnum("code", bool)
    dpdhl_identcheck = lib.OptionEnum("code", bool)
    dpdhl_no_neighbour_delivery = lib.OptionEnum("code", bool)
    dpdhl_preferred_day = lib.OptionEnum("code")
    dpdhl_endorsement = lib.OptionEnum("code")
    dpdhl_go_green = lib.OptionEnum("code", bool)
    dpdhl_additional_insurance = lib.OptionEnum("code", float)
    dpdhl_bulky_goods = lib.OptionEnum("code", bool)
    dpdhl_cash_on_delivery = lib.OptionEnum("code", float)
    dpdhl_premium = lib.OptionEnum("code", bool)
    dpdhl_retoure = lib.OptionEnum("code", bool)

    """ Unified Option type mapping """
    insurance = dpdhl_additional_insurance
    email_notification = dpdhl_notification


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


DEFAULT_SERVICES = [
    models.ServiceLevel(
        service_name="DHL Paket",
        service_code="dpdhl_paket",
        cost="0.00",
        currency="EUR",
        domicile=True,
    ),
    models.ServiceLevel(
        service_name="DHL Paket International",
        service_code="dpdhl_paket_international",
        cost="0.00",
        currency="EUR",
        international=True,
    ),
    models.ServiceLevel(
        service_name="DHL EuroPaket",
        service_code="dpdhl_europaket",
        cost="0.00",
        currency="EUR",
        international=True,
    ),
    models.ServiceLevel(
        service_name="DHL Paket Connect",
        service_code="dpdhl_paket_connect",
        cost="0.00",
        currency="EUR",
        international=True,
    ),
    models.ServiceLevel(
        service_name="DHL Warenpost",
        service_code="dpdhl_warenpost",
        cost="0.00",
        currency="EUR",
        domicile=True,
    ),
    models.ServiceLevel(
        service_name="DHL Warenpost International",
        service_code="dpdhl_warenpost_international",
        cost="0.00",
        currency="EUR",
        international=True,
    ),
]
