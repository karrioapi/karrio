
from karrio.core.metadata import Metadata

from karrio.mappers.ninja_van.mapper import Mapper
from karrio.mappers.ninja_van.proxy import Proxy
from karrio.mappers.ninja_van.settings import Settings
import karrio.providers.ninja_van.units as units


METADATA = Metadata(
    id="ninja_van",
    label="Ninja Van",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False
)
