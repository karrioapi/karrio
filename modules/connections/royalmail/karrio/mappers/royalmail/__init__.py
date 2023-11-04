from karrio.core.metadata import Metadata

from karrio.mappers.royalmail.mapper import Mapper
from karrio.mappers.royalmail.proxy import Proxy
from karrio.mappers.royalmail.settings import Settings
# import karrio.providers.royalmail.units as units


METADATA = Metadata(
    id="royalmail",
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
