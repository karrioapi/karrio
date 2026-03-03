# PRD: Tracing HTTP Headers Enrichment

**Status:** Draft  
**Branch:** `feat/tracing-http-headers-enrichment`  
**Repo:** karrioapi/karrio  
**Owner:** Daniel K  
**Date:** 2026-03-02  

---

## 1. Problem Statement

Karrio's tracing system records carrier API request/response bodies (in `TracingRecord.record`) and inbound API calls (in `APILogIndex`), but **HTTP headers are not captured anywhere**. This creates significant debugging blind spots:

- **Carrier auth failures** — cannot tell if the `Authorization` header was missing, malformed, or expired
- **Rate limit diagnosis** — carrier response headers like `X-RateLimit-Remaining` or `Retry-After` are lost
- **Content negotiation issues** — cannot verify what `Content-Type` or `Accept` was sent/received
- **Carrier-specific debugging** — many carriers (FedEx, UPS, DHL) return error codes in response headers
- **cURL reproducibility** — the "Copy as cURL" feature in devtools only includes `Content-Type`, so the generated command is not a faithful reproduction of the actual request (missing `Authorization`, `X-Api-Key`, custom carrier headers)

### Current State (from code analysis)

**`modules/sdk/karrio/core/utils/helpers.py` — `process_request` and `process_response`:**
- `process_request` traces `{ request_id, url, data }` — **no headers**
- `process_response` traces `{ request_id, response }` — **no headers**
- `request_with_response()` already captures `dict(f.headers)` on success and `dict(e.headers)` on error — this data is available but discarded at the trace layer

**`TracingRecord` model (Django):**
- Fields: `key`, `record` (JSON), `timestamp`, `meta` (JSON), `test_mode`
- `record` stores `{ format, url, data, request_id }` for requests; `{ request_id, response/error }` for responses
- **No dedicated header fields**

**`packages/developers/components/views/logs-view.tsx` — `generateLogCurlCommand`:**
- Builds cURL from `log.method`, `log.host`, `log.path`, `log.query_params`, `log.data`
- Only appends `-H 'Content-Type: application/json'` — **hardcoded, no actual headers**

**`packages/developers/components/views/logs-view.tsx` and `tracing-records-view.tsx` — `generateTracingCurlCommand`:**
- Builds cURL from `record.url`, `record.format`, `record.data`
- Appends `Content-Type` only — **no auth headers, no carrier-specific headers**

---

## 2. Goals

| Goal | Success Metric |
|---|---|
| Capture request headers on all carrier API calls | `TracingRecord.record` includes `request_headers` for every carrier request |
| Capture response headers on all carrier API calls | `TracingRecord.record` includes `response_headers` for every carrier response/error |
| Sensitive headers redacted before storage | No plaintext secrets in DB; `Authorization: Bearer val_xxx` format |
| cURL copy includes headers | Generated cURL commands include all `-H` flags from the traced headers |
| No breaking changes | All new fields nullable; existing records unaffected |

### Non-Goals
- Capturing inbound karrio API request headers (the `APILogIndex` model — separate scope)
- Header-based filtering/search (future)
- Streaming response headers (chunked transfer encoding)

---

## 3. Architecture

### How carrier HTTP calls flow (from code analysis)

```
Carrier connector (e.g. fedex/rating.py)
  → lib.request(..., trace=self.settings.trace_as("carrier_name"), **kwargs)
     → helpers.process_request(request_id, trace, proxy, url=..., headers=..., data=...)
        → trace({ request_id, url, data }, "request")     ← headers NOT included here
        → urllib.request.Request(url, headers=..., data=...)
     → urlopen(_request) as f:
        → helpers.process_response(request_id, f, decoder, trace=trace)
           → trace({ request_id, response }, "response")  ← headers NOT included here
           ← f.headers available as dict(f.headers)       ← DISCARDED
```

The request headers are passed to `urllib.request.Request` as `kwargs["headers"]` but never forwarded to the trace callback. The response headers are read by `request_with_response()` but `process_response()` doesn't extract them from the response object.

### Fix: Thread headers through `process_request` and `process_response`

```python
# process_request — add headers to trace payload
trace({
    "request_id": request_id,
    "url": ...,
    "data": ...,
    "request_headers": redact_headers(kwargs.get("headers", {})),
}, "request")

# process_response — capture response headers
trace({
    "request_id": request_id,
    "response": ...,
    "response_headers": redact_headers(dict(response.headers)),
}, "response")
```

---

## 4. Sensitive Data Redaction

### Rules

