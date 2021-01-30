from typing import List, Tuple, cast
from canpar_lib.CanparAddonsService import (
    trackByBarcodeV2,
    TrackByBarcodeV2Rq,
    TrackingResult,
    TrackingEvent as CanparTrackingEvent,
    Address
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
)
from purplship.providers.canpar.error import parse_error_response
from purplship.providers.canpar.utils import Settings, default_request_serializer


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
            location=_format_location(event.address),
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


def _format_location(address: Address) -> str:
    details = [
        address.address_line_1,
        address.address_line_2,
        address.city,
        address.province,
        address.country
    ]
    return ", ".join([detail for detail in details if detail is not None and detail != ""])


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
        default_request_serializer(envelope) for envelope in envelopes
    ]
