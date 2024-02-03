from karrio.core.metadata import Metadata

from karrio.mappers.deutschepost_international.mapper import Mapper
from karrio.mappers.deutschepost_international.proxy import Proxy
from karrio.mappers.deutschepost_international.settings import Settings
import karrio.providers.deutschepost_international.units as units


METADATA = Metadata(
    id="deutschepost_international",
    label="Deutsche Post International",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    services=units.ShippingService,
    service_levels=units.DEFAULT_SERVICES,
    connection_configs=units.ConnectionConfig,
)
