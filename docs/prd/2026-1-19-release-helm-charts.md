# PRD: karrio v2026.1.19 Release + Official Kubernetes Helm Charts

**Author:** Daniel Kobina Manu  
**Date:** 2026-03-06  
**Status:** Approved — Implementation in progress

---

## 1. Overview

This PRD covers two deliverables bundled into the `release/2026.1.19` milestone:

1. **v2026.1.19 Release** — Merges Ansh's MyDHL fixes (PR #993) and the shipment status rename `purchased → created` (PR #998) into a clean release branch.
2. **Official Kubernetes Helm Charts** — A production-grade `charts/karrio` Helm chart at the repo root that allows users to self-host karrio on any Kubernetes cluster using a single `helm install`.

---

## 2. Goals

- Ship a clean, tested release that resolves two significant pending issues
- Provide an official, first-class K8s deployment path for the karrio open source community
- Reduce friction for self-hosted deployments (currently requires manual compose + config wrangling)
- Charts follow Helm best practices and are usable by both developers and platform teams
- Full local validation via OrbStack before PR

---

## 3. Release Scope (v2026.1.19)

### 3.1 PR #993 — MyDHL Fixes (Ansh Nagar)
- Bug fixes and improvements for the MyDHL carrier integration
- Merged into `release/2026.1.19` via PR merge (not cherry-pick)

### 3.2 PR #998 — Shipment Status Rename (Daniel Manu)
- Renames `purchased` → `created` across the codebase
- Includes data migration for existing records
- Removes `choices` constraint from `Shipment.status` field
- Merged into `release/2026.1.19` via PR merge

### 3.3 Release Commit
- Version bump to `2026.1.19`
- Changelog entry

---

## 4. Helm Charts — Detailed Spec

### 4.1 Directory Structure

```
charts/
└── karrio/
    ├── Chart.yaml              # Chart metadata, version, appVersion
    ├── values.yaml             # Default values (all configurable)
    ├── values.production.yaml  # Production-ready overrides example
    ├── values.minimal.yaml     # Minimal single-node example
    ├── README.md               # Usage docs
    ├── .helmignore
    └── templates/
        ├── NOTES.txt           # Post-install instructions
        ├── _helpers.tpl        # Shared template helpers
        ├── configmap.yaml      # App config (KARRIO_* env vars)
        ├── secret.yaml         # Secret template (DB URL, secret key, etc.)
        ├── serviceaccount.yaml
        ├── api/
        │   ├── deployment.yaml     # karrio API server
        │   ├── service.yaml
        │   └── hpa.yaml            # Horizontal Pod Autoscaler
        ├── worker/
        │   ├── deployment.yaml     # Huey async worker (DETACHED_WORKER=true)
        │   └── service.yaml
        ├── dashboard/
        │   ├── deployment.yaml     # karrio dashboard (Next.js)
        │   └── service.yaml
        ├── migrate/
        │   └── job.yaml            # Pre-upgrade migration Job (Helm hook)
        ├── ingress.yaml            # Optional ingress
        └── tests/
            └── test-connection.yaml
```

### 4.2 Components

| Component | Image | Notes |
|---|---|---|
| `api` | `ghcr.io/karrioapi/karrio:{{ .Chart.AppVersion }}` | Django + gunicorn |
| `worker` | same as api | `DETACHED_WORKER=true`, `SKIP_MIGRATIONS=true` |
| `dashboard` | `ghcr.io/karrioapi/dashboard:{{ .Chart.AppVersion }}` | Next.js |
| `migrate` (Job) | same as api | Pre-upgrade hook, runs `manage.py migrate` |

### 4.3 Dependencies (subcharts, optional)

```yaml
dependencies:
  - name: postgresql
    version: "~15.x"
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled

  - name: redis
    version: "~19.x"
    repository: https://charts.bitnami.com/bitnami
    condition: redis.enabled
```

External DB/Redis is the default (recommended for prod). Bundled is available for dev/testing.

### 4.4 Key values.yaml Sections

