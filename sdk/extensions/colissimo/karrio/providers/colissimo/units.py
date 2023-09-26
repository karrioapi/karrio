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
    lang = lib.OptionEnum("lang")


class ShippingService(lib.Enum):
    """Carrier specific services"""

    colissimo_home_without_signature = "Colissimo Home - without signature"
    colissimo_home_with_signature = "Colissimo Home - with signature"
    colissimo_eco_france = "Colissimo Eco France"
    colissimo_return_france = "Colissimo Return France CORE 8R***"
    colissimo_flash_without_signature = "Colissimo Flash – without signature"
    colissimo_flash_with_signature = "Colissimo Flash – with signature"
    colissimo_eco_om_without_signature = "Colissimo Eco OM - without signature"
    colissimo_eco_om_with_signature = "Colissimo Eco OM - with signature"
    colissimo_retour_om = "Colissimo Retour OM"
    colissimo_home_international_without_signature = "Colissimo Home International - without signature***"
    colissimo_home_international_with_signature = "Colissimo Home International - with signature***"
    colissimo_return_international_to_france = "Colissimo Return International – Foreign country to France"
    colissimo_return_international_from_france = "Colissimo Return International – France to foreign cournty"
    colissimo_economical_big_export_offer = "Economical Big Export offer (test offer for China for a pilot customer)"
    colissimo_out_of_home_national_international = "Colissimo Out Of Home National and International : **"
    colissimo_out_of_home_post_office = "Colissimo - Out Of Home – at Post Office"
    colissimo_out_of_home_pickup_points_station_lockers = "Colissimo - Out Of Home – at Pickup points or Pickup Station lockers"
    colissimo_out_of_home_pickup_point = "Colissimo - Out Of Home – at pickup point"
    colissimo_out_of_home_pickup_station_lockers = "Colissimo - Out Of Home – at Pickup Station lockers"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    # colissimo_option = lib.OptionEnum("code")

    """ Unified Option type mapping """
    # insurance = colissimo_coverage  #  maps unified karrio option to carrier specific

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
        service_name="Colissimo Home - without signature",
        service_code="colissimo_home_without_signature",
        currency="EUR",
        domicile=True,
        zones=[models.ServiceZone(label="Zone 1", rate=0.0)]
    ),
]