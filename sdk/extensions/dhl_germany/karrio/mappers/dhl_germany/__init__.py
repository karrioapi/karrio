
from karrio.core.metadata import Metadata

from karrio.mappers.dhl_germany.mapper import Mapper
from karrio.mappers.dhl_germany.proxy import Proxy
from karrio.mappers.dhl_germany.settings import Settings
import karrio.providers.dhl_germany.units as units


METADATA = Metadata(
    id="dhl_germany",
    label="DHL Parcel Germany",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False
)
