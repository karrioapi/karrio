from purplship.core.metadata import Metadata

from purplship.mappers.tnt.mapper import Mapper
from purplship.mappers.tnt.proxy import Proxy
from purplship.mappers.tnt.settings import Settings
import purplship.providers.tnt.units as units


METADATA = Metadata(
    label="TNT",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # Data Units
    options=units.ShipmentOption,
    package_presets=units.PackagePresets,
    packaging_types=units.PackageType,
    services=units.ShipmentService,
)
