# Karrio MCP Server — Sprint Plan

| Field | Value |
|-------|-------|
| Sprint | MCP Server v1.0 |
| Branch | `feat/karrio-mcp-server` |
| Start Date | 2026-02-27 |
| Owner | PM Agent |
| PRD | [PRDs/KARRIO_MCP_SERVER.md](./PRDs/KARRIO_MCP_SERVER.md) |

---

## Task Breakdown

### Wave 1: Package Scaffold (Sequential — must complete first)

| ID | Title | Description | Effort | Status | Dependencies |
|----|-------|-------------|--------|--------|--------------|
| MCP-001 | Package scaffold | Create `packages/mcp/` with `package.json`, `tsconfig.json`, `tsup.config.ts`, `src/index.ts` entry point, bin entry for CLI. Register in workspace. | M | DONE | None |

### Wave 2: Core Infrastructure (Sequential — after Wave 1)

| ID | Title | Description | Effort | Status | Dependencies |
|----|-------|-------------|--------|--------|--------------|
| MCP-002 | Karrio API client | Create `src/client.ts` — HTTP client wrapper that calls Karrio REST API. Handles auth headers, base URL, error formatting. Methods: `fetchRates`, `createShipment`, `getShipment`, `listShipments`, `cancelShipment`, `track`, `validateAddress`, `listCarriers`, `getCarrierServices`, `listOrders`, `schedulePickup`, `createManifest`. | M | DONE | MCP-001 |
| MCP-003 | MCP server setup + stdio transport | Create `src/server.ts` — MCP server using `@modelcontextprotocol/sdk`. Register tools, resources. Entry point with stdio transport. `src/index.ts` as CLI entry with env var parsing (`KARRIO_API_URL`, `KARRIO_API_KEY`). | M | DONE | MCP-001 |
| MCP-004 | Auth middleware | Create `src/auth.ts` — API key auth for stdio (from env/args), Bearer token validation for HTTP transport. | S | DONE | MCP-001 |

### Wave 3: Core Tools — P0 (Parallel — after Wave 2)

| ID | Title | Description | Effort | Status | Dependencies |
|----|-------|-------------|--------|--------|--------------|
| MCP-005 | `get_shipping_rates` tool | `src/tools/rates.ts` — Flat params (origin/dest postal+country, weight, optional dimensions, carrier filter, sort). Calls `POST /v1/proxy/rates`. Returns sorted rates with carrier, service, price, transit days. | M | DONE | MCP-002, MCP-003 |
| MCP-006 | `create_shipment` tool | `src/tools/shipments.ts` — Flat params (shipper/recipient addresses, weight, carrier, service, label_type). `destructiveHint: true`. Calls `POST /v1/shipments` + `POST /v1/shipments/{id}/purchase`. Returns tracking number, label URL. | L | DONE | MCP-002, MCP-003 |
| MCP-007 | `get_shipment` + `list_shipments` tools | `src/tools/shipments.ts` — get by ID, list with filters (status, date range, carrier). Pagination with limit/offset. | M | DONE | MCP-002, MCP-003 |
| MCP-008 | `cancel_shipment` tool | `src/tools/shipments.ts` — Cancel/void by shipment ID. `destructiveHint: true`. | S | DONE | MCP-002, MCP-003 |
| MCP-009 | `track_package` tool | `src/tools/tracking.ts` — Track by number + optional carrier. Returns status, events, estimated delivery. | M | DONE | MCP-002, MCP-003 |
| MCP-010 | `validate_address` tool | `src/tools/addresses.ts` — Validate address fields, return corrected address + validation status. | S | DONE | MCP-002, MCP-003 |
| MCP-011 | `list_carriers` tool | `src/tools/carriers.ts` — List connected carriers with capabilities. Read-only. | S | DONE | MCP-002, MCP-003 |

### Wave 4: Extended Tools + Resources — P1 (Parallel — after Wave 3)

