from karrio.core.metadata import Metadata

from karrio.mappers.chronopost.mapper import Mapper
from karrio.mappers.chronopost.proxy import Proxy
from karrio.mappers.chronopost.settings import Settings, DEFAULT_SERVICES
from karrio.providers.chronopost import units


METADATA = Metadata(
    id="chronopost",
    label="Chronopost",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
)
