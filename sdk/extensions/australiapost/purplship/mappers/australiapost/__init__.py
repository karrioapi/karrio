from karrio.core.metadata import Metadata

from karrio.mappers.australiapost.mapper import Mapper
from karrio.mappers.australiapost.proxy import Proxy
from karrio.mappers.australiapost.settings import Settings
# import karrio.providers.australiapost.units as units


METADATA = Metadata(
    id="australiapost",
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
