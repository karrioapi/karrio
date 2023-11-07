from karrio.core.metadata import Metadata

from karrio.mappers.dhl_universal.mapper import Mapper
from karrio.mappers.dhl_universal.proxy import Proxy
from karrio.mappers.dhl_universal.settings import Settings


METADATA = Metadata(
    id="dhl_universal",
    label="DHL Universal",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
)
