import typing
from karrio.core.models import Message
from karrio.providers.chronopost.utils import Settings
from chronopost_lib import quickcostservice, shippingservice, trackingservice
import karrio.lib as lib


def parse_error_response(
    response: lib.Element, settings: Settings, response_type: str
) -> typing.List[Message]:
    element = (
        shippingservice.shippingMultiParcelV5Response
        if response_type == "shippingMultiParcelV5Response"
        else trackingservice.cancelSkybillResponse
        if response_type == "cancelSkybillResponse"
        else quickcostservice.calculateProductsResponse
        if response_type == "calculateProductsResponse"
        else trackingservice.trackSkybillV2Response
    )
    errors = lib.find_element(response_type, response, element)
    return [
        Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            message=error.return_.errorMessage,
            code=error.return_.errorCode,
        )
        for error in errors
        if error.return_.errorCode != 0
    ]
