
from karrio.core.metadata import Metadata

from karrio.mappers.dpd_belux.mapper import Mapper
from karrio.mappers.dpd_belux.proxy import Proxy
from karrio.mappers.dpd_belux.settings import Settings
import karrio.providers.dpd_belux.units as units


METADATA = Metadata(
    id="dpd_belux",
    label="DPD Belux",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False
)
