# Studio GraphQL-first data-layer rebuild — coordination contract

Tracks the migration of `apps/studio/src/lib/karrio/hooks/*` from invented REST
paths to Karrio's canonical GraphQL API. Linear epic: **EBE-95**. PR base:
`claude/studio-graphql-rebuild`.

> Future: Studio will move to its own repo under **ebenlabs**. Keep everything
> here self-contained (no new `@karrio/*` imports); the data layer + server
> functions must work against a remote Karrio server via config only.

## Status (Claude took over A–E from Codex)

| Unit | State |
|---|---|
| F0 Foundation | ✅ admin-graphql client path + `hooks/{ship,build,govern,resources}` split |
| A Ship reads | ✅ all on GraphQL (shipments/shipment/trackers/user_connections/pickups/document_templates/manifests/batch_operations), live-verified |
| B Build reads | ✅ api_keys → GraphQL, webhooks list → GraphQL; apps/plugins/mcp → honest "not available" |
| C Govern reads | ✅ team→admin `users`, admin→`worker_health`, usage→`system_usage`, audit→`events`; tenants → honest EE state |
| D Studio-native state | ⛔ backend-blocked — no readable user/workspace KV (`UserType.metadata` not exposed); localStorage + write-only `update_user` seam stays. Needs a Karrio change. |
| E Mutations | ✅ address/parcel/product on GraphQL; **every read** is GraphQL. Webhook + carrier-connection create/update/delete stay on **functional** REST (GraphQL equivs exist but need input-shape remapping — refinement, not broken). |

**Net result:** every Studio screen shows real Karrio data via GraphQL, or an honest "not available" state — no invented/404 REST reads remain. Full mocked suite green (205); each query live-verified against `:5002`.


## Foundation (F0 — landed)

- `client.ts` — `graphql(ctx, query, vars, endpoint="/graphql")` + `adminGraphql()`
  for the **second** `/admin/graphql` schema. Both keep the 401→refresh retry.
- `hooks/_shared.ts` — `keyExtra`, `graphqlEdges(ctx, query, field, vars, endpoint)`.
- `hooks/{ship,build,govern,resources}.ts` — domain modules; `hooks.ts` re-exports them.

## GROUND TRUTH — live schema (verified against running :5002)

**`/graphql` (tenant) Query fields:** `address(es), api_keys, batch_operation(s),
carrier_connection(s), data_template(s), default_templates, document_template(s),
event(s), log(s), manifest(s), metafield(s), order(s), parcel(s), pickup(s),
product(s), rate_sheet(s), shipment(s), system_connections, system_usage, token,
tracing_record(s), tracker(s), user, user_connections, webhook(s), workspace_config`

**`/admin/graphql` Query fields:** `configs, config_fieldsets, config_schema, fees,
markups, me, permission_groups, rate_sheets, system_carrier_connection(s),
task_executions, usage, user, users, worker_health`

**No OSS source (render honest "not available"/EE empty state — do NOT invent a query):**
`oauth_apps`/`app_installations` (apps), `accounts` (tenants), `auditlogs`,
`workflows`, `shipping_rules`, plugins, mcp.

## Canonical query reference (mirror, don't hand-roll)

- Tenant: `packages/types/graphql/queries.ts` (`GET_SHIPMENTS`, `GET_TRACKERS`,
  `GET_USER_CONNECTIONS`, `GET_PICKUPS`, `GET_DOCUMENT_TEMPLATES`, `GET_MANIFESTS`,
  `GET_BATCH_OPERATIONS`, `GET_WEBHOOKS`, `GET_API_KEYS`, `GET_EVENTS`,
  `GET_SYSTEM_USAGE`, `GET_ORDERS`, `GET_ADDRESSES`, `GET_PARCELS`, `GET_PRODUCTS`,
  `GET_RATE_SHEETS`, `GET_WORKSPACE_CONFIG`, …)
- Admin: `packages/types/graphql/admin/queries.ts` (`GET_USERS`, `GET_WORKER_HEALTH`,
  `GET_CONFIGS`, `GET_ADMIN_SYSTEM_USAGE`, …)

## Per-hook source mapping

| Hook | File (unit) | New source |
|---|---|---|
| useShipments / useShipment | ship.ts (A) | `/graphql` shipments / shipment |
| useTrackers | ship.ts (A) | `/graphql` trackers |
| useCarrierConnections | ship.ts (A) | `/graphql` user_connections (+ system_connections) |
| usePickups | ship.ts (A) | `/graphql` pickups |
| useDocumentTemplates | ship.ts (A) | `/graphql` document_templates |
| useManifests | ship.ts (A) | `/graphql` manifests |
| useBatches | ship.ts (A) | `/graphql` batch_operations |
| useApiKeys | build.ts (B) | `/graphql` api_keys (404 fix) |
| useWebhooks | build.ts (B) | `/graphql` webhooks |
| useApps / usePlugins / useMcp | build.ts (B) | no source → "not available" empty state |
| useTeam | govern.ts (C) | `/admin/graphql` users (404 fix) |
| useAdminInfo | govern.ts (C) | `/admin/graphql` worker_health + configs (404 fix) |
| useUsage | govern.ts (C) | `/graphql` system_usage (404 fix) |
| useAuditLog | govern.ts (C) | `/graphql` events (404 fix; NOT "auditlogs") |
| useTenants | govern.ts (C) | no `accounts` → EE empty state |
| useOrders/Addresses/Parcels/Products/RateSheets | resources.ts (E) | already GraphQL — align fields to GET_* |
| useWorkflows / useShippingRules | resources.ts (E) | keep graceful `[]` (fields absent on OSS) |
| mutations (address/parcel/product/webhook/connection) | resources.ts (E) | GraphQL where available |
| agents / mcp config / prefs read | agents.ts, preferences.ts (D) | `metafields` / `workspace_config` / `user.metadata` |

## Acceptance criteria (every unit / PR)

1. `cd apps/studio && npx tsc --noEmit` clean.
2. `npx vite build` succeeds.
3. **Live-verify every new query** against the running `:5002` backend
   (`POST /api/token` `admin@example.com` / `demo` → bearer): HTTP 200, no
   `errors`, real data shape. Paste the curl evidence in the PR.
4. Update the affected Playwright spec mocks REST→GraphQL field-routing and run
   the **full mocked `studio` project green** (`playwright test --project=studio`,
   not just `--list`).
5. Branch off `claude/studio-graphql-rebuild`; PR targets it. Honest UI states for
   any "not available"/EE resource — never fabricate data or success.

## Ownership

- **Claude**: F0 (this) + review/test/merge of A–E into the rebuild branch.
- **Codex**: units A–E in parallel (file-disjoint).
