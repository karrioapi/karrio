from karrio.core.metadata import PluginMetadata

from karrio.mappers.landmark.mapper import Mapper
from karrio.mappers.landmark.proxy import Proxy
from karrio.mappers.landmark.settings import Settings
import karrio.providers.landmark.units as units
import karrio.providers.landmark.utils as utils


# This METADATA object is used by Karrio to discover and register this plugin
# when loaded through Python entrypoints or local plugin directories.
# The entrypoint is defined in pyproject.toml under [project.entry-points."karrio.plugins"]
METADATA = PluginMetadata(
    id="landmark",
    label="Landmark Global",
    description="Landmark Global shipping integration for Karrio",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    options=units.ShippingOption,
    services=units.ShippingService,
    connection_configs=units.ConnectionConfig,
    service_levels=units.DEFAULT_SERVICES,
    # Extra info
    website="https://landmarkglobal.com",
    documentation="https://mercurydocs.landmarkglobal.com/docs/api-documentation",
)
