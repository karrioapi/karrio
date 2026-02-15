from karrio.core.metadata import PluginMetadata

from karrio.mappers.smartkargo.mapper import Mapper
from karrio.mappers.smartkargo.proxy import Proxy
from karrio.mappers.smartkargo.settings import Settings
import karrio.providers.smartkargo.units as units
import karrio.providers.smartkargo.utils as utils


# This METADATA object is used by Karrio to discover and register this plugin
# when loaded through Python entrypoints or local plugin directories.
# The entrypoint is defined in pyproject.toml under [project.entry-points."karrio.plugins"]
METADATA = PluginMetadata(
    id="smartkargo",
    label="SmartKargo",
    description="SmartKargo shipping integration for Karrio",
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
