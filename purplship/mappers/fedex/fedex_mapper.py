import time
from datetime import datetime
from typing import List, Tuple
from functools import reduce
from pyfedex import rate_v22 as Rate, track_service_v14 as Track, ship_service_v21 as Ship
from purplship.mappers.fedex import FedexClient, factory
from purplship.domain.mapper import Mapper
from purplship.domain import entities as E
from pyfedex.rate_v22 import WebAuthenticationCredential, WebAuthenticationDetail, ClientDetail
from base64 import b64encode

class FedexMapper(Mapper):
    def __init__(self, client: FedexClient):
        self.client = client

        userCredential = WebAuthenticationCredential(Key=client.user_key, Password=client.password)
        self.webAuthenticationDetail = WebAuthenticationDetail(UserCredential=userCredential)
        self.clientDetail = ClientDetail(AccountNumber=client.account_number, MeterNumber=client.meter_number)

    """ 
        Mapper interface methods implementation
    """


    """ Request creators """

    def create_quote_request(self, payload: E.quote_request) -> Rate.RateRequest:
        return factory.create_rate_request(self, payload)


    def create_tracking_request(self, payload: E.tracking_request) -> Track.TrackRequest:    
        return factory.create_track_request(self, payload)


    def create_shipment_request(self, payload: E.shipment_request) -> Ship.ProcessShipmentRequest:
        return factory.create_shipment_request(self, payload)


    """ Response parsers """

    def parse_error_response(self, response: 'XMLElement') -> List[E.Error]:
        notifications = response.xpath(
            './/*[local-name() = $name]', name="Notifications"
        ) + response.xpath(
            './/*[local-name() = $name]', name="Notification"
        )
        return reduce(self._extract_error, notifications, [])


    def parse_quote_response(self, response: 'XMLElement') -> Tuple[List[E.QuoteDetails], List[E.Error]]:
        rate_replys = response.xpath('.//*[local-name() = $name]', name="RateReplyDetails")
        quotes = reduce(self._extract_quote, rate_replys, [])
        return (quotes, self.parse_error_response(response))


    def parse_tracking_response(self, response: 'XMLElement') -> Tuple[List[E.TrackingDetails], List[E.Error]]:
        track_details = response.xpath('.//*[local-name() = $name]', name="TrackDetails")
        trackings = reduce(self._extract_tracking, track_details, [])
        return (trackings, self.parse_error_response(response))


    def parse_shipment_response(self, response: 'XMLElement') -> Tuple[E.ShipmentDetails, List[E.Error]]:
        details = response.xpath('.//*[local-name() = $name]', name="CompletedShipmentDetail")
        shipment = self._extract_shipment(details[0]) if len(details) > 0 else None
        return (shipment, self.parse_error_response(response))



    """ Internal private methods """

    def _extract_error(self, errors: List[E.Error], notificationNode: 'XMLElement') -> List[E.Error]:
        notification = Rate.Notification()
        notification.build(notificationNode)
        if notification.Severity in ('SUCCESS', 'NOTE'):
            return errors
        return errors + [
            E.Error(code=notification.Code, message=notification.Message, carrier=self.client.carrier_name)
        ]


    def _extract_quote(self, quotes: List[E.QuoteDetails], detailNode: 'XMLElement') -> List[E.QuoteDetails]: 
        detail = Rate.RateReplyDetail()
        detail.build(detailNode)
        if not detail.RatedShipmentDetails:
            return quotes
        shipmentDetail = detail.RatedShipmentDetails[0].ShipmentRateDetail
        Discounts_ = map(lambda d: E.ChargeDetails(name=d.RateDiscountType, amount=float(d.Amount.Amount)), shipmentDetail.FreightDiscounts)
        Surcharges_ = map(lambda s: E.ChargeDetails(name=s.SurchargeType, amount=float(s.Amount.Amount)), shipmentDetail.Surcharges)
        Taxes_ = map(lambda t: E.ChargeDetails(name=t.TaxType, amount=float(t.Amount.Amount)), shipmentDetail.Taxes)
        return quotes + [
            E.QuoteDetails(
                carrier=self.client.carrier_name,
                service_name=detail.ServiceType,
                service_type=detail.ActualRateType,
                currency=shipmentDetail.CurrencyExchangeRate.IntoCurrency if shipmentDetail.CurrencyExchangeRate else None,
                base_charge=float(shipmentDetail.TotalBaseCharge.Amount),
                total_charge=float(shipmentDetail.TotalNetChargeWithDutiesAndTaxes.Amount),
                duties_and_taxes=float(shipmentDetail.TotalTaxes.Amount),
                discount=float(shipmentDetail.TotalFreightDiscounts.Amount),
                extra_charges=list(Discounts_) + list(Surcharges_) + list(Taxes_)
            )
        ]


    def _extract_tracking(self, trackings: List[E.TrackingDetails], trackDetailNode: 'XMLElement') -> List[E.TrackingDetails]:
        trackDetail = Track.TrackDetail()
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


    def _extract_shipment(self, shipmentDetailNode: 'XMLElement') -> E.ShipmentDetails:
        detail = Ship.CompletedShipmentDetail()
        detail.build(shipmentDetailNode)

        def get_rateDetail() -> Ship.ShipmentRateDetail:
            return detail.ShipmentRating.ShipmentRateDetails[0]

        def get_packages() -> List[Ship.CompletedPackageDetail]:
            return detail.CompletedPackageDetails

        shipment = get_rateDetail()
        packages = get_packages()

        return E.ShipmentDetails(
            carrier=self.client.carrier_name,
            tracking_numbers=reduce(
                lambda ids, pkg: ids + [id.TrackingNumber for id in pkg.TrackingIds], packages, []
            ),
            total_charge=E.ChargeDetails(
                name="Shipment charge",
                amount=shipment.TotalNetChargeWithDutiesAndTaxes.Amount,
                currency=shipment.TotalNetChargeWithDutiesAndTaxes.Currency
            ),
            charges=[E.ChargeDetails(
                    name="base_charge",
                    amount=shipment.TotalBaseCharge.Amount,
                    currency=shipment.TotalBaseCharge.Currency
            ), E.ChargeDetails(
                    name="discount",
                    amount=detail.ShipmentRating.EffectiveNetDiscount.Amount,
                    currency=detail.ShipmentRating.EffectiveNetDiscount.Currency
            )] + 
            [E.ChargeDetails(
                    name=surcharge.SurchargeType,
                    amount=surcharge.Amount.Amount,
                    currency=surcharge.Amount.Currency
            ) for surcharge in shipment.Surcharges] + 
            [E.ChargeDetails(
                    name=fee.Type,
                    amount=fee.Amount.Amount,
                    currency=fee.Amount.Currency
            ) for fee in shipment.AncillaryFeesAndTaxes],
            services=[
                detail.ServiceTypeDescription
            ],
            documents=reduce(
               lambda labels, pkg: labels + [str(b64encode(part.Image), 'utf-8') for part in pkg.Label.Parts], packages, []
            )
        )
