from karrio.core.metadata import Metadata

from karrio.mappers.locate2u.mapper import Mapper
from karrio.mappers.locate2u.proxy import Proxy
from karrio.mappers.locate2u.settings import Settings
import karrio.providers.locate2u.units as units


METADATA = Metadata(
    id="locate2u",
    label="Locate2u",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    services=units.ShippingService,
    options=units.ShippingOption,
    service_levels=units.DEFAULT_SERVICES,
)
