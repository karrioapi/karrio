# @karrio/e2e — Playwright E2E Tests

End-to-end tests for the Karrio dashboard (default: `localhost:3002`) and
API (default: `localhost:5002`).

> **Note:** `node_modules` are not committed. Run `npm install` at the repo
> root before executing tests, and `npx playwright install chromium firefox`
> on first run.

## Layout

| Path | Purpose |
|------|---------|
| `playwright.config.ts` | Chromium + Firefox, retries on CI, trace/video capture |
| `fixtures/auth.ts` | Extended Playwright test with a REST `api` fixture |
| `fixtures/wiremock/` | Canned carrier JSON served by WireMock in CI |
| `helpers/env.ts` | Centralised env-var resolution |
| `helpers/api.ts` | Thin REST client (JWT bearer auth) |
| `helpers/selectors.ts` | Shared role-based locators |
| `helpers/wait-for-stack.ts` | Polls API + dashboard until healthy |
| `tests/auth.setup.ts` | Persists NextAuth session to storageState |
| `tests/rate-sheet-editor.spec.ts` | Legacy rate-sheet editor suite |
| `specs/*.spec.ts` | Golden-path smoke suite (auth, shipment, tracking, order, settings) |
| `scripts/seed.ts` | CI-only data seeding via REST |

## Setup

```bash
cd karrio
npm install
cd packages/e2e
npx playwright install chromium firefox   # first time only
```

## Run against a running dev stack

```bash
npm test                   # full suite (chromium + firefox)
npm run test:smoke         # specs/ only (chromium)
npm run test:headed        # see the browser
npm run test:ui            # Playwright UI / trace viewer
```

## Run against the CI compose stack

```bash
docker compose -f docker-compose.e2e.yml up -d --wait
npx tsx packages/e2e/scripts/seed.ts
npm --prefix packages/e2e test
docker compose -f docker-compose.e2e.yml down -v
```

## Env overrides

| Env var | Default |
|---------|---------|
| `KARRIO_EMAIL` | `admin@example.com` |
| `KARRIO_PASSWORD` | `demo` |
| `KARRIO_DASHBOARD_URL` | `http://localhost:3002` |
| `KARRIO_API_URL` | `http://localhost:5002` |

## Carrier stubbing

The smoke suite never touches real carrier APIs.  In CI the compose stack
launches a `wiremock/wiremock` container with mappings from
`fixtures/wiremock/` returning canned rate/shipment/tracking JSON.

## CI

Runs on every push + PR in `.github/workflows/tests.yml` under the `e2e` job.
Reports, traces, and videos are uploaded as artifacts on failure.
