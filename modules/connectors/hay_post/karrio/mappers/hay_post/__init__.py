
from karrio.core.metadata import Metadata

from karrio.mappers.hay_post.mapper import Mapper
from karrio.mappers.hay_post.proxy import Proxy
from karrio.mappers.hay_post.settings import Settings
import karrio.providers.hay_post.units as units


METADATA = Metadata(
    id="hay_post",
    label="HayPost",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # Data Units
    services=units.ShippingService,
    options=units.ShippingOption,
    connection_configs=units.ConnectionConfig,
    # package_presets=units.PackagePresets,  # Enum of parcel presets/templates

    is_hub=False
)
