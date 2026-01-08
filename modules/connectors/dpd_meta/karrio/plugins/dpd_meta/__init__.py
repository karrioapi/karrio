from karrio.core.metadata import PluginMetadata

from karrio.mappers.dpd_meta.mapper import Mapper
from karrio.mappers.dpd_meta.proxy import Proxy
from karrio.mappers.dpd_meta.settings import Settings
import karrio.providers.dpd_meta.units as units
import karrio.providers.dpd_meta.utils as utils


# This METADATA object is used by Karrio to discover and register this plugin
# when loaded through Python entrypoints or local plugin directories.
# The entrypoint is defined in pyproject.toml under [project.entry-points."karrio.plugins"]
METADATA = PluginMetadata(
    id="dpd_meta",
    label="DPD Group",
    description="DPD Group shipping integration for Karrio",
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
    website="https://www.dpdgroup.com",
    documentation="https://api-preprod.dpsin.dpdgroup.com:8443/shipping/v1/meta-api-docs",
)
