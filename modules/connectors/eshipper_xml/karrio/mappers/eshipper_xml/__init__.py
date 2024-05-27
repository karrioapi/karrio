from karrio.core.metadata import Metadata

from karrio.mappers.eshipper_xml.mapper import Mapper
from karrio.mappers.eshipper_xml.proxy import Proxy
from karrio.mappers.eshipper_xml.settings import Settings
import karrio.providers.eshipper_xml.units as units


METADATA = Metadata(
    id="eshipper_xml",
    label="eShipper XML",
    is_hub=True,
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    options=units.ShippingOption,
    services=units.ShippingService,
    hub_carriers=units.CARRIER_IDS,
)
