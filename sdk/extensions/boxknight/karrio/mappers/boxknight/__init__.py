from karrio.core.metadata import Metadata

from karrio.mappers.boxknight.mapper import Mapper
from karrio.mappers.boxknight.proxy import Proxy
from karrio.mappers.boxknight.settings import Settings


METADATA = Metadata(
    id="boxknight",
    label="BoxKnight",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # Data Units
)
