# @karrio/e2e — Playwright E2E Tests

End-to-end tests for the Karrio dashboard at `localhost:3002`.

> **Note:** `node_modules` are not committed. Run `npm install` before executing
> tests, and `npx playwright install chromium` on first run.

## Setup

```bash
cd karrio/packages/e2e
npm install
npx playwright install chromium   # first time only
```

## Run (requires dev server on localhost:3002)

```bash
npm test                  # headless
npm run test:headed       # headed (see browser)
npm run test:ui           # Playwright UI / trace viewer
```

## Auth

Tests log in once via `helpers/auth.ts` and reuse the session via
`playwright/.auth/user.json` (auto-created, git-ignored).

Set credentials via env vars or use the defaults:

| Env var           | Default                |
|-------------------|------------------------|
| `KARRIO_EMAIL`    | `admin@example.com`    |
| `KARRIO_PASSWORD` | `demo`                 |
| `KARRIO_DASHBOARD_URL` | `http://localhost:3002` |

## Test Targets

| Test # | Description | URL |
|--------|-------------|-----|
| 1  | Carrier Network page loads | `/admin/carriers` |
| 2  | Rate Sheets tab switch | `/admin/carriers` |
| 3  | Create Rate Sheet editor opens | `/admin/carriers` |
| 4  | Mode buttons (edit/import/export) visible | editor panel |
| 5  | Switch to import mode → file input | editor panel |
| 6  | Upload valid xlsx → diff preview | editor import panel |
| 7  | Upload error xlsx → validation errors | editor import panel |
| 8  | Cancel import → returns to edit mode | editor import panel |
| 9  | Export button triggers download | editor panel |
| 10 | Connections rate-sheets page loads | `/connections/rate-sheets` |
| 11 | Escape key closes editor | editor panel |
| 12 | Close button dismisses editor | editor panel |

## Fixtures

| File | Description |
|------|-------------|
| `fixtures/rate-sheet-valid.xlsx` | Valid rate sheet — dry-run succeeds, diff preview shown |
| `fixtures/rate-sheet-errors.xlsx` | Invalid data — validation errors shown |
| `fixtures/rate-sheet-updated.xlsx` | Updated rates — for confirm-import flow |

## CI

Set `CI=true` to enable GitHub reporter and 2 retries per test.
