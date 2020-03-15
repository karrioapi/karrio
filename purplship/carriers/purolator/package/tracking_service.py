from datetime import datetime
from typing import List, Tuple, cast
from pypurolator.tracking_service import (
    TrackPackagesByPinRequest, PIN, ArrayOfPIN, RequestContext, TrackingInformation, Scan, Depot
)
from purplship.core.models import TrackingRequest, TrackingDetails, Error, TrackingEvent
from purplship.core.utils.xml import Element
from purplship.core.utils.helpers import export
from purplship.core.utils.soap import create_envelope
from pysoap.envelope import Envelope
from purplship.core.utils.serializable import Serializable
from purplship.carriers.purolator.utils import Settings
from purplship.carriers.purolator.error import parse_error_response


def parse_track_package_response(response: Element, settings: Settings) -> Tuple[List[TrackingDetails], List[Error]]:
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
                date=str(cast(Scan, scan).ScanDate),
                description=cast(Scan, scan).Description,
                location=cast(Depot, cast(Scan, scan).Depot).Name,
                code=cast(Scan, scan).ScanType,
                time=datetime.utcfromtimestamp(int(cast(Scan, scan).ScanTime)).strftime('%H:%M'),
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
    return Serializable(request, _request_serializer)


def _request_serializer(envelope: Envelope) -> str:
    namespacedef_ = 'xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://purolator.com/pws/datatypes/v1"'
    envelope.ns_prefix_ = "SOAP-ENV"
    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    envelope.Header.ns_prefix_ = envelope.ns_prefix_
    envelope.Body.anytypeobjs_[0].ns_prefix_ = "ns1"
    envelope.Header.anytypeobjs_[0].ns_prefix_ = "ns1"
    return export(envelope, namespacedef_=namespacedef_)
