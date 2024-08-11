from karrio.core.metadata import Metadata

from karrio.mappers.allied_express_local.mapper import Mapper
from karrio.mappers.allied_express_local.proxy import Proxy
from karrio.mappers.allied_express_local.settings import Settings
import karrio.providers.allied_express_local.units as units
import karrio.providers.allied_express_local.utils as utils


METADATA = Metadata(
    id="allied_express_local",
    label="Allied Express Local",
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
