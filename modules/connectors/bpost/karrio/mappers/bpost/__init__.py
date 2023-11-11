
from karrio.core.metadata import Metadata

from karrio.mappers.bpost.mapper import Mapper
from karrio.mappers.bpost.proxy import Proxy
from karrio.mappers.bpost.settings import Settings
import karrio.providers.bpost.units as units


METADATA = Metadata(
    id="bpost",
    label="Belgian Post",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False
)
