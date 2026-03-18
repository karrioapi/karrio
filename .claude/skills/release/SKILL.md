# Release Skill

Create a new Karrio release by bumping versions, syncing packages, generating frozen requirements, updating the changelog, committing, and optionally generating API schemas.

## Prerequisites

- Python virtualenv active: `source bin/activate-env`
- Working tree clean (no uncommitted changes unrelated to the release)
- All submodules (`ee/insiders`, `ee/platform`, `community`) merged to main if changed

## Release Workflow

### Step 1: Bump Version

```bash
# Replace OLD_VERSION → NEW_VERSION in central files
./bin/update-version <OLD_VERSION> <NEW_VERSION>
```

**Files touched by `update-version`:**
- `apps/api/karrio/server/VERSION` (central source of truth)
- `apps/web/public/openapi.yml`
- `apps/www/openapi.yml`
- `schemas/openapi.yml`
- `packages/types/rest/api.ts`
- `bin/deploy-hobby`, `bin/upgrade-hobby`
- `bin/deploy-insiders`, `bin/upgrade-insiders`
- `docker/.env`
- `ee/platform/infra/Pulumi.karrio-us.yaml` (if ee/platform exists)

### Step 2: Sync Package Versions

```bash
# Update ALL pyproject.toml files to match central VERSION
./bin/update-package-versions
```

This updates version in:
- Core modules: `modules/sdk`, `modules/core`, `modules/data`, `modules/documents`, `modules/events`, `modules/graph`, `modules/manager`, `modules/orders`, `modules/pricing`, `modules/proxy`, `modules/soap`, `modules/cli`
- All connectors: `modules/connectors/*/pyproject.toml`
- Community plugins: `community/plugins/*/pyproject.toml`
- Root plugins: `plugins/*/pyproject.toml`
- Insiders modules: `ee/insiders/modules/*/pyproject.toml` (if exists)
- Platform modules: `ee/platform/modules/*/pyproject.toml` (if exists)

### Step 3: Generate Frozen Requirements

```bash
# Generate frozen pip requirements from incremental builds
./bin/update-version-freeze
```

This creates a clean virtualenv and generates:
- `requirements.txt` (public-only packages)
- `requirements.insiders.txt`
- `requirements.platform.txt`

### Step 4: Generate Source Requirements

```bash
# Convert git URLs to PyPI versions and generate source requirements
./bin/update-source-version-freeze
```

This generates:
- `source.requirements.txt` (local file paths for development)
- `source.requirements.insiders.txt`
- `source.requirements.platform.txt`
- Updates `requirements.txt` with PyPI package versions
- Updates `requirements.insiders.txt` and `requirements.platform.txt`

### Step 5: Update CHANGELOG.md

Review commits since the last release and update `CHANGELOG.md`:
- Use `git log <last-release-tag>..HEAD --oneline` to see all commits
- Categorize into: Features, Fixes, Chores, Breaking Changes
- Add breaking change warnings if applicable

### Step 6: Check Submodules

Before committing, verify submodules are on the correct branch:

```bash
git submodule status
# Ensure ee/insiders, ee/platform, community are on main
cd ee/insiders && git checkout main && git pull && cd ../..
cd ee/platform && git checkout main && git pull && cd ../..
cd community && git checkout main && git pull && cd ..
```

### Step 7: Commit

```bash
git add -A
git commit -m "release: <NEW_VERSION>"
```

### Step 8: Generate API Schemas (Optional)

Start the server and generate latest OpenAPI and GraphQL schemas:

```bash
# Start server in background
./bin/start &

# Wait for server to be ready (check http://localhost:5002/health)
# Then generate schemas:

# OpenAPI schema
curl http://localhost:5002/shipping-openapi -o schemas/openapi.yml
curl http://localhost:5002/shipping-openapi?docs -o apps/www/openapi.yml

# GraphQL schema (requires running server)
karrio graphql_schema --schema karrio.server.graph.schema --out schemas/graphql.json

# Generate TypeScript types from GraphQL schema
./bin/generate-graphql-types

# Stop the server
kill %1
```

### Step 9: Build Packages (Optional)

```bash
# Dry run - check what would be built
./bin/build-and-release-packages --dry-run

# Build only (no publish)
./bin/build-and-release-packages --build-only

# Build and publish
./bin/build-and-release-packages
```

## Automated Release

The full release process is automated via `bin/release`:

```bash
# Auto-increment patch version
./bin/release

# Or specify a version explicitly
./bin/release 2026.2.0
```

This script handles everything: version bump, package sync, frozen requirements,
CHANGELOG generation, submodule commits, branch push, and PR creation/update.

## Manual Release Command

For a manual release with no schema regeneration:

```bash
./bin/update-version <OLD> <NEW> && \
./bin/update-package-versions && \
./bin/update-version-freeze && \
./bin/update-source-version-freeze && \
git add -A && \
git commit -m "release: <NEW>"
```

## Version Format

Karrio uses calendar versioning: `YYYY.M.PATCH` (e.g., `2026.1.20`).
The central version file is `apps/api/karrio/server/VERSION`.

## Troubleshooting

- **Version mismatch**: Run `./bin/update-package-versions` to sync all pyproject.toml
- **Freeze fails**: Ensure clean virtualenv with `source bin/create-new-env --empty`
- **Submodule out of date**: `git submodule update --remote --merge`
- **Build fails**: Check `pip install build setuptools wheel` are available
