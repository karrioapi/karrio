from karrio.core.metadata import PluginMetadata

from karrio.mappers.teleship.mapper import Mapper
from karrio.mappers.teleship.proxy import Proxy
from karrio.mappers.teleship.settings import Settings
from karrio.mappers.teleship.hooks import Hooks
import karrio.providers.teleship.units as units
import karrio.providers.teleship.utils as utils


# This METADATA object is used by Karrio to discover and register this plugin
# when loaded through Python entrypoints or local plugin directories.
# The entrypoint is defined in pyproject.toml under [project.entry-points."karrio.plugins"]
METADATA = PluginMetadata(
    id="teleship",
    label="Teleship",
    description="Teleship is an international shipping platform providing end-to-end logistics solutions with real-time rates, automated customs compliance, and shipment tracking.",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    Hooks=Hooks,
    # Data Units
    is_hub=False,
    options=units.ShippingOption,
    services=units.ShippingService,
    connection_configs=units.ConnectionConfig,
    system_config=units.SYSTEM_CONFIG,
    # Extra info
    website="https://www.teleship.com",
    documentation="https://developers.teleship.com",
)
