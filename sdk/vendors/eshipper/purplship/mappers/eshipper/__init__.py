from purplship.core.metadata import Metadata

from purplship.mappers.eshipper.mapper import Mapper
from purplship.mappers.eshipper.proxy import Proxy
from purplship.mappers.eshipper.settings import Settings
import purplship.providers.eshipper.units as units


METADATA = Metadata(
    id="freightcom",
    label="eShipper",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # Data Units
    options=units.Option,
    services=units.Service,
)
