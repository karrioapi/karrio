from karrio.core.metadata import PluginMetadata

from karrio.mappers.parcelone.mapper import Mapper
from karrio.mappers.parcelone.proxy import Proxy
from karrio.mappers.parcelone.settings import Settings
import karrio.providers.parcelone.units as units


# This METADATA object is used by Karrio to discover and register this plugin
# when loaded through Python entrypoints or local plugin directories.
# The entrypoint is defined in pyproject.toml under [project.entry-points."karrio.plugins"]
METADATA = PluginMetadata(
    id="parcelone",
    label="ParcelOne",
    description="ParcelOne multi-carrier shipping integration for Karrio",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=True,  # ParcelOne is a multi-carrier hub
    options=units.ShippingOption,
    services=units.ShippingService,
    connection_configs=units.ConnectionConfig,
    # Extra info
    website="https://parcel.one",
    documentation="https://parcel.one/api-documentation",
)
