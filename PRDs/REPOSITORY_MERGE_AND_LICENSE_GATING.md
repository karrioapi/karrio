# Repository Merge & Enterprise License Gating

<!-- ARCHITECTURE: System design PRD for merging karrio-insiders into the main repo -->

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-01-30 |
| Status | Planning |
| Owner | Daniel Kobina |
| Type | Architecture |
| Reference | [AGENTS.md](../AGENTS.md) |

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Open Questions & Decisions](#open-questions--decisions)
3. [Problem Statement](#problem-statement)
4. [Goals & Success Criteria](#goals--success-criteria)
5. [Alternatives Considered](#alternatives-considered)
6. [Industry Research](#industry-research)
7. [Technical Design](#technical-design)
8. [Edge Cases & Failure Modes](#edge-cases--failure-modes)
9. [Implementation Plan](#implementation-plan)
10. [Testing Strategy](#testing-strategy)
11. [Risk Assessment](#risk-assessment)
12. [Migration & Rollback](#migration--rollback)
13. [Appendices](#appendices)

---

## Executive Summary

This PRD proposes merging the private `karrio-insiders` and `karrio-platform` repositories into the main `karrio` repository under the `ee/` directory, replacing the current git submodule approach. Enterprise features will be gated behind a cryptographically signed license key validated at runtime, following the industry-standard pattern used by GitLab, Cal.com, PostHog, Metabase, and n8n. The open-source code retains its LGPL-3.0 license while enterprise code is governed by a new Karrio Commercial License.

### Key Architecture Decisions

1. **Single repository with `ee/` directory**: All enterprise code moves into `ee/` within the main repo, eliminating git submodules. Old repos archived.
2. **Dual licensing**: LGPL-3.0 for open-source code, Karrio Commercial License for `ee/` directory contents.
3. **Hybrid license validation**: RSA-2048 signed license keys (offline-capable) with optional online validation/renewal against a Karrio license server.
4. **Runtime-only enforcement**: Enterprise code always ships in builds. License checked at runtime; unlicensed features return 403 or are hidden in the UI.
5. **CLI-first key issuance**: `karrio license` CLI commands for generating and managing signed license keys. License server planned for later phase.

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| Merge insiders + platform repos into `ee/` | License management web dashboard (Phase 2) |
| Karrio Commercial License creation | New enterprise feature development |
| RSA-signed license key infrastructure | Billing/payment integration |
| Runtime feature gating (backend + frontend) | Per-connector licensing (future) |
| `karrio license` CLI tool | Usage metering/analytics |
| Docker image builds with EE code included | FOSS mirror repository |
| Archive old private repositories | Changes to existing OSS features |

---

## Open Questions & Decisions

### Resolved Decisions

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| D1 | Enterprise code license | Karrio Commercial License (custom proprietary) | Aligns with Cal.com, PostHog, n8n precedent. Allows dev/testing without license, requires paid license for production. Maximum control over terms. | 2026-01-30 |
| D2 | Open-source code license | Keep LGPL-3.0 | Maintains current community contract. Copyleft on Karrio itself but allows proprietary applications built on top. | 2026-01-30 |
| D3 | License validation approach | Hybrid (online + offline) | Offline RSA-signed keys as primary (air-gap support). Optional online validation for renewal/revocation. Falls back to offline if server unreachable. | 2026-01-30 |
| D4 | Repository strategy | Archive old repos, single repo | Eliminates submodule complexity. Single source of truth. Simplest development workflow. | 2026-01-30 |
| D5 | Code organization | Top-level `ee/` directory | Maintains current structure. Clear visual separation between OSS and EE code. Industry standard (GitLab, Cal.com, PostHog). | 2026-01-30 |
| D6 | Gated features | All current insiders features | Admin, Organizations, Audit, Automation, Apps, Cloud settings, Multi-tenancy. | 2026-01-30 |
| D7 | Enforcement model | Runtime-only | Industry consensus across all researched projects. Code always builds; license checked per-request. Simplest CI/CD. | 2026-01-30 |
| D8 | Key issuance method | CLI tool first, server later | `karrio license generate` CLI for initial launch. License management server deferred to Phase 2. Fastest path to production. | 2026-01-30 |

### Pending Questions

| # | Question | Context | Options | Status |
|---|----------|---------|---------|--------|
| Q1 | Plan tier names and feature mapping | Need to decide exact plan tiers (e.g., Professional/Enterprise or Growth/Scale/Enterprise) | Define during implementation | ⏳ Pending |
| Q2 | License expiry grace period | How long should the system continue working after license expires? | 7 days / 14 days / 30 days | ⏳ Pending |
| Q3 | Seat counting mechanism | How are seats counted? Active users? All users? Per-org? | Define during implementation | ⏳ Pending |

---

## Problem Statement

### Current State

Karrio uses **git submodules** to separate enterprise code into private repositories:

```
karrio/                          # Public repo (github.com/karrioapi/karrio)
├── ee/
│   ├── insiders/                # SUBMODULE → github.com/karrioapi/karrio-insiders (private)
│   │   ├── modules/
│   │   │   ├── admin/
│   │   │   ├── apps/
│   │   │   ├── audit/
│   │   │   ├── automation/
│   │   │   ├── cloud/
│   │   │   └── orgs/
│   │   └── architecture/        # PRDs and design docs
│   ├── platform/                # SUBMODULE → github.com/karrioapi/karrio-platform (private)
│   │   ├── modules/
│   │   │   └── tenants/         # Multi-tenancy
│   │   └── infra/               # Pulumi infrastructure
│   ├── apps/
│   │   └── platform/            # Next.js platform app
│   └── packages/
│       └── console/             # Console UI package
└── .gitmodules                  # Submodule configuration
```

```ini
# .gitmodules (current)
[submodule "insiders"]
    path = ee/insiders
    url = git@github.com:karrioapi/karrio-insiders.git

[submodule "platform"]
    path = ee/platform
    url = git@github.com:karrioapi/karrio-platform.git
```

**No license validation exists.** Enterprise features are gated solely by repository access control (private GitHub repos + private Docker registry).

### Desired State

All code in a single repository with enterprise features gated by cryptographically signed license keys:

```
karrio/                          # Single repo (everything visible)
├── ee/
│   ├── LICENSE                  # Karrio Commercial License
│   ├── modules/
│   │   ├── admin/               # System administration
│   │   ├── apps/                # App marketplace
│   │   ├── audit/               # Audit logging
│   │   ├── automation/          # Workflow automation
│   │   ├── cloud/               # Cloud settings
│   │   ├── orgs/                # Organizations & teams
│   │   ├── tenants/             # Multi-tenancy (from platform)
│   │   └── connectors/
│   │       └── dtdc/            # Enterprise carrier connectors
│   ├── apps/
│   │   ├── platform/            # Platform app (existing)
│   │   └── jtl-foundation/      # JTL integration (from insiders)
│   ├── packages/
│   │   └── console/             # Console UI package (existing)
│   └── infra/                   # Infrastructure (from platform)
├── modules/
│   └── sdk/
│       └── karrio/
│           └── server/
│               └── licensing/   # NEW: License validation module
│                   ├── models.py
│                   ├── service.py
│                   ├── crypto.py
│                   ├── middleware.py
│                   ├── decorators.py
│                   ├── management/
│                   │   └── commands/
│                   │       └── license.py   # CLI tool
│                   └── keys/
│                       └── public.pem       # Embedded public key
├── LICENSE                      # LGPL-3.0 (unchanged)
└── (no .gitmodules)
```

```python
# Desired: Runtime license check in Django
from karrio.server.licensing.decorators import licensed_feature
from karrio.server.licensing.service import LicenseService

# View-level gating
@licensed_feature("organizations")
class OrganizationViewSet(GenericAPIView):
    ...

# Programmatic check
license = LicenseService.get_current()
if license.is_feature_available("automation"):
    # Enable automation features
    ...
```

### Problems

1. **Submodule complexity**: Git submodules create friction for development (separate commits, version pinning, auth requirements, CI/CD complexity). Contributors need access to multiple private repos.
2. **No license enforcement**: Enterprise features are protected only by GitHub repository access control and private Docker registry. Anyone who obtains the code can use all features without restriction.
3. **Split development workflow**: Changes spanning OSS + EE require coordinated commits across repositories. PRs cannot be atomic.
4. **Deployment coupling**: Docker images must be built from private registries. Self-hosted users cannot customize or extend enterprise features without full repo access.
5. **No feature granularity**: Current model is all-or-nothing. No ability to offer different tiers (e.g., Professional vs Enterprise) with different feature sets.

---

## Goals & Success Criteria

### Goals

1. Eliminate git submodules by merging all enterprise code into the main repository under `ee/`
2. Implement RSA-signed license key infrastructure with offline validation and optional online renewal
3. Gate all current insiders features behind runtime license checks (backend + frontend)
4. Provide a CLI tool (`karrio license`) for generating, inspecting, and validating license keys
5. Maintain full backward compatibility for existing OSS users (no license required for community features)

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| All insiders modules load only with valid license | 100% of EE modules gated | Must-have |
| OSS features work without any license key | Zero regression in community features | Must-have |
| License validation adds < 50ms to startup | Measured via profiling | Must-have |
| Offline license keys work in air-gapped environments | No network calls required for validation | Must-have |
| License CLI can generate/inspect/verify keys | All commands functional | Must-have |
| Frontend hides EE features when unlicensed | All EE UI routes/components gated | Must-have |
| Online license renewal works when server available | Auto-renew within configured interval | Nice-to-have |
| License expiry triggers graceful degradation | Warning period before hard cutoff | Nice-to-have |

### Launch Criteria

**Must-have (P0):**
- [ ] All `ee/insiders` and `ee/platform` code merged into `ee/` (no submodules)
- [ ] Karrio Commercial License file in `ee/LICENSE`
- [ ] Root `LICENSE` updated with dual-license declaration
- [ ] RSA key pair generation and license signing implemented
- [ ] License validation service (offline mode) integrated into Django
- [ ] `@licensed_feature` decorator gating all EE Django views
- [ ] `LicenseMiddleware` injecting license state into requests
- [ ] Frontend `LicenseRequired` component wrapping EE pages
- [ ] `karrio license generate` CLI command
- [ ] `karrio license verify` CLI command
- [ ] All existing tests pass (OSS and EE)
- [ ] Docker builds work with and without license key

**Nice-to-have (P1):**
- [ ] Online license validation/renewal endpoint
- [ ] License expiry grace period with warnings
- [ ] `karrio license info` command showing current license details
- [ ] GraphQL/REST API endpoint for license status
- [ ] Seat counting and enforcement
- [ ] Plan tier differentiation (Professional vs Enterprise)

---

## Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **A: Single repo + signed license keys** | Single development workflow; industry standard; cryptographic enforcement; supports offline; granular feature tiers | Enterprise code publicly visible; requires license infrastructure | **Selected** |
| **B: Keep submodules + add license keys** | Code remains private; simpler initial migration | Submodule friction persists; split PRs; CI/CD complexity unchanged | Rejected |
| **C: Legal-only enforcement (Sentry model)** | Zero technical complexity; no license key needed | No technical enforcement; relies entirely on legal action; no feature tiers | Rejected |
| **D: Build-time gating (conditional compilation)** | Strongest protection (code not in binary); smaller community builds | Complex CI/CD; two different build artifacts; harder to test; no industry precedent | Rejected |
| **E: Separate FOSS mirror (PostHog model)** | Clean OSS repo without EE code; dual-repo with auto-sync | Maintenance overhead; sync failures; still need license for main repo | Rejected (may revisit) |

### Trade-off Analysis

**Option A was selected** because it aligns with the dominant industry pattern (GitLab, Cal.com, PostHog, Metabase, n8n all use this approach). Key reasons:

- **Developer experience**: Single repo means atomic PRs, unified CI/CD, no submodule auth dance
- **Industry validation**: Every major OSS-with-enterprise project has converged on this model
- **Cryptographic enforcement**: RSA-signed keys provide tamper-proof license verification without requiring internet
- **Graceful degradation**: App always works; EE features simply disabled. No broken builds.
- **Future flexibility**: Plan tiers, seat limits, and feature flags all become possible with a license data structure

The main trade-off (code visibility) is accepted because:
1. The Karrio Commercial License legally prohibits production use without a paid license
2. Visibility enables community contribution to EE code (bug fixes, improvements)
3. Security through obscurity is not a viable long-term strategy
4. Every comparable project has proven this model works commercially

---

## Industry Research

### Comparison of Enterprise Licensing Models

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    INDUSTRY LICENSING LANDSCAPE                         │
├──────────┬────────────┬──────────────┬──────────────┬──────────────────┤
│ Project  │ OSS License│ EE License   │ Key Tech     │ Enforcement      │
├──────────┼────────────┼──────────────┼──────────────┼──────────────────┤
│ GitLab   │ MIT        │ Proprietary  │ RSA+AES blob │ Runtime          │
│ Cal.com  │ AGPLv3     │ Commercial   │ Remote API   │ Runtime          │
│ PostHog  │ MIT        │ Commercial   │ Remote API   │ Runtime + FOSS   │
│ Sentry   │ FSL-1.1    │ Private repo │ None         │ Legal only       │
│ Metabase │ AGPLv3     │ MCL          │ Remote/JWE   │ Runtime          │
│ n8n      │ Custom     │ Commercial   │ RSA cert     │ Runtime          │
│ Airbyte  │ ELv2       │ Commercial   │ JWT          │ Runtime          │
├──────────┼────────────┼──────────────┼──────────────┼──────────────────┤
│ KARRIO   │ LGPL-3.0   │ Commercial   │ RSA+AES      │ Runtime (hybrid) │
│ (planned)│            │              │ + online opt │                  │
└──────────┴────────────┴──────────────┴──────────────┴──────────────────┘
```

### Key Patterns Adopted from Research

| Pattern | Source | Karrio Adaptation |
|---------|--------|-------------------|
| Dual-license declaration in root LICENSE | Cal.com, PostHog | Root LICENSE references `ee/LICENSE` for EE code |
| RSA-signed license blob (offline) | GitLab (`gitlab-license` gem) | RSA-2048 + AES-128-CBC for license data encryption/signing |
| Runtime feature gating via decorators | n8n (`@Licensed`), PostHog (DRF permissions) | `@licensed_feature` Django decorator + DRF permission class |
| Django conditional app loading | PostHog (`try: from ee.apps`) | Auto-detect `ee/` directory, conditionally add to `INSTALLED_APPS` |
| Frontend `LicenseRequired` wrapper | Cal.com | Vue/React component that shows fallback when unlicensed |
| Session-level license state | Cal.com (`hasValidLicense` in session) | API metadata endpoint exposes license state to frontend |
| Dev mode bypass | Cal.com, n8n | `DEBUG=True` shows warning banner but allows EE feature access |
| Grace period on expiry | n8n, Metabase | Configurable grace period before hard cutoff |
| Feature enum registry | PostHog (`AvailableFeature`), n8n (`LICENSE_FEATURES`) | `LicenseFeature` StrEnum with all gated features |

---

## Technical Design

> **IMPORTANT**: Before designing, carefully study related existing code and utilities.
> Search the codebase for similar patterns to reuse. Never reinvent the wheel.
> Follow `AGENTS.md` coding style exactly as the original authors.

### Existing Code Analysis

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| Django settings conditional loading | `apps/api/karrio/server/settings/` | Extend to conditionally load EE apps |
| `karrio.lib` utilities | `modules/sdk/karrio/lib/` | Use `lib.to_json`, `lib.to_dict`, `lib.failsafe` |
| Management commands pattern | `apps/api/karrio/server/` | Follow existing `manage.py` command patterns |
| Middleware pattern | `apps/api/karrio/server/` | Follow existing middleware registration |
| Feature flags (Client model) | `ee/platform/modules/tenants/models.py` | `feature_flags` JSONField already exists on Client model |
| API metadata endpoint | `packages/hooks/api-metadata.ts` | Extend to include license state |
| DRF permission classes | `apps/api/karrio/server/core/` | Follow existing permission class patterns |

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                      KARRIO APPLICATION                              │
│                                                                      │
│  ┌──────────────┐     ┌──────────────┐     ┌─────────────────────┐  │
│  │   Frontend   │────>│   REST/GQL   │────>│   Django Views      │  │
│  │  (Next.js)   │     │   Gateway    │     │  + EE Views         │  │
│  └──────┬───────┘     └──────┬───────┘     └──────────┬──────────┘  │
│         │                    │                         │             │
│         │              ┌─────▼──────┐            ┌─────▼──────┐     │
│         │              │  License   │            │  @licensed  │     │
│         │              │ Middleware │            │  _feature() │     │
│         │              └─────┬──────┘            └─────┬──────┘     │
│         │                    │                         │             │
│         │              ┌─────▼─────────────────────────▼──────┐     │
│         │              │         LicenseService                │     │
│         │              │                                       │     │
│         │              │  ┌─────────────┐  ┌───────────────┐  │     │
│         │              │  │   Offline   │  │    Online     │  │     │
│         │              │  │  Validator  │  │  Validator    │  │     │
│         │              │  │ (RSA+AES)  │  │ (HTTP API)   │  │     │
│         │              │  └──────┬──────┘  └──────┬────────┘  │     │
│         │              │         │                 │           │     │
│         │              │  ┌──────▼──────┐  ┌──────▼────────┐  │     │
│         │              │  │ Public Key  │  │  License      │  │     │
│         │              │  │ (embedded)  │  │  Server API   │  │     │
│         │              │  └─────────────┘  └───────────────┘  │     │
│         │              └───────────────────────────────────────┘     │
│         │                                                            │
│  ┌──────▼───────────────────────────────────────────────────────┐   │
│  │                    License State Cache                         │   │
│  │  { plan, features[], seats, valid_until, licensee, ... }     │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌───────────────────┐     ┌───────────────────┐                    │
│  │  OSS Modules      │     │  EE Modules        │                   │
│  │  (always active)  │     │  (license-gated)   │                   │
│  │  - connectors     │     │  - admin            │                   │
│  │  - core SDK       │     │  - organizations    │                   │
│  │  - server         │     │  - audit            │                   │
│  │  - dashboard      │     │  - automation       │                   │
│  │                   │     │  - apps             │                   │
│  │                   │     │  - cloud            │                   │
│  │                   │     │  - tenants          │                   │
│  └───────────────────┘     └───────────────────┘                    │
└─────────────────────────────────────────────────────────────────────┘
```

### Sequence Diagram: License Validation Flow

```
┌────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│ Client │     │  Django   │     │ License  │     │ Offline  │     │ Online   │
│        │     │  Server   │     │ Service  │     │ Validator│     │ Validator│
└───┬────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
    │               │                │                 │                 │
    │   1. Startup  │                │                 │                 │
    │               │  2. Load       │                 │                 │
    │               │  license key   │                 │                 │
    │               │───────────────>│                 │                 │
    │               │                │  3. Validate    │                 │
    │               │                │  offline first  │                 │
    │               │                │────────────────>│                 │
    │               │                │                 │                 │
    │               │                │  4. RSA verify  │                 │
    │               │                │  + parse claims │                 │
    │               │                │<────────────────│                 │
    │               │                │                 │                 │
    │               │                │  5. (Optional)  │                 │
    │               │                │  Online renew   │                 │
    │               │                │────────────────────────────────>│
    │               │                │                 │   6. Renewed  │
    │               │                │<────────────────────────────────│
    │               │                │                 │                 │
    │               │  7. Cache      │                 │                 │
    │               │  license state │                 │                 │
    │               │<───────────────│                 │                 │
    │               │                │                 │                 │
    │  8. Request   │                │                 │                 │
    │  (EE feature) │                │                 │                 │
    │──────────────>│                │                 │                 │
    │               │  9. Check      │                 │                 │
    │               │  cached state  │                 │                 │
    │               │───────────────>│                 │                 │
    │               │                │                 │                 │
    │               │  10. Feature   │                 │                 │
    │               │  available?    │                 │                 │
    │               │<───────────────│                 │                 │
    │               │                │                 │                 │
    │  11a. 200 OK  │  (if licensed) │                 │                 │
    │<──────────────│                │                 │                 │
    │               │                │                 │                 │
    │  11b. 403     │  (if not)      │                 │                 │
    │<──────────────│                │                 │                 │
    │               │                │                 │                 │
```

### Data Flow Diagram: License Key Lifecycle

```
┌──────────────────────────────────────────────────────────────────────┐
│                     LICENSE KEY GENERATION                            │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌───────────┐    ┌─────────────┐    ┌─────────────┐    ┌────────┐ │
│  │ License   │───>│ JSON encode │───>│ AES-128-CBC │───>│ RSA    │ │
│  │ Claims    │    │ (plan,      │    │ encrypt     │    │ encrypt│ │
│  │ (dict)    │    │  features,  │    │ (random key)│    │ AES key│ │
│  └───────────┘    │  expiry...) │    └──────┬──────┘    └───┬────┘ │
│                   └─────────────┘           │               │      │
│                                      ┌──────▼───────────────▼────┐ │
│                                      │   Base64 encode           │ │
│                                      │   { data, key, iv }       │ │
│                                      └──────────┬────────────────┘ │
│                                                 │                  │
│                                      ┌──────────▼────────────────┐ │
│                                      │   License Key String      │ │
│                                      │   (portable, offline)     │ │
│                                      └───────────────────────────┘ │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│                     LICENSE KEY VALIDATION                            │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌───────────┐    ┌─────────────┐    ┌─────────────┐    ┌────────┐ │
│  │ License   │───>│ Base64      │───>│ RSA decrypt │───>│ AES    │ │
│  │ Key       │    │ decode      │    │ AES key     │    │ decrypt│ │
│  │ (string)  │    │             │    │ (public key)│    │ claims │ │
│  └───────────┘    └─────────────┘    └─────────────┘    └───┬────┘ │
│                                                             │      │
│                                      ┌──────────────────────▼────┐ │
│                                      │   Validate claims:        │ │
│                                      │   - expiry not passed     │ │
│                                      │   - plan is recognized    │ │
│                                      │   - features are valid    │ │
│                                      │   - seat count met        │ │
│                                      └──────────┬────────────────┘ │
│                                                 │                  │
│                                      ┌──────────▼────────────────┐ │
│                                      │   LicenseState (cached)   │ │
│                                      │   Available in request    │ │
│                                      └───────────────────────────┘ │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Data Models

#### License Claims (Signed Payload)

```python
# The data structure signed into the license key
@attr.s(auto_attribs=True)
class LicenseClaims:
    """Claims encoded in a signed license key."""

    version: int = 1                              # Schema version
    licensee: dict = {}                           # {"name": "Acme Corp", "email": "..."}
    plan: str = "community"                       # Plan tier identifier
    features: typing.List[str] = []               # Enabled feature slugs
    max_seats: int = 0                            # 0 = unlimited
    issued_at: str = ""                           # ISO 8601 datetime
    expires_at: str = ""                          # ISO 8601 datetime
    license_id: str = ""                          # Unique license identifier (UUID)
    metadata: dict = {}                           # Additional custom fields
```

#### Django License Model

```python
# ee/modules/licensing/models.py
from django.db import models


class License(models.Model):
    """Stored license record in the database."""

    key = models.TextField(
        help_text="The signed license key string"
    )
    license_id = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique license identifier from claims"
    )
    plan = models.CharField(
        max_length=50,
        help_text="Plan tier (community, professional, enterprise)"
    )
    licensee = models.JSONField(
        default=dict,
        help_text="Licensee information (name, email, company)"
    )
    features = models.JSONField(
        default=list,
        help_text="List of enabled feature slugs"
    )
    max_seats = models.IntegerField(
        default=0,
        help_text="Maximum allowed seats (0 = unlimited)"
    )
    valid_until = models.DateTimeField(
        help_text="License expiration datetime"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this license is the active one"
    )
    last_validated = models.DateTimeField(
        null=True, blank=True,
        help_text="Last successful online validation timestamp"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"License({self.license_id}, plan={self.plan})"
```

#### Feature Registry

```python
# ee/modules/licensing/features.py
import karrio.lib as lib


class LicenseFeature(lib.StrEnum):
    """All features that can be gated behind a license."""

    # Current insiders features
    ADMIN = "admin"
    ORGANIZATIONS = "organizations"
    AUDIT_LOGGING = "audit"
    AUTOMATION = "automation"
    APPS = "apps"
    CLOUD = "cloud"
    MULTI_TENANCY = "multi_tenancy"

    # Enterprise carrier connectors
    CONNECTOR_DTDC = "connector_dtdc"


# Plan-to-feature mapping
PLANS: dict = {
    "community": [],
    "professional": [
        LicenseFeature.ADMIN,
        LicenseFeature.ORGANIZATIONS,
        LicenseFeature.AUDIT_LOGGING,
    ],
    "enterprise": list(LicenseFeature),  # All features
}
```

### License Cryptography Module

```python
# ee/modules/licensing/crypto.py
import json
import base64
import os
import typing

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class LicenseCrypto:
    """RSA-2048 + AES-128-CBC license key signing and verification.

    Follows the GitLab pattern:
    1. License claims → JSON → AES encrypt (random key)
    2. AES key → RSA encrypt (private key)
    3. Package as { data, key, iv } → Base64 encode
    """

    @staticmethod
    def generate_key_pair() -> tuple:
        """Generate RSA-2048 key pair for license signing."""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend(),
        )
        public_key = private_key.public_key()

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        return private_pem, public_pem

    @staticmethod
    def sign_license(claims: dict, private_key_pem: bytes) -> str:
        """Sign license claims into a portable license key string."""
        # 1. Serialize claims to JSON
        claims_json = json.dumps(claims, sort_keys=True).encode("utf-8")

        # 2. Generate random AES key and IV
        aes_key = os.urandom(16)  # AES-128
        iv = os.urandom(16)

        # 3. AES encrypt the claims
        # Pad to AES block size
        pad_len = 16 - (len(claims_json) % 16)
        padded = claims_json + bytes([pad_len]) * pad_len

        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded) + encryptor.finalize()

        # 4. RSA encrypt the AES key
        private_key = serialization.load_pem_private_key(
            private_key_pem, password=None, backend=default_backend()
        )
        # Sign the AES key (not encrypt, since we use public key to verify)
        signed_key = private_key.sign(
            aes_key,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )

        # 5. Package and Base64 encode
        package = {
            "data": base64.b64encode(encrypted_data).decode("ascii"),
            "key": base64.b64encode(aes_key).decode("ascii"),
            "sig": base64.b64encode(signed_key).decode("ascii"),
            "iv": base64.b64encode(iv).decode("ascii"),
            "v": 1,
        }

        return base64.b64encode(
            json.dumps(package).encode("utf-8")
        ).decode("ascii")

    @staticmethod
    def verify_license(license_key: str, public_key_pem: bytes) -> typing.Optional[dict]:
        """Verify and decode a license key. Returns claims dict or None."""
        try:
            # 1. Base64 decode the package
            package = json.loads(base64.b64decode(license_key))

            # 2. Extract components
            encrypted_data = base64.b64decode(package["data"])
            aes_key = base64.b64decode(package["key"])
            signature = base64.b64decode(package["sig"])
            iv = base64.b64decode(package["iv"])

            # 3. Verify RSA signature on AES key
            public_key = serialization.load_pem_public_key(
                public_key_pem, backend=default_backend()
            )
            public_key.verify(
                signature,
                aes_key,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )

            # 4. AES decrypt the claims
            cipher = Cipher(
                algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend()
            )
            decryptor = cipher.decryptor()
            padded = decryptor.update(encrypted_data) + decryptor.finalize()

            # Remove PKCS7 padding
            pad_len = padded[-1]
            claims_json = padded[:-pad_len]

            # 5. Parse and return claims
            return json.loads(claims_json)

        except Exception:
            return None
```

### License Service

```python
# ee/modules/licensing/service.py
import typing
import logging
from datetime import datetime, timezone

from django.conf import settings
from django.core.cache import cache

import karrio.lib as lib
from ee.modules.licensing.crypto import LicenseCrypto
from ee.modules.licensing.features import LicenseFeature, PLANS

logger = logging.getLogger(__name__)

CACHE_KEY = "karrio:license:state"
CACHE_TTL = 3600  # 1 hour


class LicenseState:
    """Immutable snapshot of the current license state."""

    def __init__(
        self,
        plan: str = "community",
        features: typing.List[str] = None,
        valid_until: typing.Optional[datetime] = None,
        licensee: typing.Optional[dict] = None,
        max_seats: int = 0,
        license_id: str = "",
        is_valid: bool = False,
    ):
        self.plan = plan
        self.features = features or []
        self.valid_until = valid_until
        self.licensee = licensee or {}
        self.max_seats = max_seats
        self.license_id = license_id
        self.is_valid = is_valid

    def is_feature_available(self, feature: str) -> bool:
        """Check if a specific feature is available under the current license."""
        if not self.is_valid:
            return False
        return feature in self.features

    @property
    def is_expired(self) -> bool:
        if self.valid_until is None:
            return True
        return datetime.now(timezone.utc) > self.valid_until

    @property
    def is_in_grace_period(self) -> bool:
        """Check if the license is expired but within the grace period."""
        if not self.is_expired or self.valid_until is None:
            return False
        grace_days = getattr(settings, "LICENSE_GRACE_PERIOD_DAYS", 14)
        from datetime import timedelta
        grace_end = self.valid_until + timedelta(days=grace_days)
        return datetime.now(timezone.utc) <= grace_end

    def to_dict(self) -> dict:
        return {
            "plan": self.plan,
            "features": self.features,
            "valid_until": self.valid_until.isoformat() if self.valid_until else None,
            "licensee": self.licensee,
            "max_seats": self.max_seats,
            "license_id": self.license_id,
            "is_valid": self.is_valid,
            "is_expired": self.is_expired,
        }


# Community (no license) state
COMMUNITY_STATE = LicenseState(plan="community", is_valid=True)


class LicenseService:
    """Singleton service for license validation and state management."""

    _instance: typing.Optional["LicenseService"] = None
    _state: typing.Optional[LicenseState] = None

    @classmethod
    def get_instance(cls) -> "LicenseService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def get_current_state(cls) -> LicenseState:
        """Get the current license state (cached)."""
        instance = cls.get_instance()
        if instance._state is not None:
            return instance._state

        # Try cache first
        cached = cache.get(CACHE_KEY)
        if cached is not None:
            instance._state = cached
            return cached

        # Load and validate from database or environment
        state = instance._load_license()
        instance._state = state
        cache.set(CACHE_KEY, state, CACHE_TTL)
        return state

    def _load_license(self) -> LicenseState:
        """Load license from environment variable or database."""
        # Priority 1: Environment variable
        license_key = getattr(settings, "KARRIO_LICENSE_KEY", None)

        # Priority 2: Database
        if not license_key:
            license_key = self._load_from_database()

        if not license_key:
            return COMMUNITY_STATE

        return self._validate_offline(license_key)

    def _load_from_database(self) -> typing.Optional[str]:
        """Load the active license key from the database."""
        try:
            from ee.modules.licensing.models import License
            active = License.objects.filter(is_active=True).first()
            return active.key if active else None
        except Exception:
            return None

    def _validate_offline(self, license_key: str) -> LicenseState:
        """Validate a license key using the embedded public key."""
        import os

        public_key_path = os.path.join(
            os.path.dirname(__file__), "keys", "public.pem"
        )
        try:
            with open(public_key_path, "rb") as f:
                public_key = f.read()
        except FileNotFoundError:
            logger.error("License public key not found")
            return COMMUNITY_STATE

        claims = LicenseCrypto.verify_license(license_key, public_key)
        if claims is None:
            logger.warning("License key validation failed: invalid signature")
            return COMMUNITY_STATE

        # Parse claims into LicenseState
        valid_until = lib.to_date(claims.get("expires_at"))
        plan = claims.get("plan", "community")
        features = claims.get("features", PLANS.get(plan, []))

        state = LicenseState(
            plan=plan,
            features=features,
            valid_until=valid_until,
            licensee=claims.get("licensee", {}),
            max_seats=claims.get("max_seats", 0),
            license_id=claims.get("license_id", ""),
            is_valid=True,
        )

        # Check expiry (but allow grace period)
        if state.is_expired and not state.is_in_grace_period:
            logger.warning(
                "License key expired on %s", state.valid_until
            )
            return LicenseState(
                plan=state.plan,
                features=[],
                valid_until=state.valid_until,
                licensee=state.licensee,
                is_valid=False,
            )

        if state.is_expired and state.is_in_grace_period:
            logger.warning(
                "License expired but in grace period (expires fully on grace end)"
            )

        return state

    @classmethod
    def invalidate_cache(cls):
        """Force reload of license state on next access."""
        cache.delete(CACHE_KEY)
        if cls._instance:
            cls._instance._state = None
```

### Django Integration: Middleware

```python
# ee/modules/licensing/middleware.py
from ee.modules.licensing.service import LicenseService


class LicenseMiddleware:
    """Inject license state into every request."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.license_state = LicenseService.get_current_state()
        response = self.get_response(request)
        return response
```

### Django Integration: Decorator & Permission Class

```python
# ee/modules/licensing/decorators.py
import functools
from rest_framework import permissions, status
from rest_framework.response import Response

from ee.modules.licensing.service import LicenseService


class LicensePermission(permissions.BasePermission):
    """DRF permission class that checks for a specific licensed feature."""

    feature: str = ""

    def has_permission(self, request, view):
        feature = getattr(view, "licensed_feature", self.feature)
        if not feature:
            return True

        state = LicenseService.get_current_state()
        if not state.is_feature_available(feature):
            return False
        return True


def licensed_feature(feature: str):
    """Decorator to gate a Django view or viewset behind a license feature.

    Usage:
        @licensed_feature("organizations")
        class OrganizationViewSet(GenericAPIView):
            ...
    """
    def decorator(view_class_or_func):
        if isinstance(view_class_or_func, type):
            # Class-based view (ViewSet)
            view_class_or_func.licensed_feature = feature
            existing = list(getattr(view_class_or_func, "permission_classes", []))
            if LicensePermission not in existing:
                existing.append(LicensePermission)
            view_class_or_func.permission_classes = existing
            return view_class_or_func
        else:
            # Function-based view
            @functools.wraps(view_class_or_func)
            def wrapper(request, *args, **kwargs):
                state = LicenseService.get_current_state()
                if not state.is_feature_available(feature):
                    return Response(
                        {
                            "error": "feature_not_licensed",
                            "message": (
                                f"Your license does not include the '{feature}' feature. "
                                "Please upgrade your license to access this functionality."
                            ),
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )
                return view_class_or_func(request, *args, **kwargs)
            return wrapper
    return decorator
```

### Django Integration: Conditional EE App Loading

```python
# In karrio/server/settings/base.py (modification to existing file)

# --- Enterprise Edition ---
# Auto-detect and load EE modules if the ee/ directory exists.
# Follows PostHog pattern: try import, add to INSTALLED_APPS if available.

EE_AVAILABLE = False

try:
    from ee.modules.licensing.apps import LicensingConfig  # noqa: F401
    EE_AVAILABLE = True
except ImportError:
    pass

if EE_AVAILABLE:
    INSTALLED_APPS += [
        "ee.modules.licensing",
    ]
    MIDDLEWARE += [
        "ee.modules.licensing.middleware.LicenseMiddleware",
    ]

# Conditionally load EE modules based on license (loaded at runtime)
EE_MODULES = {
    "admin": "ee.modules.admin",
    "organizations": "ee.modules.orgs",
    "audit": "ee.modules.audit",
    "automation": "ee.modules.automation",
    "apps": "ee.modules.apps",
    "cloud": "ee.modules.cloud",
    "multi_tenancy": "ee.modules.tenants",
}

# EE modules are always in INSTALLED_APPS (code always loads).
# Feature gating happens at runtime via @licensed_feature decorator.
if EE_AVAILABLE:
    for module_key, module_path in EE_MODULES.items():
        try:
            __import__(module_path)
            INSTALLED_APPS += [module_path]
        except ImportError:
            pass
```

### CLI: License Management Commands

```python
# ee/modules/licensing/management/commands/license.py
import json
import uuid
from datetime import datetime, timedelta, timezone

from django.core.management.base import BaseCommand

from ee.modules.licensing.crypto import LicenseCrypto
from ee.modules.licensing.features import PLANS


class Command(BaseCommand):
    help = "Karrio license management commands"

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest="subcommand")

        # generate
        gen = subparsers.add_parser("generate", help="Generate a signed license key")
        gen.add_argument("--plan", required=True, choices=list(PLANS.keys()))
        gen.add_argument("--licensee-name", required=True)
        gen.add_argument("--licensee-email", required=True)
        gen.add_argument("--licensee-company", default="")
        gen.add_argument("--seats", type=int, default=0, help="Max seats (0=unlimited)")
        gen.add_argument("--days", type=int, default=365, help="Validity in days")
        gen.add_argument("--private-key", required=True, help="Path to RSA private key PEM")
        gen.add_argument("--output", help="Output file path (default: stdout)")

        # verify
        ver = subparsers.add_parser("verify", help="Verify a license key")
        ver.add_argument("--key", help="License key string")
        ver.add_argument("--key-file", help="Path to license key file")
        ver.add_argument("--public-key", required=True, help="Path to RSA public key PEM")

        # info
        subparsers.add_parser("info", help="Show current license information")

        # keygen
        kg = subparsers.add_parser("keygen", help="Generate RSA key pair")
        kg.add_argument("--output-dir", default=".", help="Output directory")

        # activate
        act = subparsers.add_parser("activate", help="Activate a license key")
        act.add_argument("--key", help="License key string")
        act.add_argument("--key-file", help="Path to license key file")

    def handle(self, *args, **options):
        subcommand = options.get("subcommand")
        if subcommand == "generate":
            self._handle_generate(options)
        elif subcommand == "verify":
            self._handle_verify(options)
        elif subcommand == "info":
            self._handle_info(options)
        elif subcommand == "keygen":
            self._handle_keygen(options)
        elif subcommand == "activate":
            self._handle_activate(options)
        else:
            self.stderr.write("Usage: karrio license <generate|verify|info|keygen|activate>")

    def _handle_generate(self, options):
        plan = options["plan"]
        now = datetime.now(timezone.utc)

        claims = {
            "version": 1,
            "license_id": str(uuid.uuid4()),
            "plan": plan,
            "features": PLANS.get(plan, []),
            "licensee": {
                "name": options["licensee_name"],
                "email": options["licensee_email"],
                "company": options.get("licensee_company", ""),
            },
            "max_seats": options["seats"],
            "issued_at": now.isoformat(),
            "expires_at": (now + timedelta(days=options["days"])).isoformat(),
        }

        with open(options["private_key"], "rb") as f:
            private_key = f.read()

        license_key = LicenseCrypto.sign_license(claims, private_key)

        if options.get("output"):
            with open(options["output"], "w") as f:
                f.write(license_key)
            self.stdout.write(f"License key written to {options['output']}")
        else:
            self.stdout.write(license_key)

        self.stderr.write(
            f"\nLicense generated:"
            f"\n  ID:      {claims['license_id']}"
            f"\n  Plan:    {plan}"
            f"\n  Seats:   {claims['max_seats'] or 'unlimited'}"
            f"\n  Expires: {claims['expires_at']}"
            f"\n  For:     {claims['licensee']['name']} ({claims['licensee']['email']})"
        )

    def _handle_verify(self, options):
        license_key = options.get("key")
        if not license_key and options.get("key_file"):
            with open(options["key_file"], "r") as f:
                license_key = f.read().strip()

        if not license_key:
            self.stderr.write("Error: provide --key or --key-file")
            return

        with open(options["public_key"], "rb") as f:
            public_key = f.read()

        claims = LicenseCrypto.verify_license(license_key, public_key)
        if claims is None:
            self.stderr.write("INVALID: License key verification failed")
            return

        self.stdout.write(json.dumps(claims, indent=2))
        self.stderr.write("VALID: License key signature verified")

    def _handle_info(self, options):
        from ee.modules.licensing.service import LicenseService
        state = LicenseService.get_current_state()
        self.stdout.write(json.dumps(state.to_dict(), indent=2, default=str))

    def _handle_keygen(self, options):
        import os
        output_dir = options["output_dir"]
        private_pem, public_pem = LicenseCrypto.generate_key_pair()

        private_path = os.path.join(output_dir, "private.pem")
        public_path = os.path.join(output_dir, "public.pem")

        with open(private_path, "wb") as f:
            f.write(private_pem)
        with open(public_path, "wb") as f:
            f.write(public_pem)

        self.stdout.write(f"Key pair generated:\n  Private: {private_path}\n  Public:  {public_path}")
        self.stderr.write(
            "\nIMPORTANT: Keep private.pem secure. "
            "Copy public.pem to ee/modules/licensing/keys/public.pem"
        )

    def _handle_activate(self, options):
        license_key = options.get("key")
        if not license_key and options.get("key_file"):
            with open(options["key_file"], "r") as f:
                license_key = f.read().strip()

        if not license_key:
            self.stderr.write("Error: provide --key or --key-file")
            return

        from ee.modules.licensing.service import LicenseService
        from ee.modules.licensing.models import License

        # Validate first
        state = LicenseService.get_instance()._validate_offline(license_key)
        if not state.is_valid:
            self.stderr.write("Error: invalid license key")
            return

        # Deactivate existing licenses
        License.objects.filter(is_active=True).update(is_active=False)

        # Store new license
        License.objects.create(
            key=license_key,
            license_id=state.license_id,
            plan=state.plan,
            licensee=state.licensee,
            features=state.features,
            max_seats=state.max_seats,
            valid_until=state.valid_until,
            is_active=True,
        )

        # Invalidate cache
        LicenseService.invalidate_cache()

        self.stdout.write(f"License activated: {state.plan} plan (expires {state.valid_until})")
```

### Frontend Integration

```typescript
// Extension to existing API metadata hook to include license state
// packages/hooks/api-metadata.ts (modification)

interface LicenseState {
  plan: string;
  features: string[];
  valid_until: string | null;
  is_valid: boolean;
  is_expired: boolean;
}

interface APIMetadata {
  // ... existing fields ...
  license?: LicenseState;
}
```

```typescript
// packages/ui/core/components/license-required.tsx (new file)

import React from "react";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";

interface LicenseRequiredProps {
  feature: string;
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export function LicenseRequired({
  feature,
  children,
  fallback,
}: LicenseRequiredProps) {
  const { metadata } = useAPIMetadata();
  const isLicensed = metadata?.license?.features?.includes(feature) ?? false;

  if (isLicensed) {
    return <>{children}</>;
  }

  if (fallback) {
    return <>{fallback}</>;
  }

  return (
    <div className="has-text-centered p-6">
      <p className="is-size-5 has-text-weight-bold mb-2">
        Enterprise Feature
      </p>
      <p className="has-text-grey mb-4">
        This feature requires a Karrio Enterprise license.
      </p>
      <a
        href="https://karrio.io/pricing"
        className="button is-primary"
        target="_blank"
        rel="noopener noreferrer"
      >
        Learn More
      </a>
    </div>
  );
}
```

### Configuration

```python
# Environment variables for license configuration
# Added to settings/base.py

# License key (offline mode - primary)
KARRIO_LICENSE_KEY = config("KARRIO_LICENSE_KEY", default=None)

# Online validation (optional)
KARRIO_LICENSE_SERVER_URL = config(
    "KARRIO_LICENSE_SERVER_URL",
    default="https://license.karrio.io/v1",
)
KARRIO_LICENSE_AUTO_RENEW = config(
    "KARRIO_LICENSE_AUTO_RENEW",
    default=True,
    cast=bool,
)
KARRIO_LICENSE_RENEW_INTERVAL_HOURS = config(
    "KARRIO_LICENSE_RENEW_INTERVAL_HOURS",
    default=72,
    cast=int,
)

# Grace period after license expiry (days)
LICENSE_GRACE_PERIOD_DAYS = config(
    "LICENSE_GRACE_PERIOD_DAYS",
    default=14,
    cast=int,
)
```

### Docker Integration

```yaml
# docker/docker-compose.yml (modification)
# No changes needed for community edition - license is optional

services:
  api:
    image: karrio/server:latest
    environment:
      # Optional: provide license key for enterprise features
      - KARRIO_LICENSE_KEY=${KARRIO_LICENSE_KEY:-}
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `KARRIO_LICENSE_KEY` | string | No | Signed license key string (env var or DB) |
| `KARRIO_LICENSE_SERVER_URL` | string | No | URL of online license validation server |
| `KARRIO_LICENSE_AUTO_RENEW` | bool | No | Enable automatic online license renewal. Default: `true` |
| `LICENSE_GRACE_PERIOD_DAYS` | int | No | Days after expiry before hard cutoff. Default: `14` |
| `license.plan` | string | - | Plan tier: `community`, `professional`, `enterprise` |
| `license.features` | list | - | List of enabled feature slugs |
| `license.max_seats` | int | - | Maximum users allowed (0 = unlimited) |
| `license.valid_until` | datetime | - | License expiration timestamp |
| `license.license_id` | string | - | Unique license identifier (UUID) |

### API Changes

**Endpoints (new):**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/license` | Get current license status (admin only) |
| POST | `/api/v1/license/activate` | Activate a license key |
| DELETE | `/api/v1/license` | Deactivate current license |

**GET /api/v1/license Response:**

```json
{
  "plan": "enterprise",
  "features": ["admin", "organizations", "audit", "automation", "apps", "cloud", "multi_tenancy"],
  "valid_until": "2027-01-30T00:00:00Z",
  "licensee": {
    "name": "Acme Corp",
    "email": "admin@acme.com",
    "company": "Acme Corporation"
  },
  "max_seats": 50,
  "is_valid": true,
  "is_expired": false
}
```

**POST /api/v1/license/activate Request:**

```json
{
  "key": "<base64-encoded-signed-license-key>"
}
```

### Security Considerations

- [x] RSA-2048 key pair (private key never shipped with application)
- [x] AES-128-CBC encryption for license claims (prevents tampering)
- [x] PSS signature padding with SHA-256 (industry standard)
- [x] Public key embedded in application (read-only, used for verification only)
- [x] No secrets in code or logs (license key is opaque, claims only logged at debug level)
- [x] License activation endpoint requires admin authentication
- [x] Grace period prevents abrupt service disruption
- [x] Cache invalidation on license change
- [x] SQL injection prevention (uses Django ORM exclusively)

---

## Edge Cases & Failure Modes

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| No license key provided | App runs in community mode, all EE features disabled | `COMMUNITY_STATE` returned by `LicenseService` |
| Invalid/corrupt license key | App runs in community mode with warning log | `LicenseCrypto.verify_license` returns `None`, falls back to community |
| License expired within grace period | EE features still work, warning logged | `is_in_grace_period` check allows continued access |
| License expired beyond grace period | EE features disabled, app continues running | `is_valid=False`, features list cleared |
| Online server unreachable | Offline validation used, no disruption | Online validator falls back to cached/offline state |
| Multiple license keys in database | Most recently created active license used | `is_active=True` filter + `ordering = ["-created_at"]` |
| License key set in both env var and DB | Environment variable takes priority | Explicit priority order in `_load_license()` |
| Public key file missing | Community mode with error log | `FileNotFoundError` caught, returns community state |
| `ee/` directory removed from repo | App runs as pure OSS, no EE modules loaded | `try: import` pattern handles missing `ee/` gracefully |
| License downgrade (fewer features) | Previously enabled features immediately disabled | Cache invalidated on activation, new state takes effect |
| Clock manipulation (system time set back) | License appears valid longer than intended | Mitigated by online renewal checks; accepted trade-off for offline mode |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| Private key compromise | Attacker can generate valid license keys | Rotate key pair, ship new public key in update, revoke old keys via online server |
| License server downtime | Online renewal fails | Offline validation unaffected; grace period for expired licenses |
| Database corruption (license record lost) | License state reverts to community | Re-activate from env var or re-enter key; license key string is portable |
| Cache poisoning | Stale license state served | TTL-based cache expiry (1 hour); manual `invalidate_cache()` available |
| Django migration failure | License model not created | Standard migration rollback; app still starts (community mode) |
| Concurrent license activations | Race condition on `is_active` flag | Database transaction wraps deactivate + create; last write wins |

---

## Implementation Plan

### Phase 1: Repository Merge & License Infrastructure

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Create `ee/LICENSE` (Karrio Commercial License) | `ee/LICENSE` | Pending | S |
| Update root `LICENSE` with dual-license declaration | `LICENSE` | Pending | S |
| Move `ee/insiders/modules/*` → `ee/modules/` | `ee/modules/` | Pending | M |
| Move `ee/platform/modules/tenants` → `ee/modules/tenants` | `ee/modules/tenants/` | Pending | M |
| Move `ee/platform/infra` → `ee/infra/` | `ee/infra/` | Pending | S |
| Move `ee/insiders/apps/*` → `ee/apps/` | `ee/apps/` | Pending | S |
| Remove `.gitmodules` and submodule references | `.gitmodules`, `.git/config` | Pending | S |
| Update `pyproject.toml` paths for moved EE modules | `ee/modules/*/pyproject.toml` | Pending | M |
| Update workspace config in root `package.json` | `package.json` | Pending | S |
| Archive `karrio-insiders` and `karrio-platform` repos | GitHub | Pending | S |

### Phase 2: License Cryptography & Service

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Implement `LicenseCrypto` (RSA+AES sign/verify) | `ee/modules/licensing/crypto.py` | Pending | M |
| Implement `LicenseFeature` enum and `PLANS` mapping | `ee/modules/licensing/features.py` | Pending | S |
| Implement `License` Django model | `ee/modules/licensing/models.py` | Pending | S |
| Create database migration for License model | `ee/modules/licensing/migrations/` | Pending | S |
| Implement `LicenseService` (state management, caching) | `ee/modules/licensing/service.py` | Pending | L |
| Implement `LicenseMiddleware` | `ee/modules/licensing/middleware.py` | Pending | S |
| Implement `@licensed_feature` decorator + `LicensePermission` | `ee/modules/licensing/decorators.py` | Pending | M |
| Generate RSA key pair and embed public key | `ee/modules/licensing/keys/public.pem` | Pending | S |
| Implement `karrio license` CLI commands | `ee/modules/licensing/management/commands/license.py` | Pending | L |
| Add `LicensingConfig` Django app config | `ee/modules/licensing/apps.py` | Pending | S |

**Dependencies:** Phase 2 depends on Phase 1 completion.

### Phase 3: Backend Feature Gating

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add `@licensed_feature("admin")` to admin views | `ee/modules/admin/` views | Pending | M |
| Add `@licensed_feature("organizations")` to org views | `ee/modules/orgs/` views | Pending | M |
| Add `@licensed_feature("audit")` to audit views | `ee/modules/audit/` views | Pending | M |
| Add `@licensed_feature("automation")` to automation views | `ee/modules/automation/` views | Pending | M |
| Add `@licensed_feature("apps")` to apps views | `ee/modules/apps/` views | Pending | M |
| Add `@licensed_feature("cloud")` to cloud views | `ee/modules/cloud/` views | Pending | S |
| Add `@licensed_feature("multi_tenancy")` to tenant views | `ee/modules/tenants/` views | Pending | M |
| Update Django settings for conditional EE loading | `apps/api/karrio/server/settings/` | Pending | M |
| Expose license state in API metadata endpoint | `apps/api/karrio/server/core/` | Pending | M |

**Dependencies:** Phase 3 depends on Phase 2 completion.

### Phase 4: Frontend Feature Gating

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Create `LicenseRequired` React component | `packages/ui/core/components/` | Pending | M |
| Update API metadata hook to include license state | `packages/hooks/api-metadata.ts` | Pending | S |
| Wrap EE dashboard pages with `LicenseRequired` | `apps/dashboard/src/` | Pending | M |
| Wrap EE platform pages with `LicenseRequired` | `ee/apps/platform/src/` | Pending | M |
| Add license status display in admin/settings UI | `apps/dashboard/src/` | Pending | M |
| Add license activation UI flow | `apps/dashboard/src/` | Pending | L |

**Dependencies:** Phase 4 depends on Phase 3 completion.

### Phase 5: Docker & CI/CD Updates

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Update Dockerfiles to include `ee/` directory | `docker/` | Pending | M |
| Remove private registry auth requirements from CI | `.github/workflows/` | Pending | M |
| Update docker-compose files (remove submodule references) | `docker/docker-compose*.yml` | Pending | M |
| Add `KARRIO_LICENSE_KEY` to `.env.sample` | `.env.sample` | Pending | S |
| Test builds with and without license key | CI pipeline | Pending | M |
| Update documentation for new licensing model | `docs/` | Pending | M |

**Dependencies:** Phase 5 depends on Phase 3 completion.

### Phase 6: Online License Validation (P1)

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Design license server API contract | PRD | Pending | M |
| Implement online validator in `LicenseService` | `ee/modules/licensing/service.py` | Pending | L |
| Implement auto-renewal background task | `ee/modules/licensing/tasks.py` | Pending | M |
| Add license revocation support | `ee/modules/licensing/service.py` | Pending | M |

**Dependencies:** Phase 6 is independent (P1 feature, deferred).

---

## Testing Strategy

> **CRITICAL**: All tests must follow `AGENTS.md` guidelines exactly as the original authors.

### Test Categories

| Category | Location | Coverage Target |
|----------|----------|-----------------|
| License Crypto Unit Tests | `ee/modules/licensing/tests/test_crypto.py` | 100% |
| License Service Unit Tests | `ee/modules/licensing/tests/test_service.py` | 90%+ |
| Feature Gating Integration Tests | `ee/modules/licensing/tests/test_gating.py` | Key flows |
| CLI Command Tests | `ee/modules/licensing/tests/test_commands.py` | All subcommands |
| Migration Tests | `ee/modules/licensing/tests/test_models.py` | Model CRUD |

### Test Cases

#### Unit Tests: License Cryptography

```python
"""Tests for license key signing and verification."""

import unittest
from ee.modules.licensing.crypto import LicenseCrypto


class TestLicenseCrypto(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.private_key, self.public_key = LicenseCrypto.generate_key_pair()

    def test_sign_and_verify_roundtrip(self):
        """Verify that a signed license can be verified with the matching public key."""
        claims = {
            "version": 1,
            "license_id": "test-123",
            "plan": "enterprise",
            "features": ["admin", "organizations"],
            "licensee": {"name": "Test Corp", "email": "test@example.com"},
            "max_seats": 10,
            "issued_at": "2026-01-30T00:00:00Z",
            "expires_at": "2027-01-30T00:00:00Z",
        }

        license_key = LicenseCrypto.sign_license(claims, self.private_key)
        result = LicenseCrypto.verify_license(license_key, self.public_key)

        print(result)
        self.assertIsNotNone(result)
        self.assertEqual(result["plan"], "enterprise")
        self.assertEqual(result["license_id"], "test-123")
        self.assertListEqual(result["features"], ["admin", "organizations"])

    def test_verify_with_wrong_public_key(self):
        """Verify that a license signed with one key fails with a different key."""
        claims = {"version": 1, "plan": "enterprise"}

        license_key = LicenseCrypto.sign_license(claims, self.private_key)

        # Generate a different key pair
        _, wrong_public_key = LicenseCrypto.generate_key_pair()
        result = LicenseCrypto.verify_license(license_key, wrong_public_key)

        self.assertIsNone(result)

    def test_verify_corrupted_key(self):
        """Verify that a corrupted license key returns None."""
        result = LicenseCrypto.verify_license("corrupted-data", self.public_key)
        self.assertIsNone(result)

    def test_verify_empty_key(self):
        """Verify that an empty license key returns None."""
        result = LicenseCrypto.verify_license("", self.public_key)
        self.assertIsNone(result)

    def test_key_pair_generation(self):
        """Verify that key pair generation produces valid PEM keys."""
        private_pem, public_pem = LicenseCrypto.generate_key_pair()
        self.assertTrue(private_pem.startswith(b"-----BEGIN PRIVATE KEY-----"))
        self.assertTrue(public_pem.startswith(b"-----BEGIN PUBLIC KEY-----"))
```

#### Unit Tests: License Service

```python
"""Tests for license state management and validation."""

import unittest
from unittest.mock import patch, MagicMock, ANY
from datetime import datetime, timedelta, timezone

from ee.modules.licensing.service import LicenseService, LicenseState, COMMUNITY_STATE
from ee.modules.licensing.features import LicenseFeature


class TestLicenseState(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_community_state_has_no_features(self):
        """Verify community state returns False for all feature checks."""
        state = COMMUNITY_STATE

        self.assertTrue(state.is_valid)
        self.assertEqual(state.plan, "community")
        self.assertFalse(state.is_feature_available("admin"))
        self.assertFalse(state.is_feature_available("organizations"))

    def test_enterprise_state_has_all_features(self):
        """Verify enterprise state returns True for all features."""
        state = LicenseState(
            plan="enterprise",
            features=list(LicenseFeature),
            valid_until=datetime.now(timezone.utc) + timedelta(days=365),
            is_valid=True,
        )

        self.assertTrue(state.is_feature_available("admin"))
        self.assertTrue(state.is_feature_available("organizations"))
        self.assertTrue(state.is_feature_available("automation"))

    def test_expired_state_denies_features(self):
        """Verify expired license denies feature access."""
        state = LicenseState(
            plan="enterprise",
            features=[],
            valid_until=datetime.now(timezone.utc) - timedelta(days=30),
            is_valid=False,
        )

        self.assertFalse(state.is_feature_available("admin"))
        self.assertTrue(state.is_expired)

    def test_grace_period_allows_features(self):
        """Verify license in grace period still allows features."""
        state = LicenseState(
            plan="enterprise",
            features=list(LicenseFeature),
            valid_until=datetime.now(timezone.utc) - timedelta(days=5),
            is_valid=True,
        )

        self.assertTrue(state.is_expired)
        self.assertTrue(state.is_in_grace_period)
        self.assertTrue(state.is_feature_available("admin"))

    def test_to_dict_serialization(self):
        """Verify LicenseState serializes correctly."""
        valid_until = datetime(2027, 1, 30, tzinfo=timezone.utc)
        state = LicenseState(
            plan="professional",
            features=["admin", "organizations"],
            valid_until=valid_until,
            licensee={"name": "Test"},
            max_seats=10,
            license_id="test-id",
            is_valid=True,
        )

        result = state.to_dict()
        print(result)
        self.assertDictEqual(result, {
            "plan": "professional",
            "features": ["admin", "organizations"],
            "valid_until": "2027-01-30T00:00:00+00:00",
            "licensee": {"name": "Test"},
            "max_seats": 10,
            "license_id": "test-id",
            "is_valid": True,
            "is_expired": False,
        })
```

#### Integration Tests: Feature Gating

```python
"""Tests for runtime feature gating on API endpoints."""

import unittest
from unittest.mock import patch, ANY

from django.test import TestCase, RequestFactory

from ee.modules.licensing.service import LicenseState, LicenseService
from ee.modules.licensing.decorators import licensed_feature


class TestFeatureGating(TestCase):
    def setUp(self):
        self.maxDiff = None

    @patch.object(LicenseService, "get_current_state")
    def test_licensed_endpoint_returns_200(self, mock_state):
        """Verify licensed feature returns 200 with valid license."""
        mock_state.return_value = LicenseState(
            plan="enterprise",
            features=["organizations"],
            is_valid=True,
        )

        response = self.client.get("/api/v1/organizations")
        # print(response)
        self.assertNotEqual(response.status_code, 403)

    @patch.object(LicenseService, "get_current_state")
    def test_unlicensed_endpoint_returns_403(self, mock_state):
        """Verify unlicensed feature returns 403."""
        mock_state.return_value = LicenseState(
            plan="community",
            features=[],
            is_valid=True,
        )

        response = self.client.get("/api/v1/organizations")
        # print(response)
        self.assertEqual(response.status_code, 403)
```

### Running Tests

```bash
# From repository root
source bin/activate-env

# License module tests
python -m unittest discover -v -f ee/modules/licensing/tests

# All EE module tests
python -m unittest discover -v -f ee/modules/

# Server tests (includes EE integration)
karrio test --failfast karrio.server.licensing.tests
```

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Private key leak enables unauthorized license generation | High | Low | Store private key in HSM/secrets manager; rotate keys with new public key in releases; online revocation list |
| Submodule removal breaks existing CI/CD pipelines | Medium | Medium | Phase migration; maintain both approaches briefly; update all workflow files |
| Enterprise code visibility enables competitors | Medium | Low | Legal protection via Karrio Commercial License; code visibility is industry standard |
| License validation adds latency to requests | Low | Low | Cached license state (1h TTL); validation only on startup/activation |
| Django migration conflicts with existing EE modules | Medium | Medium | Careful migration ordering; squash migrations before merge |
| Frontend breaking changes from moved packages | Medium | Medium | Update workspace paths; test all builds before merge |
| Clock manipulation bypasses offline license expiry | Low | Low | Online renewal checks mitigate; accepted trade-off for air-gap support |
| Community backlash from code visibility change | Low | Low | Clear communication; dual-license is industry standard; OSS features unchanged |

---

## Migration & Rollback

### Backward Compatibility

- **API compatibility**: All existing REST/GraphQL endpoints continue working. New `/api/v1/license` endpoints are additive.
- **Data compatibility**: No existing data modified. New `License` model is additive. Existing `feature_flags` JSONField on Client model unchanged.
- **Docker compatibility**: Existing docker-compose files work without license (community mode). `KARRIO_LICENSE_KEY` env var is optional.
- **OSS user impact**: Zero. All community features work identically without any license key.

### Data Migration

**Migration Steps:**
1. Run `karrio migrate` to create the `License` table
2. (Optional) Activate a license key via CLI: `karrio license activate --key-file license.key`
3. Verify with `karrio license info`

No data backfill required. The License table starts empty (community mode).

### Repository Migration

```bash
# Step 1: Remove submodules
git submodule deinit --all --force
git rm .gitmodules
git rm --cached ee/insiders ee/platform

# Step 2: Copy content from submodule checkouts into ee/
# (Detailed script to be created during implementation)
cp -r ee/insiders/modules/* ee/modules/
cp -r ee/platform/modules/tenants ee/modules/tenants
cp -r ee/platform/infra ee/infra/
cp -r ee/insiders/apps/* ee/apps/
cp -r ee/insiders/architecture ee/architecture/

# Step 3: Clean up empty directories
rm -rf ee/insiders ee/platform

# Step 4: Update import paths and pyproject.toml files
# (Automated script to be created during implementation)

# Step 5: Commit
git add -A
git commit -m "feat: merge insiders and platform repos into ee/"
```

### Rollback Procedure

1. **Identify issue**: CI/CD failures, broken imports, test failures after merge
2. **Stop rollout**: Do not deploy the merged version
3. **Revert changes**: `git revert <merge-commit>` to restore submodule configuration
4. **Re-initialize submodules**: `git submodule update --init --recursive`
5. **Verify recovery**: Run full test suite to confirm rollback is clean

---

## Appendices

### Appendix A: Karrio Commercial License (Draft)

```
The Karrio Enterprise License
Copyright (c) 2020-2026 Karrio Inc.

With regard to the Karrio Software:

This software and associated documentation files (the "Software") may
only be used in production, if you (and any entity that you represent)
have agreed to, and are in compliance with, the Karrio Subscription
Terms of Service, available at https://karrio.io/terms (the "Enterprise
Terms"), or other agreement governing the use of the Software, as
agreed by you and Karrio, and otherwise have a valid Karrio Enterprise
Edition subscription ("Commercial Subscription") for the correct number
of user seats. Subject to the foregoing sentence, you are free to
modify this Software and publish patches to the Software. You agree
that Karrio and/or its licensors (as applicable) retain all right,
title and interest in and to all such modifications and/or patches,
and all such modifications and/or patches may only be used, copied,
modified, displayed, distributed, or otherwise exploited with a valid
Commercial Subscription for the correct number of user seats.
Notwithstanding the foregoing, you may copy and modify the Software
for development and testing purposes, without requiring a subscription.
You agree that Karrio and/or its licensors (as applicable) retain all
right, title and interest in and to all such modifications. You are
not granted any other rights beyond what is expressly stated herein.
Subject to the foregoing, it is forbidden to copy, merge, publish,
distribute, sublicense, and/or sell the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For all third party components incorporated into the Karrio Software,
those components are licensed under the original license provided by
the owner of the applicable component.
```

### Appendix B: Root LICENSE Update (Draft)

The root `LICENSE` file should be updated to include a dual-license declaration header:

```
Copyright (c) 2020-2026 Karrio Inc.

Portions of this software are licensed as follows:

* All content that resides under the "ee/" directory of this
  repository, if that directory exists, is licensed under the
  license defined in "ee/LICENSE".

* All third party components incorporated into the Karrio Software
  are licensed under the original license provided by the owner of
  the applicable component.

* Content outside of the above mentioned directories or restrictions
  above is available under the "LGPL-3.0" license as defined below.

---

[Existing LGPL-3.0 license text follows]
```

### Appendix C: Industry Research Detail

Full research findings for each project (Cal.com, PostHog, Sentry, GitLab, Metabase, n8n, Airbyte) are documented in the working notes used to produce this PRD. Key takeaways:

| Pattern | Industry Consensus | Karrio Adoption |
|---------|-------------------|-----------------|
| Single repo with `ee/` | 6/7 projects (all except Sentry) | Yes |
| Runtime-only enforcement | 7/7 projects | Yes |
| Cryptographic license keys | 5/7 projects (GitLab, Metabase, n8n, Airbyte, Cal.com) | Yes (RSA+AES) |
| Proprietary EE license | 6/7 projects | Yes (Karrio Commercial License) |
| Graceful degradation | 7/7 projects | Yes (community mode fallback) |
| Dev mode bypass | 3/7 projects (Cal.com, n8n, PostHog) | Considered for Phase 2 |
| FOSS mirror | 2/7 projects (PostHog, GitLab) | Not planned (may revisit) |
| License server | 4/7 projects (Cal.com, PostHog, Metabase, n8n) | Deferred to Phase 2 |

### Appendix D: CLI Usage Examples

```bash
# Generate RSA key pair (one-time setup)
karrio license keygen --output-dir /secure/path/

# Generate a license key
karrio license generate \
  --plan enterprise \
  --licensee-name "Acme Corp" \
  --licensee-email "admin@acme.com" \
  --licensee-company "Acme Corporation" \
  --seats 50 \
  --days 365 \
  --private-key /secure/path/private.pem \
  --output license.key

# Verify a license key
karrio license verify \
  --key-file license.key \
  --public-key /secure/path/public.pem

# Activate a license (stores in database)
karrio license activate --key-file license.key

# Check current license status
karrio license info
```
