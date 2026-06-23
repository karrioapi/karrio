"""Karrio Amazon Shipping plugin."""

import karrio.core.metadata as metadata
import karrio.mappers.amazon_shipping as mappers
import karrio.providers.amazon_shipping.units as units

METADATA = metadata.PluginMetadata(
    status="beta",
    id="amazon_shipping",
    label="Amazon Shipping",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    services=units.ShippingService,
    options=units.ShippingOption,
    has_intl_accounts=True,
)
