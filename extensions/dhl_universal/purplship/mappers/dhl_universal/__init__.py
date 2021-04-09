from purplship.core.metadata import Metadata

from purplship.mappers.dhl_universal.mapper import Mapper
from purplship.mappers.dhl_universal.proxy import Proxy
from purplship.mappers.dhl_universal.settings import Settings


METADATA = Metadata(
    label="DHL Universal",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
)
