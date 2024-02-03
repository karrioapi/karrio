from karrio.core.metadata import Metadata

from karrio.mappers.deutschepost.mapper import Mapper
from karrio.mappers.deutschepost.proxy import Proxy
from karrio.mappers.deutschepost.settings import Settings
import karrio.providers.deutschepost.units as units


METADATA = Metadata(
    id="deutschepost",
    label="Deutsche Post Germany",
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
