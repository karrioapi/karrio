import time
from typing import Tuple, List
from pydhl.cancel_pickup_global_req_20 import CancelPURequest
from purplship.core.utils.helpers import export
from purplship.core.utils.serializable import Serializable
from purplship.core.models import PickupCancellationRequest, Error
from purplship.carriers.dhl.utils import Settings
from purplship.carriers.dhl.error import parse_error_response


def parse_cancel_pickup_response(response, settings) -> Tuple[dict, List[Error]]:
    successful = len(response.xpath(".//*[local-name() = $name]", name="ConfirmationNumber")) > 0
    cancellation = dict(
        confirmation_number=response.xpath(".//*[local-name() = $name]", name="ConfirmationNumber")[0].text
    ) if successful else None
    return cancellation, parse_error_response(response, settings)


def cancel_pickup_request(payload: PickupCancellationRequest, settings: Settings) -> Serializable[CancelPURequest]:
    request = CancelPURequest(
        Request=settings.Request(),
        schemaVersion="2.0",
        RegionCode=payload.extra.get("RegionCode") or "AM",
        ConfirmationNumber=payload.confirmation_number,
        RequestorName=payload.person_name,
        CountryCode=payload.country_code,
        Reason=payload.extra.get("Reason") or "006",
        PickupDate=payload.pickup_date,
        CancelTime=time.strftime("%H:%M"),
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: CancelPURequest) -> str:
    return export(
        request,
        name_="req:CancelPURequest",
        namespacedef_='xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com cancel-pickup-global-req.xsd" schemaVersion="2.0"',
    )
