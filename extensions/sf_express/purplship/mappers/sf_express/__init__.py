from purplship.core.metadata import Metadata

from purplship.mappers.sf_express.mapper import Mapper
from purplship.mappers.sf_express.proxy import Proxy
from purplship.mappers.sf_express.settings import Settings
# import purplship.providers.sf_express.units as units


METADATA = Metadata(
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
