from typing import List, Tuple, Optional
from pyfedex.track_service_v18 import (
    TrackDetail,
    TrackRequest,
    TransactionDetail,
    Localization,
    VersionId,
    TrackSelectionDetail,
    TrackPackageIdentifier,
)
from purplship.core.utils import export, Serializable, Element, format_date, format_time
from purplship.core.utils.soap import clean_namespaces, create_envelope
from purplship.core.models import (
    TrackingRequest,
    TrackingDetails,
    TrackingEvent,
    Message,
)
from purplship.providers.fedex.error import parse_error_response
from purplship.providers.fedex.utils import Settings


def parse_track_response(
    response: Element, settings: Settings
) -> Tuple[List[TrackingDetails], List[Message]]:
    track_details = response.xpath(".//*[local-name() = $name]", name="TrackDetails")
    tracking_details = [
        _extract_tracking(track_detail_node, settings)
        for track_detail_node in track_details
    ]
    return (
        [details for details in tracking_details if details is not None],
        parse_error_response(response, settings),
    )


def _extract_tracking(
    track_detail_node: Element, settings: Settings
) -> Optional[TrackingDetails]:
    track_detail = TrackDetail()
    track_detail.build(track_detail_node)
    if track_detail.Notification.Severity == "ERROR":
        return None
    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=track_detail.TrackingNumber,
        events=list(
            map(
                lambda e: TrackingEvent(
                    date=format_date(e.Timestamp, "%Y-%m-%d %H:%M:%S%z"),
                    time=format_time(e.Timestamp, "%Y-%m-%d %H:%M:%S%z"),
                    code=e.EventType,
                    location=e.ArrivalLocation,
                    description=e.EventDescription,
                ),
                track_detail.Events,
            )
        ),
    )


def track_request(
    payload: TrackingRequest, settings: Settings
) -> Serializable[TrackRequest]:
    request = TrackRequest(
        WebAuthenticationDetail=settings.webAuthenticationDetail,
        ClientDetail=settings.clientDetail,
        TransactionDetail=TransactionDetail(
            CustomerTransactionId="Track By Number_v14",
            Localization=Localization(LanguageCode=payload.language_code or "en"),
        ),
        Version=VersionId(ServiceId="trck", Major=14, Intermediate=0, Minor=0),
        SelectionDetails=[
            TrackSelectionDetail(
                CarrierCode="FDXE",  # Read doc for carrier code customization
                OperatingCompany=None,
                PackageIdentifier=TrackPackageIdentifier(
                    Type="TRACKING_NUMBER_OR_DOORTAG", Value=tracking_number
                ),
                TrackingNumberUniqueIdentifier=None,
                ShipDateRangeBegin=None,
                ShipDateRangeEnd=None,
                ShipmentAccountNumber=None,
                SecureSpodAccount=None,
                Destination=None,
                PagingDetail=None,
                CustomerSpecifiedTimeOutValueInMilliseconds=None,
            )
            for tracking_number in payload.tracking_numbers
        ],
        TransactionTimeOutValueInMilliseconds=None,
        ProcessingOptions=None,
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: TrackRequest) -> str:
    return clean_namespaces(
        export(
            create_envelope(body_content=request),
            namespacedef_='tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v18="http://fedex.com/ws/track/v18"',
        ),
        envelope_prefix="tns:",
        body_child_prefix="ns:",
        body_child_name="TrackRequest",
    )
