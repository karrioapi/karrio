# python-fedex

Fedex Python Data Structure generated from .xsd files with [generateDS](http://www.davekuhlman.org/generateDS.html) library

## Installation

```bash
pip install -f https://git.io/purplship py-fedex
```

```python
from pyfedex.fedex import rate_v22 as Rate

# Considering that payload is an object containing your shipment info

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

rateRequest =  Rate.RateRequest(
    WebAuthenticationDetail=self.client.webAuthenticationDetail,
    ClientDetail=self.client.clientDetail,
    TransactionDetail=transactionDetail,
    Version=version,
    RequestedShipment=shipment
)
```

TODO:

- Add tests to consolidate/ensure data structures generate proper Fedex xml files
- Add more Generated Data Structures using Fedex .xsd files

Contributions are welcome.