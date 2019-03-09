from pydhl import tracking_request_known as Track, tracking_response as TrackRes
from lxml import etree
from .interface import reduce, Tuple, List, T, DHLMapperBase


class DHLMapperPartial(DHLMapperBase):
    def parse_dhltracking_response(
        self, response
    ) -> Tuple[List[T.TrackingDetails], List[T.Error]]:
        awbinfos = response.xpath(".//*[local-name() = $name]", name="AWBInfo")
        tracking: List[T.TrackingDetails] = reduce(
            self._extract_tracking, awbinfos, []
        )
        return (tracking, self.parse_error_response(response))

    def _extract_tracking(
        self, tracking: List[T.TrackingDetails], awbInfoNode: etree.ElementBase
    ) -> List[T.TrackingDetails]:
        awbInfo = TrackRes.AWBInfo()
        awbInfo.build(awbInfoNode)
        if awbInfo.ShipmentInfo == None:
            return tracking
        return tracking + [
            T.TrackingDetails(
                carrier=self.client.carrier_name,
                tracking_number=awbInfo.AWBNumber,
                shipment_date=str(awbInfo.ShipmentInfo.ShipmentDate),
                events=list(
                    map(
                        lambda e: T.TrackingEvent(
                            date=str(e.Date),
                            time=str(e.Time),
                            signatory=e.Signatory,
                            code=e.ServiceEvent.EventCode,
                            location=e.ServiceArea.Description,
                            description=e.ServiceEvent.Description,
                        ),
                        awbInfo.ShipmentInfo.ShipmentEvent,
                    )
                ),
            )
        ]

    def create_dhltracking_request(
        self, payload: T.TrackingRequest
    ) -> Track.KnownTrackingRequest:
        known_request = Track.KnownTrackingRequest(
            Request=self.init_request(),
            LanguageCode=payload.language_code or "en",
            LevelOfDetails=payload.level_of_details or "ALL_CHECK_POINTS",
        )
        for tn in payload.tracking_numbers:
            known_request.add_AWBNumber(tn)
        return known_request
