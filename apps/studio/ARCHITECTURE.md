# Karrio Studio — Architecture

Studio is a **standalone full‑stack TanStack Start app** (`apps/studio/`) that
replaces the legacy Next.js dashboard. It is intentionally **decoupled** from the
monorepo: its own `package.json`/lockfile, its own data layer, shadcn + Tailwind
(no `@karrio/ui`), and its own auth (no `@karrio/hooks`/NextAuth). It talks to a
running Karrio server purely as a **client** — there is **no Studio database**;
Karrio is the single source of truth (passthrough).

```
            ┌──────────────────────────────────────────────────────────┐
            │                     apps/studio (SSR)                      │
            │                                                            │
  Browser ──┤  TanStack Router (file routes)                            │
            │     __root → _app (guard) → _app.$screen (lazy registry)  │
            │                                                            │
            │  React screens ──useQuery──►  data hooks (lib/karrio)      │
            │                                   │                        │
            │  Server Functions (BFF)           │ KarrioCtx              │
            │   auth.* / assistant.*            ▼                        │
            │        │                   client.ts (REST + GraphQL)      │
            └────────┼───────────────────────────┼───────────────────────┘
                     │ (server‑to‑server)         │ (browser fetch, Bearer)
                     ▼                            ▼
          Anthropic API                    Karrio server  (REST /v1/*, /graphql,
          (Claude, optional)                /api/token[/refresh])
```

## 1. Module map

```
apps/studio/src/
├── routes/                      # TanStack Router file routes
│   ├── __root.tsx               # Providers (QueryClient, Session), <html> shell
│   ├── index.tsx                # "/" → redirect to /home or /login
│   ├── login.tsx signup.tsx forgot.tsx   # public auth pages
│   ├── _app.tsx                 # authenticated layout + beforeLoad guard
│   └── _app.$screen.tsx         # dynamic screen dispatcher (one route, N screens)
├── server/                      # Server Functions = Studio's BFF "API"
│   ├── auth.ts                  # login/refresh/logout/register/reset/getSession
│   └── assistant.ts             # sendAssistantMessage → Anthropic (server-side)
├── lib/karrio/                  # Decoupled data layer (no @karrio/*)
│   ├── env.ts                   # base URL resolution (KARRIO_API / VITE_KARRIO_API)
│   ├── client.ts                # restGet/restMutate/graphql + authedFetch (401→refresh)
│   ├── session.tsx              # SessionProvider → KarrioCtx, refresh handler
│   ├── hooks.ts                 # 19 REST + 6 GraphQL TanStack Query hooks + mutations
│   ├── types.ts                 # local API types (no @karrio/types)
│   ├── display.ts               # entity → display-string helpers
│   ├── agents.ts                # AgentDef + McpServerConfig store (localStorage + seam)
│   └── preferences.ts           # UI prefs (localStorage + update_user(metadata) seam)
├── lib/{modes,studio-state}.ts  # nav model (Ship/Build/Govern) + UI state
├── screens/                     # registry.tsx (React.lazy) → ship/* build/* govern/*
└── components/                  # shell (Sidebar/Topbar), ui (primitives/Sheet/...),
                                 #   overlays (CommandPalette/Workbench/TweaksPanel)
```

## 2. Request / data flow

Reads use TanStack Query hooks; writes use mutation hooks that invalidate the
relevant query keys. Every call carries auth + tenant context derived from the
session.

```
Screen (useShipments)                  lib/karrio/hooks.ts
   │ useQuery(["shipments", …])  ───►   queryFn: restGet(ctx, "/v1/shipments")
   │                                         │
   │                                    client.ts authedFetch(ctx, url)
   │                                         │  headers: Authorization: Bearer <access>
   │                                         │           x-org-id, x-test-mode
   │                                         ▼
   │                                    Karrio  GET /v1/shipments  ──► 200 JSON
   │                                         │
   │   on 401 ──► refreshHandler() ──► refreshSession() (server fn) ──► new access
   │             (de-duped, single retry with the rotated token)
   ▼
 render
```

`KarrioCtx = { baseUrl, token, orgId, testMode }` is assembled once by
`SessionProvider` and read by every hook via `useKarrioCtx()`. The token comes
from the httpOnly session cookie (never exposed to JS except as the in-memory
bearer surfaced through the session query).

**REST vs GraphQL split** (mirrors the Karrio API surface):

| Transport | Used for |
|---|---|
| **REST `/v1/*`** | shipments, trackers, connections, pickups, documents, manifests, batches, apps, plugins, webhooks, api_keys, admin, mcp, usage (19 hooks) |
| **GraphQL `/graphql`** | orders, address/parcel/product templates, rate_sheets, shipping_rules, workflows (6 hooks) + mutations (create/update/delete address/parcel/product, update_user, register_user, request_password_reset) |

## 3. Auth & session flow

Studio runs a thin **Backend‑for‑Frontend**: server functions proxy Karrio's JWT
endpoints and keep tokens in a single httpOnly cookie so SSR can authenticate and
the browser never stores raw tokens.

