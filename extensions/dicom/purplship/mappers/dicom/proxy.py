from typing import List
from purplship.core.utils.serializable import Serializable, Deserializable
from purplship.api.proxy import Proxy as BaseProxy
from purplship.mappers.dicom.settings import Settings


class Proxy(BaseProxy):
    settings: Settings
