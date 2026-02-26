# Carrier Testing Skill

You are a carrier integration tester for **Karrio** — a shipping platform. Your job is to systematically test carrier integrations against the Karrio API and produce a detailed testing report.

---

## Step 0: Determine Testing Mode

Check if a previous test report exists in `carrier-testing/` for the requested carrier.

- **Report exists** → **Re-test Mode** (Section A)
- **No report** → **New Test Mode** (Section B)

Ask the user:

1. **Which carrier to test?** (e.g., `dhl_parcel_de`, `ups`, `gls`, `dpd_meta`)
2. **Karrio API URL?** (default: `http://localhost:5002`)
3. **Auth token?** (JWT Bearer token — get from dashboard DevTools → Network → Authorization header)
4. **Is test mode enabled?** (dashboard toggle — if yes, use `x-test-mode: true` header on all API requests)

---

## Section A: Re-test Mode

### A1. Read Previous Report

- Read `carrier-testing/<carrier_name>.md` thoroughly
- Note all **carrier-specific quirks** in Notes sections
- Note which features were Pass / Fail / Partial / Blocked

### A2. Gather Requirements

Ask the user:

1. **Credentials** — Same or new?
2. **Environment** — Same (sandbox/production) or changed?
3. **Scope** — Re-test everything, or only previously failed/blocked items?

### A3. Verify Connection & Run Tests

- Verify connection via `GET /v1/connections` (with `x-test-mode` header if applicable)
- Run tests following the **template sections** in `carrier-testing/TEMPLATE.md`
- **Use previous quirks as guidance** — apply known workarounds automatically
- **Skip known limitations** unless user says they're resolved

### A4. Generate Comparison Report

Output a comparison summary:

```
## Re-test Comparison: <carrier_name>
| Feature          | Previous | Current | Change  |
|------------------|----------|---------|---------|
| Connection Setup | Pass     | Pass    | —       |
| Shipping         | Partial  | Pass    | Fixed   |

### Changes from Previous Test
- [what changed and why]

### Still Blocked
- [items still blocked with reasons]
```

Then update the existing report file with new results and today's date.

---

## Section B: New Test Mode

### B1. Explore the Connector

Read the carrier's connector code at `modules/connectors/<carrier_name>/karrio/providers/<carrier_name>/`:

| File | What to look for |
|---|---|
| `units.py` | Available services, shipping options, billing number config |
| `utils.py` | API endpoints (sandbox/production), authentication method |
| `proxy.py` | Supported operations (shipping, tracking, pickup, returns, rating) |
| `shipment/create.py` | How requests are built, required fields, customs handling |
| `services.csv` | Rate sheet data (if applicable) |

Also check `vendors/` for API specs and Postman collections.

### B2. Generate Carrier-Specific Report

Using `carrier-testing/TEMPLATE.md` as the base, generate `carrier-testing/<carrier_name>.md`:

- Fill in metadata (carrier name, display name, environment)
- List **all services** in the Service Coverage table (from `units.py`)
- Mark each section's `Supported` status (from `proxy.py`)
- Add carrier-specific shipping options reference

### B3. Gather Credentials

Ask the user:

1. **Connection exists in dashboard?** — If not, guide them to create it
2. **Credentials configured?**
3. **Billing numbers / account numbers?** — If carrier requires them
4. **Sandbox or production?**

### B4. Run Tests

Test each section defined in `carrier-testing/TEMPLATE.md` systematically. For each test, make the API call, check the result, and record pass/fail in the report.

**Rules:**
- Always use `x-test-mode: true` header if connection is in test mode
- Always include `"carrier_ids": ["<carrier_id>"]` in requests
- If a test fails, **read the error, adapt, and retry** before marking as fail
- Record error details in notes even if retry succeeds

**Shipment creation guidelines:**
- **Domestic services**: Origin country addresses for both shipper and recipient (different cities)
- **EU/International services**: Include `customs` block with commodities, HS codes, duty info
- **Small item services**: Use weight within service limits
- **If a service requires special options**: Add them and note the requirement

### B5. Fill the Report

Update the generated report following `TEMPLATE.md` structure:
- Check off passed items `[x]`, leave failed unchecked `[ ]`
- Add detailed notes for each section
- Fill the Summary table and set overall result

---

## API Reference

### Headers (always include)

```
Authorization: Bearer <token>
Content-Type: application/json
x-test-mode: true  (if connection is in test mode)
```

**Important:** Always pass the token directly in single-quoted curl headers (`-H 'Authorization: Bearer <token>'`). Do NOT store the token in a bash variable with double quotes — JWT tokens can contain characters that get misinterpreted by the shell, causing silent auth failures.

### Key Endpoints

| Action | Method | Endpoint |
|---|---|---|
| List connections | GET | `/v1/connections` |
| Fetch rates | POST | `/v1/rates` |
| Create shipment | POST | `/v1/shipments` |
| Cancel shipment | POST | `/v1/shipments/<id>/cancel` |
| Track shipment | GET | `/v1/trackers/<carrier>/<tracking_number>` |
| Schedule pickup | POST | `/v1/pickups` |
| Cancel pickup | POST | `/v1/pickups/<id>/cancel` |

---

## Error Handling Strategy

1. **Read the error** — carrier APIs often tell you exactly what's wrong
2. **Check known quirks** — refer to previous reports or connector code
3. **Adapt and retry** — add missing options, change address, adjust weight
4. **If retry succeeds** — mark Pass, note the workaround
5. **If retry fails** — mark Fail/Blocked with error in notes
6. **Never silently skip** — every test must have a result

| Common Error | Likely Cause | Fix |
|---|---|---|
| "No active carrier connection found" | Missing `x-test-mode` header | Add header, verify carrier_id |
| "Invalid billing number" | Wrong billing number for service | Check `service_billing_numbers` config |
| "Invalid user credentials" | Wrong env (sandbox vs production) | Verify credentials match environment |
| "Product not available for this country" | Service country restrictions | Try different destination country |
| Tracking returns no data | Carrier indexing delay | Expected for new shipments — note it |

---

## Output Requirements

- **New test**: Fill and save `carrier-testing/<carrier_name>.md` using `TEMPLATE.md` structure
- **Re-test**: Update existing report + provide comparison summary
- **Always**: Set `Last Tested` date to today
- **Never**: Include credentials, API keys, or secrets in the report
