import karrio.providers.parcelone.units as units
from karrio.core.metadata import PluginMetadata
from karrio.mappers.parcelone.mapper import Mapper
from karrio.mappers.parcelone.proxy import Proxy
from karrio.mappers.parcelone.settings import Settings

# This METADATA object is discovered and registered when the plugin is loaded
# through Python entrypoints or local plugin directories. The entrypoint is
# defined in pyproject.toml under [project.entry-points."karrio.plugins"].
METADATA = PluginMetadata(
    id="parcelone",
    label="ParcelOne",
    description="ParcelOne multi-carrier shipping integration",
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
    system_config=units.SYSTEM_CONFIG,
    # Extra info
    website="https://parcel.one",
    documentation="https://parcel.one/api-documentation",
)
