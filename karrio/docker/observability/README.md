# Karrio Observability Stack

This folder contains OpenTelemetry and observability configurations for monitoring Karrio applications.

## Quick Start Options

### 1. Jaeger Tracing (Simple)
```bash
# Start Karrio with Jaeger tracing
docker-compose -f ../docker-compose.yml -f docker-compose.otel.yml up -d
```
- **Jaeger UI**: http://localhost:16686
- **What you get**: Distributed tracing across API and worker services

### 2. Prometheus Metrics (Intermediate) 
```bash
# Start standalone Prometheus + OTEL Collector for testing
docker-compose -f docker-compose.prometheus-standalone.yml up -d

# Or integrate with full Karrio stack
docker-compose -f ../docker-compose.yml -f docker-compose.prometheus.yml up -d
```
- **Prometheus**: http://localhost:9090
- **What you get**: Custom metrics collection and storage

### 3. Complete Observability (Advanced)
```bash
# Full stack: Grafana + Prometheus + Tempo + Loki + OTEL Collector
docker-compose -f ../docker-compose.yml -f docker-compose.observability.yml up -d
```
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Tempo**: http://localhost:3200
- **Loki**: http://localhost:3100
- **What you get**: Complete observability with unified dashboards

## Configuration Files

| File | Purpose |
|------|---------|
| `docker-compose.otel.yml` | Basic Jaeger tracing setup |
| `docker-compose.prometheus.yml` | Prometheus metrics integration |
| `docker-compose.prometheus-standalone.yml` | Standalone Prometheus testing |
| `docker-compose.observability.yml` | Complete observability stack |
| `otel-collector-config.yaml` | OTEL Collector for Jaeger |
| `otel-collector-prometheus.yaml` | OTEL Collector for Prometheus |
| `prometheus.yml` | Prometheus scraping configuration |
| `tempo.yaml` | Tempo tracing backend configuration |
| `grafana/` | Grafana dashboards and data sources |

## Environment Variables

Enable observability in your Karrio application with these environment variables:

```bash
# Required
OTEL_ENABLED=true
OTEL_SERVICE_NAME=karrio-api
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317

# Optional
OTEL_EXPORTER_OTLP_PROTOCOL=grpc
OTEL_ENVIRONMENT=development
OTEL_RESOURCE_ATTRIBUTES="deployment.environment=docker,service.namespace=karrio"
```

## Development Tips

1. **Start small**: Begin with Jaeger tracing to understand request flows
2. **Add metrics**: Use Prometheus setup for performance monitoring  
3. **Full stack**: Deploy complete observability for production-like monitoring
4. **Custom metrics**: Add application-specific metrics in your code

## Troubleshooting

- Check OTEL Collector logs: `docker-compose logs otel-collector`
- Verify endpoints are accessible: `curl http://localhost:4317` (should refuse connection - expected)
- Test metrics export: `curl http://localhost:8889/metrics` (when using Prometheus setup)