# DPD France — cargoNET (EPrintWebservice) vendor docs

This directory contains the official DPD France / cargoNET web service documentation
used to implement the `dpd_france` connector.

## Source PDFs

| File | Description | Version |
|------|-------------|---------|
| `DPD France Shipping WebService - GeoLabel.pdf` | EPrintWebservice — label generation, shipment creation, cancellation (`TerminateShipment`) | v1.9a — 02/2026 |
| `DPD France Tracking WebService.pdf` | Webtrace_Service — shipment status and event lookup | v5.0 — 10/2025 |

## Endpoints

| Service | Environment | URL |
|---------|-------------|-----|
| Shipping (EPrintWebservice) | Test | `https://e-station-testenv.cargonet.software/eprintwebservice/eprintwebservice.asmx` |
| Shipping (EPrintWebservice) | Production | `https://e-station.cargonet.software/dpd-eprintwebservice/eprintwebservice.asmx` |
| Tracking (Webtrace_Service) | Test | `https://e-station-testenv.cargonet.software/trace-service/Webtrace_Service.asmx` |
| Tracking (Webtrace_Service) | Production | `https://webtrace.dpd.fr/trace-service/Webtrace_Service.asmx` |

Note: the production shipping URL has a `dpd-` prefix that the test URL does not. The production
tracking URL uses a completely different host (`webtrace.dpd.fr`).

## Authentication

Both services use a SOAP header for authentication. Credentials are passed via
`<imt:UserCredentials>` in the SOAP envelope header (Shipping PDF p.7):

```xml
<soap:Header>
  <imt:UserCredentials>
    <imt:userid>User</imt:userid>
    <imt:password>Password</imt:password>
  </imt:UserCredentials>
</soap:Header>
```

Credentials are issued by DPD France sales. Contact details below.

## Required Customer Identifiers

| Field | Value | Notes |
|-------|-------|-------|
| `customer_countrycode` | `250` | ISO numeric code for France — always hardcoded |
| `customer_centernumber` | assigned | DPD France depot/centre number |
| `customer_number` | assigned | DPD France customer account number |

## Security — IP Whitelist

Both services require the calling server's IP address to be whitelisted by cargoNET (§3 of both PDFs).
Calls from non-whitelisted IPs return a SOAP fault with error code `IpPermissionDenied`.
Request whitelisting when obtaining credentials.

## Contact for Credentials and Whitelisting

- Email: `support.webservices@cargonet-software.fr`
- Phone: `+33 3 88 79 79 50`

## Refreshing the Documentation

When DPD France issues updated PDFs:

1. Replace the PDF files in this directory with the new versions.
2. Review any schema changes against `schemas/EPrintWebservice.xsd` and `schemas/Webtrace_Service.xsd`.
3. If the XSD types or operations changed, update the schema files and re-run the `generate` script
   to regenerate `karrio/schemas/dpd_france/`.
4. Update `units.py` for any new service codes, label types, or enum values.
5. Update this README with the new version numbers.

## SOAP binding details

The cargoNET services are .NET ASMX endpoints exposing SOAP 1.1 and SOAP 1.2 bindings.
This connector uses SOAP 1.1 with `Content-Type: text/xml; charset=utf-8`. Transport is
HTTPS POST, UTF-8. Authoritative WSDL files for both test and production environments
were provided by DPD France / cargoNET via email; the `<xs:schema>` blocks were extracted
into `schemas/EPrintWebservice.xsd` and `schemas/Webtrace_Service.xsd` (with `s:` → `xs:`
prefix normalization so generateDS accepts them). Those XSDs are the source-of-truth for
type generation. If cargoNET issues a WSDL revision, request the updated file, re-extract
the `<xs:schema>`, and re-run `./generate`.

### Target namespaces

- Shipping (EPrintWebservice): `http://www.cargonet.software` — **no trailing slash**
- Tracking (Webtrace_Service): `http://www.cargonet.software/` — **with trailing slash**

### SOAPAction header strings

SOAP 1.1 requires a `SOAPAction` HTTP header per operation, formatted as
`<targetNamespace>/<OperationName>`. The three operations this connector implements:

| Operation | SOAPAction |
|---|---|
| `CreateShipmentWithLabelsBc` | `http://www.cargonet.software/CreateShipmentWithLabelsBc` |
| `TerminateShipment` | `http://www.cargonet.software/TerminateShipment` |
| `GetShipmentTrace` | `http://www.cargonet.software/GetShipmentTrace` |
| `CreateCollectionRequestBc` | `http://www.cargonet.software/CreateCollectionRequestBc` |
| `TerminateCollectionRequestBc` | `http://www.cargonet.software/TerminateCollectionRequestBc` |
| `CreateReverseInverseShipmentWithLabelsBc` | `http://www.cargonet.software/CreateReverseInverseShipmentWithLabelsBc` |

### TerminateShipment caveat (Shipping PDF §8.14)

`TerminateShipment` is only callable **before the parcel has been physically
shipped** (i.e. before pickup/handover). cargoNET will reject the request once
the shipment has entered the network. Callers should treat a missing `<Error>`
element in the response body as success — the operation otherwise returns an
empty body.

## Directory Contents

```
vendor/
├── README.md                                        # This file
├── DPD France Shipping WebService - GeoLabel.pdf   # EPrintWebservice spec
└── DPD France Tracking WebService.pdf              # Webtrace_Service spec
```
