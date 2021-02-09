from purplship.core.metadata import Metadata

from purplship.mappers.aramex.mapper import Mapper
from purplship.mappers.aramex.proxy import Proxy
from purplship.mappers.aramex.settings import Settings
# import purplship.providers.aramex.units as units


METADATA = Metadata(
    label="Aramex",

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
