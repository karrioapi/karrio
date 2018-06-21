import time
from datetime import datetime
from typing import List, Tuple
from functools import reduce
from pyfedex import rate_v22 as Rate
from .fedex_client import FedexClient
from ...domain.mapper import Mapper
from ...domain import entities as E
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
            Contact=None if not payload.shipper.contact else Rate.Contact(
                CompanyName=payload.shipper.contact.company_name, 
                PhoneNumber=payload.shipper.contact.phone_number
            ),
            Address=Rate.Address(
                City=payload.shipper.address.city,
                StateOrProvinceCode=payload.shipper.address.state_or_province,
                PostalCode=payload.shipper.address.postal_code,
                CountryCode=payload.shipper.address.country_code
            )
        )
        for line in payload.shipper.address.address_lines:
            shipper.Address.StreetLines.append(line)

        recipient = Rate.Party(
            Contact=None if not payload.recipient.contact else Rate.Contact(
                CompanyName=payload.recipient.contact.company_name, 
                PhoneNumber=payload.recipient.contact.phone_number
            ),
            Address=Rate.Address(
                City=payload.recipient.address.city,
                StateOrProvinceCode=payload.recipient.address.state_or_province,
                PostalCode=payload.recipient.address.postal_code,
                CountryCode=payload.recipient.address.country_code
            )
        )
        for line in payload.recipient.address.address_lines:
            recipient.Address.StreetLines.append(line)

        totalWeight = reduce(lambda r, p: r + p.weight, payload.shipment_details.packages, 0)

        packagin_type = "YOUR_PACKAGING" if not payload.shipment_details.packaging_type else payload.shipment_details.packaging_type

        currency = "USD" if not payload.shipment_details.currency else payload.shipment_details.currency

        payment_type = "SENDER" 
        if payload.shipment_details.charges_payment and payload.shipment_details.charges_payment.type:
            payment_type = payload.shipment_details.charges_payment.type

        payment_account = self.client.account_number
        if payload.shipment_details.charges_payment and payload.shipment_details.charges_payment.account_number:
            payment_account = payload.shipment_details.charges_payment.account_number

        shipment = Rate.RequestedShipment(
            ShipTimestamp=datetime.now(),
            PackagingType=packaging_type,
            TotalWeight=Rate.Weight(
                Units=payload.shipment_details.weight_unit, 
                Value=totalWeight
            ),
            PreferredCurrency=currency,
            Shipper=shipper,
            Recipient=recipient,
            ShippingChargesPayment=Rate.Payment(
                PaymentType=payment_type,
                Payor=Rate.Payor(ResponsibleParty=Rate.Party(
                    AccountNumber=payment_account
                ))
            ),
            PackageCount=len(payload.shipment_details.packages)
        )

        for p in payload.shipment_details.packages:
            shipment.RequestedPackageLineItems.append(Rate.RequestedPackageLineItem(
                GroupPackageCount=1,
                Weight=Rate.Weight(
                    Units=payload.shipment_details.weight_unit, 
                    Value=p.weight
                ),
                Dimensions=Rate.Dimensions(
                    Length=p.lenght, Width=p.width, Height=p.height, 
                    Units=payload.shipment_details.dimension_unit
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



    def parse_quote_response(self, res: Rate.RateReply) -> Tuple[List[E.quote_details], List[E.Error]]:
        quotes = reduce(extract_details, res.RateReplyDetails, [])
        errors = []
        return (quotes, errors)


def extract_details(quotes: List[E.quote_details], detail: Rate.RateReplyDetail): 
    if not detail.RatedShipmentDetails:
        return quotes
    shipmentDetail = detail.RatedShipmentDetails[0].ShipmentRateDetail
    Discounts_ = map(lambda d: E.Charge(name=d.RateDiscountType, value=float(d.Amount.Amount)), shipmentDetail.FreightDiscounts)
    Surcharges_ = map(lambda s: E.Charge(name=s.SurchargeType, value=float(s.Amount.Amount)), shipmentDetail.Surcharges)
    Taxes_ = map(lambda t: E.Charge(name=t.TaxType, value=float(t.Amount.Amount)), shipmentDetail.Taxes)
    return quotes + [
        E.Quote.parse(
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