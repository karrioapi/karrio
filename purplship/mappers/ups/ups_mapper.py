import time
from typing import List, Tuple
from functools import reduce
from purplship.mappers.ups.ups_client import UPSClient
from purplship.domain.mapper import Mapper
from purplship.domain import entities as E
from pyups import freight_rate as Rate, package_track as Track, UPSSecurity as Security, common as Common, error as Err

class UPSMapper(Mapper):
    def __init__(self, client: UPSClient):
        self.client = client

        self.Security = Security.UPSSecurity(
            UsernameToken=Security.UsernameTokenType(
                Username=self.client.username,
                Password=self.client.password
            ),
            ServiceAccessToken=Security.ServiceAccessTokenType(
                AccessLicenseNumber=self.client.access_license_number
            )
        )



    def create_quote_request(self, payload: E.quote_request) -> Rate.FreightRateRequest:
        Request_ = Common.RequestType(
            TransactionReference=Common.TransactionReferenceType(
                TransactionIdentifier="TransactionIdentifier"
            )
        )

        Request_.add_RequestOption(1)

        ShipFrom_ = Rate.ShipFromType(
            Name=payload.shipper.company_name,
            Address=Rate.AddressType(
                City=payload.shipper.city,
                PostalCode=payload.shipper.postal_code,
                CountryCode=payload.shipper.country_code
            ),
            AttentionName=payload.shipper.person_name,
        )

        for line in payload.shipper.address_lines:
            ShipFrom_.Address.add_AddressLine(line)

        if len(payload.shipper.address_lines) == 0:
            ShipFrom_.Address.add_AddressLine("...")

        ShipTo_ = Rate.ShipToType(
            Name=payload.recipient.company_name,
            Address=Rate.AddressType(
                City=payload.recipient.city,
                PostalCode=payload.recipient.postal_code,
                CountryCode=payload.recipient.country_code
            ),
            AttentionName=payload.recipient.person_name,
        )

        for line in payload.recipient.address_lines:
            ShipTo_.Address.add_AddressLine(line)

        PaymentInformation_ = Rate.PaymentInformationType(
            Payer=Rate.PayerType(
                Name=payload.shipment.payment_country_code or payload.shipper.country_code,
                Address=ShipFrom_.Address,
                ShipperNumber=payload.shipment.shipper_account_number or payload.shipment.payment_account_number or self.client.account_number
            ),
            ShipmentBillingOption=Rate.RateCodeDescriptionType(
                Code=10
            )
        )

        FreightRateRequest_ = Rate.FreightRateRequest(
            Request=Request_,
            ShipFrom=ShipFrom_,
            ShipTo=ShipTo_,
            PaymentInformation=PaymentInformation_,
            Service=Rate.RateCodeDescriptionType(Code=309, Description="UPS Ground Freight"),
            HandlingUnitOne=Rate.HandlingUnitType(
                Quantity=1, Type=Rate.RateCodeDescriptionType(Code="SKD")
            ),
            ShipmentServiceOptions=Rate.ShipmentServiceOptionsType(
                PickupOptions=Rate.PickupOptionsType(WeekendPickupIndicator="")
            ),
            DensityEligibleIndicator="",
            AdjustedWeightIndicator="",
            HandlingUnitWeight=Rate.HandlingUnitWeightType(
                Value=1,
                UnitOfMeasurement=Rate.UnitOfMeasurementType(Code="LB")
            ),
            PickupRequest=Rate.PickupRequestType(PickupDate=time.strftime('%Y%m%d')),
            GFPOptions=Rate.OnCallInformationType(),
            TimeInTransitIndicator=""
        )

        for c in payload.shipment.packages:
            FreightRateRequest_.add_Commodity(
                Rate.CommodityType(
                    Description=c.description or "...",
                    Weight=Rate.WeightType(
                        UnitOfMeasurement=Rate.UnitOfMeasurementType(Code="LBS"),
                        Value=c.weight
                    ),
                    Dimensions=Rate.DimensionsType(
                        UnitOfMeasurement=Rate.UnitOfMeasurementType(Code="IN"),
                        Width=c.width,
                        Height=c.height,
                        Length=c.length
                    ),
                    NumberOfPieces=len(payload.shipment.packages),
                    PackagingType=Rate.RateCodeDescriptionType(Code="BAG", Description="BAG"),
                    FreightClass=50
                )
            )

        return FreightRateRequest_


    def create_tracking_request(self, payload: E.tracking_request) -> List[Track.TrackRequest]:    
        Request_ = Common.RequestType(
            TransactionReference=Common.TransactionReferenceType(
                TransactionIdentifier="TransactionIdentifier"
            )
        )

        Request_.add_RequestOption(1)

        TrackRequests_ = [Track.TrackRequest(
            Request=Request_,
            InquiryNumber=number
        ) for number in payload.tracking_numbers]

        return TrackRequests_


    def parse_error_response(self, response) -> List[E.Error]:
        notifications = response.xpath('.//*[local-name() = $name]', name="PrimaryErrorCode")
        return reduce(self._extract_error, notifications, [])


    def parse_quote_response(self, response) -> Tuple[List[E.QuoteDetails], List[E.Error]]:
        rate_replys = response.xpath('.//*[local-name() = $name]', name="FreightRateResponse")
        quotes = reduce(self._extract_quote, rate_replys, [])
        return (quotes, self.parse_error_response(response))


    def parse_tracking_response(self, response) -> Tuple[List[E.QuoteDetails], List[E.Error]]:
        track_details = response.xpath('.//*[local-name() = $name]', name="Shipment")
        trackings = reduce(self._extract_tracking, track_details, [])
        return (trackings, self.parse_error_response(response))




    def _extract_error(self, errors: List[E.Error], errorNode) -> List[E.Error]:
        error = Err.CodeType()
        error.build(errorNode)
        return errors + [
            E.Error(code=error.Code, message=error.Description, carrier=self.client.carrier_name)
        ]


    def _extract_quote(self, quotes: List[E.QuoteDetails], detailNode) -> List[E.QuoteDetails]: 
        detail = Rate.FreightRateResponse()
        detail.build(detailNode)

        total_charge = [r for r in detail.Rate if r.Type.Code == 'AFTR_DSCNT'][0]
        Discounts_ = [E.ChargeDetails(name=r.Type.Code, currency=r.Factor.UnitOfMeasurement.Code, amount=float(r.Factor.Value)) for r in detail.Rate if r.Type.Code == 'DSCNT']
        Surcharges_ = [E.ChargeDetails(name=r.Type.Code, currency=r.Factor.UnitOfMeasurement.Code, amount=float(r.Factor.Value)) for r in detail.Rate if r.Type.Code not in ['DSCNT', 'AFTR_DSCNT', 'DSCNT_RATE', 'LND_GROSS']]
        extra_charges = Discounts_ + Surcharges_
        return quotes + [
            E.QuoteDetails(
                carrier=self.client.carrier_name, 
                currency=detail.TotalShipmentCharge.CurrencyCode,
                service_name=detail.Service.Description,
                service_type=detail.Service.Code,
                base_charge=float(detail.TotalShipmentCharge.MonetaryValue),
                total_charge=float(total_charge.Factor.Value or 0),
                duties_and_taxes=reduce(lambda r, c: r + c.amount, Surcharges_, 0),
                discount=reduce(lambda r, c: r + c.amount, Discounts_, 0),
                extra_charges=extra_charges
            )
        ]


    def _extract_tracking(self, trackings: List[E.TrackingDetails], shipmentNode) -> List[E.TrackingDetails]:
        trackDetail = Track.ShipmentType()
        trackDetail.build(shipmentNode)
        activityNodes = shipmentNode.xpath('.//*[local-name() = $name]', name="Activity")
        def buildActivity(node): 
            activity = Track.ActivityType()
            activity.build(node)
            return activity 
        activities = map(buildActivity, activityNodes)
        return trackings + [
            E.TrackingDetails(
                carrier=self.client.carrier_name,
                tracking_number=trackDetail.InquiryNumber.Value,
                events=list(map(lambda a: E.TrackingEvent(
                    date=str(a.Date),
                    time=str(a.Time),
                    code=a.Status.Code if a.Status else None,
                    location=a.ActivityLocation.Address.City if a.ActivityLocation and a.ActivityLocation.Address else None,
                    description=a.Status.Description if a.Status else None
                ), activities))
            )
        ]
