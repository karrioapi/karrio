from purplship.core.metadata import Metadata

from purplship.mappers.boxknight.mapper import Mapper
from purplship.mappers.boxknight.proxy import Proxy
from purplship.mappers.boxknight.settings import Settings


METADATA = Metadata(
    id="boxknight",
    label="BoxKnight",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # Data Units
)
