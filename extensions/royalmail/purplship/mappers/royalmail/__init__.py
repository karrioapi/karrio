from purplship.core.metadata import Metadata

from purplship.mappers.royalmail.mapper import Mapper
from purplship.mappers.royalmail.proxy import Proxy
from purplship.mappers.royalmail.settings import Settings
# import purplship.providers.royalmail.units as units


METADATA = Metadata(
    label="Royal Mail",

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
