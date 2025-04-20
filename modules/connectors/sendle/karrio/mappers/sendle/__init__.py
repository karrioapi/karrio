from karrio.core.metadata import Metadata

from karrio.mappers.sendle.mapper import Mapper
from karrio.mappers.sendle.proxy import Proxy
from karrio.mappers.sendle.settings import Settings
import karrio.providers.sendle.units as units


METADATA = Metadata(
    status="production-ready",
    id="sendle",
    label="Sendle",
    is_hub=False,
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    options=units.ShippingOption,
    services=units.ShippingService,
    has_intl_accounts=True,
    # New fields
    website="https://www.sendle.com",
    documentation="https://www.sendle.com/developers",
    description="Sendle is a registered B Corp and 100% carbon neutral shipping carrier for small businesses, offering affordable package delivery services in Australia and the United States.",
)
