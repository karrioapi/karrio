from karrio.core.metadata import Metadata

from karrio.mappers.sendle.mapper import Mapper
from karrio.mappers.sendle.proxy import Proxy
from karrio.mappers.sendle.settings import Settings
# import karrio.providers.sendle.units as units


METADATA = Metadata(
    id="sendle",
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
