# Karrio Studio — Sandbox & seeded sample data

Brings up a local Karrio backend (SQLite) with a default admin and **provisioned
sample data for every Studio feature**, so Studio can be driven end-to-end and
the live Playwright project (`studio-live`) can run against real data.

## 1. Python env (one time)

Official setup:

```bash
./bin/install-dev
```

…or a lean install with uv:

```bash
uv venv .venv/karrio --python 3.12
source .venv/karrio/bin/activate
uv pip install -r requirements.server.dev.txt
```

> Restricted-egress note: the `documents` module fetches a CDN stylesheet at
> import. `generator.py` is offline-resilient (skips it when unreachable) so the
> server boots air-gapped.

## 2. Bring up the sandbox + seed

```bash
./bin/studio-sandbox            # migrate → create admin → seed → run API :5002
# or seed only (server already running):
./bin/studio-sandbox --seed-only
```

Admin: `admin@example.com` / `demo` (from `.env` `ADMIN_EMAIL`/`ADMIN_PASSWORD`).

The seed (`apps/studio/sandbox/seed.py`, run via `karrio shell`) provisions:
addresses, parcels, products, a test carrier connection, trackers, shipments,
and orders — idempotently (safe to re-run).

## 3. Run Studio against it

```bash
cp apps/studio/.env.sample apps/studio/.env   # KARRIO_API / VITE_KARRIO_API = http://localhost:5002
npm run dev -w @karrio/studio                 # http://localhost:3003
```

## 4. Live integration tests

```bash
cd packages/e2e
KARRIO_LIVE=1 KARRIO_STUDIO_URL=http://localhost:3003 \
  npx playwright test --project=studio-live
```

The default (mocked) `studio` Playwright project needs no backend; `studio-live`
exercises the real login + API-backed screens against this seeded sandbox.
