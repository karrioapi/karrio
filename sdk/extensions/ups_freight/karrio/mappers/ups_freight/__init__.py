
from karrio.core.metadata import Metadata

from karrio.mappers.ups_freight.mapper import Mapper
from karrio.mappers.ups_freight.proxy import Proxy
from karrio.mappers.ups_freight.settings import Settings
import karrio.providers.ups_freight.units as units


METADATA = Metadata(
    id="ups_freight",
    label="UPS Freight",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False
)
