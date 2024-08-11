from karrio.core.metadata import Metadata

from karrio.mappers.allied_express.mapper import Mapper
from karrio.mappers.allied_express.proxy import Proxy
from karrio.mappers.allied_express.settings import Settings
import karrio.providers.allied_express.units as units
import karrio.providers.allied_express.utils as utils


METADATA = Metadata(
    id="allied_express",
    label="Allied Express",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    services=units.ShippingService,
    options=units.ShippingOption,
    connection_configs=utils.ConnectionConfig,
)
