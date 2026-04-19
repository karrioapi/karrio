# Karrio Helm Chart

Deploy [Karrio](https://karrio.io) — the universal shipping API — to any Kubernetes cluster.

| Field          | Value         |
| -------------- | ------------- |
| Chart version  | `0.1.0`       |
| App version    | `2026.1.27`   |
| Kubernetes     | `>= 1.26`     |
| Helm           | `>= 3.12`     |

## Status

| Target           | Status                        |
| ---------------- | ----------------------------- |
| EKS + ALB        | Tested                        |
| Local kind       | Tested                        |
| GKE + GCE        | Example provided — user verification required |
| AKS              | Not yet verified              |

## Quickstart

```bash
# 1. Pull subchart deps (only required if you enable postgresql / redis)
helm dependency build charts/karrio

# 2. Install against an existing Postgres / Redis (recommended)
helm install karrio ./charts/karrio \
  -f charts/karrio/values-examples/eks-alb.yaml \
  --set database.host=$RDS_ENDPOINT \
  --set database.password=$DB_PASSWORD \
  --set redis.host=$ELASTICACHE_ENDPOINT \
  --set config.secretKey=$SECRET_KEY \
  --set config.jwtSecret=$JWT_SECRET \
  --set dashboardUrl=https://app.example.com \
  --set karrioPublicUrl=https://api.example.com

# 3. Run the helm test hook after install
helm test karrio
```

## Values examples

| File                                   | Use case                                                    |
| -------------------------------------- | ----------------------------------------------------------- |
| `values-examples/eks-alb.yaml`         | EKS + AWS Load Balancer Controller, external RDS/ElastiCache |
| `values-examples/gke.yaml`             | GKE + GCE Ingress + Google-managed certs (untested)          |
| `values-examples/local.yaml`           | kind / minikube with in-cluster Bitnami Postgres + Redis     |

## Required inputs

| Key                      | Required | Notes                                                                   |
| ------------------------ | -------- | ----------------------------------------------------------------------- |
| `config.secretKey`       | yes      | Django `SECRET_KEY`. Generate via `openssl rand -hex 32`.               |
| `config.jwtSecret`       | yes      | Dashboard `NEXTAUTH_SECRET`. Generate via `openssl rand -hex 32`.       |
| `database.host`          | yes      | External Postgres hostname (unless `postgresql.enabled: true`).          |
| `database.password`      | yes      | External Postgres password.                                              |
| `redis.host`             | yes      | External Redis hostname (unless `redis.enabled: true`).                  |
| `dashboardUrl`           | yes      | Public dashboard URL (e.g. `https://app.example.com`).                   |
| `karrioPublicUrl`        | yes      | Public API URL (e.g. `https://api.example.com`).                         |

### Using an existing Secret

Set `existingSecret: <name>` where the referenced Secret contains keys:

- `SECRET_KEY`
- `JWT_SECRET`
- `DATABASE_PASSWORD`

When `existingSecret` is set, the chart does not create its own Secret and `config.secretKey`, `config.jwtSecret`, and `database.password` are ignored.

**Never** commit plaintext secrets into `values.yaml`. Use `--set`, `--set-file`, sealed-secrets, External Secrets Operator, or an existing Secret.

## Environment variables rendered into the API / Worker pods

Generated from `templates/configmap.yaml` and `templates/secret.yaml`:

| Env var                         | Source                          |
| ------------------------------- | ------------------------------- |
| `DEBUG_MODE`                    | `config.debugMode`              |
| `USE_HTTPS`                     | `config.useHttps`               |
| `DETACHED_WORKER`               | `config.detachedWorker`         |
| `ENABLE_ALL_PLUGINS_BY_DEFAULT` | `config.enableAllPlugins`       |
| `DATABASE_HOST`                 | `database.host`                 |
| `DATABASE_NAME`                 | `database.name`                 |
| `DATABASE_PORT`                 | `database.port`                 |
| `DATABASE_USERNAME`             | `database.username`             |
| `DATABASE_ENGINE`               | `postgresql_psycopg2` (fixed)   |
| `REDIS_HOST`                    | `redis.host`                    |
| `REDIS_PORT`                    | `redis.port`                    |
| `SECRET_KEY`                    | Secret key `SECRET_KEY`         |
| `DATABASE_PASSWORD`             | Secret key `DATABASE_PASSWORD`  |

## Optional subcharts

Both default to `false`. Enable for dev / smoke installs only — the Bitnami defaults are not production-tuned.

| Toggle                 | Subchart (Bitnami)                                                   |
| ---------------------- | -------------------------------------------------------------------- |
| `postgresql.enabled`   | [`postgresql 15.5.38`](https://github.com/bitnami/charts/tree/main/bitnami/postgresql) |
| `redis.enabled`        | [`redis 20.1.7`](https://github.com/bitnami/charts/tree/main/bitnami/redis)             |

## Autoscaling

- **API** — CPU-based HPA via `api.autoscaling.{enabled,minReplicas,maxReplicas,targetCPUUtilizationPercentage}` (see `templates/api/hpa.yaml`).
- **Worker** — Gated behind `worker.autoscaling.enabled`. Requires a custom metric (e.g. `karrio_queue_depth` exposed via Prometheus Adapter / KEDA). Provide `worker.autoscaling.targetMetricName` + `worker.autoscaling.targetValue`, or fall back to `targetCPUUtilizationPercentage` for installs without the custom metric. See `templates/worker/hpa.yaml`.

## Ingress

Configure `ingress.className` for your platform:

| Platform                      | `className` |
| ----------------------------- | ----------- |
| AWS Load Balancer Controller  | `alb`       |
| GCE Ingress                   | `gce`       |
| ingress-nginx                 | `nginx`     |
| Traefik                       | `traefik`   |

Put platform-specific annotations under `ingress.annotations`. See the `values-examples/` files for working configurations.

## Helm test

`helm test <release>` runs the Pod in `templates/tests/connection.yaml`, which curls `/v1/references` on the API service. Exit 0 = pass.

```bash
helm install karrio ./charts/karrio -f values-examples/local.yaml
helm test karrio
```

## Troubleshooting

| Symptom                                            | Check                                                                                 |
| -------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `helm lint` warns about missing dependencies       | Run `helm dependency build charts/karrio`                                             |
| API pods crash with `SECRET_KEY must not be empty` | `config.secretKey` or the `existingSecret` `SECRET_KEY` key is unset                  |
| Dashboard loads but auth fails                     | `dashboardUrl` / `karrioPublicUrl` / `config.jwtSecret` do not match the deployed URL |
| Worker HPA stuck in `ScalingActive=False`          | Custom metric source (Prometheus Adapter / KEDA) not installed                        |

## Uninstall

```bash
helm uninstall karrio
```

The chart-managed Secret is deleted automatically; any `existingSecret` you referenced is left intact.
