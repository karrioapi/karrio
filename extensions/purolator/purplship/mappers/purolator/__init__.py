from purplship.core.metadata import Metadata

from purplship.mappers.purolator.mapper import Mapper
from purplship.mappers.purolator.proxy import Proxy
from purplship.mappers.purolator.settings import Settings
import purplship.providers.purolator.units as units


METADATA = Metadata(
    label="Purolator",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # Data Units
    options=units.Service,
    package_presets=units.PackagePresets,
    packaging_types=units.PackagingType,
    services=units.Product,
)
