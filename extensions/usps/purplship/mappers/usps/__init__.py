from purplship.core.metadata import Metadata

from purplship.mappers.usps.mapper import Mapper
from purplship.mappers.usps.proxy import Proxy
from purplship.mappers.usps.settings import Settings
import purplship.providers.usps.units as units


METADATA = Metadata(
    label="USPS",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # Data Units
    services=units.ShipmentService,
    options=units.ShipmentOption,
)
