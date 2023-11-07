from karrio.core.metadata import Metadata

from karrio.mappers.postnl.mapper import Mapper
from karrio.mappers.postnl.proxy import Proxy
from karrio.mappers.postnl.settings import Settings
import karrio.providers.postnl.units as units


METADATA = Metadata(
    id="postnl",
    label="Post NL",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
)
