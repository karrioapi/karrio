import karrio.core.metadata as metadata
import karrio.mappers.dpd as mappers
import karrio.providers.dpd.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="dpd",
    label="DPD",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=False,
    services=units.ShippingService,
    options=units.ShippingOption,
    has_intl_accounts=True,
)
