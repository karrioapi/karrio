# PRD: @karrio/mcp — npm Publishing, CI, and Developer Experience

**Status:** Draft
**Author:** Daniel K
**Date:** 2026-03-20

---

## Background

`@karrio/mcp` exists in `packages/mcp/` and provides a Model Context Protocol server
for multi-carrier shipping intelligence. It exposes Karrio API operations (rates,
shipments, tracking, carriers, pickups, manifests, logs) as MCP tools for AI agents.

**Current gaps:**
- Not published to npm — contributors cannot `npx @karrio/mcp` or `npm install @karrio/mcp`
- No CI test job — regressions go undetected until manual testing
- Not included in `bin/dev up` — developers must start the MCP server manually

**Impact:** Discoverability, quality assurance, and developer experience are all degraded.

---

## Section 1: npm Publishing

### Package Configuration

```
+-----------------------------+-----------------------------------+
| Field                       | Value                             |
+-----------------------------+-----------------------------------+
| name                        | @karrio/mcp                       |
| version                     | 1.0.0 (already set)               |
| registry                    | https://registry.npmjs.org        |
| publishConfig.access        | public (required for scoped pkg)  |
| files                       | ["dist", "README.md"]             |
| prepublishOnly              | npm run build (already set)       |
+-----------------------------+-----------------------------------+
```

### Publish Trigger

- Primary: GitHub Release creation (tag `v*`) — aligns with existing Python/Docker release flow
- Secondary: `workflow_dispatch` for manual publish (useful for hotfixes or testing)

### Version Strategy

Semver, manually bumped in `package.json` before release. Publish workflow validates
that unit tests pass before pushing to npm.

### Workflow File

New file: `.github/workflows/mcp-publish.yml`

```
+-------------------+     +-------------------+     +-------------------+
| GitHub Release    | --> | Build + Test      | --> | npm publish       |
| (or manual)       |     | (packages/mcp)    |     | --access public   |
+-------------------+     +-------------------+     +-------------------+
```

### Required GitHub Secret

- `NPM_TOKEN` — automation token from npmjs.com with publish access to `@karrio` scope

### Setup Steps for Daniel

1. Ensure `@karrio` org exists on npmjs.com (or that your npm account can publish to the scope)
2. Create an automation token on npmjs.com -> add as `NPM_TOKEN` secret on `karrioapi/karrio`
3. Confirm publish trigger preference (release tag vs manual — both are supported)

---

## Section 2: CI Test Job

### Job Definition

New job `mcp-ci` in `.github/workflows/tests.yml`, following `dashbaord-ci` pattern:

```
+-------------------+     +-------------------+     +-------------------+     +-------------------+
| Checkout          | --> | npm ci            | --> | tsc --noEmit      | --> | vitest unit tests |
| (no submodules)   |     | (packages/mcp)    |     | (typecheck)       |     | + build check     |
+-------------------+     +-------------------+     +-------------------+     +-------------------+
```

### Scope

- **Unit tests:** Run in CI (no external dependencies)
- **Integration tests:** Skipped in CI (require live Karrio API instance)
- **Node version:** 22.x (matching dashboard-ci)
- **Trigger:** On every push (same as existing test jobs)

### Why Not Integration Tests in CI

Integration tests (`tests/integration/`) require a running Karrio API server with
valid credentials. Running these in CI would require a service container and seed data.
This can be added later as a scheduled workflow if needed.

---

## Section 3: `bin/dev up` MCP Component

### Design

```
+-------------------------------------------------------------------+
| bin/dev up                                                        |
|                                                                   |
|   api (5002)  dashboard (3002)  docs (3005)  studio (4002)       |
|                                                                   |
|   mcp (stdio/3100) <-- NEW, opt-in via --with-mcp or "mcp" arg  |
+-------------------------------------------------------------------+
```

### Behavior

- **Opt-in:** `--with-mcp` flag or `mcp` component argument (also included in `all`)
- **Not default:** Avoids breaking existing workflows; MCP requires Karrio API running
- **Start command:** `npm run dev -w packages/mcp` (tsup watch mode, rebuilds on change)
- **PID tracking:** `MCP_PID` alongside `SERVER_PID`, `DASHBOARD_PID`, etc.
- **Cleanup:** Killed in `cleanup_trap` and shown in startup summary

### Port

MCP defaults to stdio transport. HTTP transport uses port 3100 (set in `src/index.ts`).
In dev mode, tsup watch rebuilds the server — the developer runs it separately or
connects via stdio from an AI client.

---

## Open Questions for Daniel

1. Does the `@karrio` npm org already exist? (Check npmjs.com/org/karrio)
2. Should npm publish trigger on GitHub Release only, or also allow `workflow_dispatch`?
   (Current implementation supports both.)
3. Should integration tests ever run in CI (e.g. scheduled workflow with live Karrio)?
4. Should `mcp` start by default in `bin/dev up` or only with `--with-mcp`?
   (Current implementation: opt-in only.)
5. What version should `@karrio/mcp` start at — keep `1.0.0` or drop to `0.x` until stable?
6. Should we add `npx @karrio/mcp` as the canonical usage in README/docs?

---

## Files Changed

```
+--------------------------------------------+---------------------------+
| File                                       | Change                    |
+--------------------------------------------+---------------------------+
| docs/prd/mcp-publish-ci-devex.md           | NEW — this PRD            |
| packages/mcp/package.json                  | Add publishConfig, files  |
| .github/workflows/mcp-publish.yml          | NEW — npm publish workflow |
| .github/workflows/tests.yml               | Add mcp-ci job            |
| bin/dev                                    | Add --with-mcp component  |
+--------------------------------------------+---------------------------+
```
