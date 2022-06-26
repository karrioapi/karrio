from karrio.core.metadata import Metadata

from karrio.mappers.ups.mapper import Mapper
from karrio.mappers.ups.proxy import Proxy
from karrio.mappers.ups.settings import Settings
import karrio.providers.ups.units as units


METADATA = Metadata(
    id="ups",
    label="UPS",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    options=units.ShippingOption,
    package_presets=units.PackagePresets,
    packaging_types=units.PackagingType,
    services=units.ShippingService,
)
