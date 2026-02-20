# DHL Parcel DE — Carrier Testing

## Metadata

| Field                      | Value                                |
|----------------------------|--------------------------------------|
| **Carrier Name**           | `dhl_parcel_de`                      |
| **Carrier Display Name**   | DHL Parcel Germany                   |
| **Environment**            | Production                           |
| **Connection Credentials** | Production account configured in Dashboard |

---

## 1. Connection Setup

> Verify the carrier can be connected and authenticated. DHL Parcel DE uses OAuth2 (ROPC grant) with `client_id`, `client_secret`, `username`, and `password`.

- [x] Carrier connection created successfully in Dashboard
- [x] Authentication succeeds (no credential errors)
- [x] Connection appears in carrier list

**Notes:**

---

## 2. Rating / Rate Fetching

> DHL Parcel DE uses a **rate sheet** (CSV-based static rates via `RatingMixinProxy`), not a live rate endpoint.

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
- [ ] Create shipment with each available service (list services tested below)

| Service Code                              | Service Name                   | Carrier Code | Result      |
|-------------------------------------------|--------------------------------|--------------|-------------|
| dhl_parcel_de_paket                       | DHL Paket                      | V01PAK       | Pass        |
| dhl_parcel_de_kleinpaket                  | DHL Kleinpaket                 | V62KP        | Blocked     |
| dhl_parcel_de_europaket                   | DHL Europaket                  | V54EPAK      | Blocked     |
| dhl_parcel_de_paket_international         | DHL Paket International        | V53WPAK      | Blocked     |
| dhl_parcel_de_warenpost_international     | DHL Warenpost International    | V66WPI       | Blocked     |

### Multi-Piece Shipment
- [x] Create shipment with 2+ parcels
- [x] All parcel tracking numbers returned
- [x] Combined label generated

### International Shipment (if applicable)
- [ ] Create international shipment with customs info

**Notes:** None of the default sandbox billing numbers work against the production API. V01PAK (DHL Paket domestic) only works after manually configuring the billing number provided with the production credentials. All other services (V62KP, V54EPAK, V53WPAK, V66WPI) return `"The selected billing number is invalid."` — the provided credentials only include a billing number valid for PAKET. DHL requires service-specific billing numbers configured via `service_billing_numbers` in connection config. Blocked pending valid billing numbers for these services.

---

## 4. Label

> Test label output options. DHL Parcel DE supports PDF and ZPL2 formats in multiple layout sizes.

**Supported:** `Yes`

- [x] Label downloads as PDF
- [x] Label format matches requested format (PDF / ZPL)
- [x] Label contains correct shipper and recipient info

**Available label formats:** `PDF_A4`, `ZPL2_A4`, `PDF_910-300-700`, `ZPL2_910-300-700`, `PDF_910-300-600`, `ZPL2_910-300-600`, and others.

**Notes:**

---

## 5. Shipment Cancellation

> Test cancelling/voiding shipments via `DELETE /v2/orders`.

**Supported:** `Yes`

- [x] Cancel a newly created shipment
- [x] Shipment status updates to cancelled
- [x] Cancel shipment that has no pickup
- [x] Cancel shipment that has an active pickup (correctly blocks with warning to cancel pickup first)
- [x] Cancel shipment after pickup is already cancelled

**Notes:** DHL automatically manifests (closes out) shipments at a fixed time each day (e.g., 6 PM, configured per account) — this is called "Tagesabschluss". Once manifested, shipments return `UNKNOWN_SHIPMENT_NUMBER` and cannot be cancelled. This is documented DHL API behavior: "Deletion of shipments is only possible prior to them being manifested." Cancellation must be done before the daily closeout. (Ref: `parcel-de-shipping-v2_2.yaml`, DELETE /orders and POST /manifests descriptions)

---

## 6. Tracking

> Test tracking shipment status. DHL Parcel DE uses a dedicated XML-based Tracking API with HTTP Basic Auth + XML credentials.

**Supported:** `Yes`

- [x] Track a shipment by tracking number (single-piece)
- [x] Tracking events returned with timestamps
- [x] Tracking status reflects current state (in_transit, delivered, etc.)
- [ ] Track multi-piece shipment

**Notes:** Production tracking works — verified via both direct API call and Karrio UI tracker refresh (returns `code="0"` with full tracking data). Initial refresh after shipment creation may return `code="100"` ("No data found") due to DHL indexing delay — tracking data becomes available after DHL processes the shipment (can take minutes to hours). Subsequent refreshes succeed once DHL has indexed the tracking number. Karrio auto-creates a tracker with a synthetic "Label created" event on shipment creation; the DHL tracking API is only called on tracker refresh with a 1-minute cooldown between calls.

