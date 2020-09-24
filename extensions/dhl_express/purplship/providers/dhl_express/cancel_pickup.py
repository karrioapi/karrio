import time
from typing import Tuple, List
from pydhl.cancel_pickup_global_req_3_0 import CancelPURequest, MetaData
from purplship.core.utils.helpers import export
from purplship.core.utils.serializable import Serializable
from purplship.core.models import PickupCancellationRequest, Message
from purplship.providers.dhl_express.utils import Settings, reformat_time
from purplship.providers.dhl_express.error import parse_error_response
from purplship.providers.dhl_express.units import CountryRegion


def parse_cancel_pickup_response(response, settings) -> Tuple[dict, List[Message]]:
    successful = (
        len(response.xpath(".//*[local-name() = $name]", name="ConfirmationNumber")) > 0
    )
    cancellation = (
        dict(
            confirmation_number=response.xpath(
                ".//*[local-name() = $name]", name="ConfirmationNumber"
            )[0].text
        )
        if successful
        else None
    )
    return cancellation, parse_error_response(response, settings)


def cancel_pickup_request(
    payload: PickupCancellationRequest, settings: Settings
) -> Serializable[CancelPURequest]:
    request = CancelPURequest(
        Request=settings.Request(
            MetaData=MetaData(SoftwareName="XMLPI", SoftwareVersion=1.0)
        ),
        schemaVersion=3.0,
        RegionCode=CountryRegion[payload.country_code].value
        if payload.country_code
        else "AM",
        ConfirmationNumber=payload.confirmation_number,
        RequestorName=payload.person_name,
        CountryCode=payload.country_code,
        Reason="006",
        PickupDate=payload.pickup_date,
        CancelTime=time.strftime("%H:%M:%S"),
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: CancelPURequest) -> str:
    xml_str = export(
        request,
        name_="req:CancelPURequest",
        namespacedef_='xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com cancel-pickup-global-req.xsd"',
    )

    xml_str = reformat_time("CancelTime", xml_str)
    return xml_str
