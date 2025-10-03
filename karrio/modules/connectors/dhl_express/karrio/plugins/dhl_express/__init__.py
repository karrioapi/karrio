import karrio.core.metadata as metadata
import karrio.mappers.dhl_express as mappers
import karrio.providers.dhl_express.units as units


METADATA = metadata.PluginMetadata(
    status="production-ready",
    id="dhl_express",
    label="DHL Express",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    options=units.ShippingOption,
    package_presets=units.PackagePresets,
    packaging_types=units.DCTPackageType,
    services=units.ShippingService,
    connection_configs=units.ConnectionConfig,
    has_intl_accounts=True,
    # New fields
    website="https://www.dhl.com/ca-en/home/express.html",
    documentation="https://developer.dhl.com/api-reference/dhl-express-xml",
    description="When your shipment needs to be there fast, choose the International Specialists for quick, reliable expedited shipments to and from more than 220 countries and territories.",
)
