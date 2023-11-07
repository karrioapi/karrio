from karrio.core.metadata import Metadata

from karrio.mappers.boxknight.mapper import Mapper
from karrio.mappers.boxknight.proxy import Proxy
from karrio.mappers.boxknight.settings import Settings
import karrio.providers.boxknight.units as units


METADATA = Metadata(
    id="boxknight",
    label="BoxKnight",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    services=units.ShippingService,
    options=units.ShippingOption,
)
