from karrio.core.metadata import Metadata

from karrio.mappers.seko.mapper import Mapper
from karrio.mappers.seko.proxy import Proxy
from karrio.mappers.seko.settings import Settings
import karrio.providers.seko.units as units
import karrio.providers.seko.utils as utils


METADATA = Metadata(
    id="seko",
    label="SEKO Logistics",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    options=units.ShippingOption,
    services=units.ShippingService,
    connection_configs=utils.ConnectionConfig,
)
