import karrio.core.metadata as metadata
import karrio.mappers.laposte as mappers
import karrio.providers.laposte.units as units


METADATA = metadata.PluginMetadata(
    status="production-ready",
    id="laposte",
    label="La Poste",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=False,
    # New fields
    website="https://www.laposte.fr/",
    documentation="https://www.lapostegroupe.com/en/services-mail-parcels-business-unit",
    description="La Poste is a postal service company in France, operating in Metropolitan France and French overseas territories. The company provides mail delivery, parcel shipping, banking services, and digital solutions.",
)
