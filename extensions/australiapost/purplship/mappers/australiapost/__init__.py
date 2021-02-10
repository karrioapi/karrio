from purplship.core.metadata import Metadata

from purplship.mappers.australiapost.mapper import Mapper
from purplship.mappers.australiapost.proxy import Proxy
from purplship.mappers.australiapost.settings import Settings
# import purplship.providers.australiapost.units as units


METADATA = Metadata(
    label="Australia Post",

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
