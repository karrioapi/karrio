import karrio.core.metadata as metadata
import karrio.mappers.usps as mappers
import karrio.providers.usps.units as units
import karrio.providers.usps.utils as utils


METADATA = metadata.PluginMetadata(
    status="production-ready",
    id="usps",
    label="USPS",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=False,
    options=units.ShippingOption,
    services=units.ShippingService,
    connection_configs=utils.ConnectionConfig,
    # New fields
    website="https://www.usps.com",
    documentation="https://www.usps.com/business/web-tools-apis",
    description="The United States Postal Service is an independent agency of the executive branch of the United States federal government responsible for providing postal service in the United States.",
)
