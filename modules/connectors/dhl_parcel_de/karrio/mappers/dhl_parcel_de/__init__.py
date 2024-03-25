from karrio.core.metadata import Metadata

from karrio.mappers.dhl_parcel_de.mapper import Mapper
from karrio.mappers.dhl_parcel_de.proxy import Proxy
from karrio.mappers.dhl_parcel_de.settings import Settings
import karrio.providers.dhl_parcel_de.units as units


METADATA = Metadata(
    id="dhl_parcel_de",
    label="DHL Parcel DE",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    options=units.ShippingOption,
    services=units.ShippingService,
    service_levels=units.DEFAULT_SERVICES,
    connection_configs=units.ConnectionConfig,
)
