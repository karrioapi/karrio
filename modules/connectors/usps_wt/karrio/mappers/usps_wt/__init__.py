from karrio.core.metadata import Metadata

from karrio.mappers.usps_wt.mapper import Mapper
from karrio.mappers.usps_wt.proxy import Proxy
from karrio.mappers.usps_wt.settings import Settings
import karrio.providers.usps_wt.units as units


METADATA = Metadata(
    id="usps_wt",
    label="USPS Web Tools",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    services=units.ShipmentService,
    options=units.ShippingOption,
)
