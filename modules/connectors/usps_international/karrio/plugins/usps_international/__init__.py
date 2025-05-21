import karrio.core.metadata as metadata
import karrio.mappers.usps_international as mappers
import karrio.providers.usps_international.units as units
import karrio.providers.usps_international.utils as utils


METADATA = metadata.PluginMetadata(
    status="production-ready",
    id="usps_international",
    label="USPS International",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=False,
    options=units.ShippingOption,
    services=units.ShippingService,
    connection_configs=utils.ConnectionConfig,
)
