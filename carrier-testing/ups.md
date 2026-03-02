# UPS — Carrier Testing

## Metadata

| Field                      | Value                                |
|----------------------------|--------------------------------------|
| **Carrier Name**           | `ups`                                |
| **Carrier Display Name**   | UPS                                  |
| **Environment**            | Production (`onlinetools.ups.com`)   |
| **Connection Credentials** | DE production account configured in Dashboard |
| **Last Tested**            | 2026-02-27                           |

---

## 1. Connection Setup

> Verify the carrier can be connected and authenticated. UPS uses OAuth2 (client credentials grant) with `client_id`, `client_secret`, `account_number`, and `account_country_code`.

- [x] Carrier connection created successfully in Dashboard
- [x] Authentication succeeds (no credential errors)
- [x] Connection appears in carrier list

**Notes:**

---

## 2. Rating / Rate Fetching

> Test rate retrieval for shipments. UPS provides a **live rate endpoint** via `/api/rating/v2409/Shop`.

**Rate Type:** `Live API Endpoint`

### Live API Endpoint:
- [x] Fetch domestic rates successfully
- [x] Fetch international rates successfully (if applicable)
- [x] Rates returned for all expected services

**Notes:** DE domestic returns 5 services in EUR with German-specific charges (MWST, German Road Tax). DE→US returns 4 international services. DE→FR EU cross-border returns 5 services.

---

## 3. Shipping / Shipment Creation

> Test creating shipments and generating labels via `/api/shipments/v2409/ship`.

**Supported:** `Yes`

### Basic Shipment
- [x] Create domestic shipment with default service
- [x] Label generated and downloadable as PDF
- [x] Tracking number returned in response
- [x] Shipment appears in shipment list

### Service Coverage
- [x] Create shipment with each available service (list services tested below)

**DE / EU Services:**

| Service Code                    | Service Name                  | Carrier Code | Result |
|---------------------------------|-------------------------------|--------------|--------|
| ups_standard_eu                 | UPS Standard EU               | 11           | Pass   |
| ups_worldwide_saver_eu          | UPS Worldwide Saver EU        | 65           | Pass   |
| ups_express_12_00_de            | UPS Express 12:00 DE          | 74           | Pass   |
| ups_express_eu                  | UPS Express EU                | 07           | Pass   |
| ups_worldwide_express_plus_eu   | UPS Worldwide Express Plus EU | 54           | Pass   |

**International Services (DE origin):**

| Service Code                    | Service Name                  | Carrier Code | Result |
|---------------------------------|-------------------------------|--------------|--------|
| ups_worldwide_saver_eu          | UPS Worldwide Saver EU        | 65           | Pass (DE→US with customs) |
| ups_standard_eu                 | UPS Standard EU               | 11           | Pass (DE→FR EU cross-border) |

### Multi-Piece Shipment
- [x] Create shipment with 2+ parcels (tested with 3 parcels)
- [x] All parcel tracking numbers returned (3 tracking numbers in `meta.tracking_numbers`)
- [x] Combined label generated

### International Shipment (if applicable)
- [x] Create international shipment with customs info

**Notes:** International shipments (DE→US) require `shipment_description` in options — without it UPS returns `120512: "Shipment Description is required"`. EU cross-border (DE→FR) requires omitting recipient phone number — see Bug 4.

---

## 4. Label

> Test label output options. UPS supports PDF (PNG internally) and ZPL label formats.

**Supported:** `Yes`

- [x] Label downloads as PDF
- [x] Label format matches requested format (PDF / ZPL / PNG)
- [x] Label contains correct shipper and recipient info

**Available label formats:** `PDF_6x4` (default), `PDF_8x4`, `ZPL_6x4`. Can enforce ZPL via `enforce_zpl` connection config.

**Notes:**

---

## 5. Shipment Cancellation

> Test cancelling/voiding shipments via `DELETE /api/shipments/v2409/void/cancel/{shipment_id}`.

**Supported:** `Yes`

- [x] Cancel a newly created shipment
- [x] Shipment status updates to cancelled
- [x] Cancel shipment that has no pickup
- [ ] Cancel shipment that has an active pickup (should warn)
- [ ] Cancel shipment after pickup is already cancelled

**Notes:** Last two items untested because pickup is blocked (Bug 1).

---

## 6. Tracking

> Test tracking shipment status via `GET /api/track/v1/details/{tracking_number}`.

**Supported:** `Yes`

- [ ] Track a shipment by tracking number
- [ ] Tracking events returned with timestamps
- [ ] Tracking status reflects current state (in_transit, delivered, etc.)

**Notes:** Blocked by Bug 3 — missing required `transId`/`transactionSrc` headers in `get_tracking()`.

---

## 7. Pickup Scheduling

> Test scheduling and managing pickups via `/api/pickupcreation/v2409/pickup`.

**Supported:** `Yes` (Blocked for DE — see Bug 1)

### Schedule Pickup
- [ ] Schedule pickup with valid address and date
- [ ] Confirmation number returned
- [ ] Pickup appears in pickup list

### Pickup with Shipment
- [ ] Schedule pickup associated with a shipment
- [ ] Schedule pickup without an associated shipment (standalone)

