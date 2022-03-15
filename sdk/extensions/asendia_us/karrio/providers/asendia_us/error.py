from typing import List, Union
from asendia_us_lib.tracking_milestone_response import ResponseStatus
from karrio.core.utils import DP
from karrio.core.models import Message
from karrio.providers.asendia_us import Settings

successes = [200, 204]


def parse_error_response(response: Union[List[dict], dict], settings: Settings) -> List[Message]:
    carrier_errors = [
        (e if "responseStatusCode" in e else e.get("responseStatus"))
        for e in response
        if (
            e.get("responseStatusCode") != 200 and
            e.get("responseStatus", {}).get("responseStatusCode") != 200
        )
    ]
    return [_extract_error(node, settings) for node in carrier_errors]


def _extract_error(error: dict, settings: Settings) -> Message:
    carrier_error = DP.to_object(ResponseStatus, error)

    return Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        # carrier error info
        code=carrier_error.responseStatusCode,
        message=carrier_error.responseStatusMessage
    )
