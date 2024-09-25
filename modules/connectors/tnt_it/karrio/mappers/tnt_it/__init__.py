from karrio.core.metadata import Metadata

from karrio.mappers.tnt_it.mapper import Mapper
from karrio.mappers.tnt_it.proxy import Proxy
from karrio.mappers.tnt_it.settings import Settings
import karrio.providers.tnt_it.units as units
import karrio.providers.tnt_it.utils as utils


METADATA = Metadata(
    id="tnt_it",
    label="TNT Connect Italy",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    # options=units.ShippingOption,
    # services=units.ShippingService,
    # connection_configs=utils.ConnectionConfig,
)
