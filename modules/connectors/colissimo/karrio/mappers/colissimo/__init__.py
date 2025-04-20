from karrio.core.metadata import Metadata

from karrio.mappers.colissimo.mapper import Mapper
from karrio.mappers.colissimo.proxy import Proxy
from karrio.mappers.colissimo.settings import Settings
import karrio.providers.colissimo.units as units


METADATA = Metadata(
    status="beta",
    id="colissimo",
    label="Colissimo",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    options=units.ShippingOption,
    services=units.ShippingService,
    connection_configs=units.ConnectionConfig,
    service_levels=units.DEFAULT_SERVICES,
    # New fields
    website="https://www.colissimo.entreprise.laposte.fr/en",
    documentation="https://www.colissimo.entreprise.laposte.fr/en/tools-and-services",
    description="Envoi de colis en France et dans le monde entier, livraison à domicile ou en point de retrait, Colissimo vous offre un choix de services qui facilitent votre quotidien.",
)
