from pycaps.track import pin_summary
from lxml import etree
from .interface import reduce, Tuple, List, T, CanadaPostMapperBase


class CanadaPostMapperPartial(CanadaPostMapperBase):
    def parse_tracking_summary(
        self, response: etree.ElementBase
    ) -> Tuple[List[T.TrackingDetails], List[T.Error]]:
        pin_summaries = response.xpath(".//*[local-name() = $name]", name="pin-summary")
        trackings: List[T.TrackingDetails] = reduce(
            self._extract_tracking, pin_summaries, []
        )
        return (trackings, self.parse_error_response(response))

    def _extract_tracking(
        self, trackings: List[T.TrackingDetails], pin_summaryNode: etree.ElementBase
    ) -> List[T.TrackingDetails]:
        pin_summary_ = pin_summary()
        pin_summary_.build(pin_summaryNode)
        return trackings + [
            T.TrackingDetails(
                carrier=self.client.carrier_name,
                tracking_number=pin_summary_.pin,
                shipment_date=str(pin_summary_.mailed_on_date),
                events=[
                    T.TrackingEvent(
                        date=str(pin_summary_.event_date_time),
                        signatory=pin_summary_.signatory_name,
                        code=pin_summary_.event_type,
                        location=pin_summary_.event_location,
                        description=pin_summary_.event_description,
                    )
                ],
            )
        ]

    def create_tracking_pins(self, payload: T.TrackingRequest) -> List[str]:
        return payload.tracking_numbers
