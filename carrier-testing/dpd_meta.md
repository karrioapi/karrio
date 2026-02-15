# DPD Meta — Carrier Testing

## Metadata

| Field                      | Value                                |
|----------------------------|--------------------------------------|
| **Carrier Name**           | `dpd_meta`                           |
| **Carrier Display Name**   | DPD Group (META-API)                 |
| **Environment**            | Sandbox                              |
| **Connection Credentials** | Test account configured in Dashboard |

---

## 1. Connection Setup

> Verify the carrier can be connected and authenticated.

- [x] Carrier connection created successfully in Dashboard
- [x] Authentication succeeds (no credential errors)
- [x] Connection appears in carrier list

**Notes:**

---

## 2. Rating / Rate Fetching

> DPD Meta uses a **rate sheet** (CSV-based static rates), not a live rate endpoint.

**Rate Type:** `Rate Sheet`

- [x] Rate sheet uploaded/configured
- [x] Rates fetched correctly based on weight and destination
- [x] All configured services return rates

**Notes:**

---

## 3. Shipping / Shipment Creation

> Test creating shipments and generating labels.

**Supported:** `Yes`

### Basic Shipment
- [x] Create domestic shipment with default service
- [x] Label generated and downloadable as PDF
- [x] Tracking number returned in response
- [x] Shipment appears in shipment list

### Service Coverage
- [x] Create shipment with each available service (list services tested below)

| Service Code | Service Name              | Result  |
|--------------|---------------------------|---------|
| CL           | DPD Classic               | Pass    |
| E830         | DPD Express 8:30          | Pass    |
| E12          | DPD Express 12            | Pass    |
| E18          | DPD Express 18            | Pass    |
| IE2          | DPD International Express | Pass    |
| PL           | DPD Parcel Letter         | Pass    |
| MAIL         | DPD Mail                  | Pass    |
| MAX          | DPD Max                   | Pass    |

### Multi-Piece Shipment
- [x] Create shipment with 2+ parcels (tested with 3 parcels)
- [x] All parcel tracking numbers returned (in `meta.tracking_numbers`; UI shows primary only)
- [x] Combined label generated (single PDF with one label per parcel)

### International Shipment (if applicable)
- [x] Create international shipment with customs info

**Notes:** International shipment initially failed with two issues, both now fixed:

1. **Commodity weight crash** (`'float' object has no attribute 'G'`): `Product.weight` returns a plain float, not a `Weight` object. Fixed by wrapping in `units.Weight(item.weight, item.weight_unit or "KG").G` before converting to string. (commit `78655422e`)

2. **Missing `contactPerson` in importer/exporter contact** (`COMMON_2: commercialInvoiceConsignee.contact`): The German BU internally maps `importer` to `commercialInvoiceConsignee` and requires `contactPerson` in the contact block. This field is not documented in any of the three vendor docs (`meta-api-docs.json`, `openapi_metaapi_shipping.yaml`, `METAAPI_CUSTOMER_DOCUMENTATION_1_2.pdf`). Error origin was `BU-API`. Fixed by adding `contactPerson` to both importer and exporter contact. (commit `b725a8a56`)

---

## 4. Label

> Test label output options.

**Supported:** `Yes`

- [x] Label downloads as PDF
- [x] Label format matches requested format (PDF / ZPL / PNG)
- [x] Label contains correct shipper and recipient info

**Notes:**

---

## 5. Shipment Cancellation

> DPD META-API does not expose a cancel/void endpoint.

**Supported:** `Not Supported`

**Notes:** No carrier API cancel endpoint. 

---

## 6. Tracking

> DPD META-API does not expose a tracking endpoint.

**Supported:** `Not Supported`

**Notes:** No `get_tracking` method in proxy. Tracking is available via DPD portal using the tracking URL.

---

## 7. Pickup Scheduling

> Test scheduling and managing pickups.

**Supported:** `Yes` (schedule only — no cancel endpoint)

### Schedule Pickup
- [x] Schedule pickup with valid address and date
- [x] Confirmation number returned
- [x] Pickup appears in pickup list

### Pickup with Shipment
- [x] Schedule pickup associated with a DPD shipment
- [x] Schedule pickup without an associated shipment (standalone)

### Cancel Pickup
**Not Supported** — No `cancel_pickup` method in proxy.

**Notes:**

---

## 8. Return Shipment

> DPD META-API does not expose a dedicated return shipment endpoint.

**Supported:** `N/A`

**Notes:** Return options exist as shipping options (`return_enabled`, `include_return_label`) but no separate return endpoint.

---

## Edge Cases & Error Handling

> General robustness checks.

- [x] Invalid credentials show clear error message
- [x] Missing required fields return descriptive validation errors
- [x] Duplicate shipment creation handled

**Notes:**

---

## Summary

| Feature          | Status        |
|------------------|---------------|
| Connection Setup | Pass          |
| Rating           | Pass          |
| Shipping         | Pass          |
| Label            | Pass          |
| Cancellation     | Not Supported |
| Tracking         | Not Supported |
| Pickup           | Pass          |
| Return Shipment  | N/A           |

**Overall Result:** Pass

**Additional Notes:** All domestic and international services work. Multi-piece shipment tested with 3 parcels. Cancellation, tracking, and cancel pickup are not supported by the META-API.
