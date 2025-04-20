from karrio.core.metadata import Metadata

from karrio.mappers.canpar.mapper import Mapper
from karrio.mappers.canpar.proxy import Proxy
from karrio.mappers.canpar.settings import Settings


METADATA = Metadata(
    status="beta",
    id="canpar",
    label="Canpar",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # Data Units

    # New fields
    website="https://www.canpar.com/",
    documentation="https://www.canpar.com/en/solutions/ecommerce_tools.htm",
    description="Everything Canpar Express does-product development, technological upgrades, customer service-is shaped and tailored to transporting our customers' parcels efficiently and cost-effectively.",
)
