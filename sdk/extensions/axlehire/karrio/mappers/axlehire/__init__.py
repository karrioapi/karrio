
from karrio.core.metadata import Metadata

from karrio.mappers.axlehire.mapper import Mapper
from karrio.mappers.axlehire.proxy import Proxy
from karrio.mappers.axlehire.settings import Settings
import karrio.providers.axlehire.units as units


METADATA = Metadata(
    id="axlehire",
    label="AxleHire",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False
)
