from purplship.core.metadata import Metadata

from purplship.mappers.canpar.mapper import Mapper
from purplship.mappers.canpar.proxy import Proxy
from purplship.mappers.canpar.settings import Settings


METADATA = Metadata(
    label="Canpar",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # Data Units
)
