from typing import List, Tuple
from aramex_lib.array_of_string import ArrayOfstring
from aramex_lib.tracking import (
    ShipmentTrackingRequest,
    ClientInfo,
    Transaction,
    TrackingResult
)
from purplship.core.utils import (
    create_envelope,
    Element,
    Serializable,
    XP,
    DF,
)
from purplship.core.models import (
    TrackingEvent,
    TrackingDetails,
    TrackingRequest,
    Message,
)
from purplship.providers.aramex.utils import Settings
from purplship.providers.aramex.error import parse_error_response


def parse_tracking_response(response, settings: Settings) -> Tuple[List[TrackingDetails], List[Message]]:
    details = response.xpath(".//*[local-name() = $name]", name="TrackingResult")
    tracking_details = [_extract_detail(detail, settings) for detail in details]

    return tracking_details, parse_error_response(response, settings)


def _extract_detail(detail: Element, settings: Settings) -> TrackingDetails:
    result = XP.build(TrackingResult, detail)

    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        tracking_number=result.WaybillNumber,
        events=[
            TrackingEvent(
                date=DF.date(result.UpdateDateTime, '%Y-%m-%dT%H:%M:%S'),
                description=result.UpdateDescription,
                location=result.UpdateLocation,
                code=result.UpdateCode,
                time=DF.ftime(result.UpdateDateTime, '%Y-%m-%dT%H:%M:%S'),
            )
        ],
    )


def tracking_request(payload: TrackingRequest, settings: Settings) -> Serializable[ShipmentTrackingRequest]:
    request = create_envelope(
        body_content=ShipmentTrackingRequest(
            ClientInfo=ClientInfo(
                UserName=settings.username,
                Password=settings.password,
                Version='1.0',
                AccountNumber=settings.account_number,
                AccountPin=settings.account_pin,
                AccountEntity=settings.account_entity,
                AccountCountryCode=settings.account_country_code,
            ),
            Transaction=Transaction(Reference1='Tracking Request'),
            Shipments=ArrayOfstring(
                string=payload.tracking_numbers
            ),
            GetLastTrackingUpdateOnly=False,
        )
    )

    return Serializable(request, _request_serializer)


def _request_serializer(request: ShipmentTrackingRequest) -> str:
    return XP.export(request)