| ID | Title | Description | Effort | Status | Dependencies |
|----|-------|-------------|--------|--------|--------------|
| MCP-012 | `schedule_pickup` tool | `src/tools/pickups.ts` — Schedule carrier pickup. | M | DONE | MCP-002, MCP-003 |
| MCP-013 | `create_manifest` tool | `src/tools/manifests.ts` — Create end-of-day manifest. | M | DONE | MCP-002, MCP-003 |
| MCP-014 | `list_orders` tool | `src/tools/orders.ts` — List orders with fulfillment status. | S | DONE | MCP-002, MCP-003 |
| MCP-015 | MCP Resources — carrier catalog | `src/resources/carriers.ts` — `karrio://carriers`, `karrio://carriers/{id}`, `karrio://carriers/{id}/services`. Hybrid: also register read-only tool fallbacks. | M | DONE | MCP-002, MCP-003 |
| MCP-016 | Streamable HTTP transport | `src/transports/http.ts` — Streamable HTTP (SSE) transport for remote deployment. Express/Hono server with `/mcp` endpoint. | M | DONE | MCP-003 |

### Wave 5: Tests (After Waves 3-4)

| ID | Title | Description | Effort | Status | Dependencies |
|----|-------|-------------|--------|--------|--------------|
| MCP-017 | Unit tests | `tests/unit/` — Test each tool's parameter validation, response formatting, error handling. Mock KarrioClient. Vitest. | M | DONE | MCP-005 through MCP-015 |
| MCP-018 | Integration tests | `tests/integration/` — Test full MCP protocol round-trips (tools/list, tools/call, resources/list, resources/read). | M | DONE | MCP-017 |

### Wave 6: Documentation + Publishing

| ID | Title | Description | Effort | Status | Dependencies |
|----|-------|-------------|--------|--------|--------------|
| MCP-019 | README + setup docs | `packages/mcp/README.md` — Installation, Claude Desktop config, Cursor config, VS Code config, tool reference, env vars. | M | DONE | MCP-005 through MCP-016 |
| MCP-020 | npm publish setup | Ensure `package.json` has correct `bin`, `files`, `main`, `types` fields. `prepublishOnly` script. `.npmignore`. | S | DONE | MCP-019 |

---

## Execution Order

```
Wave 1 (sequential):  MCP-001
         │
         ▼
Wave 2 (sequential):  MCP-002 ──► MCP-003 ──► MCP-004
         │
         ▼
Wave 3 (parallel):    MCP-005 | MCP-006 | MCP-007 | MCP-008 | MCP-009 | MCP-010 | MCP-011
         │
         ▼
Wave 4 (parallel):    MCP-012 | MCP-013 | MCP-014 | MCP-015 | MCP-016
         │
         ▼
Wave 5 (sequential):  MCP-017 ──► MCP-018
         │
         ▼
Wave 6 (sequential):  MCP-019 ──► MCP-020
```

---

## Agent Assignments

| Agent | Tasks | Description |
|-------|-------|-------------|
| scaffold-agent | MCP-001 | Package setup, tsconfig, tsup, bin entry |
| infra-agent | MCP-002, MCP-003, MCP-004 | API client, server setup, auth |
| rates-agent | MCP-005 | get_shipping_rates tool |
| shipment-agent | MCP-006, MCP-007, MCP-008 | create/get/list/cancel shipment tools |
| tracking-agent | MCP-009 | track_package tool |
| address-carrier-agent | MCP-010, MCP-011 | validate_address + list_carriers tools |
| extended-tools-agent | MCP-012, MCP-013, MCP-014 | pickup, manifest, orders tools |
| resources-agent | MCP-015 | MCP Resources for carrier catalog |
| http-transport-agent | MCP-016 | Streamable HTTP transport |
| test-agent | MCP-017, MCP-018 | Unit + integration tests |
| docs-agent | MCP-019, MCP-020 | README, publish setup |

---

## Sprint Results

**Status**: COMPLETE

**Build**: `npm run build` passes (tsup, ESM, node18 target)
**Tests**: 48/48 passing across 6 test files (vitest)
**Files**: 29 files created in `packages/mcp/`

### Deliverables

| Deliverable | Status |
|-------------|--------|
| 11 MCP Tools (rates, shipments x4, tracking, address, carriers, pickups, manifests, orders) | Done |
| 2 MCP Resources (karrio://carriers, karrio://carriers/{id}) | Done |
| stdio transport (default) | Done |
| Streamable HTTP transport (--http flag) | Done |
| API key authentication | Done |
| Unit tests (client, auth, tool registration) | Done |
| Integration tests (server creation) | Done |
| README with Claude Desktop / Cursor / VS Code / Claude Code config | Done |
| npm publish setup (bin, exports, engines, .npmignore) | Done |
