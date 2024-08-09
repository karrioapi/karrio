from karrio.core.metadata import Metadata

from karrio.mappers.fedex_ws.mapper import Mapper
from karrio.mappers.fedex_ws.proxy import Proxy
from karrio.mappers.fedex_ws.settings import Settings
import karrio.providers.fedex_ws.units as units


METADATA = Metadata(
    id="fedex_ws",
    label="FedEx Web Service",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    options=units.ShippingOption,
    package_presets=units.PackagePresets,
    packaging_types=units.PackagingType,
    services=units.ServiceType,
    connection_configs=units.ConnectionConfig,
    has_intl_accounts=True,
)
