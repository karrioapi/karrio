from typing import List, Tuple, cast
from canpar_lib.CanparAddonsService import (
    trackByBarcodeV2,
    TrackByBarcodeV2Rq,
    TrackingResult,
    TrackingEvent as CanparTrackingEvent
)
from purplship.core.models import (
    Message,
    TrackingRequest,
    TrackingDetails,
    TrackingEvent,
)
from purplship.core.utils import (
    Serializable,
    Element,
    create_envelope,
    Envelope,
    DF,
    XP,
    SF,
)
from purplship.providers.canpar.error import parse_error_response
from purplship.providers.canpar.utils import Settings


def parse_tracking_response(response: Element, settings: Settings) -> Tuple[List[TrackingDetails], List[Message]]:
    results = response.xpath(".//*[local-name() = $name]", name="result")
    details: List[TrackingDetails] = [
        _extract_tracking_details(result, settings) for result in results
    ]

    return details, parse_error_response(response, settings)


def _extract_tracking_details(node: Element, settings: Settings) -> TrackingDetails:
    result = XP.build(TrackingResult, node)
    is_en = settings.language == "en"
    events = [
        TrackingEvent(
            date=DF.fdate(event.local_date_time, '%Y%m%d %H%M%S'),
            description=(event.code_description_en if is_en else event.code_description_fr),
            location=SF.concat_str(
                event.address.address_line_1,
                event.address.address_line_2,
                event.address.city,
                event.address.province,
                event.address.country,
                join=True, separator=", "
            ),
            code=event.code,
            time=DF.ftime(event.local_date_time, '%Y%m%d %H%M%S'),
        ) for event in cast(List[CanparTrackingEvent], result.events)
    ]

    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=result.barcode,
        events=events,
        delivered=any(event.code == 'DEL' for event in events)
    )


def tracking_request(payload: TrackingRequest, _) -> Serializable[List[Envelope]]:

    request = [
        create_envelope(
            body_content=trackByBarcodeV2(
                request=TrackByBarcodeV2Rq(
                    barcode=barcode,
                    filter=None,
                    track_shipment=True
                )
            )
        ) for barcode in payload.tracking_numbers
    ]

    return Serializable(request, _request_serializer)


def _request_serializer(envelopes: List[Envelope]) -> List[str]:
    return [
        Settings.serialize(envelope) for envelope in envelopes
    ]
