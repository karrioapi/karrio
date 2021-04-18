from purplship.core.metadata import Metadata

from purplship.mappers.usps_international.mapper import Mapper
from purplship.mappers.usps_international.proxy import Proxy
from purplship.mappers.usps_international.settings import Settings
import purplship.providers.usps_international.units as units


METADATA = Metadata(
    label="USPS International",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # Data Units
    services=units.ShipmentService,
    options=units.ShipmentOption,
)
