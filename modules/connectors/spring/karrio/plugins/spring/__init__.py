import karrio.core.metadata as metadata
import karrio.mappers.spring as mappers
import karrio.providers.spring.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="spring",
    label="Spring",
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
)
