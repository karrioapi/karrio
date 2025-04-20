from karrio.core.metadata import Metadata

from karrio.mappers.boxknight.mapper import Mapper
from karrio.mappers.boxknight.proxy import Proxy
from karrio.mappers.boxknight.settings import Settings
import karrio.providers.boxknight.units as units


METADATA = Metadata(
    status="beta",
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
    # New fields
    website="https://www.boxknight.com/",
    documentation="https://www.docs.boxknight.com/",
    description="Specializes in same-day delivery at affordable prices for e-commerce retailers. Our mission is to get packages to your customers when they are actually home and as quickly as possible.",
)
