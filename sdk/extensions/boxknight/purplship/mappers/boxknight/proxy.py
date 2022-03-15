from typing import List
from karrio.core.utils.serializable import Serializable, Deserializable
from karrio.mappers.boxknight.settings import Settings
from karrio.api.proxy import Proxy as BaseProxy


class Proxy(BaseProxy):
    settings: Settings
