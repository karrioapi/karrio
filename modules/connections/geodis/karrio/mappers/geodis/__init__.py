from karrio.core.metadata import Metadata

from karrio.mappers.geodis.mapper import Mapper
from karrio.mappers.geodis.proxy import Proxy
from karrio.mappers.geodis.settings import Settings
import karrio.providers.geodis.units as units


METADATA = Metadata(
    id="geodis",
    label="GEODIS",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    options=units.ShippingOption,
    services=units.ShippingService,
    connection_configs=units.ConnectionConfig,
    service_levels=units.DEFAULT_SERVICES,
)
