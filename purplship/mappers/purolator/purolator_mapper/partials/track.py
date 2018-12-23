from pypurolator.TrackingService import TrackPackagesByPinRequestContainer
from .interface import reduce, Tuple, List, T, PurolatorMapperBase


class PurolatorMapperPartial(PurolatorMapperBase):

    def parse_package_tracking_response(self, response: 'XMLElement') -> Tuple[List[T.TrackingDetails], List[T.Error]]:
        pass

    def _extract_tracking(self, trackings: List[T.TrackingDetails], track: 'XMLElement') -> List[T.TrackingDetails]:
        pass

    def create_package_tracking_request(self, payload: T.tracking_request) -> TrackPackagesByPinRequestContainer:
        return TrackPackagesByPinRequestContainer(
            PINs=payload.tracking_numbers
        )

    