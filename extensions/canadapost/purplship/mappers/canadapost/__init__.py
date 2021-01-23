from purplship.core.metadata import Metadata

from purplship.mappers.canadapost.mapper import Mapper
from purplship.mappers.canadapost.proxy import Proxy
from purplship.mappers.canadapost.settings import Settings
import purplship.providers.canadapost.units as units


METADATA = Metadata(
    label="Canada Post",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # Data Units
    options=units.OptionCode,
    package_presets=units.PackagePresets,
    services=units.ServiceType,
)
