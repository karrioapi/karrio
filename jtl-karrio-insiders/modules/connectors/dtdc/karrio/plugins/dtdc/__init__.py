import karrio.core.metadata as metadata
import karrio.mappers.dtdc as mappers
import karrio.providers.dtdc.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="dtdc",
    label="DTDC",
    is_hub=False,
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    options=units.ShippingOption,
    services=units.ShippingService,
    packaging_types=units.PackagingType,
    connection_configs=units.ConnectionConfig,
    service_levels=units.DEFAULT_SERVICES,
    # Extra info
    website="https://dtdc.in",
    documentation="https://www.dtdc.in/dtdcapi/trackCnno.do",
    description="DTDC is India's leading express distribution and logistics solutions provider, offering domestic and international courier services.",
)
