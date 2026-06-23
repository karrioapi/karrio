import karrio.core.metadata as metadata
import karrio.mappers.dhl_freight as mappers
import karrio.providers.dhl_freight.units as units

METADATA = metadata.PluginMetadata(
    status="beta",
    id="dhl_freight",
    label="DHL Freight",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=False,
    options=units.ShippingOption,
    services=units.ShippingService,
    service_levels=units.DEFAULT_SERVICES,
    connection_configs=units.ConnectionConfig,
    system_config=units.SYSTEM_CONFIG,
)
