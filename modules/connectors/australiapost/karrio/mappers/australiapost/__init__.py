from karrio.core.metadata import Metadata

from karrio.mappers.australiapost.mapper import Mapper
from karrio.mappers.australiapost.proxy import Proxy
from karrio.mappers.australiapost.settings import Settings
import karrio.providers.australiapost.units as units


METADATA = Metadata(
    status="beta",
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
    # New fields
    website="https://auspost.com.au/",
    documentation="https://developers.auspost.com.au/apis/shipping-and-tracking/reference",
    description="Australia Post, formally known as the Australian Postal Corporation, is a Commonwealth government-owned corporation that provides postal services throughout Australia.",
)
