from karrio.core.metadata import Metadata

from karrio.mappers.dpd.mapper import Mapper
from karrio.mappers.dpd.proxy import Proxy
from karrio.mappers.dpd.settings import Settings
import karrio.providers.dpd.units as units


METADATA = Metadata(
    id="dpd",
    label="DPD",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    services=units.ShippingService,
    options=units.ShippingOption,
)
