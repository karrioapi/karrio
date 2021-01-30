from purplship.core.metadata import Metadata

from purplship.mappers.purolator_courier.mapper import Mapper
from purplship.mappers.purolator_courier.proxy import Proxy
from purplship.mappers.purolator_courier.settings import Settings
import purplship.providers.purolator_courier.units as units


METADATA = Metadata(
    label="Purolator Courier",

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
