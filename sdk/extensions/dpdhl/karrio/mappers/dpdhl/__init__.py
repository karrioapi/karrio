from karrio.core.metadata import Metadata

from karrio.mappers.dpdhl.mapper import Mapper
from karrio.mappers.dpdhl.proxy import Proxy
from karrio.mappers.dpdhl.settings import Settings
import karrio.providers.dpdhl.units as units


METADATA = Metadata(
    id="dpdhl",
    label="Deutsche Post DHL",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
)
