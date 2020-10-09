from typing import List, Tuple
from pycanpar.CanparAddonsService import (
    trackByBarcodeV2,
    TrackByBarcodeV2Rq
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
    Envelope
)
from purplship.providers.canpar.error import parse_error_response
from purplship.providers.canpar.utils import Settings, default_request_serializer


def parse_track_response(response: Element, settings: Settings) -> Tuple[List[TrackingDetails], List[Message]]:
    details: List[TrackingDetails] = []

    return details, parse_error_response(response, settings)


def _extract_tracking_details(node: Element, settings: Settings) -> TrackingDetails:

    return TrackingDetails()


def track_by_barcode(payload: TrackingRequest, _) -> Serializable[List[Envelope]]:

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
