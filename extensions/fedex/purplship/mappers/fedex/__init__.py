from purplship.core.metadata import Metadata

from purplship.mappers.fedex.mapper import Mapper
from purplship.mappers.fedex.proxy import Proxy
from purplship.mappers.fedex.settings import Settings
import purplship.providers.fedex.units as units


METADATA = Metadata(
    label="FedEx",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # Data Units
    options=units.SpecialServiceType,
    package_presets=units.PackagePresets,
    packaging_types=units.PackagingType,
    services=units.ServiceType,
)

