import karrio.core.metadata as metadata
import karrio.mappers.australiapost as mappers
import karrio.providers.australiapost.units as units
import karrio.providers.australiapost.utils as utils


METADATA = metadata.PluginMetadata(
    status="beta",
    id="australiapost",
    label="Australia Post",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=False,
    services=units.ShippingService,
    options=units.ShippingOption,
    # New fields
    website="https://auspost.com.au/",
    documentation="https://developers.auspost.com.au/apis/shipping-and-tracking/reference",
    description="Australia Post, formally known as the Australian Postal Corporation, is a Commonwealth government-owned corporation that provides postal services throughout Australia.",
)