Headers to fully redact (replace value with `val_xxx`):
- `Authorization` → e.g. `Bearer val_xxx` or `Basic val_xxx` (keep scheme prefix)
- `X-Api-Key`, `Api-Key`, `X-Auth-Token`, `X-Client-Secret`, `X-Password`
- Any header name containing `secret`, `password`, `token`, `credential`

Query param values to redact (used in some carriers like FedEx OAuth):
- `client_id`, `client_secret`, `username`, `password`, `api_key`, `access_token`

### Redaction format

```python
# Authorization: Bearer eyJhbGc... → Authorization: Bearer val_xxx
# Authorization: Basic dXNlcjpwYXNz → Authorization: Basic val_xxx  
# X-Api-Key: sk-abc123... → X-Api-Key: val_xxx
# client_secret=abc123 → client_secret=val_xxx
```

Keep the scheme prefix for Authorization (Bearer/Basic/etc.) for readability. All other sensitive headers: replace entire value with `val_xxx`.

---

## 5. Implementation Plan

### Step 1 — Redaction utility (new file)
**`modules/sdk/karrio/core/utils/redaction.py`**
- `redact_headers(headers: dict) -> dict`
- `redact_query_params(params: dict | str) -> dict | str`
- Unit tests: `modules/sdk/karrio/core/tests/test_redaction.py`

### Step 2 — Thread headers through tracing in `helpers.py`
**`modules/sdk/karrio/core/utils/helpers.py`**
- `process_request`: add `request_headers` (redacted) to trace payload
- `process_response`: extract `dict(response.headers)`, redact, add `response_headers` to trace payload
- `process_error`: extract `dict(error.headers)`, redact, add `response_headers` to trace payload
- `request_with_response`: already captures headers — expose `response_headers` in returned dict

### Step 3 — GraphQL: expose headers on TracingRecordType
**`modules/graph/karrio/server/graph/schemas/base/types.py`**
- Add `request_headers` and `response_headers` strawberry fields on `TracingRecordType`
- These are resolved from `self.record` (the stored JSON), not new model fields — **no migration needed**

### Step 4 — Dashboard: include headers in cURL copy
**`packages/developers/components/views/logs-view.tsx`**
- `generateLogCurlCommand`: add `-H` flags from `log.headers` (if available)
- `generateTracingCurlCommand`: add `-H` flags from `record.request_headers` (if available)

**`packages/developers/components/views/tracing-records-view.tsx`**  
- `generateTracingCurlCommand`: same as above

---

## 6. Data Changes

**No Django migration required.** Headers are stored inside the existing `record` JSONField:

```json
// TracingRecord.record for a "request" key — after this change:
{
  "format": "json",
  "request_id": "req_abc123",
  "url": "https://apis.fedex.com/rate/v1/rates/quotes",
  "data": { ... },
  "request_headers": {
    "Authorization": "Bearer val_xxx",
    "X-locale": "en_US",
    "Content-Type": "application/json"
  }
}

// TracingRecord.record for a "response" key — after this change:
{
  "request_id": "req_abc123",
  "response": "...",
  "response_headers": {
    "X-RateLimit-Remaining": "95",
    "Content-Type": "application/json",
    "X-B3-TraceId": "abc123"
  }
}
```

---

## 7. Open Questions

1. **Inbound karrio API headers** — Should we also capture `Authorization`, `X-Karrio-Org-Id`, `X-Request-Id` etc. on the `APILogIndex`? Deferred to a follow-up PR.
2. **Header size limits** — Some carriers return large headers (cookies, etc.). Should we cap stored headers at e.g. 50 fields or 10KB? Current proposal: no cap, trust the existing JSONField.
3. **Existing records** — Records before this change will have no `request_headers`/`response_headers` — the UI should handle this gracefully (show nothing if absent).

---

## 8. Files Changed

| File | Change |
|---|---|
| `modules/sdk/karrio/core/utils/redaction.py` | **NEW** — redaction utility |
| `modules/sdk/karrio/core/tests/test_redaction.py` | **NEW** — unit tests |
| `modules/sdk/karrio/core/utils/helpers.py` | Add headers to `process_request`, `process_response`, `process_error` trace payloads |
| `modules/graph/karrio/server/graph/schemas/base/types.py` | Add `request_headers` + `response_headers` to `TracingRecordType` |
| `packages/developers/components/views/logs-view.tsx` | Add `-H` flags in `generateLogCurlCommand` + `generateTracingCurlCommand` |
| `packages/developers/components/views/tracing-records-view.tsx` | Add `-H` flags in `generateTracingCurlCommand` |

No migrations required. No model changes.
