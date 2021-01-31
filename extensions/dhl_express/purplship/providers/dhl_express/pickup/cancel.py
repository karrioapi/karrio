import time
from typing import Tuple, List
from dhl_express_lib.cancel_pickup_global_req_3_0 import CancelPURequest, MetaData
from purplship.core.utils import XP,  Serializable
from purplship.core.models import (
    PickupCancelRequest,
    Message,
    ConfirmationDetails,
)
from purplship.providers.dhl_express.utils import Settings, reformat_time
from purplship.providers.dhl_express.error import parse_error_response
from purplship.providers.dhl_express.units import CountryRegion


def parse_pickup_cancel_response(
    response, settings
) -> Tuple[ConfirmationDetails, List[Message]]:
    successful = (
        len(response.xpath(".//*[local-name() = $name]", name="ConfirmationNumber")) > 0
    )
    cancellation = (
        ConfirmationDetails(
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
            success=successful,
            operation="Cancel Pickup",
        )
        if successful
        else None
    )

    return cancellation, parse_error_response(response, settings)


def pickup_cancel_request(
    payload: PickupCancelRequest, settings: Settings
) -> Serializable[CancelPURequest]:

    request = CancelPURequest(
        Request=settings.Request(
            MetaData=MetaData(SoftwareName="XMLPI", SoftwareVersion=1.0)
        ),
        schemaVersion=3.0,
        RegionCode=(
            CountryRegion[payload.address.country_code].value
            if payload.address is not None and payload.address.country_code is not None else "AM"
        ),
        ConfirmationNumber=payload.confirmation_number,
        RequestorName=payload.address.person_name,
        CountryCode=payload.address.country_code,
        Reason="006",
        PickupDate=payload.pickup_date,
        CancelTime=time.strftime("%H:%M:%S"),
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: CancelPURequest) -> str:
    xml_str = XP.export(
        request,
        name_="req:CancelPURequest",
        namespacedef_='xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com cancel-pickup-global-req.xsd"',
    )

    xml_str = reformat_time("CancelTime", xml_str)
    return xml_str
