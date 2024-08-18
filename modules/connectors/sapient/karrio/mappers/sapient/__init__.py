from karrio.core.metadata import Metadata

from karrio.mappers.sapient.mapper import Mapper
from karrio.mappers.sapient.proxy import Proxy
from karrio.mappers.sapient.settings import Settings
import karrio.providers.sapient.units as units
import karrio.providers.sapient.utils as utils


METADATA = Metadata(
    id="sapient",
    label="SAPIENT",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=True,
    options=units.ShippingOption,
    services=units.ShippingService,
    connection_configs=utils.ConnectionConfig,
)
