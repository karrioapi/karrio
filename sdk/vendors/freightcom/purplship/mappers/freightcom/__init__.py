from purplship.core.metadata import Metadata

from purplship.mappers.freightcom.mapper import Mapper
from purplship.mappers.freightcom.proxy import Proxy
from purplship.mappers.freightcom.settings import Settings
import purplship.providers.freightcom.units as units


METADATA = Metadata(
    id="freightcom",
    label="Freightcom",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # Data Units
    options=units.Option,
    services=units.Service,
)
