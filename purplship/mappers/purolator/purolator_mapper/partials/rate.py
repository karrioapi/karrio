from pypurolator import (
    EstimatorService as Estimator,
    FreightEstimatingService as FEstimator
)
from .interface import reduce, Tuple, List, T, PurolatorMapperBase


class PurolatorMapperPartial(PurolatorMapperBase):
    
    def parse_estimate_response(self, response: 'XMLElement') -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        pass

    def _extract_quote(self, quotes: List[T.QuoteDetails], price_quoteNode: 'XMLElement') -> List[T.QuoteDetails]: 
        pass


    def create_estimate_request(self, payload: T.shipment_request) -> Estimator.GetFullEstimateRequestContainer:
        return Estimator.GetFullEstimateRequestContainer(
            Shipment=Estimator.Shipment(
                SenderInformation=None,
                ReceiverInformation=None,
                FromOnLabelIndicator=None,
                FromOnLabelInformation=None,
                ShipmentDate=None,
                PackageInformation=None,
                InternationalInformation=None,
                ReturnShipmentInformation=None,
                PaymentInformation=None,
                PickupInformation=None,
                NotificationInformation=None,
                TrackingReferenceInformation=None,
                OtherInformation=None,
                ProactiveNotification=None
            ),
            ShowAlternativeServicesIndicator=None
        )

    def create_freight_estimate_request(self, payload: T.shipment_request) -> FEstimator.GetEstimateRequestContainer:
        return FEstimator.GetEstimateRequestContainer(
            Estimate=FEstimator.Shipment(
                SenderInformation=FEstimator.SenderInformation(
                    Address=FEstimator.Address(
                        Name=payload.shipper.person_name,
                        Company=payload.shipper.company_name,
                        Department=None,
                        StreetNumber=None,
                        StreetSuffix=None,
                        StreetName=None,
                        StreetType=None,
                        StreetDirection=None,
                        Suite=None,
                        Floor=None,
                        StreetAddress2=None,
                        StreetAddress3=None,
                        City=None,
                        Province=None,
                        Country=None,
                        PostalCode=None,
                        PhoneNumber=None,
                        FaxNumber=None
                    ),
                    EmailAddress=payload.shipper.email_address
                ),
                ReceiverInformation=FEstimator.ReceiverInformation(
                    Address=None,
                    EmailAddress=None
                ),
                PaymentInformation=None,
                ShipmentDetails=None
            )
        )