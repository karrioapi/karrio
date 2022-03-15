from karrio.core.metadata import Metadata

from karrio.mappers.usps.mapper import Mapper
from karrio.mappers.usps.proxy import Proxy
from karrio.mappers.usps.settings import Settings
import karrio.providers.usps.units as units


METADATA = Metadata(
    id="usps",
    label="USPS",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # Data Units
    services=units.ShipmentService,
    options=units.ShipmentOption,
)
