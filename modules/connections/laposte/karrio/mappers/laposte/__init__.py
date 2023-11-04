
from karrio.core.metadata import Metadata

from karrio.mappers.laposte.mapper import Mapper
from karrio.mappers.laposte.proxy import Proxy
from karrio.mappers.laposte.settings import Settings
import karrio.providers.laposte.units as units


METADATA = Metadata(
    id="laposte",
    label="La Poste",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False
)
