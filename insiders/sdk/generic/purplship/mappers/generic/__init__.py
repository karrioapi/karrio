from karrio.core.metadata import Metadata

from karrio.mappers.generic.mapper import Mapper
from karrio.mappers.generic.proxy import Proxy
from karrio.mappers.generic.settings import Settings
from karrio.providers.generic import units


DEFAULT_SERVICES = units.DEFAULT_SERVICES

METADATA = Metadata(
    id="generic",
    label="Custom Carrier",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    services=units.Service,
    options=units.Option,
    service_levels=DEFAULT_SERVICES,
)
