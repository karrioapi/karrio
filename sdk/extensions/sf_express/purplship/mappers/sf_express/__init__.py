from karrio.core.metadata import Metadata

from karrio.mappers.sf_express.mapper import Mapper
from karrio.mappers.sf_express.proxy import Proxy
from karrio.mappers.sf_express.settings import Settings
# import karrio.providers.sf_express.units as units


METADATA = Metadata(
    id="sf_express",
    label="SF-Express",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # Data Units
    # options=units.OptionCode,
    # package_presets=units.PackagePresets,
    # packaging_types=units.PackagingType,
    # services=units.Serives,
)
