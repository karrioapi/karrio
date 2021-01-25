from purplship.core.metadata import Metadata

from purplship.mappers.fedex_express.mapper import Mapper
from purplship.mappers.fedex_express.proxy import Proxy
from purplship.mappers.fedex_express.settings import Settings
import purplship.providers.fedex.units as units


METADATA = Metadata(
    label="FedEx Express",

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

