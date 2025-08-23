# Karrio Docker Configuration

This directory contains Docker configurations for running Karrio in various deployment scenarios.

## Core Docker Compose Files

| File | Purpose | Usage |
|------|---------|--------|
| `docker-compose.yml` | Main Karrio stack (API, Dashboard, Database, Redis) | Base configuration for all deployments |
| `docker-compose.hobby.yml` | Hobby deployment with Caddy reverse proxy | Production-ready single-server setup |
| `docker-compose.insiders.yml` | Karrio Insiders edition configuration | Enterprise features and extensions |
| `docker-compose.insiders.local.yml` | Local development for Insiders | Development environment for enterprise features |

## Service Directories

| Directory | Contents |
|-----------|----------|
| `api/` | API server Dockerfile, entrypoint, and worker script |
| `dashboard/` | Dashboard Dockerfile and entrypoint |
| `insiders/` | Insiders-specific Docker configurations |
| `nginx/` | Nginx reverse proxy configurations |
| `observability/` | OpenTelemetry and monitoring stack configurations |

## Development Files

| File | Purpose |
|------|---------|
| `dev.Dockerfile` | Development container with all tools |
| `dev.tool.Dockerfile` | Development tools and utilities |

## Quick Start

### Basic Development Setup
```bash
# Start core Karrio services
docker-compose up -d
```

### Production Deployment
```bash
# Start with Caddy reverse proxy for SSL
docker-compose -f docker-compose.yml -f docker-compose.hobby.yml up -d
```

### With Monitoring
```bash
# Start with complete observability stack
docker-compose -f docker-compose.yml -f observability/docker-compose.observability.yml up -d
```

## Monitoring and Observability

For detailed monitoring configurations including OpenTelemetry, Prometheus, Grafana, and Jaeger, see the [observability README](./observability/README.md).

## Service URLs (Default)

- **Dashboard**: http://localhost:3002
- **API**: http://localhost:5002  
- **Database**: localhost:5432
- **Redis**: localhost:6379
- **Grafana**: http://localhost:3000 (when using observability stack)
- **Prometheus**: http://localhost:9090 (when using observability stack)
- **Jaeger**: http://localhost:16686 (when using tracing)

## Environment Configuration

Key environment variables are defined in the compose files. For custom configurations, create a `.env` file in the project root or override specific variables as needed.

Common variables:
- `KARRIO_TAG`: Docker image version to use
- `DATABASE_*`: Database connection settings  
- `REDIS_*`: Redis connection settings
- `OTEL_*`: OpenTelemetry configuration (see observability README)