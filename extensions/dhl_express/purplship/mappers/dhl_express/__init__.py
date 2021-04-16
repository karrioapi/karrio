from purplship.core.metadata import Metadata

from purplship.mappers.dhl_express.mapper import Mapper
from purplship.mappers.dhl_express.proxy import Proxy
from purplship.mappers.dhl_express.settings import Settings
import purplship.providers.dhl_express.units as units


METADATA = Metadata(
    label="DHL Express",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # Data Units
    options=units.SpecialServiceCode,
    package_presets=units.PackagePresets,
    packaging_types=units.DCTPackageType,
    services=units.ProductCode,
)
