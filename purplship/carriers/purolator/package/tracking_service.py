from typing import List, Tuple, cast
from pypurolator.tracking_service import (
    TrackPackagesByPinRequest, PIN, ArrayOfPIN, RequestContext, TrackingInformation, Scan, Depot
)
from purplship.core.models import TrackingRequest, TrackingDetails, Message, TrackingEvent
from purplship.core.utils import Element, format_date, format_timestamp
from purplship.core.utils.soap import create_envelope
from pysoap.envelope import Envelope
from purplship.core.utils.serializable import Serializable
from purplship.carriers.purolator.utils import Settings, standard_request_serializer
from purplship.carriers.purolator.error import parse_error_response


def parse_track_package_response(response: Element, settings: Settings) -> Tuple[List[TrackingDetails], List[Message]]:
    track_infos = response.xpath(".//*[local-name() = $name]", name="TrackingInformation")
    return (
        [_extract_tracking(node, settings) for node in track_infos],
        parse_error_response(response, settings)
    )


def _extract_tracking(node: Element, settings: Settings) -> TrackingDetails:
    track = TrackingInformation()
    track.build(node)
    return TrackingDetails(
        carrier=settings.carrier_name,
        tracking_number=str(track.PIN.Value),
        events=[
            TrackingEvent(
                date=format_date(cast(Scan, scan).ScanDate),
                time=format_timestamp(cast(Scan, scan).ScanTime),
                description=cast(Scan, scan).Description,
                location=cast(Depot, cast(Scan, scan).Depot).Name,
                code=cast(Scan, scan).ScanType,
            ) for scan in track.Scans.Scan
        ]
    )


def track_package_by_pin_request(payload: TrackingRequest, settings: Settings) -> Serializable[Envelope]:
    request = create_envelope(
        header_content=RequestContext(
            Version='1.1',
            Language=settings.language,
            GroupID=None,
            RequestReference=None,
            UserToken=settings.user_token
        ),
        body_content=TrackPackagesByPinRequest(
            PINs=ArrayOfPIN(
                PIN=[
                    PIN(Value=pin) for pin in payload.tracking_numbers
                ]
            )
        )
    )
    return Serializable(request, standard_request_serializer)
