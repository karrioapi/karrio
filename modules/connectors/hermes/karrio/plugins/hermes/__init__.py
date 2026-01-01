from karrio.core.metadata import PluginMetadata

from karrio.mappers.hermes.mapper import Mapper
from karrio.mappers.hermes.proxy import Proxy
from karrio.mappers.hermes.settings import Settings
import karrio.providers.hermes.units as units


# This METADATA object is used by Karrio to discover and register this plugin
# when loaded through Python entrypoints or local plugin directories.
# The entrypoint is defined in pyproject.toml under [project.entry-points."karrio.plugins"]
METADATA = PluginMetadata(
    id="hermes",
    label="Hermes",
    description="Hermes shipping integration for Karrio",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    options=units.ShippingOption,
    services=units.ShippingService,
    service_levels=units.DEFAULT_SERVICES,
    connection_configs=units.ConnectionConfig,
    # Extra info
    website="https://www.hermesworld.com",
    documentation="https://de-api-int.hermesworld.com/docs/applications/order",
)
