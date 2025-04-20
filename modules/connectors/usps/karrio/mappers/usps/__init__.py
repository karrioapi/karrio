from karrio.core.metadata import Metadata

from karrio.mappers.usps.mapper import Mapper
from karrio.mappers.usps.proxy import Proxy
from karrio.mappers.usps.settings import Settings
import karrio.providers.usps.units as units
import karrio.providers.usps.utils as utils


METADATA = Metadata(
    status="production-ready",
    id="usps",
    label="USPS",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    options=units.ShippingOption,
    services=units.ShippingService,
    connection_configs=utils.ConnectionConfig,
    # New fields
    website="https://www.usps.com",
    documentation="https://www.usps.com/business/web-tools-apis",
    description="The United States Postal Service is an independent agency of the executive branch of the United States federal government responsible for providing postal service in the United States.",
)
