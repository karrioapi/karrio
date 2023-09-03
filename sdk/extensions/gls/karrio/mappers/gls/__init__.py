
from karrio.core.metadata import Metadata

from karrio.mappers.gls.mapper import Mapper
from karrio.mappers.gls.proxy import Proxy
from karrio.mappers.gls.settings import Settings
import karrio.providers.gls.units as units


METADATA = Metadata(
    id="gls",
    label="GLS",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False
)
