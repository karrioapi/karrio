from purplship.core.metadata import Metadata

from purplship.mappers.sendle.mapper import Mapper
from purplship.mappers.sendle.proxy import Proxy
from purplship.mappers.sendle.settings import Settings
# import purplship.providers.sendle.units as units


METADATA = Metadata(
    label="Sendle",

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
