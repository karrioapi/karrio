# Asendia Vendor Documentation

This directory contains the Asendia Sync API specification used by the Asendia connector.

## API Overview

- **Source**: Asendia Sync API — https://www.asendia-sync.com/swagger-ui/index.html
- **Spec URL**: https://www.asendia-sync.com/v3/api-docs
- **Authentication**: JWT Bearer — obtain token via `POST /api/authenticate` with `{username, password}`

## Endpoints Used

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/authenticate` | Obtain JWT access token |
| POST | `/api/parcels` | Create shipment (one request per package) |
| DELETE | `/api/parcels/{id}` | Cancel shipment (HTTP 204, empty body) |
| GET | `/api/parcels/{id}/label` | Fetch label (base64 PDF/PNG/ZPL) |
| GET | `/api/parcels/{id}/return-label` | Fetch return label |
| GET | `/api/customers/{customerId}/tracking/{trackingNumber}` | Get tracking events |
| POST | `/api/manifests` | Close manifest |
| GET | `/api/manifests/{id}/document` | Fetch manifest document |

## Rate Handling

No native rating API. The connector uses `RatingMixinProxy` with a rate sheet loaded from `services.csv`.
Service definitions, weight limits, and zone rates live in that CSV — not in the OpenAPI spec.

## Enums (see `karrio/providers/asendia/units.py`)

| Enum class | Field | Values |
|------------|-------|--------|
| `ShippingService` | `asendiaService.product` | `EPAQSTD`, `EPAQPLS`, `EPAQSCT`, `EPAQELT`, `EPAQGO`, `EPAQRETDOM`, `EPAQRETINT` |
| `ServiceCode` | `asendiaService.service` | `CUP`, `CPPR`, `CPPS`, `RETPP`, `RETPAP` |
| `PackagingType` | `asendiaService.format` | `B` (boxable), `N` (non-boxable), `L` (large), `XL` (extra-large) |
| `InsuranceOption` | insurance option | `EL45`, `EL150`, `EL500` |

## Returns

- **Domestic return product**: `EPAQRETDOM` — used when shipper and recipient are in the same country
- **International return product**: `EPAQRETINT` — used when countries differ
- **Payment options**: `RETPP` (prepaid), `RETPAP` (partially prepaid)

The connector auto-selects the correct default based on `shipper.country_code == recipient.country_code`.

## Directory Contents

```
vendor/
├── README.md        # This file
├── openapi.json     # OpenAPI 3.0.1 spec (machine-readable)
└── openapi.yaml     # OpenAPI 3.0.1 spec (human-readable)
```

## Refreshing the Spec

```bash
cd karrio/modules/connectors/asendia
curl -sL https://www.asendia-sync.com/v3/api-docs -o vendor/openapi.json
python3 -c "import json,yaml; yaml.safe_dump(json.load(open('vendor/openapi.json')), open('vendor/openapi.yaml','w'), sort_keys=False)"
```
