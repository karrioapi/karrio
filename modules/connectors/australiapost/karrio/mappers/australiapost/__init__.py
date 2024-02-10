from karrio.core.metadata import Metadata

from karrio.mappers.australiapost.mapper import Mapper
from karrio.mappers.australiapost.proxy import Proxy
from karrio.mappers.australiapost.settings import Settings
import karrio.providers.australiapost.units as units


METADATA = Metadata(
    id="australiapost",
    label="Australia Post",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    services=units.ShippingService,
    options=units.ShippingOption,
)
