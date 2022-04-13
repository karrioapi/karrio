from karrio.core.metadata import Metadata

from karrio.mappers.amazon_mws.mapper import Mapper
from karrio.mappers.amazon_mws.proxy import Proxy
from karrio.mappers.amazon_mws.settings import Settings
import karrio.providers.amazon_mws.units as units


METADATA = Metadata(
    id="amazon_mws",
    label="AmazonMws",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    services=units.Service,
)
