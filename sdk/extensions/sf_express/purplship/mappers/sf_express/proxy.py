from purplship.core.utils import DP, request as http, Serializable, Deserializable
from purplship.api.proxy import Proxy as BaseProxy
from purplship.mappers.sf_express.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    """ Proxy Methods """

    def get_tracking(self, request: Serializable) -> Deserializable[str]:
        data = self.settings.parse(request.serialize(), "EXP_RECE_SEARCH_ROUTES")
        response = http(
            url=self.settings.server_url,
            data=bytearray(data, "utf-8"),
            method="POST",
        )

        return Deserializable(response, DP.to_dict)