### Cancel Pickup
- [ ] Cancel a scheduled pickup
- [ ] Pickup status updates to cancelled

**Notes:** Blocked by Bug 1 — pickup `ServiceCode` hardcoded to US-only value.

---

## 8. Return Shipment

> Test return shipment creation. UPS supports returns via `ups_return_service` shipping option on shipment creation.

**Supported:** `Yes` (Blocked — see Bug 2)

- [ ] Create return shipment
- [ ] Return label generated
- [ ] Return tracking number provided

**Available return service codes:**
- `ups_print_and_mail` (2)
- `ups_return_1_attempt` (3)
- `ups_return_3_attempt` (5)
- `ups_electronic_return_label` (8)
- `ups_print_return_label` (9)
- `ups_exchange_print_return_label` (10)

**Notes:** Blocked by Bug 2 — response parsing crashes on null `ShippingLabel`. Return requests also require `description` on parcels and `shipment_description` in options.

---

## Shipping Options Reference

> Key shipping options available for testing.

| Option                                    | Type    | Description                                  |
|-------------------------------------------|---------|----------------------------------------------|
| `ups_saturday_delivery_indicator`         | bool    | Saturday delivery                            |
| `ups_sunday_delivery_indicator`           | bool    | Sunday delivery                              |
| `ups_deliver_to_addressee_only_indicator` | bool    | Delivery to addressee only                   |
| `ups_direct_delivery_only_indicator`      | bool    | Direct delivery only                         |
| `ups_cod`                                 | float   | Cash on delivery amount                      |
| `ups_hold_for_pickup_indicator`           | bool    | Hold at UPS facility for pickup              |
| `ups_delivery_confirmation`               | enum    | 1=Signature Required, 2=Adult Signature      |
| `ups_return_service`                      | enum    | Return service code (see Section 8)          |
| `ups_carbonneutral_indicator`             | bool    | Carbon neutral shipping                      |
| `ups_restricted_articles`                 | bool    | Restricted articles / dangerous goods        |
| `ups_lift_gate_for_pickup_indicator`      | bool    | Lift gate at pickup                          |
| `ups_lift_gate_for_delivery_indicator`    | bool    | Lift gate at delivery                        |
| `ups_access_point_pickup`                 | bool    | PUDO (Pick Up Drop Off) pickup               |
| `ups_access_point_delivery`              | bool    | PUDO delivery                                |
| `ups_inside_delivery`                     | enum    | Inside delivery type (01, 02, 03)            |
| `ups_negotiated_rates_indicator`          | bool    | Use negotiated rates                         |

---

## Edge Cases & Error Handling

> General robustness checks.

- [x] Invalid credentials show clear error message
- [x] Missing required fields return descriptive validation errors
- [x] Duplicate shipment creation handled

**Notes:**

---

## Bugs Found

> Integration bugs discovered during testing that need fixing.

### Bug 1: Pickup ServiceCode hardcoded to US-only value
**File:** `modules/connectors/ups/karrio/providers/ups/pickup/create.py` line 113
**Issue:** Default pickup `ServiceCode` is `"001"` (US-only). Invalid for DE — UPS returns `9510119: "Invalid service designation"`.
**Fix:** Map pickup service codes by origin country. UPS Pickup API appendix defines region-specific codes (not in the OpenAPI spec).

### Bug 2: Return shipment crashes on label parsing
**File:** `modules/connectors/ups/karrio/providers/ups/shipment/create.py` line 143
**Issue:** `_process_label()` accesses `ShippingLabel.ImageFormat.Code` without null-checking. For return shipments, `ShippingLabel` is `None` → `'NoneType' object has no attribute 'ImageFormat'`.
**Fix:** Add null check before accessing `ImageFormat`.

### Bug 3: Tracking API missing required headers (regression)
**File:** `modules/connectors/ups/karrio/mappers/ups/proxy.py` — `get_tracking()`
**Issue:** UPS Tracking API requires `transId` and `transactionSrc` headers (`required: true` in spec). These were in the old `_send_request()` helper but dropped in the proxy rewrite (commit `b77de1f19`). Without them → `TV0001: "Missing transId"` and `TV0011: "Missing transactionSrc"`.
**Fix:** Add `transId` (unique per request, e.g. UUID) and `transactionSrc` (e.g. `"karrio"`) to `get_tracking()` headers.

### Bug 4: EU cross-border phone number rejection
**Symptom:** UPS returns `120217: "ShipTo phone number cannot be more than 15 digits long"` for any phone number on EU cross-border shipments (e.g., DE→FR), even 9-digit numbers. Omitting phone works (falls back to `000-000-0000`).
**Fix:** Needs investigation — possibly UPS API bug or connector sending phone in unexpected format for EU lanes.

---

## Summary

| Feature          | Status  |
|------------------|---------|
| Connection Setup | Pass    |
| Rating           | Pass    |
| Shipping         | Pass    |
| Label            | Pass    |
| Cancellation     | Pass    |
| Tracking         | Blocked |
| Pickup           | Blocked |
| Return Shipment  | Blocked |

**Overall Result:** Pass (with Tracking, Pickup, and Return Shipment blocked by bugs)

**Additional Notes:** Tested with DE production credentials against `onlinetools.ups.com`. 4 bugs found — see Bugs section.
