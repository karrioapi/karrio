"""Karrio DPD Group plugin metadata."""

import karrio.core.metadata as metadata
import karrio.mappers.dpd_group as mappers
import karrio.providers.dpd_group.units as units

METADATA = metadata.PluginMetadata(
    status="production-ready",
    id="dpd_group",
    label="DPD Group",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=False,
    options=units.ShippingOption,
    services=units.ShippingService,
    connection_configs=units.ConnectionConfig,
    # Extra info
    website="https://www.dpdgroup.com",
    description="DPD Group is one of Europe's leading parcel delivery networks, offering shipping solutions across multiple countries.",
)
