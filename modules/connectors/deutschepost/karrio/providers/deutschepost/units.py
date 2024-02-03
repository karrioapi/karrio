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


class ConnectionConfig(lib.Enum):
    language = lib.OptionEnum("language")
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)


class ShippingService(lib.Enum):
    """Carrier specific services"""

    deutschepost_paket = "V01PAK"
    deutschepost_paket_international = "V53WPAK"
    deutschepost_europaket = "V54EPAK"
    deutschepost_warenpost = "V62WP"
    deutschepost_warenpost_international = "V66WPI"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    # dpdhl_option = lib.OptionEnum("code")

    """ Unified Option type mapping """
    # insurance = dpdhl_coverage  #  maps unified karrio option to carrier specific

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
        service_name="DHL Paket",
        service_code="dpdhl_paket",
        currency="EUR",
        domicile=True,
        min_weight=0.01,
        max_weight=31.5,
        max_length=120,
        max_width=60,
        max_height=60,
        weight_unit="KG",
        dimension_unit="CM",
        zones=[models.ServiceZone(rate=0.0)],
    ),
    models.ServiceLevel(
        service_name="DHL Paket International",
        service_code="dpdhl_paket_international",
        currency="EUR",
        domicile=False,
        international=True,
        min_weight=0.01,
        max_weight=31.5,
        max_length=120,
        max_width=60,
        max_height=60,
        weight_unit="KG",
        dimension_unit="CM",
        zones=[models.ServiceZone(rate=0.0)],
    ),
    models.ServiceLevel(
        service_name="DHL EuroPaket",
        service_code="dpdhl_europaket",
        currency="EUR",
        domicile=False,
        international=True,
        min_weight=0.01,
        max_weight=31.5,
        max_length=120,
        max_width=60,
        max_height=60,
        weight_unit="KG",
        dimension_unit="CM",
        zones=[models.ServiceZone(rate=0.0)],
    ),
    models.ServiceLevel(
        service_name="DHL Warenpost",
        service_code="dpdhl_warenpost",
        currency="EUR",
        domicile=True,
        international=False,
        min_weight=0.01,
        max_weight=1,
        max_length=35,
        max_width=7,
        max_height=5,
        weight_unit="KG",
        dimension_unit="CM",
        zones=[models.ServiceZone(rate=0.0)],
    ),
    models.ServiceLevel(
        service_name="DHL Warenpost International",
        service_code="dpdhl_warenpost_international",
        currency="EUR",
        domicile=False,
        international=True,
        min_weight=0.01,
        max_weight=1,
        max_length=35.3,
        max_width=9,
        max_height=10,
        weight_unit="KG",
        dimension_unit="CM",
        zones=[models.ServiceZone(rate=0.0)],
    ),
]
