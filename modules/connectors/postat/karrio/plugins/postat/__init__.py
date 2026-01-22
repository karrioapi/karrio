from karrio.core.metadata import PluginMetadata

from karrio.mappers.postat.mapper import Mapper
from karrio.mappers.postat.proxy import Proxy
from karrio.mappers.postat.settings import Settings
import karrio.providers.postat.units as units


# This METADATA object is used by Karrio to discover and register this plugin
# when loaded through Python entrypoints or local plugin directories.
# The entrypoint is defined in pyproject.toml under [project.entry-points."karrio.plugins"]
METADATA = PluginMetadata(
    id="postat",
    label="Austrian Post",
    description="Austrian Post (Österreichische Post) shipping integration via Post-Labelcenter API",
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
    website="https://www.post.at",
    documentation="https://www.post.at/en/business-post-labelcenter",
)
