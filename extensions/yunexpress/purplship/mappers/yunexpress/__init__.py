from purplship.core.metadata import Metadata

from purplship.mappers.yunexpress.mapper import Mapper
from purplship.mappers.yunexpress.proxy import Proxy
from purplship.mappers.yunexpress.settings import Settings
# import purplship.providers.yunexpress.units as units


METADATA = Metadata(
    label="Yunexpress",

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
