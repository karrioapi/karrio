
from karrio.core.metadata import Metadata

from karrio.mappers.dpdhl_international.mapper import Mapper
from karrio.mappers.dpdhl_international.proxy import Proxy
from karrio.mappers.dpdhl_international.settings import Settings
import karrio.providers.dpdhl_international.units as units


METADATA = Metadata(
    id="dpdhl_international",
    label="Deutsche Post International",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False
)
