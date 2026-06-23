# GLS-validated request samples

Shipment-creation request payloads shared by **Timo (GLS)** in 2026-06 as
the reference for what a correct ShipIT `createParcels` body looks like —
the "examples from last week" referenced in his feedback. They are the
ground truth this connector's output is built to match.

| File | Service exercised | Notes |
|------|-------------------|-------|
| `service_addresseeonly.json` | `service_addresseeonly` | Flag service via `{"Service":{"ServiceName":…}}` wrapper |
| `service_signature.json` | `service_signature` | Same wrapper; two `ShipmentUnit`s |
| `service_flexdelivery.json` | `service_flexdelivery` | Same wrapper |
| `service_pickandreturn.json` | `service_pickandreturn` | Dedicated `PickAndReturn` wrapper with `PickupDate` |
| `service_shopreturn.json` | `service_shopreturn` | Dedicated `ShopReturn` wrapper with `NumberOfLabels` |

What these confirm (and what the connector emits):

- `Shipment.Middleware` is the fixed billing marker `"JTLviaGLS"`.
- **No** top-level `PartnerReference`, **no** `Volume` section.
- Request `ServiceName`s are the lowercase `service_*` codes.
- Generic "(w/o attributes)" services ride as `{"Service":{"ServiceName":"service_*"}}`;
  services with attributes (PickAndReturn, ShopReturn, …) ride under their
  own wrapper key.
- Address email field is `eMail` (lowercase leading `e`).
- Shipper carries `ContactID` (+ optional `AlternativeShipperAddress`); the
  real shipper address is not transmitted.

These are **inputs** (request bodies), not generated artefacts — keep them
verbatim as received from GLS. Cross-check `tests/gls/test_shipment.py`
expected payloads and `schemas/shipment_request.json` against them when the
spec moves.
