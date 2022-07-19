from karrio.core.metadata import Metadata

from karrio.mappers.tnt.mapper import Mapper
from karrio.mappers.tnt.proxy import Proxy
from karrio.mappers.tnt.settings import Settings
import karrio.providers.tnt.units as units


METADATA = Metadata(
    id="tnt",
    label="TNT",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    options=units.ShippingOption,
    package_presets=units.PackagePresets,
    packaging_types=units.PackageType,
    services=units.ShipmentService,
)