---

## 7. Pickup Scheduling

> Test scheduling and managing pickups via the DHL Parcel DE Pickup API v3.

**Supported:** `Yes`

### Schedule Pickup
- [x] Schedule pickup with valid address and date
- [x] Confirmation number returned
- [x] Pickup appears in pickup list

### Pickup with Shipment
- [x] Schedule pickup associated with a shipment
- [x] Schedule pickup without an associated shipment (standalone)

### Cancel Pickup
- [x] Cancel a scheduled pickup
- [x] Pickup status updates to cancelled

**Notes:**

---

## 8. Return Shipment

> DHL Parcel DE supports return labels via DHL Retoure options on shipment creation.

**Supported:** `Yes` (via shipping options on shipment creation)

- [ ] Create shipment with return label enabled (`dhl_parcel_de_return_enabled`)
- [ ] Return label generated alongside shipping label
- [ ] Return tracking number provided

**Notes:** Returns are configured via shipping options (`dhl_parcel_de_return_enabled`, `dhl_parcel_de_return_receiver_id`, `dhl_parcel_de_return_billing_number`) rather than a separate return endpoint. Implementation is verified correct, request properly includes `dhlRetoure` VAS with return address. Blocked: current account does not have a retoure-enabled billing number. DHL returns `"The billing number entered is not available for returns."`. Requires a retoure-specific billing number from DHL.

---

## Shipping Options Reference

> Key shipping options available for testing.

| Option                                           | Type   | Description                                  |
|--------------------------------------------------|--------|----------------------------------------------|
| `dhl_parcel_de_preferred_neighbour`              | string | Preferred neighbour for delivery             |
| `dhl_parcel_de_preferred_location`               | string | Preferred drop-off location                  |
| `dhl_parcel_de_preferred_day`                    | string | Preferred delivery day (YYYY-MM-DD)          |
| `dhl_parcel_de_named_person_only`                | bool   | Delivery only to the named recipient         |
| `dhl_parcel_de_signed_for_by_recipient`          | bool   | Require signature from recipient             |
| `dhl_parcel_de_no_neighbour_delivery`            | bool   | Do not deliver to neighbours                 |
| `dhl_parcel_de_additional_insurance`             | float  | Additional insurance value in EUR            |
| `dhl_parcel_de_bulky_goods`                      | bool   | Mark shipment as bulky goods                 |
| `dhl_parcel_de_cash_on_delivery`                 | float  | Cash on delivery amount in EUR               |
| `dhl_parcel_de_premium`                          | bool   | Premium shipping service                     |
| `dhl_parcel_de_closest_drop_point`               | bool   | Deliver to closest drop point (CDP)          |
| `dhl_parcel_de_visual_check_of_age`              | enum   | Age check at delivery (A16 or A18)           |
| `dhl_parcel_de_endorsement`                      | enum   | Action if delivery fails (RETURN / ABANDON)  |
| `dhl_parcel_de_postal_delivery_duty_paid`        | bool   | Sender pays customs duties (pDDP)            |
| `dhl_parcel_de_has_electronic_export_notification`| bool  | Electronic export notification (EEN)         |

---

## Edge Cases & Error Handling

> General robustness checks.

- [x] Invalid credentials show clear error message
- [x] Missing required fields return descriptive validation errors
- [x] Duplicate shipment creation handled

**Notes:** Invalid credentials return `401` with `"API Authentication failed: Invalid client identifier"`. Missing required fields (recipient, parcels, address fields) return descriptive per-field validation errors (e.g., `"recipient.city: This field is required."`). Re-purchasing an already purchased shipment returns `"The shipment is 'purchased' and cannot be purchased again"`. Note: rating uses rate sheets (not live API) so invalid credentials don't affect rate fetching.

---

## Summary

| Feature          | Status  |
|------------------|---------|
| Connection Setup | Pass    |
| Rating           | Pass    |
| Shipping         | Partial |
| Label            | Pass    |
| Cancellation     | Pass    |
| Tracking         | Pass    |
| Pickup           | Pass    |
| Return Shipment  | Blocked |

**Overall Result:** Partial

**Additional Notes:** Testing was done in production mode (`api-eu.dhl.com`) — test mode (`api-sandbox.dhl.com`) fails authentication because the credentials are production credentials, not sandbox credentials. Shipping is partial because only the V01PAK (DHL Paket domestic) service works with the current account. All other services and return shipments are blocked due to missing service-specific billing numbers. Multi-piece shipment, tracking, cancellation, pickup scheduling/cancellation, label generation, and error handling all work correctly. The tracking API has a known indexing delay for newly created shipments.
