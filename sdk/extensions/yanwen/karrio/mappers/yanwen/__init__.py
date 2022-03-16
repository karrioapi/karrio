from karrio.core.metadata import Metadata

from karrio.mappers.yanwen.mapper import Mapper
from karrio.mappers.yanwen.proxy import Proxy
from karrio.mappers.yanwen.settings import Settings
# import karrio.providers.yanwen.units as units


METADATA = Metadata(
    id="yanwen",
    label="Yanwen",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # Data Units
    # options=units.OptionCode,
    # package_presets=units.PackagePresets,
    # packaging_types=units.PackagingType,
    # services=units.Serives,
)
