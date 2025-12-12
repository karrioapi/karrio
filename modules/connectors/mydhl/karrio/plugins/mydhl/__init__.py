from karrio.core.metadata import PluginMetadata

from karrio.mappers.mydhl.mapper import Mapper
from karrio.mappers.mydhl.proxy import Proxy
from karrio.mappers.mydhl.settings import Settings
import karrio.providers.mydhl.units as units
import karrio.providers.mydhl.utils as utils


# This METADATA object is used by Karrio to discover and register this plugin
# when loaded through Python entrypoints or local plugin directories.
# The entrypoint is defined in pyproject.toml under [project.entry-points."karrio.plugins"]
METADATA = PluginMetadata(
    status="in-development",
    id="mydhl",
    label="MyDHL Express",
    description="DHL Express MyDHL API integration for Karrio",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    options=units.ShippingOption,
    services=units.ShippingService,
    connection_configs=utils.ConnectionConfig,
    # Extra info
    website="https://www.dhl.com",
    documentation="https://developer.dhl.com/api-reference/mydhl-express",
)
