from pyfedex.track_service_v14 import *
from .interface import reduce, Tuple, List, E, FedexMapperBase


class FedexMapperPartial(FedexMapperBase):

    def parse_track_reply(self, response: 'XMLElement') -> Tuple[List[E.TrackingDetails], List[E.Error]]:
        track_details = response.xpath('.//*[local-name() = $name]', name="TrackDetails")
        trackings = reduce(self._extract_tracking, track_details, [])
        return (trackings, self.parse_error_response(response))

    def _extract_tracking(self, trackings: List[E.TrackingDetails], trackDetailNode: 'XMLElement') -> List[E.TrackingDetails]:
        trackDetail = TrackDetail()
        trackDetail.build(trackDetailNode)
        if trackDetail.Notification.Severity == 'ERROR':
            return trackings
        return trackings + [
            E.TrackingDetails(
                carrier=self.client.carrier_name,
                tracking_number=trackDetail.TrackingNumber,
                shipment_date=str(trackDetail.StatusDetail.CreationTime),
                events=list(map(lambda e: E.TrackingEvent(
                    date=str(e.Timestamp),
                    code=e.EventType,
                    location=e.ArrivalLocation,
                    description=e.EventDescription
                ), trackDetail.Events))
            )
        ]

    def create_track_request(self, payload: E.tracking_request) -> TrackRequest:
        return TrackRequest(
            WebAuthenticationDetail=self.webAuthenticationDetail,
            ClientDetail=self.clientDetail,
            TransactionDetail=TransactionDetail(
                CustomerTransactionId=payload.extra.get('CustomerTransactionId') or "Track By Number_v14",
                Localization=Localization(LanguageCode=payload.language_code or "en")
            ),
            Version=VersionId(ServiceId="trck", Major=14, Intermediate=0, Minor=0),
            SelectionDetails=[TrackSelectionDetail(
                CarrierCode="FDXE",
                OperatingCompany=None,
                PackageIdentifier=TrackPackageIdentifier(
                    Type="TRACKING_NUMBER_OR_DOORTAG",
                    Value=tracking_number
                ),
                TrackingNumberUniqueIdentifier=None,
                ShipDateRangeBegin=None,
                ShipDateRangeEnd=None,
                ShipmentAccountNumber=None,
                SecureSpodAccount=None,
                Destination=None,
                PagingDetail=None,
                CustomerSpecifiedTimeOutValueInMilliseconds=None
            ) for tracking_number in payload.tracking_numbers],
            TransactionTimeOutValueInMilliseconds=None,
            ProcessingOptions=None
        )

        