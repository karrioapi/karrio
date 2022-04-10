from karrio.core.metadata import Metadata

from karrio.mappers.easypost.mapper import Mapper
from karrio.mappers.easypost.proxy import Proxy
from karrio.mappers.easypost.settings import Settings
import karrio.providers.easypost.units as units


METADATA = Metadata(
    id="easypost",
    label="EasyPost",
    is_hub=True,
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    options=units.Option,
    services=units.Service,
    CARRIER_IDS=units.CARRIER_IDS,
)
