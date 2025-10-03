import karrio.core.metadata as metadata
import karrio.mappers.purolator as mappers
import karrio.providers.purolator.units as units


METADATA = metadata.PluginMetadata(
    status="production-ready",
    id="purolator",
    label="Purolator",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    options=units.ShippingOption,
    package_presets=units.PackagePresets,
    packaging_types=units.PackagingType,
    services=units.ShippingService,
    # New fields
    website="https://www.purolator.com",
    description="Purolator Inc. is a Canadian courier company, delivering parcels and freight in Canada and internationally.",
)
