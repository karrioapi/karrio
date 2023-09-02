from typing import List
from karrio.schemas.amazon_shipping.error_response import ErrorResponse
from karrio.core.models import Message
from karrio.core.utils import DP
from karrio.providers.amazon_shipping.utils import Settings


def parse_error_response(
    response: dict, settings: Settings, details: dict = None
) -> List[Message]:
    errors = DP.to_object(ErrorResponse, response)

    return [
        Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.code,
            message=error.message,
            details={
                **(details or {}),
                **({} if error.details is None else {"note": error.details}),
            },
        )
        for error in errors.errors
    ]
