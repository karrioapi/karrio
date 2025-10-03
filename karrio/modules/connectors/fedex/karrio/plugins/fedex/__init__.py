import karrio.core.metadata as metadata
import karrio.mappers.fedex as mappers
import karrio.providers.fedex.units as units


METADATA = metadata.PluginMetadata(
    status="production-ready",
    id="fedex",
    label="FedEx",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=False,
    services=units.ShippingService,
    options=units.ShippingOption,
    connection_configs=units.ConnectionConfig,
    has_intl_accounts=True,
    # New fields
    website="https://www.fedex.com",
    description="FedEx Corporation is an American multinational conglomerate holding company which focuses on transportation, e-commerce and business services.",
)
