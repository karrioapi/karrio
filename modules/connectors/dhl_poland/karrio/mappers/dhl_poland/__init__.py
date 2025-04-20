from karrio.core.metadata import Metadata

from karrio.mappers.dhl_poland.mapper import Mapper
from karrio.mappers.dhl_poland.proxy import Proxy
from karrio.mappers.dhl_poland.settings import Settings
from karrio.providers.dhl_poland import units


METADATA = Metadata(
    status="production-ready",
    id="dhl_poland",
    label="DHL Parcel Poland",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    services=units.Service,
    options=units.ShippingOption,
    packaging_types=units.PackagingType,
    service_levels=units.DEFAULT_SERVICES,
    # New fields
    website="https://dhl24.com.pl/en",
    documentation="https://dhl24.com.pl/en/webapi2/doc.html",
    description="Global Logistics and International Shipping Poland.",
)
