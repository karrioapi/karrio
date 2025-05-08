import karrio.core.metadata as metadata
import karrio.mappers.generic as mappers
import karrio.providers.generic.units as units

METADATA = metadata.PluginMetadata(
    status="production-ready",
    id="generic",
    label="Custom Carrier",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    services=units.Service,
    options=units.Option,
    service_levels=units.DEFAULT_SERVICES,
    connection_configs=units.ConnectionConfig,
    has_intl_accounts=True,
)
