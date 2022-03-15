from karrio.core.metadata import Metadata

from karrio.mappers.ics_courier.mapper import Mapper
from karrio.mappers.ics_courier.proxy import Proxy
from karrio.mappers.ics_courier.settings import Settings


METADATA = Metadata(
    id="ics_courier",
    label="ICS Courier",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # Data Units
)
