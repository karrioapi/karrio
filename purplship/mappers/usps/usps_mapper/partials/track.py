from lxml import etree
from typing import Tuple, List
from .interface import USPSMapperBase
from pyusps.trackfieldrequest import (
    TrackFieldRequest,
    TrackIDType
)
from pyusps.trackresponse import TrackInfoType, TrackDetailType
from purplship.domain.Types import (
    TrackingRequest,
    Error,
    TrackingDetails,
    TrackingEvent
)


class USPSMapperPartial(USPSMapperBase):

    def parse_track_response(self, response: etree.ElementBase) -> Tuple[List[TrackingDetails], List[Error]]:
        return (
            [
                self._extract_tracking(node) for node
                in response.xpath(".//*[local-name() = $name]", name="TrackInfo")
            ],
            self.parse_error_response(response)
        )

    def _extract_tracking(self, tracking_node: etree.ElementBase) -> TrackingDetails:
        tracking: TrackInfoType = TrackInfoType()
        tracking.build(tracking_node)
        events: List[TrackDetailType] = tracking.TrackDetail
        return TrackingDetails(
            carrier=self.client.carrier_name,
            tracking_number=tracking.ID,
            shipment_date=None,
            events=[
                TrackingEvent(
                    code=event.EventCode,
                    date=event.EventDate,
                    description=event.ActionCode,
                    location=", ".join([
                        location for location
                        in [event.EventCity, event.EventState, event.EventCountry, event.EventZIPCode]
                        if location is not None
                    ]),
                    time=event.EventTime,
                    signatory=None
                ) for event in events
            ]
        )

    def create_track_request(self, payload: TrackingRequest) -> TrackFieldRequest:
        return TrackFieldRequest(
            USERID=self.client.username,
            Revision="1",
            ClientIp=None,
            SourceID=None,
            TrackID=[
                TrackIDType(
                    ID=tn,
                    DestinationZipCode=None,
                    MailingDate=None
                ) for tn in payload.tracking_numbers
            ]
        )
