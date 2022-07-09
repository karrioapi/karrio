import urllib.parse
from karrio.core.utils import (
    XP,
    request as http,
    Serializable,
    Deserializable,
    Job,
    Pipeline,
)
from karrio.api.proxy import Proxy as BaseProxy
from karrio.mappers.tnt.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    """ Proxy Methods """

    def get_tracking(self, request: Serializable) -> Deserializable[str]:
        response = self._send_request(request, "/expressconnect/track.do")

        return Deserializable(response, XP.to_xml)

    """ Private Methods """

    def _send_request(self, request: Serializable, path: str) -> str:
        return http(
            url=f"{self.settings.server_url}{path}",
            data=urllib.parse.urlencode(dict(xml_in=request.serialize())),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )
