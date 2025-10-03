import karrio.core.metadata as metadata
import karrio.mappers.dhl_universal as mappers


METADATA = metadata.PluginMetadata(
    status="production-ready",
    id="dhl_universal",
    label="DHL Universal",

    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,

    # New fields
    website="https://www.dhl.com/",
    documentation="https://developer.dhl.com/api-reference/shipment-tracking",
    description="DHL is a German logistics company providing courier, package delivery and express mail service, delivering over 1.8 billion parcels per year.",
)