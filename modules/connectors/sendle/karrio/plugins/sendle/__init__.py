import karrio.core.metadata as metadata
import karrio.mappers.sendle as mappers
import karrio.providers.sendle.units as units


METADATA = metadata.PluginMetadata(
    status="production-ready",
    id="sendle",
    label="Sendle",
    is_hub=False,
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    options=units.ShippingOption,
    services=units.ShippingService,
    has_intl_accounts=True,
    # New fields
    website="https://www.sendle.com",
    documentation="https://www.sendle.com/developers",
    description="Sendle is a registered B Corp and 100% carbon neutral shipping carrier for small businesses, offering affordable package delivery services in Australia and the United States.",
)
