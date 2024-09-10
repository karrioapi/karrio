from karrio.core.metadata import Metadata

from karrio.mappers.mydhl.mapper import Mapper
from karrio.mappers.mydhl.proxy import Proxy
from karrio.mappers.mydhl.settings import Settings
import karrio.providers.mydhl.units as units


METADATA = Metadata(
    id="mydhl",
    label="DHL Express",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    has_intl_accounts=True,
)
