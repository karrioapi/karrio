import time
from datetime import datetime
from typing import List, Tuple
from functools import reduce
from pyfedex import rate_v22 as Rate, track_service_v14 as Track
from openship.mappers.fedex.fedex_client import FedexClient
from openship.domain.mapper import Mapper
from openship.domain import entities as E
from pyfedex.rate_v22 import WebAuthenticationCredential, WebAuthenticationDetail, ClientDetail

class FedexMapper(Mapper):
    def __init__(self, client: FedexClient):
        self.client = client

        userCredential = WebAuthenticationCredential(Key=client.user_key, Password=client.password)
        self.webAuthenticationDetail = WebAuthenticationDetail(UserCredential=userCredential)
        self.clientDetail = ClientDetail(AccountNumber=client.account_number, MeterNumber=client.meter_number)




    def create_quote_request(self, payload: E.quote_request) -> Rate.RateRequest:
        transactionDetail = Rate.TransactionDetail(CustomerTransactionId="FTC")
        version = Rate.VersionId(ServiceId="crs", Major=22, Intermediate=0, Minor=0)

        shipper = Rate.Party(
            Contact=None if not payload.shipper.company_name and not payload.shipper.phone_number else Rate.Contact(
                CompanyName=payload.shipper.company_name, 
                PhoneNumber=payload.shipper.phone_number
            ),
            Address=Rate.Address(
                City=payload.shipper.city,
                StateOrProvinceCode=payload.shipper.state_or_province,
                PostalCode=payload.shipper.postal_code,
                CountryCode=payload.shipper.country_code
            )
        )
        for line in payload.shipper.address_lines:
            shipper.Address.StreetLines.append(line)

        recipient = Rate.Party(
            Contact=None if not payload.recipient.company_name and not payload.recipient.phone_number else Rate.Contact(
                CompanyName=payload.recipient.company_name, 
                PhoneNumber=payload.recipient.phone_number
            ),
            Address=Rate.Address(
                City=payload.recipient.city,
                StateOrProvinceCode=payload.recipient.state_or_province,
                PostalCode=payload.recipient.postal_code,
                CountryCode=payload.recipient.country_code
            )
        )
        for line in payload.recipient.address_lines:
            recipient.Address.StreetLines.append(line)

        totalWeight = reduce(lambda r, p: r + p.weight, payload.shipment.packages, 0)

        packaging_type = "YOUR_PACKAGING" if not payload.shipment.packaging_type else payload.shipment.packaging_type

        currency = payload.shipment.currency or "USD" 

        shipment = Rate.RequestedShipment(
            ShipTimestamp=datetime.now(),
            PackagingType=packaging_type,
            TotalWeight=Rate.Weight(
                Units=payload.shipment.weight_unit, 
                Value=totalWeight
            ),
            PreferredCurrency=currency,
            Shipper=shipper,
            Recipient=recipient,
            ShippingChargesPayment=Rate.Payment(
                PaymentType=payload.shipment.paid_by or "SENDER",
                Payor=Rate.Payor(ResponsibleParty=Rate.Party(
                    AccountNumber=payload.shipment.payment_account_number or self.client.account_number
                ))
            ),
            PackageCount=len(payload.shipment.packages)
        )

        for p in payload.shipment.packages:
            shipment.RequestedPackageLineItems.append(Rate.RequestedPackageLineItem(
                GroupPackageCount=1,
                Weight=Rate.Weight(
                    Units=payload.shipment.weight_unit, 
                    Value=p.weight
                ),
                Dimensions=Rate.Dimensions(
                    Length=p.length, Width=p.width, Height=p.height, 
                    Units=payload.shipment.dimension_unit
                )
            ))

        shipment.RateRequestTypes.append("LIST")
        return Rate.RateRequest(
            WebAuthenticationDetail=self.webAuthenticationDetail,
            ClientDetail=self.clientDetail,
            TransactionDetail=transactionDetail,
            Version=version,
            RequestedShipment=shipment
	    )


    def create_tracking_request(self, payload: E.tracking_request) -> Track.TrackRequest:    
        version = Track.VersionId(ServiceId="trck", Major=14, Intermediate=0, Minor=0)
        transactionDetail = Track.TransactionDetail(
            CustomerTransactionId="Track By Number_v14",
            Localization=Track.Localization(LanguageCode=payload.language_code or "en")
        )
        track_request = Track.TrackRequest(
            WebAuthenticationDetail=self.webAuthenticationDetail,
            ClientDetail=self.clientDetail,
            TransactionDetail=transactionDetail,
            Version=version,
        )
        for tracking_number in payload.tracking_numbers:
            track_request.add_SelectionDetails(Track.TrackSelectionDetail(
                CarrierCode="FDXE",
                PackageIdentifier=Track.TrackPackageIdentifier(
                    Type="TRACKING_NUMBER_OR_DOORTAG",
                    Value=tracking_number
                )
            ))
        return track_request



    def parse_error_response(self, response) -> List[E.Error]:
        notifications = response.xpath('.//*[local-name() = $name]', name="Notifications")
        return reduce(self._extract_error, notifications, [])


    def parse_quote_response(self, response) -> Tuple[List[E.quote_details], List[E.Error]]:
        rate_replys = response.xpath('.//*[local-name() = $name]', name="RateReplyDetails")
        quotes = reduce(self._extract_quote, rate_replys, [])
        return (quotes, self.parse_error_response(response))


    def parse_tracking_response(self, response) -> Tuple[List[E.quote_details], List[E.Error]]:
        track_details = response.xpath('.//*[local-name() = $name]', name="TrackDetails")
        trackings = reduce(self._extract_tracking, track_details, [])
        return (trackings, self.parse_error_response(response))




    def _extract_error(self, errors: List[E.Error], notificationNode) -> List[E.Error]:
        notification = Rate.Notification()
        notification.build(notificationNode)
        if notification.Severity != 'ERROR':
            return errors
        return errors + [
            E.Error(code=notification.Code, message=notification.Message, carrier=self.client.carrier_name)
        ]


    def _extract_quote(self, quotes: List[E.quote_details], detailNode) -> List[E.quote_details]: 
        detail = Rate.RateReplyDetail()
        detail.build(detailNode)
        if not detail.RatedShipmentDetails:
            return quotes
        shipmentDetail = detail.RatedShipmentDetails[0].ShipmentRateDetail
        Discounts_ = map(lambda d: E.Charge(name=d.RateDiscountType, amount=float(d.Amount.Amount)), shipmentDetail.FreightDiscounts)
        Surcharges_ = map(lambda s: E.Charge(name=s.SurchargeType, amount=float(s.Amount.Amount)), shipmentDetail.Surcharges)
        Taxes_ = map(lambda t: E.Charge(name=t.TaxType, amount=float(t.Amount.Amount)), shipmentDetail.Taxes)
        return quotes + [
            E.Quote.parse(
                carrier=self.client.carrier_name, 
                service_name=detail.ServiceType,
                service_type=detail.ActualRateType,
                base_charge=float(shipmentDetail.TotalBaseCharge.Amount),
                total_charge=float(shipmentDetail.TotalNetChargeWithDutiesAndTaxes.Amount),
                duties_and_taxes=float(shipmentDetail.TotalTaxes.Amount),
                discount=float(shipmentDetail.TotalFreightDiscounts.Amount),
                extra_charges=list(Discounts_) + list(Surcharges_) + list(Taxes_)
            )
        ]


    def _extract_tracking(self, trackings: List[E.tracking_details], trackDetailNode) -> List[E.tracking_details]:
        trackDetail = Track.TrackDetail()
        trackDetail.build(trackDetailNode)
        if trackDetail.Notification.Severity == 'ERROR':
            return trackings
        return trackings + [
            E.Tracking.parse(
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
