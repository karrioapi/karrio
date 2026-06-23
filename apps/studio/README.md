# Karrio Studio (`@karrio/studio`)

Full-stack **TanStack Start** app that replaces the Next.js dashboard
(`apps/dashboard`) with a modular, agent-friendly "studio" — Ship / Build /
Govern modes, a self-editable UI, and net-new carrier-integration, Editor,
Agent, and MCP-management surfaces.

> **Standalone by design.** This app is intentionally **excluded from the
> turborepo workspaces**. It has its own `package-lock.json`/`node_modules` and
> depends on **no** `@karrio/*` package — UI is **shadcn/ui + Tailwind**, and
> the Karrio API is consumed via a **self-contained fetch client + local types**
> (`src/lib/karrio/*`). This keeps Studio fast-moving and isolated from monorepo
> dependency/version conflicts, and out of root `npm ci` / `turbo build`.

See [`PRDs/KARRIO_STUDIO.md`](../../PRDs/KARRIO_STUDIO.md) for the full design,
the agent/subagent plan, and the testing strategy. Work is tracked in the
**"Karrio Studio"** Linear project (epics = orchestrator agents, issues =
subagents).

## Status — Phase 0 (foundation)

| Area | State |
|------|-------|
| Standalone TanStack Start app (Vite, SSR, file routes) | ✅ |
| Tailwind + shadcn theme (`globals.css`) + bespoke shell CSS | ✅ |
| App shell: Sidebar + Topbar + mode IA + routing | ✅ |
| Core components: `Sheet`, `Field`, `Icon`, `CarrierLogo` | ✅ (shadcn primitives added per screen) |
| Every IA route navigable (Placeholder + real Home) | ✅ `src/screens/` |
| Decoupled Karrio client + session + hooks | ✅ `src/lib/karrio/*` |
| Studio-native state contract (Karrio passthrough) | ✅ `src/lib/studio-state.ts` |
| Server-side auth (Karrio `token_auth`) | ✅ `src/server/auth.ts` |
| Playwright `studio` project + smoke specs | ✅ `packages/e2e/tests/studio/` |
| Feature screens, auth UI, agents/MCP/editor, monitoring | ⏳ tracked in Linear |

## Architecture

- **No `@karrio/*` deps.** Shipping data AND Studio-native state go through the
  Karrio backend via Studio's own client (`src/lib/karrio/client.ts`) and
  TanStack Query hooks (`src/lib/karrio/hooks.ts`), keyed by a `KarrioCtx`
  (base URL + token + org + test-mode) from `src/lib/karrio/session.tsx`.
- **Studio-native state** (customization, agents, MCP) → Karrio
  metafields/workspace-config under `studio.*` (see `src/lib/studio-state.ts`).
- **Auth** → server functions (`src/server/auth.ts`) proxy Karrio JWT auth into
  an httpOnly session cookie.
- **UI** → shadcn/ui + Tailwind (`src/styles/globals.css`, `src/lib/utils.ts`),
  with bespoke CSS for the enterprise shell (`src/styles/tokens.css`).

## Develop

```bash
cp .env.sample .env            # set KARRIO_API / VITE_KARRIO_API
cd apps/studio                 # standalone — install here, NOT at repo root
npm install
npm run dev                    # → http://localhost:3003 (generates routeTree.gen.ts)
```

## Test

```bash
# with the studio dev server running on :3003
cd packages/e2e
KARRIO_STUDIO_URL=http://localhost:3003 npx playwright test --project=studio
```

## Layout

```
apps/studio/                   # standalone (own lockfile/node_modules)
├── vite.config.ts             # TanStack Start plugin
├── tailwind.config.ts · postcss.config.js
├── src/
│   ├── router.tsx             # createRouter (routeTree.gen.ts is generated)
│   ├── routes/
│   │   ├── __root.tsx         # document, fonts, theme-init, QueryClient, Session
│   │   ├── index.tsx          # / → /home
│   │   ├── _app.tsx           # shell layout (sidebar + topbar + shortcuts)
│   │   └── _app.$screen.tsx   # screen dispatch (validates IA, 404s unknown)
│   ├── screens/               # registry + Home + Placeholder
│   ├── components/
│   │   ├── shell/             # Sidebar, Topbar
│   │   └── ui/                # Sheet, Field, icons, CarrierLogo (+ shadcn)
│   ├── lib/
│   │   ├── modes.ts           # Ship/Build/Govern IA
│   │   ├── theme.ts           # theme + density prefs
│   │   ├── utils.ts           # shadcn cn()
│   │   ├── studio-state.ts    # Studio-native state contract (Karrio passthrough)
│   │   └── karrio/            # env, client, types, session, hooks (decoupled)
│   ├── server/                # auth server functions
│   └── styles/
│       ├── globals.css        # Tailwind + shadcn theme tokens
│       └── tokens.css         # enterprise shell/sheet/table CSS
```
