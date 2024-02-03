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

    deutschepost_paket = "Packet (Standard / Priority)"
    deutschepost_paket_plus = "Packet Plus"
    deutschepost_paket_tracked = "Packet Tracked"
    deutschepost_paket_return = "Packet Return"
    deutschepost_business_mail = "Business Mail (Standard / Priority) / Letter"
    deutschepost_business_mail_plus = "Business Mail Registered / Letter Plus"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    # dpdhl_international_option = lib.OptionEnum("code")

    """ Unified Option type mapping """
    # insurance = dpdhl_international_coverage  #  maps unified karrio option to carrier specific

    pass


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
        service_name="Packet (Standard / Priority)",
        service_code="deutschepost_paket",
        currency="EUR",
        domicile=False,
        international=True,
        zones=[models.ServiceZone(rate=0.0)],
    ),
    models.ServiceLevel(
        service_name="Packet Plus",
        service_code="deutschepost_paket_plus",
        currency="EUR",
        domicile=False,
        international=True,
        zones=[models.ServiceZone(rate=0.0)],
    ),
    models.ServiceLevel(
        service_name="Packet Tracked",
        service_code="deutschepost_paket_tracked",
        currency="EUR",
        domicile=False,
        international=True,
        zones=[models.ServiceZone(rate=0.0)],
    ),
    models.ServiceLevel(
        service_name="Packet Return",
        service_code="deutschepost_paket_return",
        currency="EUR",
        domicile=False,
        international=True,
        zones=[models.ServiceZone(rate=0.0)],
    ),
    models.ServiceLevel(
        service_name="Business Mail (Standard / Priority) / Letter",
        service_code="deutschepost_business_mail",
        currency="EUR",
        domicile=False,
        international=True,
        zones=[models.ServiceZone(rate=0.0)],
    ),
    models.ServiceLevel(
        service_name="Business Mail Registered / Letter Plus",
        service_code="deutschepost_business_mail_plus",
        currency="EUR",
        domicile=False,
        international=True,
        zones=[models.ServiceZone(rate=0.0)],
    ),
]
