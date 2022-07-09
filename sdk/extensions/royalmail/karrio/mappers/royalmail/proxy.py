from typing import List
from karrio.core.utils import (
    DP,
    request as http,
    Serializable,
    Deserializable,
    exec_async,
)
from karrio.api.proxy import Proxy as BaseProxy
from karrio.mappers.royalmail.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    """ Proxy Methods """

    def get_tracking(self, request: Serializable) -> Deserializable:
        def _get_tracking(mail_piece_id: str):
            return http(
                url=f"{self.settings.server_url}/mailpieces/v2/{mail_piece_id}/events",
                trace=self.trace_as("json"),
                method="GET",
                headers={
                    "Accept": "application/json",
                    "X-IBM-Client-Id": self.settings.client_id,
                    "X-IBM-Client-Secret": self.settings.client_secret,
                    "X-Accept-RMG-Terms": "yes",
                },
            )

        responses: List[dict] = exec_async(_get_tracking, request.serialize())
        return Deserializable(
            responses, lambda res: [DP.to_dict(r) for r in res if any(r.strip())]
        )
