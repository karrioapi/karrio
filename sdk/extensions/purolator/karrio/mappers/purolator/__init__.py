from karrio.core.metadata import Metadata

from karrio.mappers.purolator.mapper import Mapper
from karrio.mappers.purolator.proxy import Proxy
from karrio.mappers.purolator.settings import Settings
import karrio.providers.purolator.units as units


METADATA = Metadata(
    id="purolator",
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
