from typing import List, Tuple, cast
from pypurolator.tracking_service_1_2_2 import (
    TrackPackagesByPinRequest,
    PIN,
    ArrayOfPIN,
    RequestContext,
    TrackingInformation,
    Scan,
    Depot,
)
from purplship.core.models import (
    TrackingRequest,
    TrackingDetails,
    Message,
    TrackingEvent,
)
from purplship.core.utils import Element, format_date, format_timestamp, export
from purplship.core.utils.soap import create_envelope, apply_namespaceprefix
from pysoap.envelope import Envelope
from purplship.core.utils.serializable import Serializable
from purplship.providers.purolator.utils import Settings
from purplship.providers.purolator.error import parse_error_response


def parse_track_package_response(
    response: Element, settings: Settings
) -> Tuple[List[TrackingDetails], List[Message]]:
    track_infos = response.xpath(
        ".//*[local-name() = $name]", name="TrackingInformation"
    )
    return (
        [_extract_tracking(node, settings) for node in track_infos],
        parse_error_response(response, settings),
    )


def _extract_tracking(node: Element, settings: Settings) -> TrackingDetails:
    track = TrackingInformation()
    track.build(node)
    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=str(track.PIN.Value),
        events=[
            TrackingEvent(
                date=format_date(cast(Scan, scan).ScanDate),
                time=format_timestamp(cast(Scan, scan).ScanTime),
                description=cast(Scan, scan).Description,
                location=cast(Depot, cast(Scan, scan).Depot).Name,
                code=cast(Scan, scan).ScanType,
            )
            for scan in track.Scans.Scan
        ],
    )


def track_package_by_pin_request(
    payload: TrackingRequest, settings: Settings
) -> Serializable[Envelope]:
    request = create_envelope(
        header_content=RequestContext(
            Version="1.2",
            Language=settings.language,
            GroupID="",
            RequestReference="",
            UserToken=settings.user_token,
        ),
        body_content=TrackPackagesByPinRequest(
            PINs=ArrayOfPIN(PIN=[PIN(Value=pin) for pin in payload.tracking_numbers])
        ),
    )
    return Serializable(request, _request_serializer)


def _request_serializer(envelope: Envelope) -> str:
    namespacedef_ = 'xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v1="http://purolator.com/pws/datatypes/v1"'
    envelope.ns_prefix_ = "soap"
    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    envelope.Header.ns_prefix_ = envelope.ns_prefix_
    apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "v1")
    apply_namespaceprefix(envelope.Header.anytypeobjs_[0], "v1")
    return export(envelope, namespacedef_=namespacedef_)
