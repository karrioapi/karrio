from purplship.core.metadata import Metadata

from purplship.mappers.ics_courier.mapper import Mapper
from purplship.mappers.ics_courier.proxy import Proxy
from purplship.mappers.ics_courier.settings import Settings


METADATA = Metadata(
    id="ics_courier",
    label="ICS Courier",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # Data Units
)
