from purplship.core.metadata import Metadata

from purplship.mappers.generic.mapper import Mapper
from purplship.mappers.generic.proxy import Proxy
from purplship.mappers.generic.settings import Settings
from purplship.providers.generic import units


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
