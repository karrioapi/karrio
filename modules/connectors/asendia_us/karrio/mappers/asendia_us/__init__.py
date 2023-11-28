from karrio.core.metadata import Metadata

from karrio.mappers.asendia_us.mapper import Mapper
from karrio.mappers.asendia_us.proxy import Proxy
from karrio.mappers.asendia_us.settings import Settings
import karrio.providers.asendia_us.units as units


METADATA = Metadata(
    id="asendia_us",
    label="Asendia US",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    options=units.ShippingOption,
    services=units.ShippingService,
    connection_configs=units.ConnectionConfig,
)
