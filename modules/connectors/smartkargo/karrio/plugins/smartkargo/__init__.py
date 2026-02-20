import karrio.providers.smartkargo.units as units
import karrio.mappers.smartkargo as mappers
from karrio.core.metadata import PluginMetadata


METADATA = PluginMetadata(
    id="smartkargo",
    label="SmartKargo",
    description="SmartKargo air cargo shipping integration",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=False,
    options=units.ShippingOption,
    services=units.ShippingService,
    connection_configs=units.ConnectionConfig,
    # Extra info
    website="https://www.smartkargo.com",
    status="beta",
)
