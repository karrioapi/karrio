from karrio.core.metadata import Metadata

from karrio.mappers.canadapost.mapper import Mapper
from karrio.mappers.canadapost.proxy import Proxy
from karrio.mappers.canadapost.settings import Settings
import karrio.providers.canadapost.units as units


METADATA = Metadata(
    id="canadapost",
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
