from typing import List
from purplship.core.utils.serializable import Serializable, Deserializable
from purplship.package.mappers.boxknight.settings import Settings
from purplship.package.proxy import Proxy as BaseProxy


class Proxy(BaseProxy):
    settings: Settings
