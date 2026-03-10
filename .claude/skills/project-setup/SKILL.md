# Project Setup Skill

Set up the Karrio development environment from scratch or after a fresh clone.

## Quick Start

### One-Time Full Setup

```bash
./bin/install-dev
```

This handles everything: Python 3.12, Node.js, system dependencies, `.env` file, Docker, HTTPS certs.

### Manual Setup (Step by Step)

#### 1. System Dependencies

```bash
# macOS
./bin/install-binaries
# Installs: gcc, pango, ghostscript, zint (barcode library)
```

#### 2. Python Environment

```bash
# Create virtualenv and install all dependencies
./bin/setup-server-env

# Or SDK-only (lighter):
./bin/setup-sdk-env
```

#### 3. Activate Environment

```bash
source bin/activate-env
```

This must be sourced before running any `karrio` commands. All `bin/*` scripts source it automatically.

#### 4. Database Setup

```bash
karrio migrate
```

#### 5. Create Admin User

```bash
karrio createsuperuser
```

#### 6. Frontend Dependencies

```bash
npm install
```

## Running the Application

### Development Servers

```bash
# Full stack (API + Worker)
./bin/start

# API only (port 5002)
./bin/start-server

# Worker only (Huey with 2 workers)
./bin/start-worker

# Dashboard only (port 3002)
npm run dev -w @karrio/dashboard

# Full stack with Docker
cd docker && docker compose up
```

### Docker Development

```bash
./bin/docker-env create    # Build image + install deps + run migrations
./bin/docker-env on        # Start container
./bin/docker-env shell     # Open bash in container
./bin/docker-env off       # Stop container
./bin/docker-env destroy   # Remove everything
./bin/docker-env exec '<command>'  # Run command in container
```

Docker compose services:
- **karriodev**: Main dev container (ports 5002, 3002, 3005)
- **caddy**: Reverse proxy for HTTPS (ports 80, 443)
- **maildev**: Email testing UI (port 1080)

## Build Commands

```bash
npm run build    # Turbo build all packages
npm run lint     # ESLint across workspaces
npm run format   # Prettier formatting
```

## Submodules

Three git submodules exist:
- `ee/insiders` → Enterprise features (private)
- `ee/platform` → Platform features (private)
- `community` → Community plugins (public)

```bash
git submodule update --init --recursive  # Initialize
git submodule update --remote --merge    # Update to latest
```

## Environment Variables

Key variables (see `.env.sample`):
- `KARRIO_API_URL=http://localhost:5002`
- `DATABASE_URL=postgres://user:pass@localhost:5432/karrio`
- `REDIS_URL=redis://localhost:6379/0`
- `SECRET_KEY=<generate>`
- `JWT_SECRET=<generate>`

## Schema Generation

### Carrier Schema Types (from JSON/XML samples)

```bash
# Regenerate Python types from JSON/XML samples
./bin/run-generate-on modules/connectors/<carrier>
# Source: modules/connectors/<carrier>/schemas/*.json
# Output: modules/connectors/<carrier>/karrio/schemas/<carrier>/*.py
```

### OpenAPI Schema

```bash
# Requires running server on port 5002
curl http://localhost:5002/shipping-openapi -o schemas/openapi.yml
./bin/generate-api-docs  # Full docs generation for apps/www
```

### GraphQL Schema

```bash
# Requires running server
karrio graphql_schema --schema karrio.server.graph.schema --out schemas/graphql.json
./bin/generate-graphql-types  # Apollo codegen → packages/types/graphql/types.ts
```

## Testing

```bash
source bin/activate-env

# SDK + all connectors
./bin/run-sdk-tests

# Single connector
python -m unittest discover -v -f modules/connectors/<carrier>/tests

# Server (Django)
./bin/run-server-tests

# Single server module
karrio test --failfast karrio.server.<module>.tests

# Type checking
./bin/run-sdk-typecheck
```

## Key Directories

| Directory | Purpose |
|-----------|---------|
| `apps/api/` | Django API service |
| `apps/dashboard/` | Next.js dashboard |
| `modules/sdk/` | Core SDK |
| `modules/connectors/` | Carrier integrations |
| `modules/core/` | Server core (serializers, gateway) |
| `packages/` | Shared TS packages (hooks, ui, types, lib) |
| `bin/` | Automation scripts |
| `docker/` | Docker compose configs |
| `schemas/` | OpenAPI + GraphQL schemas |
