from karrio.core.metadata import Metadata

from karrio.mappers.yunexpress.mapper import Mapper
from karrio.mappers.yunexpress.proxy import Proxy
from karrio.mappers.yunexpress.settings import Settings
# import karrio.providers.yunexpress.units as units


METADATA = Metadata(
    id="yunexpress",
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
