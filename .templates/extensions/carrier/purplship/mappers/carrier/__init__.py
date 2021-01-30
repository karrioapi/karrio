from purplship.core.metadata import Metadata

from purplship.mappers.carrier.mapper import Mapper
from purplship.mappers.carrier.proxy import Proxy
from purplship.mappers.carrier.settings import Settings
import purplship.providers.carrier.units as units


METADATA = Metadata(
    label="[carrier label]",

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
