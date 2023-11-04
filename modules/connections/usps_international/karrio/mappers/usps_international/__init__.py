from karrio.core.metadata import Metadata

from karrio.mappers.usps_international.mapper import Mapper
from karrio.mappers.usps_international.proxy import Proxy
from karrio.mappers.usps_international.settings import Settings
import karrio.providers.usps_international.units as units


METADATA = Metadata(
    id="usps_international",
    label="USPS International",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    services=units.ShippingService,
    options=units.ShippingOption,
)