```yaml
# Global
global:
  imageRegistry: ghcr.io/karrioapi
  imagePullPolicy: IfNotPresent

# API
api:
  replicaCount: 2
  image:
    repository: ghcr.io/karrioapi/karrio
    tag: ""  # defaults to Chart.AppVersion
  resources:
    requests: { cpu: 250m, memory: 512Mi }
    limits: { cpu: 1000m, memory: 2Gi }
  probes:
    startup:  { failureThreshold: 30, periodSeconds: 10 }   # 300s window
    liveness: { initialDelaySeconds: 0, periodSeconds: 30 }
    readiness: { initialDelaySeconds: 0, periodSeconds: 10 }
  env:
    LANGUAGE_CODE: en
    DEBUG: "False"
    ALLOW_PRIVATE_ADDRESS: "False"
    SKIP_MIGRATIONS: "true"

# Worker
worker:
  replicaCount: 1
  env:
    DETACHED_WORKER: "true"
    SKIP_MIGRATIONS: "true"

# Dashboard
dashboard:
  replicaCount: 1
  image:
    repository: ghcr.io/karrioapi/dashboard

# Migration Job
migrate:
  enabled: true
  annotations:
    helm.sh/hook: pre-upgrade,pre-install
    helm.sh/hook-weight: "-5"
    helm.sh/hook-delete-policy: before-hook-creation,hook-succeeded

# Secrets (recommend using external secret manager in prod)
karrio:
  secretKey: ""       # REQUIRED — Django secret key
  databaseUrl: ""     # REQUIRED — postgresql://user:pass@host/db
  redisHost: ""       # REQUIRED

# Optional ingress
ingress:
  enabled: false
  className: nginx
  hosts:
    - host: karrio.example.com
      paths: [{ path: /, pathType: Prefix, service: api }]
    - host: app.karrio.example.com
      paths: [{ path: /, pathType: Prefix, service: dashboard }]

# Bundled dependencies (disabled by default)
postgresql:
  enabled: false
redis:
  enabled: false
```

### 4.5 Probe Pattern (from JTL production learnings)
```yaml
# Startup probe — generous window for Django migrations
startupProbe:
  httpGet: { path: /health, port: http }
  failureThreshold: 33
  periodSeconds: 10    # 330s max window

# Liveness — after startup succeeds
livenessProbe:
  httpGet: { path: /health, port: http }
  initialDelaySeconds: 0
  periodSeconds: 30
  failureThreshold: 3

# Readiness — controls traffic routing
readinessProbe:
  httpGet: { path: /health, port: http }
  initialDelaySeconds: 0
  periodSeconds: 10
```

---

## 5. Documentation

### 5.1 `apps/web` Docs Page

Location: `apps/web/src/app/(docs)/docs/self-hosting/kubernetes/page.mdx`

Sections:
1. Prerequisites (kubectl, helm 3, a K8s cluster)
2. Quick Start — `helm install` with minimal config
3. Configuration Reference — all values explained
4. Production Setup — external DB, Redis, ingress, TLS
5. Upgrading — migration job behavior, rollback
6. OrbStack local dev setup
7. Troubleshooting

### 5.2 `charts/karrio/README.md`

Badges (artifact hub, helm version), install commands, minimal config, links to full docs.

---

## 6. Testing Plan

### 6.1 OrbStack Local K8s

```bash
# OrbStack provides a local K8s cluster
# Verify cluster is running
kubectl cluster-info

# Add bitnami for dependencies
helm repo add bitnami https://charts.bitnami.com/bitnami
helm dependency update charts/karrio

# Install with bundled postgres + redis for local testing
helm install karrio-test ./charts/karrio \
  --set postgresql.enabled=true \
  --set redis.enabled=true \
  --set karrio.secretKey=test-secret-key-local \
  --namespace karrio-test --create-namespace

# Verify all pods come up
kubectl get pods -n karrio-test -w

# Test migration job ran
kubectl get jobs -n karrio-test

# Test API health
kubectl port-forward svc/karrio-test-api 8000:8000 -n karrio-test
curl http://localhost:8000/health

# Test dashboard
kubectl port-forward svc/karrio-test-dashboard 3000:3000 -n karrio-test
```

### 6.2 Helm Lint + Test

```bash
helm lint charts/karrio
helm template karrio charts/karrio --debug
helm test karrio-test -n karrio-test
```

---

## 7. Success Criteria

- [ ] `release/2026.1.19` branch created from `main`
- [ ] PR #993 merged into `release/2026.1.19` via GitHub PR merge
- [ ] PR #998 merged into `release/2026.1.19` via GitHub PR merge
- [ ] `helm lint charts/karrio` passes with 0 errors
- [ ] All pods (api, worker, dashboard) come up healthy in OrbStack K8s
- [ ] Migration Job runs successfully pre-install
- [ ] API health endpoint responds on port-forward
- [ ] Dashboard loads on port-forward
- [ ] Docs page added to `apps/web`
- [ ] PR opened against `main` from `release/2026.1.19`

---

## 8. Non-Goals

- Publishing to ArtifactHub (future)
- CI/CD chart testing pipeline (future)
- Multi-tenancy Helm support (future)
- ArgoCD / Flux GitOps examples (future)
