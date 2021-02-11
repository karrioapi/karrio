from purplship.core.metadata import Metadata

from purplship.mappers.yanwen.mapper import Mapper
from purplship.mappers.yanwen.proxy import Proxy
from purplship.mappers.yanwen.settings import Settings
# import purplship.providers.yanwen.units as units


METADATA = Metadata(
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
