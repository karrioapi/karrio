from typing import List
from purplship.core.utils.serializable import Serializable, Deserializable
from purplship.mappers.boxknight.settings import Settings
from purplship.api.proxy import Proxy as BaseProxy


class Proxy(BaseProxy):
    settings: Settings
