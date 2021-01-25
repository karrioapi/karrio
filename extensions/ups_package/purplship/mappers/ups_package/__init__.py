from purplship.core.metadata import Metadata

from purplship.mappers.ups_package.mapper import Mapper
from purplship.mappers.ups_package.proxy import Proxy
from purplship.mappers.ups_package.settings import Settings
import purplship.providers.ups.units as units


METADATA = Metadata(
    label="UPS Package",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # Data Units
    options=units.ServiceOption,
    package_presets=units.PackagePresets,
    packaging_types=units.RatingPackagingType,
    services=units.ShippingServiceCode,
)
