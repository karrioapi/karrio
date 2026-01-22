import karrio.core.metadata as metadata
import karrio.mappers.bpost as mappers
import karrio.providers.bpost.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="bpost",
    label="Belgian Post",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    options=units.ShippingOption,
    services=units.ShippingService,
    service_levels=units.DEFAULT_SERVICES,
    connection_configs=units.ConnectionConfig,
    # New fields
    website="https://bpostgroup.com/",
    documentation="https://bpost.freshdesk.com/support/solutions/articles/4000037653-where-can-i-find-the-bpack-integration-manual-examples-and-xsd-s-",
    description="The Belgian company responsible for the delivery of national and international mail.",
)
