# python-dhl

DHL Python Data Structure generated from .xsd files with [generateDS](http://www.davekuhlman.org/generateDS.html) library


## Installation

```bash
pip install -f https://git.io/purplship py-dhl
```

```python
import time
from io import StringIO
import pydhl.datatypes_global_v61 as Dt
import pydhl.DCT_req_global as DCTR

# Considering that payload is an object containing your shipment quote information

ServiceHeader_ = Dt.ServiceHeader(
    MessageReference="1234567890123456789012345678901",
    MessageTime=time.strftime('%Y-%m-%dT%H:%M:%S'),
    SiteID="YOUR_SITE_ID",
    Password="YOUR_PASSWORD"
)

MetaData_ = Dt.MetaData(SoftwareName="3PV", SoftwareVersion="1.0")

Request_ = Dt.Request(ServiceHeader=ServiceHeader_, MetaData=MetaData_)

From_ = DCTR.DCTFrom(
    CountryCode=payload.Shipper.Address.CountryCode,
    Postalcode=payload.Shipper.Address.PostalCode,
    City=payload.Shipper.Address.City,
    Suburb=payload.Shipper.Address.StateOrProvince
)

To_ = DCTR.DCTTo(
    CountryCode=payload.Recipient.Address.CountryCode,
    Postalcode=payload.Recipient.Address.PostalCode,
    City=payload.Recipient.Address.City,
    Suburb=payload.Recipient.Address.StateOrProvince
)

Pieces = DCTR.PiecesType()
for p in payload.ShipmentDetails.Packages:
    Pieces.add_Piece(DCTR.PieceType(
        PieceID=p.Id,
        PackageTypeCode=p.PackagingType,
        Height=p.Height,
        Width=p.Width,
        Weight=p.Weight,
        Depth=p.Lenght
    ))

BkgDetails_ = DCTR.BkgDetailsType(
    PaymentCountryCode="CA",
    NetworkTypeCode="AL",
    WeightUnit=payload.ShipmentDetails.WeightUnit,
    DimensionUnit=payload.ShipmentDetails.DimensionUnit,
    ReadyTime=time.strftime("PT%HH%MM"),
    Date=time.strftime("%Y-%m-%d"),
    IsDutiable=payload.ShipmentDetails.IsDutiable,
    Pieces=Pieces
)

GetQuote_ = DCTR.GetQuoteType(
  Request=Request_,
  From=From_,
  To=To_,
  BkgDetails=BkgDetails_
)

DCTRequest_ = DCTR.DCTRequest(schemaVersion="1.0", GetQuote=GetQuote_)

output = StringIO()
DCTRequest_.export(output, 0, name_='p:DCTRequest')
xmlElt = output.getvalue()
output.close()

print(xmlElt)

```

TODO:

- Add tests to consolidate/ensure data structures generate proper DHL xml files
- Add more Generated Data Structures using DHL .xsd files

Contributions are welcome.