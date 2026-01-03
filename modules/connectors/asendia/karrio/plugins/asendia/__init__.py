from karrio.core.metadata import PluginMetadata

from karrio.mappers.asendia.mapper import Mapper
from karrio.mappers.asendia.proxy import Proxy
from karrio.mappers.asendia.settings import Settings
import karrio.providers.asendia.units as units
import karrio.providers.asendia.utils as utils


# This METADATA object is used by Karrio to discover and register this plugin
# when loaded through Python entrypoints or local plugin directories.
# The entrypoint is defined in pyproject.toml under [project.entry-points."karrio.plugins"]
METADATA = PluginMetadata(
    id="asendia",
    label="Asendia",
    description="Asendia shipping integration for Karrio",
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
