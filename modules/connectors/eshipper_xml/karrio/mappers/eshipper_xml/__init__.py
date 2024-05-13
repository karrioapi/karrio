from karrio.core.metadata import Metadata

from karrio.mappers.eshipper_xml.mapper import Mapper
from karrio.mappers.eshipper_xml.proxy import Proxy
from karrio.mappers.eshipper_xml.settings import Settings
import karrio.providers.eshipper_xml.units as units


METADATA = Metadata(
<<<<<<< HEAD:modules/connectors/eshipper/karrio/mappers/eshipper/__init__.py
    id="eshipper",
    label="eShipper",
=======
    id="eshipper_xml",
    label="eShipper XML",
    is_hub=True,
>>>>>>> 3ccfd84c0 (feat: Rename legacy eshipper integration eshipper_xml):modules/connectors/eshipper_xml/karrio/mappers/eshipper_xml/__init__.py
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    services=units.ShippingService,
    options=units.ShippingOption,
)
