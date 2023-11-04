from karrio.core.metadata import Metadata

from karrio.mappers.zoom2u.mapper import Mapper
from karrio.mappers.zoom2u.proxy import Proxy
from karrio.mappers.zoom2u.settings import Settings
import karrio.providers.zoom2u.units as units


METADATA = Metadata(
    id="zoom2u",
    label="Zoom2u",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    services=units.ShippingService,
    options=units.ShippingOption,
)
