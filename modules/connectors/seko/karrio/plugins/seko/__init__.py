import karrio.core.metadata as metadata
import karrio.mappers.seko as mappers
import karrio.providers.seko.units as units
import karrio.providers.seko.utils as utils


METADATA = metadata.PluginMetadata(
    status="production-ready",
    id="seko",
    label="SEKO Logistics",
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
