from karrio.core.metadata import Metadata

from karrio.mappers.canpar.mapper import Mapper
from karrio.mappers.canpar.proxy import Proxy
from karrio.mappers.canpar.settings import Settings


METADATA = Metadata(
    id="canpar",
    label="Canpar",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # Data Units
)
