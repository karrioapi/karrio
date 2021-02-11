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
    Envelope,
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
    tracking_details = [_extract_detail(node, settings) for node in details]

    return tracking_details, parse_error_response(response, settings)


def _extract_detail(node: Element, settings: Settings) -> TrackingDetails:
    detail = XP.build(TrackingResult, node)

    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        tracking_number=detail.WaybillNumber,
        events=[
            TrackingEvent(
                date=DF.date(detail.UpdateDateTime, '%Y-%m-%dT%H:%M:%S'),
                description=detail.UpdateDescription,
                location=detail.UpdateLocation,
                code=detail.UpdateCode,
                time=DF.ftime(detail.UpdateDateTime, '%Y-%m-%dT%H:%M:%S'),
            )
        ],
    )


def tracking_request(payload: TrackingRequest, settings: Settings) -> Serializable[Envelope]:
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

    return Serializable(request, settings.standard_request_serializer)
