from purplship.core.metadata import Metadata

from purplship.mappers.ups.mapper import Mapper
from purplship.mappers.ups.proxy import Proxy
from purplship.mappers.ups.settings import Settings
import purplship.providers.ups.units as units


METADATA = Metadata(
    label="UPS",

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
