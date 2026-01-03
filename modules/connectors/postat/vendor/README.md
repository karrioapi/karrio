# PostAT (Austrian Post) Vendor Documentation

This directory contains documentation for the Austrian Post (PostAT/PLC) shipping integration.

## API Overview

Austrian Post uses a **SOAP/WCF-based API** through the ondot platform.

- **Base URL**: `https://plc.post.at/Post.Webservice/ShippingService.svc`
- **Base Namespace**: `http://post.ondot.at`
- **Authentication**: Credentials provided during customer onboarding (ClientID, OrgUnitID, OrgUnitGuid)
- **Label Formats**: PDF, ZPL2
- **Label Sizes**: 100x150, 100x200

## Available Operations

| Operation | SOAPAction | Description |
|-----------|------------|-------------|
| ImportShipment | `http://post.ondot.at/IShippingService/ImportShipment` | Create shipment and get label |
| CancelShipments | `http://post.ondot.at/IShippingService/CancelShipments` | Cancel/void a shipment |

**Note**: There is no tracking API documented. Tracking is available via the public website: `https://www.post.at/sv/sendungssuche?snr={tracking_number}`

## Directory Structure

```
vendor/
├── README.md                    # This file
├── PLC_API_Description.xlsx     # Official API documentation
├── PLC-Test-Label.pdf          # Sample label output
├── request_leer.txt            # Full SOAP request template (all fields)
├── request-example.txt         # Sample SOAP request (minimal)
├── result-response.txt         # Sample SOAP response with label
├── services.html               # Available services documentation
└── services.png                # Services visual reference

schemas/
├── postat.xsd                  # Shipment XSD schema (ImportShipment)
└── postat_void.xsd             # Cancel/void XSD schema (CancelShipments)
```

## Key Data Structures

### Address (OUShipperAddress / OURecipientAddress)
- Name1-4: Name fields (company, person, additional lines)
- AddressLine1/2: Street address
- HouseNumber: Building number
- PostalCode, City, CountryID
- Tel1/2, Email, Fax
- VATID, EORINumber: Tax/customs identifiers

### Package (ColloRow)
- Weight, Length, Width, Height
- ColloArticleList: Customs items
- ColloCodeList: Tracking codes (in response)

### Customs Article (ColloArticleRow)
- ArticleName, ArticleNumber
- Quantity, ValueOfGoodsPerUnit, CurrencyID
- CountryOfOriginID, HSTariffNumber
- ConsumerUnitNetWeight

### Label Settings (PrinterObject)
- LabelFormatID: 100x150 or 100x200
- LanguageID: PDF or ZPL2
- PaperLayoutID: 2xA5inA4, 4xA6inA4, A4
- Encoding: UTF-8 or WINDOWS-1252 (for ZPL2)

### Features (AdditionalInformationRow)
- ThirdPartyID: Feature code (e.g., COD, INS, SIG)
- Value1-4: Feature parameters

## Service Codes (DeliveryServiceThirdPartyID)

From services.html:

| ID | Service Name | Notes |
|----|--------------|-------|
| 10 | Paket Österreich | Standard domestic |
| 45 | Paket Premium International | International |
| 01 | Post Express Österreich | Express domestic |
| 46 | Post Express International | Express international |
| 28 | Retourpaket | Return (contract only) |
| 63 | Retourpaket International | Int. return (contract only) |
| 31 | Paket Premium Österreich B2B | B2B |
| 65 | Next Day | Contract only |
| 78 | Päckchen M mit Sendungsverfolgung | Small tracked package |

## Common Feature Codes

| Code | Description |
|------|-------------|
| COD | Cash on Delivery (Value1=amount, Value2=currency) |
| INS | Insurance (Value1=amount, Value2=currency) |
| SIG | Signature Required |
| AGE | Age Verification (Value1=minimum age) |
| SAT | Saturday Delivery |
| MAIL | Email Notification (Value1=email address) |
| SMS | SMS Notification (Value1=phone number) |

## Response Structure

The ImportShipment response contains:
- `ImportShipmentResult`: Array of ColloRow with tracking codes
- `pdfData`: Base64-encoded PDF label (when LanguageID=PDF)
- `zplLabelData`: ZPL2 label data (when LanguageID=ZPL2)

## Tracking Codes

Each package receives a tracking code in `ColloCodeList`:
- `Code`: The tracking number
- `NumberTypeID`: Type of code
- `OUCarrierThirdPartyID`: Carrier identifier

## Generating Python Schemas

To generate Python dataclasses from XSD schemas:

```bash
cd /path/to/karrio/modules/connectors/postat
./generate
```

This will create Python modules in `karrio/schemas/postat/`:
- `plc_types.py` - Shipment types from postat.xsd
- `void_types.py` - Cancel types from postat_void.xsd
