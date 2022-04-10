from karrio.core.utils import DP, request as http
from karrio.api.proxy import Proxy as BaseProxy
from karrio.mappers.easypost.settings import Settings
from karrio.core.utils.serializable import Serializable, Deserializable


class Proxy(BaseProxy):
    settings: Settings

    def get_rates(self, request: Serializable) -> Deserializable[str]:
        pass

    def create_shipment(self, request: Serializable) -> Deserializable[str]:
        pass

    def cancel_shipment(self, request: Serializable) -> Deserializable[str]:
        pass
