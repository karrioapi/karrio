from karrio.core.metadata import PluginMetadata

from karrio.mappers.spring.mapper import Mapper
from karrio.mappers.spring.proxy import Proxy
from karrio.mappers.spring.settings import Settings
import karrio.providers.spring.units as units
import karrio.providers.spring.utils as utils


# This METADATA object is used by Karrio to discover and register this plugin
# when loaded through Python entrypoints or local plugin directories.
# The entrypoint is defined in pyproject.toml under [project.entry-points."karrio.plugins"]
METADATA = PluginMetadata(
    id="spring",
    label="Spring",
    description="Spring shipping integration for Karrio",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    # options=units.ShippingOption,
    # services=units.ShippingService,
    connection_configs=units.ConnectionConfig,
    # Extra info
    website="",
    documentation="",
)
