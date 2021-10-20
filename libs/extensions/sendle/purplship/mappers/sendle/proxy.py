from typing import List, Tuple
from purplship.core.utils import DP, request as http, Serializable, Deserializable, exec_async
from purplship.api.proxy import Proxy as BaseProxy
from purplship.mappers.sendle.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    """ Proxy Methods """

    def get_tracking(self, request: Serializable) -> Deserializable[List[Tuple[str, str]]]:

        def _get_tracking(ref: str):
            response = http(
                url=f"{self.settings.server_url}/api/tracking/{ref}",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Basic {self.settings.authorization}"
                },
                method="GET",
            )
            return ref, response

        responses: List[Tuple[str, str]] = exec_async(_get_tracking, request.serialize())
        return Deserializable(
            responses,
            lambda res: [(num, DP.to_dict(track)) for num, track in res if any(track.strip())]
        )
