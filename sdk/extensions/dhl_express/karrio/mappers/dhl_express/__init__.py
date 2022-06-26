from karrio.core.metadata import Metadata

from karrio.mappers.dhl_express.mapper import Mapper
from karrio.mappers.dhl_express.proxy import Proxy
from karrio.mappers.dhl_express.settings import Settings
import karrio.providers.dhl_express.units as units


METADATA = Metadata(
    id="dhl_express",
    label="DHL Express",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    options=units.ShippingOption,
    package_presets=units.PackagePresets,
    packaging_types=units.DCTPackageType,
    services=units.ProductCode,
)
