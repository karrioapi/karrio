from typing import List, Tuple, Optional
from fedex_lib.track_service_v19 import (
    TrackDetail,
    TrackRequest,
    TransactionDetail,
    Localization,
    VersionId,
    TrackSelectionDetail,
    TrackPackageIdentifier,
    TrackingDateOrTimestamp,
)
from karrio.core.utils import Serializable, Element, XP, DF
from karrio.core.utils.soap import create_envelope, apply_namespaceprefix
from karrio.core.models import (
    TrackingRequest,
    TrackingDetails,
    TrackingEvent,
    Message,
)
from karrio.providers.fedex.error import parse_error_response
from karrio.providers.fedex.utils import Settings

estimated_date_formats = [
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%dT%H:%M:%S",
]


def parse_tracking_response(
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
    detail_node: Element, settings: Settings
) -> Optional[TrackingDetails]:
    track_detail = TrackDetail()
    track_detail.build(detail_node)
    if track_detail.Notification.Severity == "ERROR":
        return None

    date_or_timestamps = XP.find("DatesOrTimes", detail_node, TrackingDateOrTimestamp)
    estimated_delivery = (
        _parse_date_or_timestamp(date_or_timestamps, "ACTUAL_DELIVERY")
        or _parse_date_or_timestamp(date_or_timestamps, "ACTUAL_TENDER")
        or _parse_date_or_timestamp(date_or_timestamps, "ANTICIPATED_TENDER")
        or _parse_date_or_timestamp(date_or_timestamps, "ESTIMATED_DELIVERY")
    )

    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=track_detail.TrackingNumber,
        events=[
            TrackingEvent(
                date=DF.fdate(e.Timestamp, "%Y-%m-%d %H:%M:%S%z"),
                time=DF.ftime(e.Timestamp, "%Y-%m-%d %H:%M:%S%z"),
                code=e.EventType,
                location=e.ArrivalLocation,
                description=e.EventDescription,
            )
            for e in track_detail.Events
        ],
        estimated_delivery=estimated_delivery,
        delivered=any(e.EventType == "DL" for e in track_detail.Events),
    )


def _parse_date_or_timestamp(
    date_or_timestamps: List[TrackingDateOrTimestamp], type: str
) -> Optional[str]:
    return next(
        iter(
            [
                DF.fdate(d.DateOrTimestamp, try_formats=estimated_date_formats)
                for d in date_or_timestamps
                if d.Type == type
            ]
        ),
        None,
    )


def tracking_request(
    payload: TrackingRequest, settings: Settings
) -> Serializable[TrackRequest]:
    request = TrackRequest(
        WebAuthenticationDetail=settings.webAuthenticationDetail,
        ClientDetail=settings.clientDetail,
        TransactionDetail=TransactionDetail(
            CustomerTransactionId="Track By Number_v18",
            Localization=Localization(LanguageCode=payload.language_code or "en"),
        ),
        Version=VersionId(ServiceId="trck", Major=18, Intermediate=0, Minor=0),
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
        ProcessingOptions=["INCLUDE_DETAILED_SCANS"],
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: TrackRequest) -> str:
    namespacedef_ = 'xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v18="http://fedex.com/ws/track/v18"'

    envelope = create_envelope(body_content=request)
    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "v18")

    return XP.export(envelope, namespacedef_=namespacedef_)
