from karrio.core.metadata import PluginMetadata

from karrio.mappers.asendia.mapper import Mapper
from karrio.mappers.asendia.proxy import Proxy
from karrio.mappers.asendia.settings import Settings
import karrio.providers.asendia.units as units
import karrio.providers.asendia.utils as utils


METADATA = PluginMetadata(
    id="asendia",
    label="Asendia",
    description="Asendia international e-commerce shipping services",
    status="beta",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    options=units.ShippingOption,
    services=units.ShippingService,
    connection_configs=units.ConnectionConfig,
    # Extra info
    website="https://www.asendia.com",
    documentation="https://www.asendia-sync.com/swagger-ui/index.html",
)
