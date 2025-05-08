import karrio.core.metadata as metadata
import karrio.mappers.dhl_poland as mappers
from karrio.providers.dhl_poland import units


METADATA = metadata.PluginMetadata(
    status="production-ready",
    id="dhl_poland",
    label="DHL Parcel Poland",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    services=units.Service,
    options=units.ShippingOption,
    packaging_types=units.PackagingType,
    service_levels=units.DEFAULT_SERVICES,
    # New fields
    website="https://dhl24.com.pl/en",
    documentation="https://dhl24.com.pl/en/webapi2/doc.html",
    description="Global Logistics and International Shipping Poland.",
)
