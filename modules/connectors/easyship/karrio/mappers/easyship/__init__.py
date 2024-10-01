from karrio.core.metadata import Metadata

from karrio.mappers.easyship.mapper import Mapper
from karrio.mappers.easyship.proxy import Proxy
from karrio.mappers.easyship.settings import Settings
import karrio.providers.easyship.units as units
import karrio.providers.easyship.utils as utils


METADATA = Metadata(
    id="easyship",
    label="Easyship",
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
