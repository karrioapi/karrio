from karrio.core.metadata import Metadata

from karrio.mappers.roadie.mapper import Mapper
from karrio.mappers.roadie.proxy import Proxy
from karrio.mappers.roadie.settings import Settings
import karrio.providers.roadie.units as units


METADATA = Metadata(
    id="roadie",
    label="Roadie",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    services=units.ShippingService,
    options=units.ShippingOption,
)
