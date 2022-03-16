from karrio.core.metadata import Metadata

from karrio.mappers.dicom.mapper import Mapper
from karrio.mappers.dicom.proxy import Proxy
from karrio.mappers.dicom.settings import Settings


METADATA = Metadata(
    id="dicom",
    label="Dicom",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # Data Units
)
