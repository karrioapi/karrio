from typing import List, Tuple, cast
from pypurolator.tracking_service import (
    TrackPackagesByPinRequestContainer, PIN, ArrayOfPIN, RequestContext, TrackingInformation, Scan, Depot
)
from purplship.core.models import TrackingRequest, TrackingDetails, Error, TrackingEvent
from purplship.core.utils.xml import Element
from purplship.core.utils.helpers import export
from pysoap.envelope import Envelope, Header, Body
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
                time=cast(Scan, scan).ScanTime,
            ) for scan in track.Scans
        ]
    )


def track_package_by_pin_request(payload: TrackingRequest, settings: Settings) -> Serializable[TrackPackagesByPinRequestContainer]:
    request = Envelope(
        Header=Header(
            RequestContext(
                Version='1.1',
                Language=settings.language,
                GroupID=None,
                RequestReference=None,
                UserToken=settings.user_token
            )
        ),
        Body=Body(
            TrackPackagesByPinRequestContainer(
                PINs=ArrayOfPIN(
                    PIN=[
                        PIN(Value=pin) for pin in payload.tracking_numbers
                    ]
                )
            )
        )
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: Element) -> str:
    namespace_ = 'xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://purolator.com/pws/datatypes/v1"'
    return export(request, namespace_=namespace_)
