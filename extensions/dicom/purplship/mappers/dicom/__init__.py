from purplship.core.metadata import Metadata

from purplship.mappers.dicom.mapper import Mapper
from purplship.mappers.dicom.proxy import Proxy
from purplship.mappers.dicom.settings import Settings


METADATA = Metadata(
    label="Dicom",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # Data Units
)
