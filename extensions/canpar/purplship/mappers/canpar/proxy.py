import base64
from typing import List
from purplship.core.utils.serializable import Serializable, Deserializable
from purplship.core.utils import to_xml, request as http
from purplship.mappers.canpar.settings import Settings
from purplship.api.proxy import Proxy as BaseProxy
from pycanpar.rating import mailing_scenario


class Proxy(BaseProxy):
    settings: Settings
