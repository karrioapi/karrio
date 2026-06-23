import karrio.core.metadata as metadata
import karrio.mappers.dpd_france as mappers
import karrio.providers.dpd_france.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="dpd_france",
    label="DPD France",
    is_hub=False,
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    options=units.ShippingOption,
    services=units.ShippingService,
    service_levels=units.DEFAULT_SERVICES,
    connection_configs=units.ConnectionConfig,
    # New fields
    website="https://www.dpd.fr",
    description="DPD France (cargoNET / EPrintWebservice) shipping integration for Karrio.",
)
