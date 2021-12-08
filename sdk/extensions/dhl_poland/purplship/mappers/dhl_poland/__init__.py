from purplship.core.metadata import Metadata

from purplship.mappers.dhl_poland.mapper import Mapper
from purplship.mappers.dhl_poland.proxy import Proxy
from purplship.mappers.dhl_poland.settings import Settings, DEFAULT_SERVICES
from purplship.providers.dhl_poland import units


METADATA = Metadata(
    id="dhl_poland",
    label="DHL Parcel Poland",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    services=units.Service,
    options=units.Option,
    packaging_types=units.PackagingType,
    service_levels=units.DEFAULT_SERVICES,
)
