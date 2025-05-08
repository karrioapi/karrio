import karrio.core.metadata as metadata
import karrio.mappers.canadapost as mappers
import karrio.providers.canadapost.units as units


METADATA = metadata.PluginMetadata(
    status="production-ready",
    id="canadapost",
    label="Canada Post",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    options=units.ShippingOption,
    package_presets=units.PackagePresets,
    services=units.ServiceType,
    connection_configs=units.ConnectionConfig,
    # New fields
    website="https://www.canadapost-postescanada.ca/cpc/en/home.page",
    documentation="https://www.canadapost-postescanada.ca/information/app/drc/home",
    description="Mailing and shipping for Personal and Business.",
)
