from karrio.core.metadata import Metadata

from karrio.mappers.fedex.mapper import Mapper
from karrio.mappers.fedex.proxy import Proxy
from karrio.mappers.fedex.settings import Settings
import karrio.providers.fedex.units as units


METADATA = Metadata(
    status="production-ready",
    id="fedex",
    label="FedEx",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    services=units.ShippingService,
    options=units.ShippingOption,
    connection_configs=units.ConnectionConfig,
    has_intl_accounts=True,
    # New fields
    website="https://www.fedex.com",
    description="FedEx Corporation is an American multinational conglomerate holding company which focuses on transportation, e-commerce and business services.",
)
