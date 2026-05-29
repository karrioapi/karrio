# Karrio Studio (`@karrio/studio`)

Full-stack **TanStack Start** app that replaces the Next.js dashboard
(`apps/dashboard`) with a modular, agent-friendly "studio" — Ship / Build /
Govern modes, a self-editable UI, and net-new carrier-integration, Editor,
Agent, and MCP-management surfaces.

See [`PRDs/KARRIO_STUDIO.md`](../../PRDs/KARRIO_STUDIO.md) for the full design,
the agent/subagent plan, and the testing strategy. Work is tracked in the
**"Karrio Studio"** Linear project (epics = orchestrator agents, issues =
subagents).

## Status — Phase 0 (foundation)

| Area | State |
|------|-------|
| TanStack Start app (Vite, SSR, file routes) | ✅ scaffolded |
| Design tokens + global CSS (ported from handoff) | ✅ `src/styles/tokens.css` |
| App shell: Sidebar + Topbar + mode IA + routing | ✅ |
| Core components: `Sheet`, `Field`, `Icon`, `CarrierLogo` | ✅ (more in later phases) |
| Every IA route navigable (Placeholder + real Home) | ✅ `src/screens/` |
| Studio-native DB schema (Drizzle) | ✅ `src/db/schema.ts` |
| Server-side auth skeleton (Karrio `token_auth`) | ✅ `src/server/auth.ts` |
| Playwright `studio` project + smoke specs | ✅ `packages/e2e/tests/studio/` |
| Feature screens, auth UI, agents/MCP/editor, monitoring | ⏳ tracked in Linear |

## Architecture

- **Shipping data** → reused `@karrio/hooks` (TanStack Query) over Karrio
  GraphQL + REST. No data is duplicated.
- **Studio-native state** (app config/tweaks, agent sessions, MCP config) →
  Drizzle DB via TanStack Start server functions.
- **Auth** → server functions proxy Karrio JWT auth into an httpOnly session
  cookie used by SSR + the Karrio client.

## Develop

```bash
cp .env.sample .env            # set KARRIO_API + DATABASE_URL
npm install                    # from repo root (workspaces)
npm run dev -w @karrio/studio  # → http://localhost:3003 (generates routeTree.gen.ts)
```

## Test

```bash
# with the studio dev server running on :3003
cd packages/e2e
KARRIO_STUDIO_URL=http://localhost:3003 npx playwright test --project=studio
```

## Layout

```
apps/studio/
├── vite.config.ts            # TanStack Start plugin
├── drizzle.config.ts
├── src/
│   ├── router.tsx            # createRouter (routeTree.gen.ts is generated)
│   ├── routes/
│   │   ├── __root.tsx        # document, fonts, theme-init, QueryClient
│   │   ├── index.tsx         # / → /home
│   │   ├── _app.tsx          # shell layout (sidebar + topbar + shortcuts)
│   │   └── _app.$screen.tsx  # screen dispatch (validates IA, 404s unknown)
│   ├── screens/              # registry + Home + Placeholder
│   ├── components/
│   │   ├── shell/            # Sidebar, Topbar
│   │   └── ui/               # Sheet, Field, icons, CarrierLogo
│   ├── lib/                  # modes (IA), theme
│   ├── db/                   # Drizzle schema + client
│   ├── server/               # auth server functions
│   └── styles/tokens.css     # ported design tokens + shell/sheet CSS
```
