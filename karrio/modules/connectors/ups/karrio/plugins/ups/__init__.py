import karrio.core.metadata as metadata
import karrio.mappers.ups as mappers
import karrio.providers.ups.units as units


METADATA = metadata.PluginMetadata(
    status="production-ready",
    id="ups",
    label="UPS",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    options=units.ShippingOption,
    package_presets=units.PackagePresets,
    packaging_types=units.PackagingType,
    services=units.ShippingService,
    connection_configs=units.ConnectionConfig,
    has_intl_accounts=True,
    # New fields
    website="https://www.ups.com",
    description="UPS is an American multinational shipping & receiving and supply chain management company.",
)
