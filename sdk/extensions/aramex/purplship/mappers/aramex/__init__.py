from karrio.core.metadata import Metadata

from karrio.mappers.aramex.mapper import Mapper
from karrio.mappers.aramex.proxy import Proxy
from karrio.mappers.aramex.settings import Settings
# import karrio.providers.aramex.units as units


METADATA = Metadata(
    id="aramex",
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
