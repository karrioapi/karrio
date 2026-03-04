# MyDHL Express — Carrier Testing

## Metadata

| Field                      | Value                                |
|----------------------------|--------------------------------------|
| **Carrier Name**           | `mydhl`                              |
| **Carrier Display Name**   | MyDHL Express                        |
| **Environment**            | Production (`express.api.dhl.com/mydhlapi`) |
| **Connection Credentials** | DE production account configured in Dashboard |
| **Last Tested**            | 2026-03-04                           |

---

## 1. Connection Setup

> Verify the carrier can be connected and authenticated. MyDHL uses Basic Authentication with `username`, `password`, and `account_number`.

- [x] Carrier connection created successfully in Dashboard
- [x] Authentication succeeds (no credential errors)
- [x] Connection appears in carrier list

**Notes:** `account_number` (DHL billing number) must be configured — without it, rate/shipment requests fail with `"required key [number] not found"`.

---

## 2. Rating / Rate Fetching

> Test rate retrieval for shipments. MyDHL provides a **live rate endpoint** via `/rates`.

**Rate Type:** `Live API Endpoint`

### Live API Endpoint:
- [x] Fetch domestic rates successfully
- [x] Fetch international rates successfully
- [x] Rates returned for all expected services

**DE Domestic:** 6 services returned in EUR — EXPRESS EASY (19.29), EXPRESS DOMESTIC (27.26), EXPRESS DOMESTIC 12:00 (33.18), EXPRESS DOMESTIC 10:30 (45.00), EXPRESS DOMESTIC 9:00 (68.65), MEDICAL EXPRESS DOMESTIC (74.98).

**DE→US International:** 5 services returned in EUR — EXPRESS EASY (112.01), EXPRESS WORLDWIDE (170.12), EXPRESS 12:00 (176.64), EXPRESS 10:30 (189.69), MEDICAL EXPRESS (206.53).

**Notes:** Tested with temporary Bug 1 workaround applied (fix reverted after testing). Some service codes in the response don't match the `ShippingService` enum (see Bug 4).

---

## 3. Shipping / Shipment Creation

> Test creating shipments and generating labels via `/shipments`.

**Supported:** `Yes`

### Basic Shipment
- [x] Create domestic shipment with default service
- [ ] Label generated and downloadable as PDF (Bug 3 — label not extracted)
- [x] Tracking number returned in response
- [x] Shipment appears in shipment list

### Service Coverage
- [ ] Create shipment with each available service (list services tested below)

| Service Code | Service Name | Product Code | Result |
|---|---|---|---|
| mydhl_express_worldwide_b2c | EXPRESS EASY | 7 | Pass (tracking returned, no label) |
| mydhl_express_domestic | EXPRESS DOMESTIC | N | Fail — `"Requested product(s) not available at origin"` |

### Multi-Piece Shipment
- [ ] Create shipment with 2+ parcels (Blocked — Bugs 1-2 require fixes first)

### International Shipment (if applicable)
- [ ] Create international shipment with customs info (Blocked — Bugs 1-2 require fixes first)

**Notes:** Tested with temporary Bug 1 + Bug 2 workarounds applied (fixes reverted after testing). Service mapping in response shows `service: "mydhl"` instead of actual service name (Bug 5). Express Domestic (N) not available for DE origin with this account — use EXPRESS EASY (7) instead.

---

## 4. Label

> Test label output options. MyDHL supports PDF, ZPL, LP2, and EPL label formats.

**Supported:** `Yes`

- [ ] Label downloads as PDF (Bug 3 — label content empty)
- [ ] Label format matches requested format
- [ ] Label contains correct shipper and recipient info

**Available label formats:** `PDF`, `ZPL`, `LP2`, `EPL`

**Notes:** DHL returns label data (7144 chars base64 PDF confirmed in raw response) but it's not extracted into the shipment response. See Bug 3.

---

## 5. Shipment Cancellation

> Test cancelling/voiding shipments.

**Supported:** `Yes` (via Karrio resource management)

- [x] Cancel a newly created shipment
- [x] Shipment status updates to cancelled

**Notes:** Tested with temporary Bug 1 + Bug 2 workarounds applied (fixes reverted after testing). Cancelled shipment `shp_e405009e929e483299ba69362caa2b04` successfully. Status updated to cancelled via Karrio resource management.

---

## 6. Tracking

> Test tracking shipment status via `/tracking`.

**Supported:** `Yes`

- [x] Track a shipment by tracking number
- [x] Tracking events returned with timestamps
- [x] Tracking status reflects current state

**Notes:** Tested with temporary Bug 1 + Bug 2 workarounds applied (fixes reverted after testing). Tracked shipment `3627506190` — returned `pending` status with "Label created" event and timestamp.

---

## 7. Pickup Scheduling

> Test scheduling and managing pickups via `/pickups`.

**Supported:** `Yes`

### Schedule Pickup
- [ ] Schedule pickup with valid address and date (Blocked — Bug 2 + Bug 6)
- [ ] Confirmation number returned
- [ ] Pickup appears in pickup list

### Cancel Pickup
- [ ] Cancel a scheduled pickup
- [ ] Pickup status updates to cancelled

**Notes:** Attempted but blocked — Bug 2 (invalid typeCode `YP` in `pickup/create.py:159`) causes request to fail, and Bug 6 (missing `additionalDetails`) hides the actual DHL error details.

---

## 8. Return Shipment

> Test return shipment creation.

**Supported:** `Yes`

- [ ] Create return shipment (Blocked — Bugs 1-2 require fixes first)
- [ ] Return label generated
- [ ] Return tracking number provided

