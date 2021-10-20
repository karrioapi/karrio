from typing import List
from purplship.core.utils import Serializable, Deserializable, request as http, exec_async, DP
from purplship.api.proxy import Proxy as BaseProxy
from purplship.mappers.dicom.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    def get_tracking(self, request: Serializable) -> Deserializable:

        def _get_tracking(tracking_number: str):
            return http(
                url=f"{self.settings.server_url}/v1/tracking/{tracking_number}",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Basic {self.settings.authorization}"
                },
                method="GET",
            )

        responses: List[dict] = exec_async(_get_tracking, request.serialize())
        return Deserializable(responses, lambda res: [DP.to_dict(r) for r in res if any(r.strip())])
