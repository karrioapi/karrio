from purplship.core.metadata import Metadata

from purplship.mappers.asendia_us.mapper import Mapper
from purplship.mappers.asendia_us.proxy import Proxy
from purplship.mappers.asendia_us.settings import Settings
# import purplship.providers.asendia_us.units as units


METADATA = Metadata(
    id="asendia_us",
    label="Asendia US",

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
