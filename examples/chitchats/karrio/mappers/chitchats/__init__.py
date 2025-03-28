from karrio.core.metadata import Metadata

from karrio.mappers.chitchats.mapper import Mapper
from karrio.mappers.chitchats.proxy import Proxy
from karrio.mappers.chitchats.settings import Settings

METADATA = Metadata(
    label="Chit Chats",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Optional ID
    id="chitchats",
)

__all__ = [
    "Settings",
    "Mapper",
    "Proxy",
    "METADATA",
] 
