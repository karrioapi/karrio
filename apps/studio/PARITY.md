# Karrio Studio ↔ Dashboard — Feature Parity Audit

Explicit mapping of the legacy Next.js dashboard surface (derived from
`packages/hooks/*`, `packages/core`, `packages/admin`, `packages/developers`,
and `apps/dashboard` routes) to Karrio Studio (`apps/studio`).

Legend: ✅ implemented · 🟡 partial · ⛔ not yet (roadmap) · ➕ net-new in Studio

## Ship (operations)

| Dashboard feature | Hook(s) | Studio | Status |
|---|---|---|---|
| Shipments list + detail | `shipment`, `bulk-shipments` | Shipments + ShipmentSheet | ✅ |
| Create label / buy rate | `label-data`, `shipment` | quick-create → Shipments (rate-buy flow) | 🟡 list+detail done; rate-buy wizard ⛔ |
| Trackers list + timeline | `tracker` | Trackers + TrackerSheet | ✅ |
| Orders + fulfillment | `order` | Orders + OrderSheet | ✅ list/detail; fulfill action 🟡 |
| Pickups (+ recurring) | `pickup` | Pickups + sheet | ✅ list/detail; schedule wizard 🟡 |
| Carrier connections | `carrier-connections`, `system-connection`, `user-connection` | Connections + sheet | ✅ list/detail; add-credentials form 🟡 |
| Shipping rules | `shipping-rules`, `shipping-rule-templates` | Rules + sheet | ✅ list/detail; rule builder 🟡 |
| Addresses | `address` | Addresses (**CRUD**) | ✅ |
| Parcels | `parcel` | Parcels (**CRUD**) | ✅ |
| Products / commodities | `product`, `customs` | Products (**CRUD**) | ✅ (customs templates 🟡) |
| Document templates | `document-template`, `default-template` | Documents + sheet | ✅ list/detail; template editor 🟡 |
| Manifests | `manifests` | Manifests + sheet | ✅ list/detail; create-manifest 🟡 |
| Batch operations | `batch-operations` | Batches + sheet | ✅ list/detail; run-batch action 🟡 |
| Rate sheets / markups | `rate-sheet`, `admin-rate-sheets`, `admin-markups` | Rate sheets + sheet | ✅ list/detail; markup editor 🟡 |
| Workflows (automation) | `workflows`, `workflow-*` | Workflows + sheet | ✅ list/detail; EE-only data (OSS GraphQL has no `workflows` field → graceful empty state) |

## Build (developer / extensibility)

| Dashboard feature | Hook(s) | Studio | Status |
|---|---|---|---|
| Apps / integrations | `apps`, app-store | Apps + sheet | ✅ list/detail; OAuth connect 🟡 |
| API keys | `api-keys`, `api-token` | API keys | ✅ list; generate/revoke 🟡 |
| Webhooks | `webhook` | Webhooks + sheet | ✅ list/detail; create-edit 🟡 |
| Logs / events / tracing | `log`, `event`, `tracing-record` | Workbench overlay | ✅ (live wiring 🟡) |
| GraphiQL / playground | — | Workbench tab | 🟡 placeholder |
| Plugins / carrier registry | registry | Plugins + sheet | ✅ ➕ |
| MCP management | `packages/mcp` | MCP screen | ➕ ✅ |
| Agent IDE / Assistant | — | Editor + Assistant (Claude) | ➕ ✅ |

## Govern (admin / platform)

| Dashboard feature | Hook(s) | Studio | Status |
|---|---|---|---|
| Admin overview / system | `admin-platform`, `admin-worker`, `system-usage` | Admin overview | ✅ |
| Tenants | `admin-platform` | Tenants | ✅ |
| Team & roles | `admin-users`, `organization`, `user` | Team & roles | ✅ list; invite/role-edit 🟡 |
| Usage / billing | `usage`, `admin-usage`, `subscription` | Usage | ✅ metrics; billing/subscription mgmt 🟡 |
| Security (2FA/SSO/sessions) | `session`, admin | Security | ✅ (wire toggles 🟡) |
| Audit log | `event` | Audit | ✅ |
| Workspace settings | `workspace-config`, `metadata` | Settings + Tweaks | ✅ ➕ self-edit |

## Cross-cutting

| Feature | Studio | Status |
|---|---|---|
| Auth (sign in/up/forgot, guards) | ✅ | wired to Karrio `/api/token`; httpOnly session + 401 token refresh |
| Home landing (stats + recent + to-do) | ✅ | real metrics from shipment/tracker/order hooks |
| Command palette (⌘K) | ➕ ✅ | |
| Self-editable appearance (theme/accent/density/font) | ➕ ✅ | |
| Responsive + dark/light | ✅ | swept across every page |
| Org / test-mode context | 🟡 | header plumbing in client; switcher UI ⛔ |

## Summary

Ship/Build/Govern **operational parity** (list + detail + core write flows) is in
place across **every** dashboard surface — including manifests, batch operations,
rate sheets, workflows, and usage (all now list/detail screens) — **plus** net-new
Studio capabilities (plugins, MCP, agent Editor/Assistant, self-editable UI).

What remains is **depth on specific write flows**, marked 🟡 above and tracked in
the Karrio Studio Linear project: the create-wizards (rate-buy, recurring pickups,
rule builder, customs/template editors, create-manifest/run-batch, markup editor),
order-fulfillment + invite/role actions, billing/subscription management, the
org/test-mode switcher UI, and live wiring for logs/GraphiQL. No dashboard surface
is missing a screen; these are deeper interactions layered on the existing screens.
