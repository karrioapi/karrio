import time
from pyups import (
    freight_rate as Rate,
    common as Common
)
from .interface import reduce, Tuple, List, E, UPSMapperBase


class UPSMapperPartial(UPSMapperBase):
    
    def parse_freight_rate_response(self, response: 'XMLElement') -> Tuple[List[E.QuoteDetails], List[E.Error]]:
        rate_replys = response.xpath('.//*[local-name() = $name]', name="FreightRateResponse")
        quotes = reduce(self._extract_quote, rate_replys, [])
        return (quotes, self.parse_error_response(response))

    def _extract_quote(self, quotes: List[E.QuoteDetails], detailNode: 'XMLElement') -> List[E.QuoteDetails]: 
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

    def create_freight_rate_request(self, payload: E.shipment_request) -> Rate.FreightRateRequest:
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
                ShipperNumber=payload.shipper.account_number or payload.shipment.payment_account_number or self.client.account_number
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

