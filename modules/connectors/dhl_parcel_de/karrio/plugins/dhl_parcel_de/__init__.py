import karrio.core.metadata as metadata
import karrio.mappers.dhl_parcel_de as mappers
import karrio.providers.dhl_parcel_de.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="dhl_parcel_de",
    label="DHL Parcel DE",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=False,
    options=units.ShippingOption,
    services=units.ShippingService,
    service_levels=units.DEFAULT_SERVICES,
    connection_configs=units.ConnectionConfig,
)
