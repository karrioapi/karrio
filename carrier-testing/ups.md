# UPS — Carrier Testing

## Metadata

| Field                      | Value                                |
|----------------------------|--------------------------------------|
| **Carrier Name**           | `ups`                                |
| **Carrier Display Name**   | UPS                                  |
| **Environment**            | Production (`onlinetools.ups.com`)   |
| **Connection Credentials** | DE production account configured in Dashboard |
| **Last Tested**            | 2026-03-03                           |

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

**Notes:** DE domestic returns 5 services in EUR (Standard, Saver, Express 12:00, Express, Express Plus). DE→US returns 4 international services. DE→FR EU cross-border returns 4 services.

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

**Notes:** International shipments (DE→US) require `shipment_description` in options — without it UPS returns `120512: "Shipment Description is required"`. EU cross-border (DE→FR) now works with phone numbers after Bug 4 fix.

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

**Notes:**

---

## 6. Tracking

> Test tracking shipment status via `GET /api/track/v1/details/{tracking_number}`.

**Supported:** `Yes`

- [x] Track a shipment by tracking number
- [x] Tracking events returned with timestamps
- [x] Tracking status reflects current state (in_transit, delivered, etc.)

**Notes:** Bug 3 fixed (merged in patch-2026.1.16) — `transId` and `transactionSrc` headers now included. Tested with freshly created shipment — returns `pending` status with "Label created" event.

---

## 7. Pickup Scheduling

> Test scheduling and managing pickups via `/api/pickupcreation/v2409/pickup`.

**Supported:** `Yes` (US/CA/PR only by default — see Bug 1 note)

### Schedule Pickup
- [x] Schedule pickup with valid address and date (US address)
- [x] Confirmation number returned
- [x] Pickup appears in pickup list

### Pickup with Shipment
- [ ] Schedule pickup associated with a shipment
- [x] Schedule pickup without an associated shipment (standalone)

### Cancel Pickup
- [x] Cancel a scheduled pickup
- [x] Pickup status updates to cancelled

**Notes:** Pickup works for US/CA/PR with default service code `"001"`. For DE and other countries, UPS returns `9510119: "Invalid service designation"` — the valid pickup service codes for non-US countries are not publicly documented (behind UPS Developer Portal appendix). Users can now override via `ups_pickup_service_code` option after Bug 1 fix.

---

## 8. Return Shipment

> Test return shipment creation. UPS supports returns via `ups_return_service` shipping option on shipment creation.

**Supported:** `Yes`

- [x] Create return shipment
- [x] Return label generated
- [x] Return tracking number provided

**Available return service codes:**
- `ups_print_and_mail` (2)
- `ups_return_1_attempt` (3)
- `ups_return_3_attempt` (5)
- `ups_electronic_return_label` (8)
- `ups_print_return_label` (9)
- `ups_exchange_print_return_label` (10)

**Notes:** Bug 2 fixed (merged in patch-2026.1.16) — null `ShippingLabel` no longer crashes. Return requests require `description` on parcels and `shipment_description` in options. Tested with `ups_print_return_label` — tracking number and label URL returned successfully.

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
| `ups_pickup_service_code`                 | string  | Override pickup service code (3-char, see Section 7) |

---

## Edge Cases & Error Handling

> General robustness checks.

- [x] Invalid credentials show clear error message
- [x] Missing required fields return descriptive validation errors
- [x] Duplicate shipment creation handled

**Notes:**

---

## Bugs Found

> Bugs discovered during testing.

### Bug 1: Pickup not working for non-US countries
**Impact:** Scheduling pickups for DE/EU addresses failed with `"Invalid service designation"`.
**Root Cause:** Pickup service code option override was non-functional — always defaulted to US-only code.
**Status:** Fixed — US/CA/PR work by default, other countries can override via `ups_pickup_service_code` option.

### Bug 2: Return shipment creation crashed
**Impact:** Creating return shipments caused a server error (`'NoneType' object has no attribute 'ImageFormat'`).
**Root Cause:** Label parser didn't handle return shipments where no shipping label is returned.
**Status:** Fixed

### Bug 3: Tracking always failed
**Impact:** All tracking requests returned `"Missing transId"` error.
**Root Cause:** Required UPS Tracking API headers were dropped during a proxy rewrite.
**Status:** Fixed

### Bug 4: EU cross-border shipments rejected phone numbers
**Impact:** Shipments between EU countries (e.g., DE→FR) failed with `"ShipTo phone number cannot be more than 15 digits long"`, even with valid numbers.
**Root Cause:** Karrio reformats phone numbers to international format (adding `+CC` and spaces), which can exceed UPS's 15-character limit.
**Status:** Fixed — phone numbers now conform to UPS's 15-character field limit before submission.

---

## Summary

| Feature          | Status  |
|------------------|---------|
| Connection Setup | Pass    |
| Rating           | Pass    |
| Shipping         | Pass    |
| Label            | Pass    |
| Cancellation     | Pass    |
| Tracking         | Pass    |
| Pickup           | Partial |
| Return Shipment  | Pass    |

**Overall Result:** Pass (Pickup partial — works for US/CA/PR, DE pickup codes not publicly documented)

**Additional Notes:** Tested with DE production credentials against `onlinetools.ups.com`. 4 bugs found and fixed — see Bugs section.
