# Carrier Testing Template

This is the universal blueprint for testing of carrier integrations. Use this template to generate a carrier-specific testing document.

---

## How to Use This Template

1. **Generate the carrier file**: Copy this template and rename it to `<carrier_name>.md` (e.g., `dpd_meta.md`). Before using it, go through the carrier's connector code (`modules/connectors/<carrier_name>/`) to **pre-fill** all details:
   - List all available **services** in the Service Coverage table (from `units.py`)
   - Mark each section as `Supported`, `Not Supported`, or `N/A` based on which proxy methods exist in `proxy.py`
   - The goal is a **ready-to-test** document — the tester only needs to test cases and check boxes, no research required
2. **Fill in the metadata** section with carrier details
3. **Run through each test case** from the UI (Karrio Dashboard) and check off passed items
4. **Add notes** for any failures, edge cases, or unexpected behavior
5. **Record the environment** (sandbox/production) 

> **Formatting note**: Keep table columns aligned with consistent padding for readability in raw markdown.

---

## Metadata

| Field                      | Value                                |
|----------------------------|--------------------------------------|
| **Carrier Name**           | `<carrier_name>`                     |
| **Carrier Display Name**   | `<Display Name>`                     |
| **Environment**            | Sandbox / Production                 |
| **Connection Credentials** | Test account configured in Dashboard |
| **Last Tested**            | YYYY-MM-DD                           |

---

## 1. Connection Setup

> Verify the carrier can be connected and authenticated.

- [ ] Carrier connection created successfully in Dashboard
- [ ] Authentication succeeds (no credential errors)
- [ ] Connection appears in carrier list

**Notes:**

---

## 2. Rating / Rate Fetching

> Test rate retrieval for shipments. Carriers either provide a **live rate endpoint** or use a **rate sheet** (CSV-based static rates).

**Rate Type:** `Live API Endpoint` / `Rate Sheet` / `Not Supported`

### If Live API Endpoint:
- [ ] Fetch domestic rates successfully
- [ ] Fetch international rates successfully (if applicable)
- [ ] Rates returned for all expected services

### If Rate Sheet:
- [ ] Rate sheet uploaded/configured
- [ ] Rates fetched correctly based on weight and destination
- [ ] All configured services return rates

**Notes:**

---

## 3. Shipping / Shipment Creation

> Test creating shipments and generating labels.

**Supported:** `Yes` / `No`

### Basic Shipment
- [ ] Create domestic shipment with default service
- [ ] Label generated and downloadable as PDF
- [ ] Tracking number returned in response
- [ ] Shipment appears in shipment list

### Service Coverage
- [ ] Create shipment with each available service (list services tested below)

| Service Code | Service Name | Result     |
|--------------|--------------|------------|
|              |              | Pass / Fail |

### Multi-Piece Shipment
- [ ] Create shipment with 2+ parcels
- [ ] All parcel tracking numbers returned
- [ ] Combined label generated

### International Shipment (if applicable)
- [ ] Create international shipment

**Notes:**

---

## 4. Label

> Test label output options.

**Supported:** `Yes` / `No`

- [ ] Label downloads as PDF
- [ ] Label format matches requested format (PDF / ZPL / PNG)
- [ ] Label contains correct shipper and recipient info

**Notes:**

---

## 5. Shipment Cancellation

> Test cancelling/voiding shipments.

**Supported:** `Yes` / `No`

- [ ] Cancel a newly created shipment
- [ ] Shipment status updates to cancelled
- [ ] Cancel shipment that has no pickup
- [ ] Cancel shipment that has an active pickup (should warn)
- [ ] Cancel shipment after pickup is already cancelled

**Notes:**

---

## 6. Tracking

> Test tracking shipment status.

**Supported:** `Yes` / `No`

- [ ] Track a shipment by tracking number
- [ ] Tracking events returned with timestamps
- [ ] Tracking status reflects current state (in_transit, delivered, etc.)

**Notes:**

---

## 7. Pickup Scheduling

> Test scheduling and managing pickups.

**Supported:** `Yes` / `No`

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

**Notes:**

---

## 8. Return Shipment

> Test return shipment creation if supported.

**Supported:** `Yes` / `No` / `N/A`

- [ ] Create return shipment
- [ ] Return label generated
- [ ] Return tracking number provided

**Notes:**

---

## Edge Cases & Error Handling

> General robustness checks.

- [ ] Invalid credentials show clear error message
- [ ] Missing required fields return descriptive validation errors
- [ ] Duplicate shipment creation handled

**Notes:**

---

## Summary

| Feature          | Status            |
|------------------|-------------------|
| Connection Setup | Pass / Fail / N/A |
| Rating           | Pass / Fail / N/A |
| Shipping         | Pass / Fail / N/A |
| Label            | Pass / Fail / N/A |
| Cancellation     | Pass / Fail / N/A |
| Tracking         | Pass / Fail / N/A |
| Pickup           | Pass / Fail / N/A |
| Return Shipment  | Pass / Fail / N/A |

**Overall Result:** Pass / Fail / Partial

**Additional Notes:**
