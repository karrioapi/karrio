from purplship.core.metadata import Metadata

from purplship.mappers.dhl_poland.mapper import Mapper
from purplship.mappers.dhl_poland.proxy import Proxy
from purplship.mappers.dhl_poland.settings import Settings


METADATA = Metadata(
    id="dhl_poland",
    label="DHL Parcel Poland",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
)
