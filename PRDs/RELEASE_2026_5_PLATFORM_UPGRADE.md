# Release 2026.5 — Platform Upgrade

<!-- ARCHITECTURE: System design PRD bundling six workstreams into a single release -->

| Field       | Value                                          |
| ----------- | ---------------------------------------------- |
| Project     | Karrio                                         |
| Version     | 1.0                                            |
| Date        | 2026-04-18                                     |
| Status      | Planning                                       |
| Owner       | Daniel Kobina                                  |
| Type        | Architecture (umbrella)                        |
| Target Tag  | `2026.5.0`                                     |
| Umbrella PR | `feat/2026.5` → `main`                         |
| Reference   | [AGENTS.md](../AGENTS.md), [issue #431](https://github.com/jtlshipping/shipping-platform/issues/431) |

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Open Questions & Decisions](#open-questions--decisions)
3. [Problem Statement](#problem-statement)
4. [Goals & Success Criteria](#goals--success-criteria)
5. [Alternatives Considered](#alternatives-considered)
6. [Technical Design](#technical-design)
7. [Workstream Breakdown (Sub-PRs)](#workstream-breakdown-sub-prs)
8. [Edge Cases & Failure Modes](#edge-cases--failure-modes)
9. [Implementation Plan](#implementation-plan)
10. [Testing Strategy](#testing-strategy)
11. [Risk Assessment](#risk-assessment)
12. [Migration & Rollback](#migration--rollback)
13. [Agent Orchestration Plan](#agent-orchestration-plan)

---

## Executive Summary

Release 2026.5 bundles six coordinated workstreams that together raise Karrio's platform-engineering floor: learn-and-apply dev-tooling from JTL shipping-platform, introduce ruff + pre-commit, consolidate the three core server packages (`core` + `graph` + `admin`) into a single auto-discovering `modules/server/` package, finish the Helm chart for EKS with an HPA-friendly worker split, add an HTTP producer layer in front of Huey so API and worker pods scale independently, and add a Playwright golden-path E2E suite gated in CI before the release-tag job. Work is tracked under umbrella branch `feat/2026.5` with one sub-PR per workstream; the release tag `2026.5.0` lands after all sub-PRs and the new E2E suite are green on `main`.

### Key Architecture Decisions

1. **Umbrella branch + sequential sub-PRs** — Each workstream ships as its own PR into `feat/2026.5`; final merge into `main` happens only when all sub-PRs and the new E2E gate are green. Preserves reviewability and isolates rollback.
2. **Consolidation scope = OSS core server only** — Merge `modules/core`, `modules/graph`, and the OSS `modules/admin` (NOT `ee/insiders/modules/admin`) into `modules/server/` as a single package with Django auto-discovery. Connectors (`modules/connectors/*`) and the shipping SDK (`modules/sdk`, `modules/soap`) stay as separate packages because they are plugin-scoped and benefit from independent install. EE modules under `ee/insiders/modules/*` are out of scope for this release.
3. **Auto-discovery via `pkgutil.iter_modules()`** — Replace explicit `INSTALLED_APPS` + schema registration with runtime discovery, matching the pattern validated in JTL shipping-platform's `karrio/server/graph/schema.py`.
4. **Huey producer HTTP API, not worker protocol** — Expose a minimal internal HTTP endpoint on API pods that enqueues tasks into the existing huey/Redis backend. Workers keep consuming huey directly. This splits API autoscaling from worker autoscaling under EKS HPA without rewriting the task runtime.
5. **Ruff + pre-commit adopted from JTL config** — Port `py312` target, rule selection `E,W,F,I,B,S,UP,SIM,DJ,T20`, and per-file ignores verbatim. Add pre-commit hooks for ruff-check, ruff-format, prettier on the frontend. One sub-PR applies fixes in bulk; no mixed semantic/style changes.
6. **E2E scope = golden-path smoke** — Playwright suite (~10–15 specs) covering auth → shipment → label → track → order → settings. Runs in CI against docker-compose before the release-tag workflow. Carrier calls stubbed with fixtures; no live-carrier E2E in this release.
7. **Feature picks = subtree sync per `SUBTREE_SYNC_WORKFLOW.md`** — Upstream changes from `jtlshipping/shipping-platform` land via the scripted subtree-export workflow (`bin/export-karrio-patches` → `git apply --3way` → sync PR into `karrioapi/karrio` main and `karrioapi/karrio-insiders` main). No manual diff-and-propose; the existing scripts and conflict matrix govern. Dev-tooling (ruff, pre-commit, `.claude/` skills/rules) is applied directly to this branch in sub-PRs 1–2; proprietary JTL modules are excluded by the patch-export filters and the conflict matrix.

### Scope

| In Scope                                                                  | Out of Scope                                                              |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `feat/2026.5` umbrella branch + 6 sub-PRs                                 | Full 9-module consolidation (only core/graph/admin in this release)       |
| Ruff + pre-commit config, bulk auto-fixes                                 | Rewriting tests to pytest (project stays on unittest / `karrio test`)      |
| `modules/server/` consolidation w/ auto-discovery                          | Connector module restructuring                                             |
| Helm chart finalization (values schema, HPA, PDB, ingress variants)       | New managed deployment offering / SaaS control plane                       |
| Huey HTTP producer endpoint + deploy split                                 | Replacing Huey with Celery/SQS/PubSub                                      |
| Playwright golden-path E2E wired into CI                                   | Live-carrier E2E, visual regression, multi-browser matrix                  |
| `.claude/` skills + rules + agents imports from JTL                        | Shipping JTL-proprietary modules (entitlements, wawi, servicebus, beta…)  |
| `karrio-insiders` submodule pointer bump (after insiders sync PR merges)   | Repository-merge / license-gating work (explicitly ignored for this release) |
| Upstream subtree sync PRs into `karrioapi/karrio` main + `karrioapi/karrio-insiders` main per `SUBTREE_SYNC_WORKFLOW.md` | Manual feature-by-feature picking from shipping-platform |
| Release tag `2026.5.0` + changelog                                         | Backport of 2026.5 features to 2026.1.x                                    |

---

## Open Questions & Decisions

### Resolved Decisions

| #  | Decision                         | Choice                                        | Rationale                                                                                 | Date       |
| -- | -------------------------------- | --------------------------------------------- | ----------------------------------------------------------------------------------------- | ---------- |
| D1 | Consolidation scope              | Core server only (core + graph + admin)       | Minimizes blast radius; proves the auto-discovery pattern before expanding                | 2026-04-18 |
| D2 | Huey architecture                | Producer-only HTTP API on API pods            | Enables EKS HPA split without rewriting workers; smallest diff                            | 2026-04-18 |
| D3 | E2E scope                        | Playwright golden-path smoke, CI-gated        | Catches the 80% regressions that block releases; stub carriers to keep CI deterministic   | 2026-04-18 |
| D4 | Orchestration                    | Umbrella branch + sequential sub-PRs          | Each sub-PR is reviewable; rollback is per-workstream                                     | 2026-04-18 |
| D5 | Feature-pick scope               | Scripted subtree sync per `SUBTREE_SYNC_WORKFLOW.md` | The canonical workflow already exists (`bin/export-karrio-patches`) and has documented conflict resolution; inventing a manual recon would duplicate it | 2026-04-18 |
| D6 | Version bump                     | `2026.5.0`                                    | Clear minor jump from `2026.1.28` signals a large feature drop                             | 2026-04-18 |
| D7 | Ruff config source               | Port JTL `ruff.toml` verbatim, then fix       | JTL config is battle-tested on Django; verbatim port avoids bikeshedding                  | 2026-04-18 |
| D8 | `.claude/` skill/rule source     | Adopt JTL skill/rule names + structure        | Aligns sister-repo documentation contract; makes cross-repo agent work consistent         | 2026-04-18 |

### Pending Questions

| #   | Question                                                            | Context                                                                                                                 | Status   |
| --- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | -------- |
| Q1  | Ruff format vs Black for Python formatting                          | JTL uses Black; ruff-format is now feature-complete. Recommend ruff-format to drop a dependency                         | ⏳ Pending |
| Q2  | Huey HTTP endpoint authentication                                   | Internal-only (cluster network policy) vs shared secret header. Recommend shared secret + network policy (belt+braces)  | ⏳ Pending |
| Q3  | Where does the E2E suite live?                                      | `apps/dashboard/e2e/` (co-located with Next dashboard) vs top-level `e2e/` (parallel to docker-compose). Recommend top-level | ⏳ Pending |
| Q4  | Helm chart subcharts for Postgres/Redis?                            | Ship Bitnami postgresql + redis as optional subcharts, or require cluster-provided services. Recommend optional subcharts | ⏳ Pending |
| Q5  | Subtree sync PRs land in `karrioapi/karrio` main directly \| do they block `feat/2026.5`? | Sync PRs target main, not `feat/2026.5`. After they merge, feat/2026.5 rebases main. Sub-PRs 4+ should rebase after the sync lands to avoid re-resolving the same conflicts. Recommend: run 3a/3b early | ⏳ Pending |
| Q6  | Drop `black` + `bandit` from `requirements.dev.txt` after ruff lands | Ruff covers both. Recommend drop in the ruff sub-PR                                                                      | ⏳ Pending |

---

## Problem Statement

### Current State

1. **Three core server packages with duplicated plumbing.** `modules/core`, `modules/graph`, `modules/admin` each ship their own `pyproject.toml`, namespace `__init__.py` files, and separate `-e ./modules/<x>` entries in `requirements.build.txt`. Every new cross-cutting module risks the recurring "forgot to add to build requirements" / "namespace `__init__.py` collision" classes of bugs documented in shipping-platform's issue #431.

2. **No ruff, no pre-commit.** `requirements.dev.txt` lists `black`, `bandit`, `mypy` but no ruff and no pre-commit hooks. Formatting / lint drift is detected only at PR review time. Sister repo shipping-platform has a production ruff config and a rules library we can lift.

3. **Helm chart is live but not release-ready.** `charts/karrio/` contains `api`, `dashboard`, `worker` deployments plus HPA and PDB for `api`, but lacks: worker HPA, values-schema validation, subchart pinning (postgres / redis), ingress variants for ALB/Traefik, documented install quickstart, rendered manifest tests. Cannot yet be tagged `1.0.0` on Artifact Hub.

4. **Huey workers and API pods share scaling signals.** The current docker-compose pattern has API pods and huey consumers enqueue through Redis directly. On EKS, the worker deployment cannot scale on "queue depth" without either a custom metric or a producer boundary; furthermore, anything on the API path that enqueues a task needs Redis creds, widening the API pod's blast radius.

5. **No pre-release E2E gate.** The `tests.yml` workflow runs unit tests and carrier hook tests, but no browser-level flow is exercised before tagging a release. Regressions that cross API + dashboard (auth flows, shipment wizard, tracking page) have historically shipped and been caught in production.

6. **Stale agent tooling.** `.claude/skills/` has 6 skills and `.claude/rules/` has 6 rule files, but they pre-date the PRD template improvements and testing-pattern enforcement that landed in shipping-platform. Agent work in karrio silently drifts from JTL conventions.

### Desired State

```
karrio/
├── modules/
│   ├── server/                 # ← merged core + graph + admin (single package)
│   │   ├── pyproject.toml
│   │   └── karrio/server/
│   │       ├── core/           # former modules/core
│   │       ├── graph/          # former modules/graph
│   │       └── admin/          # former modules/admin
│   ├── connectors/             # unchanged — independent packages
│   ├── sdk/                    # unchanged
│   └── soap/                   # unchanged
├── charts/karrio/              # helm chart — tag 1.0.0 on Artifact Hub
│   ├── values.schema.json      # new — validated by helm lint
│   ├── templates/worker/hpa.yaml    # new
│   └── templates/tests/        # new — helm test hooks
├── modules/server/karrio/server/tasks/http.py  # new — producer HTTP API
├── e2e/                        # new — Playwright golden-path specs
│   ├── playwright.config.ts
│   ├── fixtures/
│   └── specs/
├── ruff.toml                   # new — ported from shipping-platform
├── .pre-commit-config.yaml     # new — ruff-check, ruff-format, prettier
└── .claude/
    ├── skills/                 # updated — ports from shipping-platform
    ├── rules/                  # updated — ports from shipping-platform
    └── agents/                 # new — per-workstream subagent prompts
```

```
CI timeline (new):
  push/PR ──> lint (ruff)   ──> unit tests ──> helm lint + values.schema
                                    │
                                    ▼
                           docker-compose up
                                    │
                                    ▼
                         playwright e2e smoke  ──> release-tag job (if tag push)
```

---

## Goals & Success Criteria

### Goals

| #  | Goal                                                                         | Measured by                                                                         |
| -- | ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| G1 | Ship release `2026.5.0` from `feat/2026.5` once all sub-PRs merge             | Git tag `2026.5.0` exists and has green CI                                          |
| G2 | Eliminate the "forgot to register a module" class of bug for server code      | `-e ./modules/server` is the single entry for core/graph/admin                      |
| G3 | Add a CI-enforced style floor without introducing churn in day-to-day PRs     | Ruff + pre-commit in place; fix commit is separated from semantic changes          |
| G4 | Publish a Helm chart that a fresh EKS cluster can install without editing     | `helm install karrio karrio/karrio -f values.yaml` succeeds on an empty cluster     |
| G5 | Allow worker pods to scale independently of API pods                          | `worker` HPA scales on queue-depth metric; API pods don't need Redis creds          |
| G6 | Block releases that break the 5 golden-path flows                             | Playwright smoke suite required on release-tag workflow                             |
| G7 | Bring `.claude/` tooling up to parity with shipping-platform                   | Skill/rule count matches JTL's core set; `AGENTS.md` priority section aligned       |

### Success Metrics

| Metric                                                  | Baseline (2026.1.28) | Target (2026.5.0) |
| ------------------------------------------------------- | -------------------- | ----------------- |
| `-e ./modules/*` entries for core server packages        | 3                    | 1                 |
| Python `pyproject.toml` files across repo                | N                    | N − 2             |
| Ruff errors on first `ruff check .` run                  | —                    | 0 (after fix commit) |
| Pre-commit hooks enforced                                | 0                    | ≥ 4 (ruff-check, ruff-format, prettier, trailing-whitespace) |
| Helm chart templates                                     | 12                   | ≥ 15 (+ worker/hpa, values.schema.json, tests) |
| API pod env vars referencing Redis creds                 | `REDIS_*` present    | `REDIS_*` removed (API talks HTTP to broker)  |
| CI job for Playwright E2E                                | absent               | required on release tag |
| `.claude/skills/` count                                  | 6                    | ≥ 8 (porting from JTL) |

### Launch Criteria

- [ ] All six sub-PRs merged into `feat/2026.5`
- [ ] `feat/2026.5` passes full CI (unit + helm lint + playwright + insiders submodule build)
- [ ] Helm chart installs cleanly on a scratch EKS cluster (manual smoke)
- [ ] `karrio-insiders` submodule bumped to a 2026.5-compatible commit
- [ ] CHANGELOG entry for `2026.5.0`
- [ ] Migration & rollback section reviewed by one other maintainer

---

## Alternatives Considered

| Alternative                                                             | Pros                                         | Cons                                                                                   | Decision |
| ----------------------------------------------------------------------- | -------------------------------------------- | -------------------------------------------------------------------------------------- | -------- |
| Single giant PR with all six workstreams                                | One review cycle, atomic release             | Unreviewable, unrecoverable if one workstream regresses                                | Rejected |
| Merge all nine karrio server packages (match JTL's #431 full scope)     | Eliminates the class of bug everywhere       | Doubles migration risk, blocks release on orders/events/manager refactors              | Deferred to 2026.6 |
| Huey replacement with Celery + SQS                                       | First-class AWS integration                  | Multi-quarter rewrite, blocks release                                                  | Deferred |
| Full-regression E2E (live carriers + visual regression)                  | Catches more regressions                     | Flaky on CI; live-carrier API credentials in CI surface area                           | Deferred; use fixtures for 2026.5 |
| Port all 12 JTL `.claude/rules/` verbatim                                 | Fastest path to parity                       | Some rules (entitlements, wawi, servicebus) reference JTL-only modules                 | Reject — pick only the generic 6–8 |
| Run pre-commit on server but not frontend                                | Smaller diff                                 | Frontend drift continues; prettier is cheap                                            | Rejected |

---

## Technical Design

### Architecture Overview

```
┌──────────────────────── repo top-level ────────────────────────┐
│                                                                │
│  feat/2026.5 ──► sub-PR 1 ──► .claude/ + AGENTS.md             │
│              ──► sub-PR 2 ──► ruff.toml + pre-commit + fixes    │
│              ──► sub-PR 3 ──► modules/server/ consolidation     │
│              ──► sub-PR 4 ──► charts/karrio finalization        │
│              ──► sub-PR 5 ──► huey HTTP producer + worker split │
│              ──► sub-PR 6 ──► e2e/ playwright smoke + CI gate   │
│              ──► sub-PR 7 ──► recon report (feature-pick diff)  │
│                                                                │
└────────────────────────────────────────────────────────────────┘
                             │
                             ▼
                  merge feat/2026.5 → main
                             │
                             ▼
                     tag 2026.5.0 + release
```

### Module consolidation (core-only)

Current:

```
modules/
├── core/    pyproject.toml  (setuptools, namespace karrio.server.core)
├── graph/   pyproject.toml  (setuptools, namespace karrio.server.graph)
└── admin/   pyproject.toml  (setuptools, namespace karrio.server.admin)
```

Target:

```
modules/
└── server/
    ├── pyproject.toml                       (single setuptools build)
    └── karrio/server/
        ├── __init__.py                      (namespace package, no shadowing)
        ├── core/    <── moved from modules/core/karrio/server/core/
        ├── graph/   <── moved from modules/graph/karrio/server/graph/
        └── admin/   <── moved from modules/admin/karrio/server/admin/ (OSS admin only — NOT ee/insiders/modules/admin)
```

`requirements.build.txt` delta:

```diff
- -e ./modules/core
- -e ./modules/graph
- -e ./modules/admin
+ -e ./modules/server
```

Auto-discovery (ported from shipping-platform):

```python
# modules/server/karrio/server/graph/schema.py
import pkgutil
from . import schemas
QUERIES, MUTATIONS = [], []
for _, name, _ in pkgutil.iter_modules(schemas.__path__):
    schema = __import__(f"{schemas.__name__}.{name}", fromlist=[name])
    if hasattr(schema, "Query"):    QUERIES.append(schema.Query)
    if hasattr(schema, "Mutation"): MUTATIONS.append(schema.Mutation)
```

### Huey HTTP producer — sequence

```
┌──────────────┐   HTTP POST      ┌──────────────┐   redis push   ┌──────────────┐
│ API pod      │ ───────────────► │ broker pod   │ ─────────────► │ redis        │
│ (no REDIS_*) │   /tasks/enqueue │ (has REDIS_*)│                │              │
└──────────────┘                  └──────────────┘                └──────┬───────┘
                                                                         │ consume
                                                                         ▼
                                                                  ┌──────────────┐
                                                                  │ worker pod   │
                                                                  │ huey consumer│
                                                                  └──────────────┘
```

`broker` is a thin Django view on the existing API image, but the API Deployment no longer needs Redis credentials. Workers continue to consume huey directly from Redis. Queue depth is available as a Prometheus metric from the broker endpoint and the worker HPA scales on it.

Minimal contract:

```
POST /internal/tasks/enqueue
Headers: X-Karrio-Worker-Key: <shared secret>
Body:    { "task": "karrio.server.events.send_webhook", "args": [...], "kwargs": {...}, "delay": 0 }
Return:  202 { "task_id": "..." }
```

### Helm chart finalization — key deltas

- `values.schema.json` derived from `values.yaml` via `helm-values-schema-json` plugin, checked into repo.
- `templates/worker/hpa.yaml` scaling on `karrio_queue_depth` custom metric (documented as optional / metrics-server-required).
- `templates/tests/connection.yaml` helm test hook (`helm test`) hitting `/api/status/`.
- Ingress: `values.yaml` gains `ingress.className` with examples for `alb`, `nginx`, `traefik` in `values-examples/`.
- Optional subcharts: `postgresql` (Bitnami), `redis` (Bitnami), gated on `postgresql.enabled` / `redis.enabled`.
- `README.md` quickstart: `helm install karrio . -f values-examples/eks-alb.yaml`.

### Ruff + pre-commit

Port `ruff.toml` from shipping-platform verbatim (rules `E,W,F,I,B,S,UP,SIM,DJ,T20`, `line-length = 120`, `target-version = "py312"`, per-file-ignores for migrations/tests). One sub-PR does:

1. Commit 1: add `ruff.toml`, `.pre-commit-config.yaml`, update `requirements.dev.txt` (`ruff` in, `black`/`bandit` out).
2. Commit 2: `ruff check --fix --unsafe-fixes` + `ruff format .` across the repo. No semantic changes.
3. Commit 3: fix any remaining ruff errors manually.

Pre-commit hooks:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks: [{ id: ruff, args: [--fix] }, { id: ruff-format }]
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks: [trailing-whitespace, end-of-file-fixer, check-yaml, check-merge-conflict]
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v4.0.0-alpha.8
    hooks: [{ id: prettier, types_or: [ts, tsx, js, jsx, json, yaml, css, scss] }]
```

### E2E smoke — structure

```
e2e/
├── playwright.config.ts          # chromium + firefox, CI reporter, trace on-retry
├── fixtures/
│   ├── auth.ts                   # logged-in user fixture (seeded via API)
│   └── docker-compose.ts         # waits for api + dashboard healthy
├── helpers/
│   ├── api.ts                    # REST client for seeding
│   └── selectors.ts              # shared locators
└── specs/
    ├── auth.spec.ts              # login / logout / password reset
    ├── shipment.spec.ts          # create → rate → buy label (stubbed carrier)
    ├── tracking.spec.ts          # track a shipment by tracking number
    ├── order.spec.ts             # create order → fulfill
    └── settings.spec.ts          # API key CRUD, carrier connection CRUD
```

CI wiring: new job `e2e` in `.github/workflows/tests.yml` that spins up `docker-compose.yml`, seeds a tenant, runs `npx playwright test`, uploads HTML report artifact. Required on any ref that matches `refs/tags/2026.*`.

### `.claude/` upgrades

Skills (port + adapt from shipping-platform):

| Skill name                    | Action | Source                                         |
| ----------------------------- | ------ | ---------------------------------------------- |
| `create-prd`                  | Update | JTL version is newer; our template is fine but process guide is thin |
| `create-extension-module`     | New    | Port from JTL (module bootstrap + AppConfig ready hook) |
| `create-carrier-hook`         | Keep   | Karrio-specific; already thorough              |
| `django-graphql`              | New    | Port (schema layout + auto-discovery)          |
| `django-rest-api`             | New    | Port (view / serializer / URL patterns)        |
| `review-implementation`       | Update | Align with JTL checklist                       |
| `run-tests`                   | Update | Document `karrio test` vs `python -m unittest` |
| `release`                     | Keep   | Karrio-specific; already thorough              |

Rules (ported file names in `.claude/rules/`):

- `code-style.md` (port + merge with existing)
- `extension-patterns.md` (new — "extend, don't modify core" philosophy)
- `testing.md` (update — unittest + `karrio test` enforcement, no pytest)
- `commit-conventions.md` (new)
- `git-workflow.md` (keep)
- `prd-and-review.md` (keep)
- `django-patterns.md` (keep)
- `carrier-integration.md` (keep)

AGENTS.md: add explicit "Context Priority" section (from JTL) at the top referencing the `.claude/` structure.

---

## Workstream Breakdown (Sub-PRs)

Each sub-PR targets `feat/2026.5` **except** 3a and 3b — those are subtree-sync PRs that target `karrioapi/karrio` main and `karrioapi/karrio-insiders` main directly, per `SUBTREE_SYNC_WORKFLOW.md`. After 3a/3b merge, `feat/2026.5` rebases onto the updated main to pick them up (and bumps the insiders submodule pointer for 3b).

Agents run in isolated worktrees; dependencies are shown in the table.

| #   | Sub-PR title (branch)                                                | Target                             | Scope                                                                                                                                                              | Depends on | Agent profile       | Est. effort |
| --- | -------------------------------------------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------- | ------------------- | ----------- |
| 1   | `chore/2026.5-claude-tooling` — agent rules + skills upgrade          | `feat/2026.5`                      | Import + adapt `.claude/skills/` and `.claude/rules/` from shipping-platform. Update AGENTS.md context-priority section. No Python code changes.                     | —          | general-purpose     | S           |
| 2   | `chore/2026.5-ruff-precommit` — lint floor                            | `feat/2026.5`                      | Add `ruff.toml`, `.pre-commit-config.yaml`, update `requirements.dev.txt`. One bulk auto-fix commit. One manual-fix commit.                                          | 1          | general-purpose     | M           |
| 3a  | `sync/shipping-platform-<date>` — karrio subtree sync                 | `karrioapi/karrio` main            | Run `bin/export-karrio-patches --force -o /tmp/karrio.patch` in shipping-platform; `git apply --3way` in karrio clone; resolve per conflict matrix; open sync PR into karrio main. Governed by `SUBTREE_SYNC_WORKFLOW.md`. | —          | general-purpose     | M           |
| 3b  | `sync/shipping-platform-<date>` — karrio-insiders subtree sync         | `karrioapi/karrio-insiders` main   | Same flow with `--insiders`; `ee/insiders` is a submodule so `--apply` fails — export to file then `git apply --3way` in `ee/insiders`; open sync PR into insiders main. | —          | general-purpose     | M           |
| 4   | `refactor/2026.5-modules-server` — core/graph/admin merge              | `feat/2026.5`                      | Move OSS `modules/core` + `modules/graph` + `modules/admin` under `modules/server/`, single `pyproject.toml`, auto-discovery. Update Dockerfile, `requirements.build.txt`, CI scripts. NOT `ee/insiders/modules/admin`. | 2, 3a      | general-purpose     | L           |
| 5   | `feat/2026.5-helm-chart` — finalize Helm chart                         | `feat/2026.5`                      | `values.schema.json`, worker HPA, helm test hooks, ingress variants, optional subcharts, README quickstart, `helm lint` + `helm template` in CI.                   | 2          | general-purpose     | M           |
| 6   | `feat/2026.5-huey-http` — producer HTTP API                           | `feat/2026.5`                      | New `modules/server/karrio/server/tasks/http.py` view, deploy split (API pod has no Redis creds), chart update, metrics endpoint, migration note.                   | 4, 5       | general-purpose     | M           |
| 7   | `feat/2026.5-e2e-smoke` — Playwright golden-path                       | `feat/2026.5`                      | New `e2e/` directory, ~12 specs, CI workflow step, trace + video on failure, docs.                                                                                 | 2          | general-purpose     | M           |
| 8   | `release/2026.5.0` — tag + changelog                                   | `feat/2026.5` → `main`             | CHANGELOG entry, VERSION bumps, verify insiders submodule points at the 3b-merge commit, final CI green, open PR to main.                                          | 1–7        | (human)             | S           |

Effort legend: S ≤ 1 day, M 2–4 days, L ≥ 5 days.

---

## Edge Cases & Failure Modes

| #   | Scenario                                                       | Impact                                                                     | Handling                                                                                                                    |
| --- | -------------------------------------------------------------- | -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| E1  | `modules/core`, `modules/graph`, `modules/admin` imports in insiders/platform submodules | Insiders CI breaks after consolidation                                     | Keep `modules/core`, `modules/graph`, `modules/admin` as thin shim packages that re-export from `modules/server` for one release |
| E2  | A downstream user has a pinned `karrio-server-core==2026.1.x` on PyPI | Upgrade to 2026.5 fails because package name changes                       | Publish `karrio-server` as the new name AND keep publishing shim packages for 2026.5 → 2026.7 window; drop in 2026.8         |
| E3  | Ruff auto-fix rewrites code that has unit-test expectations on formatting | Tests fail after fix commit                                                | Fix-commit PR MUST run full test suite; any failures are resolved in commit 3                                                |
| E4  | Huey HTTP broker endpoint becomes an unauth-able attack surface | Anyone with in-cluster access can enqueue arbitrary tasks                  | Shared-secret header + Kubernetes NetworkPolicy + listen on a non-public Service; never exposed via Ingress                  |
| E5  | Playwright E2E flakes on CI (docker-compose timing)             | Release-tag job is blocked                                                 | Retry-on-failure (max 2), explicit readiness waits in fixtures, `trace: on-first-retry`; flakes file an issue, don't bypass  |
| E6  | Helm chart subchart pinning drifts                              | Production installs break on Bitnami chart upstream changes                | Pin subchart versions in `Chart.lock`; Renovate PR cadence                                                                   |
| E7  | Subtree-sync patch contains JTL-proprietary modules (entitlements, wawi, servicebus, beta, support, jtl, security) | Risk of license contamination                                              | Before committing the sync, grep the applied diff for those module paths and drop any hunks that touch them; the conflict matrix already excludes JTL-specific settings/connectors |
| E8  | `pkgutil.iter_modules()` picks up a test or migration package   | Spurious Query/Mutation registration, import-time failures                  | Discovery iterates `schemas/` / `mutations/` subpackages only; explicit allowlist of module prefixes                          |

---

## Implementation Plan

### Phase 1 — Foundation (sub-PRs 1–2, ~3 days)

| File / area                           | Change                                                                                |
| ------------------------------------- | ------------------------------------------------------------------------------------- |
| `.claude/skills/*`                    | Port / update per table above                                                         |
| `.claude/rules/*`                     | Port / update per table above                                                         |
| `AGENTS.md`                           | Context-priority header; link to new rules                                            |
| `ruff.toml`                           | New, ported verbatim from shipping-platform                                           |
| `.pre-commit-config.yaml`             | New, 3 repos + prettier                                                               |
| `requirements.dev.txt`                | `+ruff`, `+pre-commit`, `-black`, `-bandit`                                           |
| `.github/workflows/tests.yml`         | New `lint` job runs `pre-commit run --all-files`                                       |

### Phase 2 — Subtree sync + server consolidation (sub-PRs 3a/3b, 4, ~6 days)

**Sub-PRs 3a/3b** land upstream first (into `karrioapi/karrio` main and `karrioapi/karrio-insiders` main). Follow the Agent Playbook in `PRDs/SUBTREE_SYNC_WORKFLOW.md`:

| Step | Command (from `/Users/danielkobina/Workspace/jtl/shipping-platform`)                                                                    |
| ---- | --------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | `git status` — confirm clean working tree                                                                                               |
| 2    | `./bin/export-karrio-patches --check-upstream`   and   `./bin/export-karrio-patches --insiders --check-upstream`                        |
| 3a   | `./bin/export-karrio-patches --force -o /tmp/karrio.patch`, then in `/Users/danielkobina/Workspace/karrio/karrio`: `git checkout main && git pull && git checkout -b sync/shipping-platform-$(date +%Y-%m-%d) && git apply --3way /tmp/karrio.patch` |
| 3b   | `./bin/export-karrio-patches --insiders --force -o /tmp/insiders.patch`, then in `/Users/danielkobina/Workspace/karrio/karrio/ee/insiders`: `git checkout main && git pull && git checkout -b sync/shipping-platform-$(date +%Y-%m-%d) && git apply --3way /tmp/insiders.patch` (NOT `--apply`; submodule `.git` is a file) |
| 4    | Resolve per conflict matrix (static assets → subtree version; upstream-only features → keep upstream; version numbers → keep upstream) |
| 5    | `grep -E 'modules/(entitlements\|wawi\|servicebus\|beta\|support\|jtl\|security)/' <diff>` — must be empty before committing            |
| 6    | Commit as `fix: sync shipping-platform patches (...)`, push, open sync PR                                                                |
| 7    | Once merged upstream: back in shipping-platform run `./bin/update-subtrees` to pull back the merged change                               |

**Sub-PR 4** (consolidation) rebases onto main after 3a has merged to avoid re-resolving the same conflicts:

| File / area                                                  | Change                                                                                        |
| ------------------------------------------------------------ | --------------------------------------------------------------------------------------------- |
| `modules/server/pyproject.toml`                              | New — single package with combined deps                                                        |
| `modules/server/karrio/server/{core,graph,admin}/*`          | `git mv` from OSS `modules/{core,graph,admin}/karrio/server/<x>/*`                              |
| `modules/{core,graph,admin}/`                                | Replace with shim packages (namespace-only) for one release                                    |
| `modules/server/karrio/server/graph/schema.py`               | Swap to `pkgutil.iter_modules()` discovery                                                     |
| `modules/server/karrio/server/admin/schema.py`               | Same                                                                                           |
| `requirements.build.txt`                                     | `-e ./modules/core`, `-e ./modules/graph`, `-e ./modules/admin` → `-e ./modules/server` (+ shims)|
| `docker/*Dockerfile*`                                        | Single `COPY modules/server`                                                                   |
| `bin/run-server-tests`                                       | Replace three test paths with `karrio test karrio.server.tests`                                 |

### Phase 3 — Helm chart finalization (sub-PR 5, ~3 days)

| File                                                      | Change                                                     |
| --------------------------------------------------------- | ---------------------------------------------------------- |
| `charts/karrio/values.schema.json`                        | New — generated + committed                                 |
| `charts/karrio/templates/worker/hpa.yaml`                 | New                                                        |
| `charts/karrio/templates/tests/connection.yaml`           | New — helm test hook                                        |
| `charts/karrio/Chart.yaml`                                 | `dependencies:` postgresql + redis (optional)               |
| `charts/karrio/values.yaml`                                | `postgresql.enabled`, `redis.enabled`, `ingress.className` |
| `charts/karrio/values-examples/{eks-alb,gke,local}.yaml`  | New                                                        |
| `charts/karrio/README.md`                                  | Quickstart + upgrade notes                                  |
| `.github/workflows/tests.yml`                             | New `helm` job: `helm lint`, `helm template`, `kubeconform`|

### Phase 4 — Huey HTTP producer (sub-PR 6, ~3 days)

| File                                                              | Change                                              |
| ----------------------------------------------------------------- | --------------------------------------------------- |
| `modules/server/karrio/server/tasks/http.py`                      | New — enqueue view + metrics endpoint                |
| `modules/server/karrio/server/tasks/urls.py`                      | New — `/internal/tasks/*`                            |
| `modules/server/karrio/server/settings/base.py`                   | Separate `BROKER_URL` (API) from `REDIS_URL` (worker) |
| `charts/karrio/templates/broker/*`                                | New optional `broker` deployment (can be colocated with worker for small installs) |
| `charts/karrio/values.yaml`                                        | `broker.*` block                                     |
| `modules/server/karrio/server/tests/tasks/test_http.py`           | Unit tests: auth, 202 on valid, 400 on bad task name |

### Phase 5 — Playwright E2E (sub-PR 7, ~3 days)

| File                                                 | Change       |
| ---------------------------------------------------- | ------------ |
| `e2e/playwright.config.ts`                           | New          |
| `e2e/fixtures/*`, `e2e/helpers/*`                    | New          |
| `e2e/specs/{auth,shipment,tracking,order,settings}.spec.ts` | New   |
| `package.json` (root)                                | `e2e:test` script |
| `.github/workflows/tests.yml`                        | New `e2e` job — required on release tags |
| `docker-compose.e2e.yml`                             | New — seeded tenant + stubbed carrier |

### Phase 6 — Release (sub-PR 8, ~1 day)

| File                                                 | Change                         |
| ---------------------------------------------------- | ------------------------------ |
| `modules/server/karrio/server/__init__.py` (etc.)    | Version strings → `2026.5.0`   |
| `CHANGELOG.md`                                       | Entry for `2026.5.0`           |
| `charts/karrio/Chart.yaml`                           | `appVersion: 2026.5.0`, `version: 1.0.0` |
| `ee/insiders`                                         | Verify submodule points at the 3b-merge commit (no extra bump) |
| `ee/platform`                                         | Final submodule bump if needed |
| Tag                                                  | `git tag -s 2026.5.0`          |

---

## Testing Strategy

- **Unit tests** — Existing `karrio test` wrappers. New modules added with co-located `tests/` following the repo's unittest convention. No pytest.
- **Helm tests** — `helm lint charts/karrio`, `helm template charts/karrio -f values-examples/eks-alb.yaml | kubeconform`, `helm test <release>` in an ephemeral kind cluster (optional).
- **Ruff** — `pre-commit run --all-files` in CI; same via local git hook.
- **Playwright E2E** — `docker-compose -f docker-compose.e2e.yml up -d --wait`, then `npx playwright test`. Trace on first retry. Required on release tag pushes.
- **Migration-safety system check** — Extend the existing `check` rolling-deploy system check (added in commit `820101b6f`) to cover the consolidated `modules/server` migrations.

Example test (producer HTTP endpoint):

```python
# modules/server/karrio/server/tests/tasks/test_http.py
import unittest
from django.test import Client

class TestTaskEnqueue(unittest.TestCase):
    def setUp(self): self.client = Client()

    def test_enqueue_requires_worker_key(self):
        response = self.client.post("/internal/tasks/enqueue", {"task": "noop"})
        self.assertEqual(response.status_code, 401)

    def test_enqueue_unknown_task_rejected(self):
        response = self.client.post(
            "/internal/tasks/enqueue",
            {"task": "karrio.tasks.does_not_exist"},
            content_type="application/json",
            HTTP_X_KARRIO_WORKER_KEY="test-secret",
        )
        self.assertEqual(response.status_code, 400)
```

---

## Risk Assessment

| Risk                                                          | Impact     | Probability | Mitigation                                                                                                                |
| ------------------------------------------------------------- | ---------- | ----------- | ------------------------------------------------------------------------------------------------------------------------- |
| Consolidation breaks downstream installs (`karrio-server-core` pinned) | High       | Medium      | Shim packages re-export from new location for 2026.5→2026.7; changelog + migration doc                                      |
| Ruff bulk fix introduces subtle semantic change               | Medium     | Low         | Separate bulk auto-fix commit; full unit-test run in CI; require manual review                                            |
| Helm chart subchart drift                                      | Medium     | Medium      | Pin in `Chart.lock`; Renovate cadence                                                                                     |
| Huey HTTP endpoint becomes attack surface                     | High       | Low         | Shared-secret header + NetworkPolicy + cluster-internal service; unit-tested 401 path                                     |
| Playwright E2E becomes flaky; blocks releases                 | High       | Medium      | Retry-on-failure; trace + video on failure; flakes file an issue, don't bypass                                            |
| Subtree-sync patch contains JTL-proprietary code               | Critical   | Low         | Pre-commit grep for `modules/(entitlements\|wawi\|servicebus\|beta\|support\|jtl\|security)/` in the applied diff; drop hunks or abort if matched; human review before push |
| Umbrella branch gets stuck because one sub-PR regresses main   | Medium     | Medium      | Sub-PRs can be dropped from 2026.5 scope and re-scheduled to 2026.6; release is not all-or-nothing                         |
| Insiders submodule CI breaks                                   | High       | Medium      | Shim packages in E1; coordinated submodule bump in sub-PR 8                                                                |

---

## Migration & Rollback

### Backward Compatibility

- **Python import paths**: `karrio.server.core`, `karrio.server.graph`, `karrio.server.admin` continue to work because the consolidated `modules/server` package owns the same namespace. Imports do not change.
- **PyPI package names**: Keep publishing `karrio-server-core`, `karrio-server-graph`, `karrio-server-admin` as shim packages for 2026.5 through 2026.7 that depend on the new `karrio-server`. Deprecation notice in 2026.5 changelog; removal in 2026.8.
- **Django settings**: `INSTALLED_APPS` stays the same (`karrio.server.core`, `karrio.server.graph`, `karrio.server.admin` are still Django app labels inside the consolidated package).
- **Environment variables**: `REDIS_URL` moves off the API Deployment and onto the new `broker` Deployment. A helm-chart upgrade note covers this.

### Rollback

- Each sub-PR is revertible independently on `feat/2026.5`. If a sub-PR regresses the umbrella branch, revert, drop from scope, reschedule to 2026.6.
- If the final release tag ships a regression, `git revert` the merge commit of `feat/2026.5` into `main`; cut `2026.5.1` with the fix. The shim packages (E1/E2) mean downstream installs survive the revert.

### Data Safety

- No schema migrations are introduced by consolidation itself (pure repackaging).
- Huey task payload format is unchanged; only the enqueue transport changes.
- E2E suite uses an isolated `karrio_e2e` database seeded per run and torn down after.

---

## Agent Orchestration Plan

### Branch + worktree layout

```
karrio/ (main working copy on feat/2026.5)
├── .claude/worktrees/
│   ├── 2026.5-claude-tooling       ← sub-PR 1 agent (branches off feat/2026.5)
│   ├── 2026.5-ruff-precommit       ← sub-PR 2 agent (branches off feat/2026.5)
│   ├── 2026.5-modules-server       ← sub-PR 4 agent (branches off feat/2026.5)
│   ├── 2026.5-helm-chart           ← sub-PR 5 agent (branches off feat/2026.5)
│   ├── 2026.5-huey-http            ← sub-PR 6 agent (branches off feat/2026.5)
│   └── 2026.5-e2e-smoke            ← sub-PR 7 agent (branches off feat/2026.5)

Sub-PRs 3a / 3b run OUTSIDE feat/2026.5 (they target karrioapi/karrio main and
karrioapi/karrio-insiders main). The sync agent works in:
├── /Users/danielkobina/Workspace/jtl/shipping-platform   (to export patches)
├── /Users/danielkobina/Workspace/karrio/karrio           (to apply → 3a branch)
└── /Users/danielkobina/Workspace/karrio/karrio/ee/insiders (to apply → 3b branch)
```

Sub-PRs 1, 2, 4, 5, 6, 7 branch off the tip of `feat/2026.5` at agent spawn time, push to `origin`, and open a draft PR back into `feat/2026.5`. Sub-PRs 3a/3b open sync PRs into `karrioapi/karrio` main and `karrioapi/karrio-insiders` main respectively; `feat/2026.5` rebases after they merge. The human operator (Daniel) is the sole merger.

### Agent brief template

Every agent receives a self-contained prompt with:

- Working directory (the worktree path)
- Target branch (e.g., `chore/2026.5-claude-tooling`)
- The subset of this PRD that scopes its work (linked sections)
- An explicit "DO NOT" list (no proprietary JTL code, no pytest, no main-repo force-push, no submodule bumps except in sub-PR 8)
- Required outputs: branch pushed, PR opened against `feat/2026.5`, brief written summary in the PR body pointing at this PRD

### Parallelism

- **Phase 1 (parallel)**: sub-PRs 1, 2, 3a, 3b, 5, 7 can all run in parallel — they touch disjoint parts of the tree. 3a/3b target upstream main, not `feat/2026.5`.
- **Phase 2 (serial)**: sub-PR 4 (modules/server) rebases onto main AFTER 3a has merged (to pick up any files that moved), then lands before 6 (huey-http) because the new broker lives in the consolidated package.
- **Phase 3 (manual)**: sub-PR 8 (release) is a human PR after all others merge.

### Kill-switch

If any agent reports a confusion or scope creep, it MUST stop and ask rather than widen the diff. Agents that push JTL-proprietary code or modify files outside their worktree scope fail the PR and are abandoned; the sub-PR is reassigned to a human or re-prompted agent.

---

## Appendices

### A. Files touched (summary count)

| Area                       | Files added | Files modified | Files removed |
| -------------------------- | ----------- | -------------- | ------------- |
| `.claude/`                 | ~8          | ~4             | 0             |
| Lint config                | 2           | 2              | 0             |
| Server consolidation       | 2           | ~30            | ~5            |
| Helm chart                 | ~8          | ~6             | 0             |
| Huey HTTP                  | ~5          | ~4             | 0             |
| E2E                        | ~15         | 2              | 0             |
| Release                    | 0           | ~4             | 0             |

### B. Reference — JTL `.claude/` artifacts studied

- `/Users/danielkobina/Workspace/jtl/shipping-platform/ruff.toml`
- `/Users/danielkobina/Workspace/jtl/shipping-platform/.claude/skills/{create-prd,create-extension-module,django-graphql,django-rest-api,run-tests,review-implementation}/`
- `/Users/danielkobina/Workspace/jtl/shipping-platform/.claude/rules/{code-style,extension-patterns,testing,commit-conventions}.md`
- `/Users/danielkobina/Workspace/jtl/shipping-platform/karrio/modules/graph/karrio/server/graph/schema.py`
- `/Users/danielkobina/Workspace/jtl/shipping-platform/karrio/modules/admin/karrio/server/admin/schema.py`

### C. Reference — issue / PRD cross-links

- Module consolidation vision: [jtlshipping/shipping-platform#431](https://github.com/jtlshipping/shipping-platform/issues/431)
- **Governing sync workflow** (sub-PRs 3a/3b): [`SUBTREE_SYNC_WORKFLOW.md`](./SUBTREE_SYNC_WORKFLOW.md)
- Related CI safety: commit `820101b6f ci(core): add rolling-deploy schema safety system check`
