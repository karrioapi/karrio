import karrio.core.metadata as metadata
import karrio.mappers.gls as mappers
import karrio.providers.gls.units as units
import karrio.providers.gls.utils as utils


METADATA = metadata.PluginMetadata(
    status="development",
    id="gls",
    label="GLS Group",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=False,
    options=units.ShippingOption,
    services=units.ShippingService,
    service_levels=units.DEFAULT_SERVICES,
    connection_configs=utils.ConnectionConfig,
    # Extra info
    website="https://www.gls-group.net",
    description="GLS Group shipping services",
)
