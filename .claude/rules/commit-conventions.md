# Commit & PR Conventions

## Commit Messages

Format: `type(scope): summary` or `type: summary`

**Types**: `feat`, `fix`, `chore`, `refactor`, `test`, `docs`, `release`

**Scopes**: carrier name (e.g. `ups`, `fedex`, `dhl_express`, `smartkargo`, `canadapost`), or module (`admin`, `graph`, `manager`, `core`, `cli`, `sdk`, `dashboard`, `mcp`, `tracing`, `documents`, `data`, `events`, `orders`, `proxy`, `pricing`, `connectors`).

Examples:

```
feat(smartkargo): add rate + shipment support
fix(dhl_parcel_de): make package dimensions optional in shipment request
chore: update requirements
refactor(graph): auto-discover schemas via pkgutil.iter_modules
test(admin): add system rate sheet CRUD tests
docs(subtree): document SUBTREE_SYNC_WORKFLOW
release: 2026.5.0
```

## Rules

- **CRITICAL**: NEVER add `Co-Authored-By: <AI model>` or any AI attribution lines.
- **CRITICAL**: NEVER add "Generated with Claude Code" or similar AI footers to commits or PR bodies.
- **CRITICAL**: NEVER commit without explicit user permission.
- Max 72-character subject line, imperative mood ("add", not "added").
- Reference issues: `refs #123` or `fixes #123`.
- Keep commits focused — one logical change per commit.
- Run tests before pushing: `./bin/run-sdk-tests` and/or `./bin/run-server-tests`.

## Pull Requests

- Title under 70 characters, same format as commits.
- Body follows [`git-workflow.md`](./git-workflow.md) — Feature / Fix / Release templates.
- No AI-generated boilerplate footers.
- Group related changes by `### Feat`, `### Fix`, `### Docs`, `### Chore` sections in release PRs.
- Use tables for file-level change summaries and audit matrices.
- Include test/build evidence in the Verification section.

## Branch Naming

Format: `type/description` — examples:

- `feat/2026.5-huey-http`
- `fix/dhl-parcel-de-dimensions-optional`
- `hotfix/2026.1.29-idempotent-archiving-migrations`
- `chore/2026.5-ruff-precommit`
- `sync/shipping-platform-2026-04-19` (upstream subtree sync; see `PRDs/SUBTREE_SYNC_WORKFLOW.md`)

## Release Commits

- Format: `release: YYYY.M.PATCH` (calendar versioning).
- Central version file: `apps/api/karrio/server/VERSION`.
- Version bump process: `./bin/update-version` → `./bin/update-package-versions` → `./bin/update-version-freeze` → `./bin/update-source-version-freeze`, or use `./bin/release [version]` for the full workflow.

## Subtree Sync Commits

When pulling changes from or pushing to `jtlshipping/shipping-platform` per `PRDs/SUBTREE_SYNC_WORKFLOW.md`:

- Prefix with `fix: sync shipping-platform patches (<brief description>)`.
- Branch name: `sync/shipping-platform-YYYY-MM-DD`.
- Isolate sync to a single commit; no mixing with semantic changes.
- Document conflict-resolution decisions in the PR body (the SUBTREE_SYNC_WORKFLOW matrix is the authority).
