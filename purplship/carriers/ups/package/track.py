from typing import List, Tuple
from pyups.common import RequestType, TransactionReferenceType
from pyups.track_web_service_schema import TrackRequest, ShipmentType, ActivityType
from purplship.core.utils import export, Serializable, Element, format_date, format_time
from purplship.core.utils.soap import apply_namespaceprefix, create_envelope, Envelope
from purplship.core.models import (
    TrackingEvent,
    TrackingRequest,
    TrackingDetails,
    Message,
)
from purplship.carriers.ups.error import parse_error_response
from purplship.carriers.ups.utils import Settings


def parse_track_response(
    response: Element, settings: Settings
) -> Tuple[List[TrackingDetails], List[Message]]:
    track_details = response.xpath(".//*[local-name() = $name]", name="Shipment")
    tracking: List[TrackingDetails] = [
        _extract_tracking(node, settings) for node in track_details
    ]
    return tracking, parse_error_response(response, settings)


def _extract_tracking(shipment_node: Element, settings: Settings) -> TrackingDetails:
    track_detail = ShipmentType()
    track_detail.build(shipment_node)
    activity_nodes = shipment_node.xpath(".//*[local-name() = $name]", name="Activity")

    def build_activity(node) -> ActivityType:
        activity = ActivityType()
        activity.build(node)
        return activity

    activities: List[ActivityType] = list(map(build_activity, activity_nodes))
    return TrackingDetails(
        carrier=settings.carrier,
        carrier_name=settings.carrier_name,
        tracking_number=track_detail.InquiryNumber.Value,
        events=list(
            map(
                lambda a: TrackingEvent(
                    date=format_date(a.Date, "%Y%m%d"),
                    time=format_time(a.Time, "%H%M%S"),
                    code=a.Status.Code if a.Status else None,
                    location=(
                        a.ActivityLocation.Address.City
                        if a.ActivityLocation and a.ActivityLocation.Address
                        else None
                    ),
                    description=a.Status.Description if a.Status else None,
                ),
                activities,
            )
        ),
    )


def track_request(
    payload: TrackingRequest, settings: Settings
) -> Serializable[List[Envelope]]:
    requests = [
        create_envelope(
            header_content=settings.Security,
            body_content=TrackRequest(
                Request=RequestType(
                    RequestOption=[1],
                    TransactionReference=TransactionReferenceType(
                        TransactionIdentifier="TransactionIdentifier"
                    ),
                ),
                InquiryNumber=number,
            ),
        )
        for number in payload.tracking_numbers
    ]
    return Serializable(requests, _request_serializer)


def _request_serializer(requests: List[Envelope]) -> List[str]:
    namespacedef_ = """
        xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0"
        xmlns:trk="http://www.ups.com/XMLSchema/XOLTWS/Track/v2.0"
        xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0"
    """.replace(
        " ", ""
    ).replace(
        "\n", " "
    )

    def serialize(envelope: Envelope):
        envelope.Body.ns_prefix_ = envelope.ns_prefix_
        envelope.Header.ns_prefix_ = envelope.ns_prefix_
        apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "trk")
        apply_namespaceprefix(envelope.Header.anytypeobjs_[0], "upss")
        apply_namespaceprefix(envelope.Body.anytypeobjs_[0].Request, "common")

        return export(envelope, namespacedef_=namespacedef_)

    return [serialize(request) for request in requests]
