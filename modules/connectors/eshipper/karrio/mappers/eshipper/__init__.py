from karrio.core.metadata import Metadata

from karrio.mappers.eshipper.mapper import Mapper
from karrio.mappers.eshipper.proxy import Proxy
from karrio.mappers.eshipper.settings import Settings
import karrio.providers.eshipper.units as units


METADATA = Metadata(
    id="eshipper",
    label="eShipper",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    services=units.ShippingService,
    options=units.ShippingOption,
)
