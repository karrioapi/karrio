from purplship.core.metadata import Metadata

from purplship.mappers.generic.mapper import Mapper
from purplship.mappers.generic.proxy import Proxy
from purplship.mappers.generic.settings import Settings
from purplship.providers.generic import units


METADATA = Metadata(
    id="generic",
    label="Generic",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    services=units.Service,
    options=units.Option,
    service_levels=units.DEFAULT_SERVICES,
)
