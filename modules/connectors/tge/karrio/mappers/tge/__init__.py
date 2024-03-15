from karrio.core.metadata import Metadata

from karrio.mappers.tge.mapper import Mapper
from karrio.mappers.tge.proxy import Proxy
from karrio.mappers.tge.settings import Settings
import karrio.providers.tge.units as units


METADATA = Metadata(
    id="tge",
    label="TGE",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    services=units.ShippingService,
    options=units.ShippingOption,
    connection_configs=units.ConnectionConfig,
)
