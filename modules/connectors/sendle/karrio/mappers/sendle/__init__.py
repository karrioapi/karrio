from karrio.core.metadata import Metadata

from karrio.mappers.sendle.mapper import Mapper
from karrio.mappers.sendle.proxy import Proxy
from karrio.mappers.sendle.settings import Settings
import karrio.providers.sendle.units as units


METADATA = Metadata(
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
)
