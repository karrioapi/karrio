from karrio.core.metadata import Metadata

from karrio.mappers.fedex.mapper import Mapper
from karrio.mappers.fedex.proxy import Proxy
from karrio.mappers.fedex.settings import Settings
import karrio.providers.fedex.units as units


METADATA = Metadata(
    id="fedex",
    label="FedEx",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    options=units.ShippingOption,
    package_presets=units.PackagePresets,
    packaging_types=units.PackagingType,
    services=units.ServiceType,
)
