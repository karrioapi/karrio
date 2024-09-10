from karrio.core.metadata import Metadata

from karrio.mappers.amazon_shipping.mapper import Mapper
from karrio.mappers.amazon_shipping.proxy import Proxy
from karrio.mappers.amazon_shipping.settings import Settings
import karrio.providers.amazon_shipping.units as units


METADATA = Metadata(
    id="amazon_shipping",
    label="AmazonShipping",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    services=units.Service,
    has_intl_accounts=True,
)
