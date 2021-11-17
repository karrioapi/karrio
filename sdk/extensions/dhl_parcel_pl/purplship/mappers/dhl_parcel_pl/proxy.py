from typing import List, Any
from purplship.core.utils import (
    Serializable,
    Deserializable,
    XP,
    request as http,
)
from purplship.core.utils.helpers import exec_async
from purplship.mappers.dhl_parcel_pl.settings import Settings
from purplship.api.proxy import Proxy as BaseProxy


class Proxy(BaseProxy):
    settings: Settings

    def _send_request(self, request: Serializable[Any], soapaction: str) -> str:
        return http(
            url=f"{self.settings.server_url}",
            data=bytearray(request.serialize(), "utf-8"),
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "soapaction": soapaction,
            },
            method="POST",
        )

    def get_tracking(self, requests: Serializable) -> Deserializable:
        responses = exec_async(
            lambda request: self._send_request(
                Serializable(request),
                soapaction="https://sandbox.dhl24.com.pl/webapi2/provider/service.html?ws=1#getTrackAndTraceInfo",
            ),
            requests.serialize(),
        )
        return Deserializable(XP.bundle_xml(responses), XP.to_xml)
