from karrio.core.metadata import Metadata

from karrio.mappers.dhl_universal.mapper import Mapper
from karrio.mappers.dhl_universal.proxy import Proxy
from karrio.mappers.dhl_universal.settings import Settings


METADATA = Metadata(
    status="production-ready",
    id="dhl_universal",
    label="DHL Universal",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # New fields
    website="https://www.dhl.com/",
    documentation="https://developer.dhl.com/api-reference/shipment-tracking",
    description="DHL is a German logistics company providing courier, package delivery and express mail service, delivering over 1.8 billion parcels per year.",
)
