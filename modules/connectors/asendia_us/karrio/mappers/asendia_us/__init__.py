from karrio.core.metadata import Metadata

from karrio.mappers.asendia_us.mapper import Mapper
from karrio.mappers.asendia_us.proxy import Proxy
from karrio.mappers.asendia_us.settings import Settings
import karrio.providers.asendia_us.units as units
import karrio.providers.asendia_us.utils as utils


METADATA = Metadata(
    status="beta",
    id="asendia_us",
    label="Asendia US",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    options=units.ShippingOption,
    services=units.ShippingService,
    connection_configs=utils.ConnectionConfig,
    # New fields
    website="https://www.asendia.com/",
    documentation="https://a1api.asendiausa.com/swagger/index.html",
    description="deliver cross-border e-commerce solutions that are loved by your shoppers worldwide.",
)
