from karrio.core.metadata import Metadata

from karrio.mappers.usps_wt_international.mapper import Mapper
from karrio.mappers.usps_wt_international.proxy import Proxy
from karrio.mappers.usps_wt_international.settings import Settings
import karrio.providers.usps_wt_international.units as units


METADATA = Metadata(
    id="usps_wt_international",
    label="USPS Web Tools International",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    services=units.ShippingService,
    options=units.ShippingOption,
)
