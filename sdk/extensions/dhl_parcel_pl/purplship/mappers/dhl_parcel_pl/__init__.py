from purplship.core.metadata import Metadata

from purplship.mappers.dhl_parcel_pl.mapper import Mapper
from purplship.mappers.dhl_parcel_pl.proxy import Proxy
from purplship.mappers.dhl_parcel_pl.settings import Settings


METADATA = Metadata(
    id="dhl_parcel_pl",
    label="DHL Parcel Poland",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
)
