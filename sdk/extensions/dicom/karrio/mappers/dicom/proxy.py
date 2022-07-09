from typing import List
from karrio.core.utils import (
    Serializable,
    Deserializable,
    request as http,
    exec_async,
    DP,
)
from karrio.api.proxy import Proxy as BaseProxy
from karrio.mappers.dicom.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    def get_tracking(self, request: Serializable) -> Deserializable:
        def _get_tracking(tracking_number: str):
            return http(
                url=f"{self.settings.server_url}/v1/tracking/{tracking_number}",
                trace=self.trace_as("json"),
                method="GET",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Basic {self.settings.authorization}",
                },
            )

        responses: List[dict] = exec_async(_get_tracking, request.serialize())
        return Deserializable(
            responses, lambda res: [DP.to_dict(r) for r in res if any(r.strip())]
        )
