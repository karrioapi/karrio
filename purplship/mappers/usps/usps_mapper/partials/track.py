from pyusps.TrackRequest import *
from pyusps.TrackResponse import *
from .interface import reduce, Tuple, List, T, USPSMapperBase


class USPSMapperPartial(USPSMapperBase):

    def parse_track_response(self, response: 'XMLElement') -> Tuple[List[T.TrackingDetails], List[T.Error]]:
        pass

    def _extract_tracking(self, trackings: List[T.TrackingDetails], track: 'XMLElement') -> List[T.TrackingDetails]:
        pass

    def create_track_request(self, payload: T.tracking_request) -> TrackRequest:
        return TrackRequest(
            USERID=self.client.username,
            TrackID=[
                TrackIDType(
                    ID=tn,
                    valueOf_=None
                ) for tn in payload.tracking_numbers
            ]
        )

        