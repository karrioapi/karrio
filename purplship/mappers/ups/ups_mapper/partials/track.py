from pyups import (
    package_track as Track,
    common as Common
)
from .interface import reduce, Tuple, List, E, UPSMapperBase


class UPSMapperPartial(UPSMapperBase):

    def parse_track_response(self, response: 'XMLElement') -> Tuple[List[E.QuoteDetails], List[E.Error]]:
        track_details = response.xpath('.//*[local-name() = $name]', name="Shipment")
        trackings = reduce(self._extract_tracking, track_details, [])
        return (trackings, self.parse_error_response(response))

    def _extract_tracking(self, trackings: List[E.TrackingDetails], shipmentNode: 'XMLElement') -> List[E.TrackingDetails]:
        trackDetail = Track.ShipmentType()
        trackDetail.build(shipmentNode)
        activityNodes = shipmentNode.xpath('.//*[local-name() = $name]', name="Activity")
        def buildActivity(node): 
            activity = Track.ActivityType()
            activity.build(node)
            return activity 
        activities = map(buildActivity, activityNodes)
        return trackings + [
            E.TrackingDetails(
                carrier=self.client.carrier_name,
                tracking_number=trackDetail.InquiryNumber.Value,
                events=list(map(lambda a: E.TrackingEvent(
                    date=str(a.Date),
                    time=str(a.Time),
                    code=a.Status.Code if a.Status else None,
                    location=a.ActivityLocation.Address.City if a.ActivityLocation and a.ActivityLocation.Address else None,
                    description=a.Status.Description if a.Status else None
                ), activities))
            )
        ]

    def create_track_request(self, payload: E.shipment_request) -> List[Track.TrackRequest]:    
        Request_ = Common.RequestType(
            TransactionReference=Common.TransactionReferenceType(
                TransactionIdentifier="TransactionIdentifier"
            )
        )

        Request_.add_RequestOption(1)

        TrackRequests_ = [Track.TrackRequest(
            Request=Request_,
            InquiryNumber=number
        ) for number in payload.tracking_numbers]

        return TrackRequests_

