# Migrate Karrio to `uv` for End-to-End Python Toolchain

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-03-03 |
| Status | Planning |
| Owner | Core Team |
| Type | Refactoring / Architecture |
| Reference | [AGENTS.md](../AGENTS.md) |

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Problem Statement](#problem-statement)
3. [Goals & Success Criteria](#goals--success-criteria)
4. [Alternatives Considered](#alternatives-considered)
5. [Technical Design](#technical-design)
6. [Edge Cases & Failure Modes](#edge-cases--failure-modes)
7. [Implementation Plan](#implementation-plan)
8. [Testing Strategy](#testing-strategy)
9. [Risk Assessment](#risk-assessment)
10. [Migration & Rollback](#migration--rollback)
11. [Appendices](#appendices)

---

## Executive Summary

Karrio's Python toolchain currently uses a patchwork of `pip`, `venv`, `setuptools`, and custom shell scripts (`bin/`) to manage environments, install packages, run tests, and publish releases. This PRD proposes migrating the entire Python development, build, CI/CD, and release pipeline to [`uv`](https://github.com/astral-sh/uv) — a single, Rust-powered tool that replaces `pip`, `pip-tools`, `venv`, `virtualenv`, `pyenv`, and portions of `tox`/`nox`.

The goal is a dramatically faster, more reproducible, and simpler developer experience — from `git clone` to first test run in under 60 seconds.

### Key Architecture Decisions

1. **`uv` as the single Python toolchain entrypoint**: replaces `python -m venv`, `pip install`, `pip-compile`, and `twine` for local dev, CI, and release
2. **Workspace-aware monorepo layout**: adopt `uv` workspaces to manage all `modules/`, `apps/`, and `modules/connectors/` packages as a unified dependency graph
3. **Lockfile-first reproducibility**: `uv.lock` replaces ad-hoc `requirements*.txt` files as the single source of truth for reproducible environments
4. **Incremental migration**: `bin/` scripts updated in place; `requirements*.txt` retained as generated artifacts during transition to avoid breaking external consumers
5. **CI unchanged structurally**: GitHub Actions workflows keep the same job names/structure but swap `pip` commands for `uv` equivalents

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| All `bin/` dev/setup/test/build scripts | Node.js / pnpm / dashboard toolchain |
| `requirements*.txt` → `pyproject.toml` + `uv.lock` | Rust/cargo builds |
| `python-packages` CI job (PyPI publish) | Docker base image changes |
| `server-build`, `sdk-tests`, `platform-ci` CI jobs | Database migrations |
| Local dev setup (`bin/setup-server-env`, `bin/create-new-env`) | Community plugins (initially) |
| Python version pinning (`.python-version`) | Windows-specific `bin/*.bat` scripts (follow-up) |
| `bin/build-and-release-packages` | CDN / npm releases |

---

## Problem Statement

### Current State

Karrio's Python toolchain is fragmented across many files and tools:

```
requirements.dev.txt
requirements.sdk.dev.txt
requirements.server.dev.txt
requirements.insiders.dev.txt
requirements.platform.dev.txt
requirements.build.txt
requirements.build.insiders.txt
requirements.build.platform.txt
requirements.txt
requirements.insiders.txt
requirements.platform.txt
```

Setup is driven by `bin/setup-server-env`, which chains:

```bash
# Current flow — takes 3–8 minutes on a cold machine
python3 -m venv .venv/karrio
source .venv/karrio/bin/activate
python -m pip install pip --upgrade
pip install -r requirements.dev.txt       # base deps
pip install -r requirements.server.dev.txt  # server deps (includes -r sdk.dev)
pip install -e ./modules/sdk              # editable installs (×60+ packages)
pip install -e ./modules/core
pip install -e ./apps/api
# ... repeated for every connector
```

CI (`.github/workflows/build.yml`) mirrors this exactly:

```yaml
- name: Install build dependencies
  run: |
    python -m pip install --upgrade pip
    pip install build twine
```

Release uses `twine upload` per package with no lock file verification.

### Desired State

```bash
# New flow — takes 10–30 seconds on cold machine, <5s cached
uv sync                          # creates venv + installs everything from uv.lock
uv run python -m unittest ...    # runs tests in managed env
uv build                         # builds all wheels
uv publish                       # publishes to PyPI
```

CI becomes:

```yaml
- uses: astral-sh/setup-uv@v5
- run: uv sync --frozen           # deterministic, lock-checked install
- run: uv run ./bin/run-server-tests
```

### Problems

1. **Slow onboarding**: A fresh `bin/setup-server-env` on a cold machine takes 3–8 minutes due to sequential `pip install` calls with no parallelism and no caching
2. **Non-reproducible environments**: `requirements*.txt` files use unpinned ranges; two developers running setup on the same day can get different transitive dependency versions
3. **11 requirements files**: Split by environment variant (dev/build/insiders/platform) and scope (sdk/server) — hard to reason about, easy to drift
4. **No lockfile**: There is no `pip freeze`-style lockfile committed to the repo, making CI results dependent on PyPI state at the moment of execution
5. **Slow CI**: Each CI job reinstalls all dependencies from scratch; pip's HTTP caching is unreliable across runners
6. **Complex `bin/` scripts**: `bin/create-new-env`, `bin/setup-server-env`, `bin/setup-sdk-env`, `bin/setup-ee-env` all reinvent venv creation + pip install in slightly different ways
7. **Release is manual and fragile**: `bin/build-and-release-packages` iterates over packages and calls `twine upload` individually; no integrity check, no lock verification

---

## Goals & Success Criteria

### Goals

1. **Speed**: Cold-start dev setup from zero to first test run in < 60 seconds on a modern machine
2. **Reproducibility**: Identical environments across all developer machines and CI runners via committed `uv.lock`
3. **Simplicity**: Reduce the number of requirements files from 11 to a structured set of `pyproject.toml` dependency groups
4. **DX**: Single command to set up, single command to run tests, single command to release — no activation rituals
5. **CI efficiency**: Leverage `uv`'s built-in cache + `--frozen` mode to make CI installs consistently fast and deterministic

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| Cold setup time (no cache) | < 60s | Must-have |
| Warm setup time (cache hit) | < 5s | Must-have |
| CI install time per job | < 30s (from cache) | Must-have |
| Requirements file count | ≤ 3 `pyproject.toml` groups | Must-have |
| `uv.lock` committed and CI-enforced | Yes | Must-have |
| `bin/setup-server-env` still works (calls `uv` internally) | Yes | Must-have |
| PyPI publish uses `uv publish` | Yes | Nice-to-have |
| `.python-version` file committed | Yes | Nice-to-have |

### Launch Criteria

**Must-have (P0):**
- [ ] `uv sync` fully sets up the dev environment from a clean clone
- [ ] All existing tests pass after migration (`sdk-tests`, `server-tests`, `platform-ci`)
- [ ] CI jobs use `uv sync --frozen` with lock verification
- [ ] `uv.lock` committed to repo and validated in CI
- [ ] `bin/setup-server-env` updated to call `uv` internally (backward-compatible interface)

**Nice-to-have (P1):**
- [ ] `uv publish` replaces `twine` in `bin/build-and-release-packages`
- [ ] `.python-version` file pinning Python 3.12 committed
- [ ] Community plugins (`community/plugins/`) migrated to uv workspace
- [ ] `uv run` wrappers for all `bin/` entry points (no manual activation needed)

---

## Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **`uv` (selected)** | 10–100× faster than pip; built-in venv; lock files; workspace support; drop-in pip replacement; actively maintained by Astral | Rust binary dependency; newer tool (lower community familiarity) | **Selected** |
| **`poetry`** | Mature; well-known; lock files | Much slower than uv; poor monorepo/workspace support; `poetry.lock` not compatible with pip; complex plugin system | Rejected |
| **`pdm`** | PEP 517/518 compliant; lock files; workspace support | Slower than uv; smaller community; less tooling integration | Rejected |
| **`pip-tools` (pip-compile)** | Incremental improvement; familiar | Still slow; no venv management; requires separate venv tool; adds `pip-compile` step | Rejected |
| **`conda`** | Good for scientific Python | Heavy; not aligned with karrio's Python-focused stack; slow | Rejected |
| **Status quo** | No migration effort | Slow, non-reproducible, complex scripts; tech debt compounds | Rejected |

### Trade-off Analysis

`uv` wins on every axis that matters for a developer tools project:
- **Performance**: pip's resolver is single-threaded; uv's is parallel and written in Rust — typically 10–100× faster on cold installs
- **Reproducibility**: `uv.lock` is a cross-platform, content-addressed lockfile; pip has no equivalent
- **Monorepo support**: `uv` workspaces allow declaring all `modules/` and `apps/` as workspace members, giving a unified dependency graph with deduplication
- **Compatibility**: `uv` is a drop-in pip replacement — `uv pip install` works everywhere `pip install` does; migration risk is low

---

## Technical Design

### Existing Code Analysis

| Component | Location | Migration Strategy |
|-----------|----------|-------------------|
| `venv` creation | `bin/create-new-env` | Replace with `uv venv` or remove (uv handles automatically) |
| `pip install -r *.txt` | `bin/setup-server-env`, `bin/setup-sdk-env` | Replace with `uv sync [--group <group>]` |
| `pip install -e ./module` | all setup scripts | Becomes workspace member declarations in root `pyproject.toml` |
| `pip install build twine` | `.github/workflows/build.yml` | `uv build` + `uv publish` |
| `python -m unittest` invocations | `bin/run-server-tests`, `bin/run-sdk-tests` | `uv run python -m unittest ...` |
| `modules/sdk/pyproject.toml` | `modules/sdk/` | Add `[tool.uv]` section; becomes workspace member |
| Python version | not pinned | Add `.python-version` (3.12) |

### Architecture Overview

```
karrio/ (uv workspace root)
├── pyproject.toml            ← workspace root; dependency groups replace requirements*.txt
├── uv.lock                   ← single committed lockfile for entire monorepo
├── .python-version           ← pins Python 3.12
│
├── modules/
│   ├── sdk/pyproject.toml    ← workspace member (already exists)
│   ├── core/pyproject.toml   ← workspace member (add)
│   ├── soap/pyproject.toml   ← workspace member (add)
│   ├── graph/pyproject.toml  ← workspace member (add)
│   ├── data/pyproject.toml   ← workspace member (add)
│   ├── events/pyproject.toml ← workspace member (add)
│   ├── manager/pyproject.toml
│   ├── orders/pyproject.toml
│   ├── proxy/pyproject.toml
│   ├── pricing/pyproject.toml
│   ├── documents/pyproject.toml
│   ├── admin/pyproject.toml
│   └── connectors/
│       └── */pyproject.toml  ← workspace members (add for each)
│
├── apps/
│   └── api/pyproject.toml    ← workspace member (add)
│
└── community/                ← Phase 3: workspace members
    └── plugins/*/pyproject.toml
```

### Dependency Groups (replacing 11 requirements files)

The root `pyproject.toml` declares dependency groups using PEP 735 / uv's `[dependency-groups]`:

```toml
[tool.uv.workspace]
members = [
    "modules/sdk",
    "modules/soap",
    "modules/core",
    "modules/graph",
    "modules/data",
    "modules/events",
    "modules/manager",
    "modules/orders",
    "modules/proxy",
    "modules/pricing",
    "modules/documents",
    "modules/admin",
    "apps/api",
    "modules/connectors/*",
]

[dependency-groups]
# Replaces: requirements.dev.txt
dev = [
    "bandit",
    "black",
    "coverage",
    "mypy",
    "lxml-stubs",
    "twine",   # removed in Phase 2 when uv publish is adopted
    "wheel",
    "setuptools",
]

# Replaces: requirements.server.dev.txt + requirements.sdk.dev.txt
server = [
    "django-debug-toolbar",
    "djangorestframework-stubs",
    { include-group = "dev" },
]

# Replaces: requirements.insiders.dev.txt
insiders = [
    { include-group = "server" },
    # insiders-specific deps
]

# Replaces: requirements.platform.dev.txt
platform = [
    { include-group = "server" },
    # platform-specific deps
]

# Replaces: requirements.build.txt (CI build/release)
build = [
    "build",
    "twine",
]
```

### Updated `bin/` Scripts

**`bin/create-new-env` (simplified to ~5 lines):**

```bash
#!/usr/bin/env bash
source "bin/_env" "$@"
log_section "Creating Python Virtual Environment"
uv venv "${ROOT}/$ENV_DIR/$BASE_DIR" --python 3.12
log_success "Virtual environment created"
```

**`bin/setup-server-env` (core change):**

```bash
# Before
python3 -m venv .venv/karrio
source .venv/karrio/bin/activate
python -m pip install pip --upgrade
pip install -r requirements.server.dev.txt

# After
uv sync --group server          # creates venv, installs everything, uses uv.lock
```

**`bin/run-server-tests` (no activation needed):**

```bash
# Before
source .venv/karrio/bin/activate
python -m unittest discover ...

# After
uv run python -m unittest discover ...
```

**`bin/run-sdk-tests`:**

```bash
# Before
source .venv/karrio/bin/activate
python -m unittest discover -s modules/connectors -p "test_*.py" -v

# After
uv run python -m unittest discover -s modules/connectors -p "test_*.py" -v
```

### CI Changes (`.github/workflows/build.yml`)

**Python package build/publish job:**

```yaml
# Before
- uses: actions/setup-python@v4
  with:
    python-version: "3.12"
- name: Install build dependencies
  run: |
    python -m pip install --upgrade pip
    pip install build twine

# After
- uses: astral-sh/setup-uv@v5
  with:
    enable-cache: true
    cache-dependency-glob: "uv.lock"
- name: Install dependencies
  run: uv sync --frozen --group build
```

**SDK tests job:**

```yaml
# Before
- run: pip install -r requirements.sdk.dev.txt

# After
- run: uv sync --frozen --group dev
```

**Server tests job:**

```yaml
# Before
- run: |
    python -m pip install pip --upgrade
    pip install -r requirements.server.dev.txt

# After
- run: uv sync --frozen --group server
```

### Sequence Diagram: Developer Setup Flow

```
┌────────────┐    ┌────────────┐    ┌──────────────┐    ┌─────────┐
│  Developer │    │  bin/setup │    │      uv      │    │  PyPI   │
└─────┬──────┘    └─────┬──────┘    └──────┬───────┘    └────┬────┘
      │                 │                  │                  │
      │  ./bin/setup-   │                  │                  │
      │  server-env     │                  │                  │
      │────────────────>│                  │                  │
      │                 │  uv sync         │                  │
      │                 │  --group server  │                  │
      │                 │─────────────────>│                  │
      │                 │                  │  resolve uv.lock │
      │                 │                  │  (no network if  │
      │                 │                  │   cache hit)     │
      │                 │                  │─────────────────>│
      │                 │                  │  fetch missing   │
      │                 │                  │<─────────────────│
      │                 │                  │  install (×fast) │
      │                 │<─────────────────│                  │
      │  Ready (< 60s)  │                  │                  │
      │<────────────────│                  │                  │
      │                 │                  │                  │
```

### Sequence Diagram: CI Pipeline

```
┌────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌───────┐
│  Push  │   │ setup-uv │   │ uv sync  │   │  Tests   │   │ PyPI  │
└───┬────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘   └───┬───┘
    │             │              │               │              │
    │  trigger    │              │               │              │
    │────────────>│              │               │              │
    │             │  install     │               │              │
    │             │  (once, cached)              │              │
    │             │─────────────>│               │              │
    │             │              │  --frozen      │              │
    │             │              │  (fail if lock │              │
    │             │              │   mismatch)   │              │
    │             │              │──────────────>│              │
    │             │              │               │  run tests   │
    │             │              │               │─────────────>│
    │             │              │               │              │
    │             │              │               │  uv publish  │
    │             │              │               │─────────────>│
    │             │              │               │              │
```

### Data Flow: requirements*.txt → uv.lock

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         BEFORE (current)                                  │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  requirements.dev.txt         ──┐                                         │
│  requirements.sdk.dev.txt     ──┤──> pip install (sequential, slow)       │
│  requirements.server.dev.txt  ──┤    → non-deterministic venv             │
│  requirements.build.txt       ──┘                                         │
│  requirements.insiders.dev.txt                                            │
│  requirements.platform.dev.txt                                            │
│  requirements.build.insiders.txt                                          │
│  requirements.build.platform.txt                                          │
│  requirements.txt                                                         │
│  requirements.insiders.txt                                                │
│  requirements.platform.txt                                                │
│                                                                           │
├──────────────────────────────────────────────────────────────────────────┤
│                         AFTER (uv)                                        │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  pyproject.toml (root)        ──┐                                         │
│    [dependency-groups]          │                                         │
│      dev / server / build       ├──> uv sync (parallel, Rust, cached)     │
│  modules/*/pyproject.toml     ──┤    → deterministic venv from uv.lock    │
│  apps/*/pyproject.toml        ──┘                                         │
│                                                                           │
│  uv.lock  ←─── single committed lockfile ───────────────────────────>    │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Edge Cases & Failure Modes

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| Developer has no `uv` installed | Setup fails immediately with clear error | `bin/_env` checks for `uv` binary, prints install instructions (`curl -LsSf https://astral.sh/uv/install.sh \| sh`) |
| `uv.lock` is out of sync with `pyproject.toml` | CI fails with explicit lock mismatch error | `uv sync --frozen` is non-interactive; exits non-zero and prints diff |
| Workspace member missing `pyproject.toml` | `uv sync` fails with clear error | Add `pyproject.toml` to every `modules/` package as part of Phase 1 |
| New connector added without workspace entry | Connector deps not resolved | CI lint step: `uv workspace list` diff against `ls modules/connectors/` |
| Insiders/platform edition on OSS clone | Extras groups just don't install | Group isolation — `uv sync --group server` only, no error |
| Windows developer | Windows paths work; `uv` supports Windows | `.bat` scripts remain as-is for now; `uv` binary is cross-platform |
| `pip install` used directly by a script | Works if venv is active; or call `uv pip install` | Audit all `bin/` scripts in Phase 1; replace all direct pip calls |
| Existing `.venv/karrio/` directory | `uv venv` recreates or reuses; deterministic | Document to `rm -rf .venv/` on first migration |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| `uv` breaks a dep resolution that pip accepted | All tests fail | Run full test matrix before merging; pin `uv` version in CI via `setup-uv@v5` |
| `uv.lock` conflicts in PRs with many dep changes | Merge conflicts in lockfile | `uv.lock` has structured format designed for merge resolution; document update procedure |
| PyPI publish fails with `uv publish` | Release blocked | Keep `twine` as fallback in Phase 2; validate in staging PyPI first |
| Editable installs behave differently | Import errors in tests | Test editable installs explicitly; `uv` supports PEP 660 editable installs |
| Community plugins not in workspace yet | Plugin tests fail on uv setup | Phase 3 explicitly covers community; Phase 1/2 maintain `pip install -e` fallback for community |

### Security Considerations

- [ ] `uv.lock` must be committed — prevents supply-chain attacks via transitive dep drift
- [ ] `uv publish` uses `UV_PUBLISH_TOKEN` env var (same as `TWINE_PASSWORD`); no secrets in code
- [ ] Pin `astral-sh/setup-uv@v5` (not `@latest`) in CI to avoid action hijacking
- [ ] Hash verification: `uv.lock` includes SHA256 hashes for all packages — equivalent to `pip install --require-hashes`

---

## Implementation Plan

### Phase 1: Foundation — Workspace + Core Dev Setup (Week 1–2)

| Task | Files | Effort |
|------|-------|--------|
| Add `uv` binary check to `bin/_env` with install hint | `bin/_env` | S |
| Add root `pyproject.toml` with `[tool.uv.workspace]` and `[dependency-groups]` | `pyproject.toml` (new) | M |
| Add `.python-version` pinning 3.12 | `.python-version` (new) | S |
| Add `pyproject.toml` to each `modules/` package that lacks one (port from `setup.cfg`/`setup.py`) | `modules/core/`, `modules/graph/`, `modules/data/`, `modules/events/`, `modules/manager/`, `modules/orders/`, `modules/proxy/`, `modules/pricing/`, `modules/documents/`, `modules/admin/`, `modules/soap/` | L |
| Add `pyproject.toml` to `apps/api/` | `apps/api/pyproject.toml` | M |
| Run `uv sync` and generate initial `uv.lock` | `uv.lock` | M |
| Update `bin/create-new-env` to use `uv venv` | `bin/create-new-env` | S |
| Update `bin/setup-server-env` to use `uv sync --group server` | `bin/setup-server-env` | S |
| Update `bin/setup-sdk-env` to use `uv sync --group dev` | `bin/setup-sdk-env` | S |
| Update `bin/activate-env` to point to uv-managed venv | `bin/activate-env` | S |
| Validate all existing tests pass (`sdk-tests`, `server-tests`) | — | M |

### Phase 2: CI/CD + Release (Week 3)

| Task | Files | Effort |
|------|-------|--------|
| Update `python-packages` CI job to use `setup-uv`, `uv build`, `uv publish` | `.github/workflows/build.yml` | M |
| Update `sdk-tests` CI job to use `uv sync --frozen` | `.github/workflows/build.yml` | S |
| Update `server-build`/`platform-ci`/`server-tests` CI jobs | `.github/workflows/build.yml` | M |
| Add CI step to validate `uv.lock` is up-to-date (fail on drift) | `.github/workflows/build.yml` | S |
| Update `bin/build-and-release-packages` to use `uv build` + `uv publish` | `bin/build-and-release-packages` | M |
| Pin `uv` version in CI (`setup-uv@v5 with: version: "0.6.x"`) | `.github/workflows/build.yml` | S |
| Update `bin/run-server-tests` and `bin/run-sdk-tests` to use `uv run` | `bin/run-server-tests`, `bin/run-sdk-tests` | S |
| Update CONTRIBUTING.md / README setup instructions | `CONTRIBUTING.md`, `README.md` | S |

### Phase 3: Community Plugins + Cleanup (Week 4)

| Task | Files | Effort |
|------|-------|--------|
| Add community plugins as optional workspace members | `community/plugins/*/pyproject.toml` | L |
| Deprecate / archive all 11 `requirements*.txt` files (keep as generated stubs with warning comment) | `requirements*.txt` | S |
| Audit and remove any remaining direct `pip` calls in `bin/` | `bin/*` | M |
| Add developer docs: "How to add a new connector with uv" | `docs/development/` | M |
| Update `bin/sdk` script | `bin/sdk` | S |

**Dependencies:** Phase 2 depends on Phase 1 completion. Phase 3 is independent and can overlap with Phase 2.

---

## Testing Strategy

> All tests use `unittest` (NOT pytest) per AGENTS.md. No new test framework is introduced.

### Validation Gates

Each phase has a mandatory validation gate before merging:

**Phase 1 gate:**

```bash
# Fresh clone test — must complete in < 60s
time (curl -LsSf https://astral.sh/uv/install.sh | sh && uv sync --group server)

# All existing tests must pass
uv run python -m unittest discover -s modules/connectors -p "test_*.py" -v
ENABLE_ALL_PLUGINS_BY_DEFAULT=true uv run ./bin/run-server-tests -v
```

**Phase 2 gate:**

```bash
# Lock file is deterministic across platforms
uv lock --check   # fails if uv.lock is out of date

# CI dry-run build
uv build --out-dir .venv/dist/ modules/sdk/
uv publish --dry-run --index testpypi
```

### Test Categories

| Category | Scope | Runner |
|----------|-------|--------|
| Connector unit tests | `modules/connectors/*/tests/` | `uv run python -m unittest discover` |
| SDK unit tests | `modules/sdk/karrio/core/tests/` | `uv run python -m unittest discover` |
| Server integration tests | `karrio.server.*` | `uv run ./bin/run-server-tests` |
| Platform tests | platform modules | `uv run ./bin/run-server-tests --platform` |

### Regression Test (pre-merge)

The following must produce identical output before and after migration:

```bash
# Generate reference output on pip-based setup
./bin/setup-server-env
ENABLE_ALL_PLUGINS_BY_DEFAULT=true ./bin/run-server-tests -v 2>&1 | grep -E "^(ok|FAIL|ERROR|Ran)" > /tmp/pip_results.txt

# Generate output on uv-based setup
rm -rf .venv/
uv sync --group server
ENABLE_ALL_PLUGINS_BY_DEFAULT=true uv run ./bin/run-server-tests -v 2>&1 | grep -E "^(ok|FAIL|ERROR|Ran)" > /tmp/uv_results.txt

# Must be identical
diff /tmp/pip_results.txt /tmp/uv_results.txt
```

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| `uv` editable install incompatibility with a package | High — tests fail | Low — uv supports PEP 660 | Test all editable installs in Phase 1 before CI changes |
| `uv.lock` merge conflicts become frequent | Medium — developer friction | Medium — monorepo has many dep changes | Document `uv lock` update procedure; add to CONTRIBUTING.md |
| `uv publish` authentication differences | Medium — release blocked | Low — uses same token env var | Test against TestPyPI in Phase 2 staging |
| `setup.py`-only packages can't be workspace members | High — package excluded | Medium — older packages may lack `pyproject.toml` | Audit all packages in Phase 1; add `pyproject.toml` stubs |
| Contributors unfamiliar with `uv` | Low — onboarding friction | Medium | Update docs + CONTRIBUTING.md; `uv` is a drop-in, learning curve is minimal |
| Windows developers broken | Medium — dev environment unusable | Low | `uv` is cross-platform; `.bat` scripts preserved in Phase 1 |
| Breaking change in `uv` between phases | Medium | Low | Pin exact `uv` version in CI; test on pin before upgrade |

---

## Migration & Rollback

### Backward Compatibility

- **`bin/` script interface unchanged**: `./bin/setup-server-env` still works; internal implementation swaps `pip` for `uv`
- **`requirements*.txt` retained as generated stubs** during transition (with deprecation comment header) for any external consumers
- **`ENABLE_ALL_PLUGINS_BY_DEFAULT` env var**: preserved as-is; passed through to `uv run` invocations

### Developer Migration Steps (one-time)

```bash
# 1. Install uv (one-time, ~10s)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Remove old venv
rm -rf .venv/

# 3. Sync from lockfile
uv sync --group server

# 4. Done — no activation needed for uv run commands
uv run python -m unittest discover ...
```

### Rollback Procedure

If a critical issue is found post-merge:

1. **Identify issue**: test suite failure or import error in CI
2. **Immediate**: Revert the `bin/` script changes (5-minute rollback via `git revert`)
3. **Restore pip path**: `python3 -m venv .venv/karrio && pip install -r requirements.server.dev.txt`
4. **CI**: Revert workflow YAML changes; `requirements*.txt` files are still present
5. **Verify**: Run full test suite on reverted branch before re-merging

---

## Appendices

### Appendix A: uv Performance Benchmarks

Published benchmarks (astral.sh, Jan 2025) for a typical Django project:

| Tool | Cold install | Warm install (cached) |
|------|--------------|-----------------------|
| pip | 60–180s | 15–30s |
| poetry | 45–120s | 10–20s |
| **uv** | **5–15s** | **< 1s** |

Karrio has ~60+ editable packages plus their transitive deps — the parallel resolver provides the largest benefit at this scale.

### Appendix B: uv Workspace Reference

```toml
# Root pyproject.toml

[tool.uv.workspace]
# Glob patterns supported
members = [
    "modules/sdk",
    "modules/soap",
    "modules/core",
    "modules/graph",
    "modules/data",
    "modules/events",
    "modules/manager",
    "modules/orders",
    "modules/proxy",
    "modules/pricing",
    "modules/documents",
    "modules/admin",
    "apps/api",
    "modules/connectors/australiapost",
    # ... all connectors
]

# Exclude community until Phase 3
exclude = ["community/*"]
```

### Appendix C: Key `uv` Commands Reference

| Old Command | New Command | Notes |
|-------------|-------------|-------|
| `python3 -m venv .venv/karrio` | `uv venv .venv/karrio` | 10× faster |
| `pip install -r requirements.server.dev.txt` | `uv sync --group server` | uses lock |
| `pip install -e ./modules/sdk` | automatic via workspace | declared in `pyproject.toml` |
| `pip install build twine && python -m build` | `uv build` | built-in |
| `twine upload dist/*` | `uv publish` | uses `UV_PUBLISH_TOKEN` |
| `python -m unittest discover` | `uv run python -m unittest discover` | no activation needed |
| `source .venv/karrio/bin/activate` | not required (use `uv run`) | or still works if preferred |
| `pip freeze > requirements.txt` | `uv lock` | cross-platform lockfile |

### Appendix D: References

- [uv documentation](https://docs.astral.sh/uv/)
- [uv workspaces](https://docs.astral.sh/uv/concepts/workspaces/)
- [uv GitHub Actions](https://github.com/astral-sh/setup-uv)
- [PEP 735 — Dependency Groups](https://peps.python.org/pep-0735/)
- [PEP 660 — Editable Installs](https://peps.python.org/pep-0660/)
- [astral-sh/setup-uv](https://github.com/astral-sh/setup-uv)
