from purplship.core.metadata import Metadata

from purplship.mappers.ups_ground.mapper import Mapper
from purplship.mappers.ups_ground.proxy import Proxy
from purplship.mappers.ups_ground.settings import Settings
import purplship.providers.ups_ground.units as units


METADATA = Metadata(
    id="ups_ground",
    label="UPS Ground",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    options=units.ServiceOption,
    package_presets=units.PackagePresets,
    packaging_types=units.PackagingType,
    services=units.ServiceCode,
)
