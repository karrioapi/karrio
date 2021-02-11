from typing import List, Tuple
from functools import partial
from aramex_lib.array_of_string import ArrayOfstring
from aramex_lib.tracking import (
    ShipmentTrackingRequest,
    ClientInfo,
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
    non_existents = next(
        (XP.build(ArrayOfstring, n) for n in response.xpath(".//*[local-name() = $name]", name="NonExistingWaybills")),
        ArrayOfstring()
    )
    results = response.xpath(".//*[local-name() = $name]", name="TrackingResult")
    tracking_details = [_extract_detail(node, settings) for node in results]
    errors = _extract_errors(non_existents, settings) + parse_error_response(response, settings)

    return tracking_details, errors


def _extract_errors(non_existents: ArrayOfstring, settings: Settings) -> List[Message]:
    return [
        Message(
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,

            message=f'Waybill "{waybill}" Not Found'
        )
        for waybill in non_existents.string
    ]


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
            Transaction=None,
            Shipments=ArrayOfstring(
                string=payload.tracking_numbers
            ),
            GetLastTrackingUpdateOnly=False,
        )
    )

    return Serializable(
        request, partial(
            settings.standard_request_serializer,
            extra_namespace='xmlns:arr="http://schemas.microsoft.com/2003/10/Serialization/Arrays',
            special_prefixes=dict(string='arr')
        )
    )
