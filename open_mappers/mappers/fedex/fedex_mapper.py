import time
from datetime import datetime
from typing import List, Tuple
from functools import reduce
from pyfedex import rate_v22 as Rate
from .fedex_client import FedexClient
from ...domain.mapper import Mapper
from ...domain import entities as E

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
            Contact=None if not payload.Shipper.Contact else Rate.Contact(
                CompanyName=payload.Shipper.Contact.CompanyName, 
                PhoneNumber=payload.Shipper.Contact.PhoneNumber
            ),
            Address=Rate.Address(
                City=payload.Shipper.Address.City,
                StateOrProvinceCode=payload.Shipper.Address.StateOrProvince,
                PostalCode=payload.Shipper.Address.PostalCode,
                CountryCode=payload.Shipper.Address.CountryCode
            )
        )
        for line in payload.Shipper.Address.AddressLines:
            shipper.Address.StreetLines.append(line)

        recipient = Rate.Party(
            Contact=None if not payload.Recipient.Contact else Rate.Contact(
                CompanyName=payload.Recipient.Contact.CompanyName, 
                PhoneNumber=payload.Recipient.Contact.PhoneNumber
            ),
            Address=Rate.Address(
                City=payload.Recipient.Address.City,
                StateOrProvinceCode=payload.Recipient.Address.StateOrProvince,
                PostalCode=payload.Recipient.Address.PostalCode,
                CountryCode=payload.Recipient.Address.CountryCode
            )
        )
        for line in payload.Recipient.Address.AddressLines:
            recipient.Address.StreetLines.append(line)

        totalWeight = reduce(lambda r, p: r + p.Weight, payload.ShipmentDetails.Packages, 0)

        shipment = Rate.RequestedShipment(
            ShipTimestamp=datetime.now(),
            PackagingType="YOUR_PACKAGING",
            TotalWeight=Rate.Weight(
                Units=payload.ShipmentDetails.WeightUnit, 
                Value=totalWeight
            ),
            PreferredCurrency="USD",
            Shipper=shipper,
            Recipient=recipient,
            ShippingChargesPayment=Rate.Payment(
                PaymentType="SENDER",
                Payor=Rate.Payor(ResponsibleParty=Rate.Party(
                    AccountNumber=self.client.account_number
                ))
            ),
            PackageCount=len(payload.ShipmentDetails.Packages)
        )

        for p in payload.ShipmentDetails.Packages:
            shipment.RequestedPackageLineItems.append(Rate.RequestedPackageLineItem(
                GroupPackageCount=1,
                Weight=Rate.Weight(
                    Units=payload.ShipmentDetails.WeightUnit, 
                    Value=p.Weight
                ),
                Dimensions=Rate.Dimensions(
                    Length=p.Lenght, Width=p.Width, Height=p.Height, 
                    Units=payload.ShipmentDetails.DimensionUnit
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



    def create_quote_response(self, res: Rate.RateReply) -> Tuple[List[E.Quote], List[E.Error]]:
        quotes = reduce(extractDetails, res.RateReplyDetails, [])
        errors = []
        return (quotes, errors)


def extractDetails(quotes: List[E.Quote], detail: Rate.RateReplyDetail): 
    if not detail.RatedShipmentDetails:
        return quotes
    shipmentDetail = detail.RatedShipmentDetails[0].ShipmentRateDetail
    Discounts_ = map(lambda d: E.Charge(name=d.RateDiscountType, value=float(d.Amount.Amount)), shipmentDetail.FreightDiscounts)
    Surcharges_ = map(lambda s: E.Charge(name=s.SurchargeType, value=float(s.Amount.Amount)), shipmentDetail.Surcharges)
    Taxes_ = map(lambda t: E.Charge(name=t.TaxType, value=float(t.Amount.Amount)), shipmentDetail.Taxes)
    return quotes + [
        E.Quote(
            carrier="Fedex", 
            service_name=detail.ServiceType,
            service_type=detail.ActualRateType,
            base_charge=float(shipmentDetail.TotalBaseCharge.Amount),
            total_charge=float(shipmentDetail.TotalNetChargeWithDutiesAndTaxes.Amount),
            duties_and_taxes=float(shipmentDetail.TotalTaxes.Amount),
            discount=float(shipmentDetail.TotalFreightDiscounts.Amount),
            extra_charges=list(Discounts_) + list(Surcharges_) + list(Taxes_)
        )
    ]