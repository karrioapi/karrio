# Karrio Studio — Full-Stack TanStack Start Migration

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-05-29 |
| Status | Planning |
| Owner | Studio Program (dan@karrio.io) |
| Type | Architecture / Enhancement / Migration |
| Reference | [AGENTS.md](../AGENTS.md), design handoff `design_handoff_karrio_studio/` |
| Linear | Project "Karrio Studio" (tracked; agents/subagents = issues) |

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Open Questions & Decisions](#open-questions--decisions)
3. [Problem Statement](#problem-statement)
4. [Goals & Success Criteria](#goals--success-criteria)
5. [Existing Code Analysis](#existing-code-analysis)
6. [Technical Design](#technical-design)
7. [Modes, Screens & Feature Matrix](#modes-screens--feature-matrix)
8. [New Features: Carrier Integration, Editor, Agents & MCP](#new-features)
9. [Agent / Subagent Orchestration Plan (Linear)](#agent--subagent-orchestration-plan-linear)
10. [Implementation Plan](#implementation-plan)
11. [Testing Strategy (Playwright)](#testing-strategy-playwright)
12. [Risk Assessment](#risk-assessment)
13. [Migration & Rollback](#migration--rollback)

---

## Executive Summary

Karrio Studio replaces the Next.js dashboard (`apps/dashboard`) with a full-stack
**TanStack Start** application (`apps/studio`) that reimagines Karrio as a modular,
agent-friendly "studio" — a WordPress-like experience for managing shipping
operations, carrier plugins, commerce apps, and a developer platform from one
interface.

The IA is organized around three **modes** — **Ship**, **Build**, **Govern** — driven
by a collapsible sidebar. Studio migrates every dashboard feature, adds **self-editable
/ customizable** app surfaces (theme/density/layout tweaks, a visual editor), and
introduces three net-new capability areas: **agent-first plugin/carrier integration
(Editor)**, **MCP server management**, and an **AI Assistant** woven through the app.

Decisions locked with the owner:

| Decision | Choice |
|----------|--------|
| App strategy | **New app `apps/studio`**, phased cutover; `apps/dashboard` stays live until parity |
| Data layer | **Studio-local DB (Drizzle)** for Studio-native state + **Karrio GraphQL/REST** (via `@karrio/hooks`) for shipping data |
| Session 1 scope | Linear project + agent plan, this PRD, and the `apps/studio` foundation scaffold + Playwright harness |

## Open Questions & Decisions

| # | Question | Decision | Rationale |
|---|----------|----------|-----------|
| 1 | Replace dashboard in place or build new? | Build `apps/studio` new, deprecate dashboard at parity | Keeps production dashboard running during the multi-phase migration |
| 2 | Where does Studio-native state live? | Drizzle DB (Postgres in prod, SQLite in dev) for Studio-only entities; Karrio API for all shipping data | Avoids backend churn for app-config/agent/MCP state while keeping one source of truth for shipping |
| 3 | Auth model | TanStack Start server functions proxy Karrio auth (JWT) + httpOnly session cookie; reuse Karrio `mutation token_auth`/refresh | Server-side session beats the dashboard's client NextAuth for SSR + security |
| 4 | Component reuse | Reuse `@karrio/types`, `@karrio/lib`; introduce a Studio token/`@karrio/ui-studio` layer for the enterprise aesthetic | `@karrio/ui` is bulma/plex-styled; Studio aesthetic is distinct (sharp, dense, dark-default) |
| 5 | Hooks reuse | `@karrio/hooks` is `"use client"` + NextAuth-coupled. Provide a Studio session adapter so hooks work under TanStack Start; net-new queries use server functions | Maximizes reuse of ~50 existing TanStack Query hooks |

## Problem Statement

The current dashboard is a Next.js app composed of many `@karrio/*` packages. It is
feature-rich but: (a) its visual language is generic, (b) it has no first-class
story for AI agents / MCP / self-customization, and (c) carrier/plugin integration
is a developer-CLI task, not an in-product experience. The Studio vision unifies
operations, extensibility, and governance with an enterprise-grade, agent-native UX.

## Goals & Success Criteria

| Goal | Success Criteria |
|------|------------------|
| Feature parity with dashboard | Every Ship/Build/Govern screen below implemented and wired to live Karrio APIs |
| Pixel-faithful enterprise UI | Design tokens from `styles.css` ported; sharp corners, 1px borders, dark-default, light theme |
| Full-stack TanStack Start | SSR routing, server functions, server-side auth/session, Drizzle DB, forms (TanStack Form), monitoring |
| New: Carrier/plugin Editor | Agent-first 3-pane IDE; scaffold + edit connectors via `@karrio/app-store`/SDK |
| New: MCP management | Start/stop server, tools table, install snippets, client + invocation monitoring (ref `packages/mcp`, `PRDs/KARRIO_MCP_SERVER.md`) |
| New: Agents | AI Assistant chat + agent sessions/runs, persisted in Studio DB |
| Self-editable app | Theme/accent/density/font + layout customization persisted per user/org |
| Full test coverage | Playwright spec per feature, run against live Karrio GraphQL+REST |
| Tracked in Linear | Project with epics/issues mirroring the agent plan below |

## Existing Code Analysis

| Asset | Location | Reuse plan |
|-------|----------|-----------|
| Karrio API client | `@karrio/types` `KarrioClient`, `packages/hooks/karrio.tsx` | Reuse client; replace NextAuth session with Studio server session |
| Data hooks (~50) | `packages/hooks/*` (shipment, tracker, order, pickup, carrier-connections, apps, webhooks, api-keys, admin-*, workflows…) | Reuse via a Studio `ClientProvider` + session adapter |
| Types | `@karrio/types` (`graphql/`, `rest/`, `base.ts`) | Reuse directly — never define inline |
| Lib utils | `@karrio/lib` (`KARRIO_API`, `url$`, `getCookie`, auth, autocomplete) | Reuse directly |
| App store / plugins | `packages/app-store`, `packages/mcp`, `plugins/` | Power Apps/Plugins/MCP screens + Editor scaffolding |
| MCP server | `packages/mcp`, `PRDs/KARRIO_MCP_SERVER.md`, `SPRINT_MCP.md` | Back the MCP management screen |
| Playwright harness | `packages/e2e` (config, `helpers/auth.ts`, `auth.setup.ts`) | Extend with a `studio` project + per-feature specs |
| Design handoff | `design_handoff_karrio_studio/prototype/studio/*` | Source of truth for tokens, IA, screen layouts, data shapes |

**Key constraint:** `@karrio/hooks` files start with `"use client"` and read the
NextAuth session via `useSyncedSession`. Studio provides a compatible session
context so these hooks run unchanged inside client islands; SSR data + Studio-native
entities go through TanStack Start **server functions** + Drizzle.

## Technical Design

### Architecture overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                         apps/studio (TanStack Start)                    │
│                                                                        │
│  ┌────────────┐   ┌──────────────────────────────────────────────┐    │
│  │  Router     │   │  App Shell (CSS grid: [sidebar] [main])       │    │
│  │ (file-based │──▶│  Sidebar: workspace · Mode(Ship/Build/Govern) │    │
│  │  routes,    │   │          · nav · user footer                  │    │
│  │  SSR)       │   │  Topbar: ⌘K · test-mode · theme · workbench   │    │
│  └────────────┘   │          · app launcher · create               │    │
│        │          │  Page: routed screen (internal scroll)         │    │
│        │          └──────────────────────────────────────────────┘    │
│        ▼                                                                │
│  ┌──────────────────────┐        ┌──────────────────────────────┐      │
│  │ Server Functions      │        │ Client islands               │      │
│  │ - auth/session (JWT)  │        │ - @karrio/hooks (TanStack Q)  │      │
│  │ - Studio-native CRUD  │        │ - forms (TanStack Form)       │      │
│  │ - agent/MCP/editor    │        │ - sheets/overlays/palette     │      │
│  └─────────┬─────────────┘        └───────────────┬──────────────┘      │
│            │                                       │                     │
└────────────┼───────────────────────────────────────┼─────────────────────┘
             │                                       │
   ┌─────────▼──────────┐                 ┌──────────▼───────────────┐
   │ Studio DB (Drizzle) │                 │  Karrio Backend           │
   │ - app_config        │                 │  - GraphQL  (/graphql)     │
   │ - layouts/tweaks    │                 │  - REST     (/v1/*)        │
   │ - agent_sessions    │                 │  - auth (token_auth)       │
   │ - agent_runs/msgs   │                 │  - MCP server (packages/mcp│
   │ - mcp_servers       │                 │    + Django)               │
   │ - mcp_clients       │                 └────────────────────────────┘
   └────────────────────┘
```

### Auth & session sequence

```
Browser            Studio server fn         Karrio GraphQL        Studio DB
  │  POST /login (email,pw)  │                    │                  │
  ├─────────────────────────▶│ mutation token_auth│                  │
  │                          ├───────────────────▶│                  │
  │                          │◀── access+refresh ──┤                  │
  │                          │ set httpOnly cookie  │                 │
  │◀── 302 → /home ──────────┤                     │                 │
  │  (SSR pages read cookie → inject token into KarrioClient + hooks) │
```

### Tech stack

| Concern | Choice |
|---------|--------|
| Framework | TanStack Start (Vite + TanStack Router, SSR + server functions) |
| Data (shipping) | `@karrio/hooks` (TanStack Query) → Karrio GraphQL + REST |
| Data (Studio-native) | Drizzle ORM (Postgres prod / SQLite dev) via server functions |
| Forms | TanStack Form + Zod validation |
| Styling | CSS custom properties ported from `styles.css` (+ Tailwind optional, tokens-first) |
| Auth | Server functions → Karrio `token_auth`/refresh; httpOnly session cookie |
| Monitoring | Workbench overlay (logs/events/health/workers/tracing) wired to Karrio admin hooks + Sentry/PostHog (`instrumentation`) |
| Tests | Playwright (`packages/e2e`, new `studio` project) |

## Modes, Screens & Feature Matrix

Routing derives mode from route (deep links land in the right mode). Defaults:
Ship→`home`, Build→`apps`, Govern→`admin`.

| Mode | Screen | Route | Karrio API | Prototype ref |
|------|--------|-------|-----------|---------------|
| Ship | Home | `home` | shipment/tracker stats | `screens-ops.jsx` HomeScreen |
| Ship | Shipments + Sheet | `shipments` | REST `/v1/shipments`, GraphQL | ShipmentsScreen, ShipmentSheet |
| Ship | Trackers + Sheet | `trackers` | `/v1/trackers` | TrackersScreen, TrackerSheet |
| Ship | Orders + Sheet | `orders` | GraphQL orders | OrdersScreen, OrderSheet |
| Ship | Pickups + Create | `pickups` | `/v1/pickups` | PickupsScreen, PickupSheet, CreatePickupSheet |
| Ship | Connections + Sheet | `connections` | carrier-connections | ConnectionsScreen, ConnectionSheet |
| Ship | Shipping rules + Sheet | `rules` | shipping-rules | ShippingRulesScreen, RuleSheet |
| Ship | Addresses + Sheet | `addresses` | address | AddressesScreen, AddressSheet |
| Ship | Parcels + Sheet | `parcels` | parcel | ParcelsScreen, ParcelSheet |
| Ship | Products + Sheet | `products` | product | ProductsScreen, ProductSheet |
| Ship | Documents + Editor | `documents` | document-template | DocumentsScreen, DocumentSheet |
| Build | Apps + Sheet | `apps` | app-store, apps hook | AppsScreen, AppSheet, AppLauncher |
| Build | Plugins + Sheet | `plugins` | plugins/registry | PluginsScreen, PluginSheet |
| Build | MCP | `mcp` | `packages/mcp` + Django | McpScreen |
| Build | Editor (agent IDE) | `editor` | Studio DB + SDK scaffold | EditorScreen |
| Build | Workbench overlay | (overlay) | admin/log/event/health/worker/tracing | workbench.jsx |
| Build | Webhooks | `webhooks` | webhook hook | screens-develop.jsx |
| Build | API keys | `apikeys` | api-keys/api-token | screens-develop.jsx |
| Govern | Admin overview | `admin` | admin-* hooks | AdminScreen |
| Govern | Tenants | `tenants` | admin-platform | AdminScreen |
| Govern | Team & roles | `team` | organization/admin-users | screens-platform.jsx |
| Govern | Security | `security` | admin/session | screens-platform.jsx |
| Govern | Audit log | `audit` | event/tracing | screens-platform.jsx |
| Govern | Settings | `settings` | workspace-config, user | SettingsScreen |
| Cross | Auth flow | `/login…` | token_auth, register, verify, 2FA, reset | `auth.jsx` |
| Cross | Command palette ⌘K | overlay | search hook | CommandPalette |
| Cross | Tweaks panel | overlay | Studio DB app_config | tweaks-panel.jsx |

### Core reusable components (Studio UI layer)

`Sheet` (right drawer sm/md/lg + fullscreen), `ActivityFeed` + `JsonView`,
`CommandPalette`, `AppLauncher`/`AppSheet`, `Toast`, `Sidebar`/`Topbar`,
`Icon`, `CarrierLogo`, `Field`. All detail/create/edit views build on `Sheet`.

### Design tokens

Ported verbatim from `styles.css`: accent `#8B5CF6`; radii xs2/sm3/md4/lg6/pill3;
dark-default + light theme palettes; status colors; density variants
(compact/regular/comfy); Inter / JetBrains Mono / IBM Plex Sans. Theme persists
(`localStorage` + Studio DB), applied pre-render to avoid flash.

## New Features

### Carrier integration & plugin Editor (`editor`)
Agent-first 3-pane IDE: **left** agent sessions, **center** Assistant chat (default)
+ closeable code tabs with inline AI diff (Apply/Reject), **right** plugin file tree.
Scaffolds connectors using the SDK extension pattern (`./bin/cli sdk add-extension`)
and `@karrio/app-store`, persisting sessions/runs/messages in Studio DB.

### MCP management (`mcp`)
Server status (start/stop, URL, stats), exposed-tools table, install snippets
(Claude Desktop/Cursor JSON + SSE URL), connected clients, recent invocations —
backed by `packages/mcp` and the MCP server PRD.

### AI Assistant & Agents
Assistant chat surface (Editor + ⌘K actions) backed by the Claude API; agent
sessions/runs/messages persisted in Studio DB; @-context chips reference Studio
entities. Tool execution flows through the Karrio MCP server.

### Self-editable / customizable app
Tweaks panel (accent/font/density/theme) + layout customization persisted per
user/org in Studio DB; applied via CSS custom properties.

## Agent / Subagent Orchestration Plan (Linear)

The build is decomposed into **orchestrator agents** (epics) and **subagents**
(issues). This maps 1:1 to the Linear project "Karrio Studio".

```
Karrio Studio (Linear Project)
├─ EPIC A · Foundation Agent
│  ├─ A1 scaffold apps/studio (TanStack Start, Vite, SSR)
│  ├─ A2 design tokens + global CSS (port styles.css)
│  ├─ A3 app shell: Sidebar + Topbar + mode IA + routing
│  ├─ A4 core components: Sheet, ActivityFeed, JsonView, Toast, Field, Icon, CarrierLogo
│  ├─ A5 Studio DB (Drizzle) schema + migrations
│  └─ A6 @karrio/hooks session adapter + ClientProvider
├─ EPIC B · Auth Agent
│  ├─ B1 server-fn auth (token_auth/refresh) + httpOnly session
│  ├─ B2 auth screens (sign in/up, verify, 2FA, forgot/reset, invite, change pw)
│  └─ B3 route guards + org/test-mode context
├─ EPIC C · Ship Agent
│  ├─ C1 Home  ├─ C2 Shipments+Sheet  ├─ C3 Trackers+Sheet  ├─ C4 Orders+Sheet
│  ├─ C5 Pickups+Create  ├─ C6 Connections  ├─ C7 Shipping rules
│  ├─ C8 Addresses  ├─ C9 Parcels  ├─ C10 Products  └─ C11 Documents+template editor
├─ EPIC D · Build Agent
│  ├─ D1 Apps + AppLauncher/AppSheet  ├─ D2 Plugins  ├─ D3 MCP management
│  ├─ D4 Editor (agent IDE)  ├─ D5 Workbench overlay  ├─ D6 Webhooks  └─ D7 API keys
├─ EPIC E · Govern Agent
│  ├─ E1 Admin overview  ├─ E2 Tenants  ├─ E3 Team & roles
│  ├─ E4 Security  ├─ E5 Audit log  └─ E6 Settings
├─ EPIC F · Agents & MCP Agent (net-new)
│  ├─ F1 Assistant chat + Claude API  ├─ F2 agent sessions/runs persistence
│  ├─ F3 MCP tool execution wiring  └─ F4 carrier-integration scaffolding flow
├─ EPIC G · Customization Agent
│  ├─ G1 Tweaks panel  ├─ G2 layout customization  └─ G3 per-user/org persistence
├─ EPIC H · Cross-cutting Agent
│  ├─ H1 Command palette ⌘K  ├─ H2 keyboard shortcuts  ├─ H3 quick-create
│  └─ H4 monitoring (Sentry/PostHog) + health
└─ EPIC I · QA / Playwright Agent
   ├─ I1 studio Playwright project + auth setup
   ├─ I2 per-feature specs (one per C/D/E screen)
   ├─ I3 GraphQL+REST integration fixtures
   └─ I4 CI wiring
```

Each subagent issue carries: scope, prototype ref, Karrio API/hook, acceptance
criteria, and a paired Playwright spec (EPIC I).

## Implementation Plan

| Phase | Agent(s) | Deliverable |
|-------|----------|-------------|
| 0 (this session) | Foundation A1–A4 (scaffold), I1 | `apps/studio` boots, shell + tokens, Playwright `studio` project |
| 1 | A5–A6, B | Studio DB, hooks adapter, full auth |
| 2 | C | Ship mode parity, each screen + spec |
| 3 | D | Build mode incl. MCP + Editor + Workbench |
| 4 | E, G, H | Govern, customization, cross-cutting |
| 5 | F | Agents & MCP execution, carrier scaffolding |
| 6 | I, cutover | Full Playwright suite green; deprecate dashboard |

## Testing Strategy (Playwright)

- Extend `packages/e2e`: add a **`studio`** Playwright project (baseURL
  `KARRIO_STUDIO_URL`, default `http://localhost:3003`) with its own `auth.setup.ts`
  (Studio server-session login) producing `playwright/.auth/studio.json`.
- **One spec per feature** (matrix above): list/table render, filters/tabs, row →
  Sheet open, create/edit/delete via Sheet forms, and the net-new MCP/Editor/Agent
  flows. Each asserts against **live Karrio GraphQL + REST** responses (seeded test
  org), not mocks.
- Follow repo Playwright conventions (role-based locators, `networkidle`, auth state
  reuse). `unittest`/`karrio test` remain for SDK/Django; Playwright covers Studio UI.
- CI: run `studio` project after `setup`; fixtures seed shipments/trackers/orders.

## Risk Assessment

| Risk | Mitigation |
|------|-----------|
| `@karrio/hooks` NextAuth coupling | Session adapter providing the same context shape under TanStack Start |
| `@karrio/ui` aesthetic mismatch | New Studio token layer; reuse types/lib only, not bulma UI |
| Scope (huge surface) | Phased per-agent delivery tracked in Linear; dashboard stays live |
| TanStack Start maturity | Pin versions; isolate SSR/server-fn boundaries; lean on TanStack Query for data |
| Agent/MCP security | Tool execution via MCP server with org scoping; no secrets in client |

## Migration & Rollback

Studio ships alongside the dashboard. Cutover is per-mode behind a feature flag;
rollback = route users back to `apps/dashboard`. No destructive backend changes —
Studio-native state is additive (Drizzle DB), shipping data untouched.
