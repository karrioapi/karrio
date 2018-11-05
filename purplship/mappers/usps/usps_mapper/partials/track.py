from pyusps.trackrequest import *
from pyusps.trackresponse import *
from .interface import reduce, Tuple, List, E, USPSMapperBase


class USPSMapperPartial(USPSMapperBase):

    def parse_track_response(self, response: 'XMLElement') -> Tuple[List[E.TrackingDetails], List[E.Error]]:
        pass

    def _extract_tracking(self, trackings: List[E.TrackingDetails], track: 'XMLElement') -> List[E.TrackingDetails]:
        pass

    def create_track_request(self, payload: E.tracking_request) -> TrackRequest:
        return TrackRequest(
            USERID=self.client.username,
            TrackID=[
                TrackIDType(
                    ID=tn,
                    valueOf_=None
                ) for tn in payload.tracking_numbers
            ]
        )

        