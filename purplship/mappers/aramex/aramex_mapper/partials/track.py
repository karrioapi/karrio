from pyaramex.Tracking import (
    ShipmentTrackingRequest
)
from .interface import reduce, Tuple, List, T, AramexMapperBase


class AramexMapperPartial(AramexMapperBase):

    def parse_shipement_tracking_response(self, response: 'XMLElement') -> Tuple[List[T.TrackingDetails], List[T.Error]]:
        pass

    def _extract_tracking(self, trackings: List[T.TrackingDetails], track: 'XMLElement') -> List[T.TrackingDetails]:
        pass

    def create_shipment_tracking_request(self, payload: T.tracking_request) -> ShipmentTrackingRequest:
        return ShipmentTrackingRequest(
            ClientInfo=self.client_info,
            Transaction=None,
            Shipments=payload.tracking_numbers,
            GetLastTrackingUpdateOnly=None
        )

        