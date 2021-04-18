from typing import List, Tuple, cast
from tnt_lib.track_response_v3_1 import ConsignmentType, StatusStructure
from tnt_lib.track_request_v3_1 import (
    TrackRequest,
    SearchCriteriaType,
    LevelOfDetailType,
    CompleteType,
)
from purplship.core.utils import (
    Element,
    Serializable,
    XP,
    SF,
    DF
)
from purplship.core.models import (
    TrackingEvent,
    TrackingDetails,
    TrackingRequest,
    Message,
)
from purplship.providers.tnt.utils import Settings
from purplship.providers.tnt.error import parse_error_response


def parse_tracking_response(response, settings: Settings) -> Tuple[List[TrackingDetails], List[Message]]:
    details = response.xpath(".//*[local-name() = $name]", name="Consignment")
    tracking_details = [_extract_detail(node, settings) for node in details]

    return tracking_details, parse_error_response(response, settings)


def _extract_detail(node: Element, settings: Settings) -> TrackingDetails:
    detail = XP.build(ConsignmentType, node)

    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        tracking_number=detail.ConsignmentNumber,
        events=[
            TrackingEvent(
                date=DF.fdate(status.LocalEventDate.valueOf_, '%Y%m%d'),
                description=status.StatusDescription,
                location=SF.concat_str(status.Depot, status.DepotName, join=True, separator='-'),
                code=status.StatusCode,
                time=DF.ftime(status.LocalEventTime.valueOf_, '%H%M')
            )
            for status in cast(List[StatusStructure], detail.StatusData)
        ],
        delivered=(detail.SummaryCode == "DEL")
    )


def tracking_request(payload: TrackingRequest, _) -> Serializable[TrackRequest]:
    request = TrackRequest(
        locale="en_US",
        version="3.1",
        SearchCriteria=SearchCriteriaType(ConsignmentNumber=payload.tracking_numbers),
        LevelOfDetail=LevelOfDetailType(
            Complete=CompleteType(
                originAddress=True,
                destinationAddress=True,
            )
        )
    )

    return Serializable(request, XP.export)
