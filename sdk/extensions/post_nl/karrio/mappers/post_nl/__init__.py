
from karrio.core.metadata import Metadata

from karrio.mappers.post_nl.mapper import Mapper
from karrio.mappers.post_nl.proxy import Proxy
from karrio.mappers.post_nl.settings import Settings
import karrio.providers.post_nl.units as units


METADATA = Metadata(
    id="post_nl",
    label="Post NL",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False
)
