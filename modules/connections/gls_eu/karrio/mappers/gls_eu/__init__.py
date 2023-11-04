from karrio.core.metadata import Metadata

from karrio.mappers.gls_eu.mapper import Mapper
from karrio.mappers.gls_eu.proxy import Proxy
from karrio.mappers.gls_eu.settings import Settings
import karrio.providers.gls_eu.units as units


METADATA = Metadata(
    id="gls_eu",
    label="GLS",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
)