```
Login page ──login({email,password})──►  server/auth.ts
                                          POST {KARRIO_API}/api/token
                                          ◄─ { access, refresh }
                                          Set httpOnly cookie "karrio-studio-session"
SSR / hydrate ──getSession()──► reads cookie → { access, email } → SessionProvider

401 on any API call:
  client.authedFetch ── refreshHandler ──► refreshSession() (server fn)
                                           POST /api/token/refresh { refresh }
                                           ◄─ { access, refresh }  (rotates)
                                           updates cookie + cached session
                        ◄── new access ──  retry original request once
```

Route protection: `_app.tsx`'s `beforeLoad` redirects unauthenticated requests to
`/login`; the public auth routes opt out of the session storage state.

## 4. Karrio integration points

| Concern | Endpoint(s) | Notes |
|---|---|---|
| Auth | `POST /api/token`, `POST /api/token/refresh`, `POST /api/logout` | simplejwt; tokens in httpOnly cookie |
| Operational data | `GET/POST/PATCH/DELETE /v1/*` | REST resources |
| Relational/template data | `POST /graphql` | connections-style queries + typed mutations |
| Tenancy | headers `x-org-id`, `x-test-mode` | passed from `KarrioCtx` on every call |
| User prefs | `update_user(input:{ metadata })` GraphQL | writes `User.metadata["studio.customization"]` |
| Registration / reset | `register_user`, `request_password_reset` GraphQL | |

No schema/migrations are added to Karrio. The one backend file touched on this
branch is `modules/documents/.../generator.py` — an offline‑CSS guard for the
local sandbox, unrelated to Studio's runtime.

## 5. Custom Studio "APIs" (server functions)

These are the **net‑new endpoints Studio adds** — TanStack Start server functions
(typed RPC), not REST routes. They form the BFF layer:

| Server function | Method | Purpose |
|---|---|---|
| `login` | POST | exchange credentials at `/api/token`, set httpOnly session |
| `refreshSession` | POST | rotate access via `/api/token/refresh`, update cookie |
| `logout` | POST | clear the session cookie |
| `register` | POST | `register_user` GraphQL mutation |
| `requestPasswordReset` | POST | `request_password_reset` GraphQL mutation |
| `getSession` | GET | read the session cookie for SSR + client |
| `sendAssistantMessage` | POST | proxy to the Anthropic Messages API (Claude) server‑side, keeping `ANTHROPIC_API_KEY` off the client; returns a deterministic stub when unset |

## 6. Net‑new Studio capabilities (beyond dashboard parity)

- **Command palette (⌘K)**, **Workbench** dev overlay, **Tweaks** appearance panel.
- **Self‑editable appearance** — `preferences.ts` is the single source of truth for
  theme/accent/density/font/layout; persisted to `localStorage` and flushed to
  `User.metadata` via `update_user`. (Read‑back from the backend is a documented
  seam: the OSS GraphQL `UserType` does not yet expose `metadata`.)
- **Agents & MCP management** — `agents.ts` is a typed store for `AgentDef` and
  `McpServerConfig` with `localStorage` persistence behind a `BackendAdapter`
  interface (the swap point for a future REST adapter). MCP entries show an honest
  **"config‑only"** status — OSS has no execution proxy, so no connection state is
  fabricated.
- **Agent IDE / Assistant** — the Editor screen pairs a Claude chat (via
  `sendAssistantMessage`) with a client‑side connector **scaffolder**.

## 7. What is NOT built (honest scope / roadmap)

Studio is a **frontend + thin BFF**. The following require Karrio **backend** work
that this branch does **not** include:

- **On‑the‑fly plugin editing with hot reload.** The Editor's `scaffold()` generates
  connector files **in the browser** from an SDK‑extension template (mappers /
  providers / schemas / tests) for display and AI‑assisted editing. It does **not**
  write to the server's plugins directory, and nothing reloads carrier modules at
  runtime. A real version needs: (a) an API to persist/edit connector files under
  the Karrio plugins path, and (b) a runtime plugin loader/reloader (Karrio imports
  connectors as Python packages at boot; hot‑reloading them is non‑trivial). Tracked
  as roadmap.
- **MCP tool execution** — config management only; no backend exec proxy.
- **Customization read‑back** — write path is real; backend read needs `metadata`
  on the GraphQL `UserType`.
- **Deeper write‑wizards** — rate‑buy, recurring pickups, rule builder,
  create‑manifest/run‑batch, markup editor, fulfillment/role actions, billing.
  See `PARITY.md` (all marked 🟡).

## 8. Testing & CI

- `packages/e2e/tests/studio/*` — ~200 mocked Playwright specs (route‑level API
  mocking, inline session cookie) + a live‑gated smoke project.
- `render-smoke.spec.ts` — loads every route and fails on any runtime `pageerror`
  (catches "build‑green‑but‑broken" crashes that `tsc`/build miss).
- `visual.spec.ts` — screenshot baselines, gated behind `KARRIO_VISUAL=1`.
- `.github/workflows/studio-e2e.yml` — builds Studio, starts the dev server, runs
  the mocked project (no Django/Postgres needed).
- Sandbox: `bin/studio-sandbox` + `apps/studio/sandbox/seed.py` provision
  high‑fidelity data (shipments with addresses/parcels/charges, trackers,
  orders) with a seed self‑check.
```