**Notes:** Not tested — blocked by Bug 1 (date parsing) and Bug 2 (invalid typeCode) which must be fixed before return shipments can be created.

---

## Shipping Options Reference

> Key shipping options available for testing.

| Option | Type | Description |
|---|---|---|
| `mydhl_saturday_delivery` | bool | Saturday delivery (AA) |
| `mydhl_hold_for_collection` | bool | Hold at service point (LX) |
| `mydhl_duty_tax_paid` | bool | DTP — Duty/Tax Paid (DD) |
| `mydhl_shipment_insurance` | float | Insurance value (II) |
| `mydhl_dangerous_goods` | bool | Dangerous goods (HE) |
| `mydhl_direct_signature` | bool | Direct signature required (SF) |
| `mydhl_paperless_trade` | bool | Paperless trade (WY) |
| `mydhl_gogreen_climate_neutral` | bool | GoGreen Carbon Neutral (EE) |

---

## Edge Cases & Error Handling

> General robustness checks.

- [ ] Invalid credentials show clear error message
- [ ] Missing required fields return descriptive validation errors
- [ ] Duplicate shipment creation handled

**Notes:** Error responses from DHL include `additionalDetails` array with specific validation errors, but the error parser doesn't capture them (see Bug 6).

---

## Bugs Found

> Bugs discovered during testing.

### Bug 1: Rate and shipment requests fail with date parsing error
**Impact:** All rate fetching and shipment creation fails without workaround.
**Root Cause:** `lib.fdatetime` called without `current_format` — defaults to `"%Y-%m-%d %H:%M:%S"` but server provides date-only `"%Y-%m-%d"` string. Shipment create also passes output format as positional arg to `current_format`.
**Files:** `rate.py:137`, `shipment/create.py:174`
**Status:** Open

### Bug 2: Shipment creation fails with invalid package typeCode
**Impact:** All shipment creation fails with `"YP is not a valid enum value"`.
**Root Cause:** `PackagingType` enum uses codes (`FLY`, `YP`, `JB`, `JJ`, `3`) that don't exist in the DHL API spec. Valid codes are: `1CE, 2BC, 2BP, 2BX, 3BX, 4BX, 5BX, 6BX, 7BX, 8BX, CE1, TBL, TBS, WB1, WB2, WB3, WB6, XPD`. Also, `typeCode` is optional — omitting it uses customer packaging by default.
**Files:** `units.py:15-41`, `shipment/create.py:266-268`, `pickup/create.py:159`
**Status:** Open

### Bug 3: Label content not extracted from shipment response
**Impact:** Shipments are created successfully but label is empty in the response.
**Root Cause:** DHL returns label data (confirmed 7144 chars base64 PDF in raw response) but the `_extract_details` parser returns empty label. Likely a `jstruct.JList` deserialization issue with the `documents` array.
**Files:** `shipment/create.py:46-50`
**Status:** Open

### Bug 4: Service code mapping mismatches (widespread)
**Impact:** Many rate responses show wrong service names. At least 9 product codes are incorrect or missing from DHL spec reference data.
**Root Cause:** `ShippingService` enum maps product codes to service names that don't match the DHL API v3.1.1 spec. Verified mismatches: `Y` (not in spec, mapped as EXPRESS 9:00), `M` (not in spec, mapped as GLOBALMAIL BUSINESS), `K` (spec: EXPRESS 9:00, mapped as EXPRESS 10:30), `8` (not in spec, mapped as EXPRESS EASY — should be `7`), `Q` (not in spec, mapped as MEDICAL EXPRESS — should be `C`), `R` (spec: GLOBALMAIL, mapped as SPRINTLINE), `G` (spec: ECONOMY SELECT DOMESTIC, mapped as GLOBALMAIL), `E` (not in spec, mapped as BREAKBULK EXPRESS — should be `B`), `F` (not in spec, mapped as EXPRESS FREIGHT).
**Files:** `units.py:44-82`
**Status:** Open

### Bug 5: Service name in shipment response always shows carrier name
**Impact:** Created shipments show `service: "mydhl"` instead of the actual service like `mydhl_express_worldwide_b2c`.
**Root Cause:** `_extract_details` sets `service=settings.carrier_name` instead of mapping the product code from the response.
**Files:** `shipment/create.py:70`
**Status:** Open

### Bug 6: Error responses missing additionalDetails
**Impact:** DHL validation errors show `"Multiple problems found, see Additional Details"` but the actual details are not included in the error response.
**Root Cause:** `ErrorResponseType` schema doesn't include `additionalDetails` field, and error parser doesn't pass it through.
**Files:** `error_response.py`, `error.py`
**Status:** Open

---

## Summary

| Feature          | Status  |
|------------------|---------|
| Connection Setup | Pass    |
| Rating           | Pass (with Bug 1 fix) |
| Shipping         | Partial (Bugs 1-3) |
| Label            | Fail (Bug 3) |
| Cancellation     | Pass    |
| Tracking         | Pass    |
| Pickup           | Blocked (Bugs 2, 6) |
| Return Shipment  | Blocked (Bugs 1-2) |

**Overall Result:** Blocked — 6 bugs found, fixes needed before full testing

**Additional Notes:** Tested with DE production credentials against `express.api.dhl.com/mydhlapi`. Rating works after Bug 1 workaround. Shipment creation works (tracking number returned) after Bug 1+2 workarounds, but label extraction is broken (Bug 3). Tracking and cancellation work correctly. Pickup blocked by invalid typeCode (Bug 2) and hidden error details (Bug 6). Return shipments and multi-piece/international shipping blocked pending bug fixes.
