# JTL Shipping Platform - Local Development with Docker

This guide covers running the JTL Shipping Platform locally using Docker Compose.

## Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 4GB+ RAM

### 1. Set Up Environment

Copy the sample environment file:

```bash
cp .env.sample .env
```

Edit `.env` and update any values as needed. The defaults are suitable for local development.

### 2. Start Services

```bash
docker compose up -d
```

This will start:
- **API** (`jtl.api`): http://localhost:5002
- **Dashboard** (`jtl.dashboard`): http://localhost:3102
- **Worker** (`jtl.worker`): Background task processor
- **Database** (`jtl.db`): PostgreSQL on port 5432
- **Redis** (`jtl.redis`): Redis on port 6379
- **Mail** (`jtl.mail`): MailDev for email testing on http://localhost:1080

### 3. Access the Platform

- **Dashboard**: http://localhost:3102
- **API**: http://localhost:5002
- **API Docs**: http://localhost:5002/docs
- **MailDev**: http://localhost:1080 (for viewing test emails)

### 4. Stop Services

```bash
docker compose down
```

To also remove volumes (database data):

```bash
docker compose down -v
```

## Configuration

### Environment Variables

All configuration is done through the `.env` file. Key variables:

**Server:**
- `JTL_TAG`: Docker image version (default: 2025.5rc25)
- `JTL_HTTP_PORT`: API server port (default: 5002)
- `SECRET_KEY`: Django secret key
- `DEBUG_MODE`: Enable debug mode (default: True for local dev)

**Database:**
- `DATABASE_HOST`: PostgreSQL host (default: db)
- `DATABASE_NAME`: Database name (default: db)
- `DATABASE_USERNAME`: Database user (default: postgres)
- `DATABASE_PASSWORD`: Database password (default: postgres)

**Redis:**
- `REDIS_HOST`: Redis host (default: redis)
- `REDIS_PORT`: Redis port (default: 6379)

**Dashboard:**
- `DASHBOARD_PORT`: Dashboard port (default: 3102)
- `DASHBOARD_URL`: Dashboard URL (default: http://localhost:3102)
- `KARRIO_PUBLIC_URL`: API public URL (default: http://localhost:5002)

**Email (MailDev for local development):**
- `EMAIL_HOST`: SMTP host (default: maildev)
- `EMAIL_PORT`: SMTP port (default: 1025)
- `EMAIL_USE_TLS`: Use TLS (default: false)

### Using External Database/Redis

If you want to use an external PostgreSQL or Redis instance:

1. Update the connection details in `.env`
2. Comment out the `db` and/or `redis` services in `docker-compose.yml`

## Common Tasks

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f api
docker compose logs -f dashboard
docker compose logs -f worker
```

### Restart Services

```bash
# All services
docker compose restart

# Specific service
docker compose restart api
```

### Execute Commands in Containers

```bash
# Django shell
docker compose exec api karrio shell

# Run migrations
docker compose exec api karrio migrate

# Create superuser
docker compose exec api karrio createsuperuser
```

### Database Access

```bash
# PostgreSQL shell
docker compose exec db psql -U postgres -d db
```

### Reset Database

```bash
# Stop services
docker compose down

# Remove volumes
docker volume rm shipping-platform_postgres-data

# Start again
docker compose up -d
```

## Development Workflow

### Working with Code Changes

The Docker images are pre-built. For local development with code changes:

1. **Build custom images** with your changes:
   ```bash
   ./bin/build-jtl-server-image dev
   ./bin/build-jtl-dashboard-image dev
   ```

2. **Update docker-compose.yml** to use local images:
   ```yaml
   services:
     api:
       image: ghcr.io/jtlshipping/server:dev
     worker:
       image: ghcr.io/jtlshipping/server:dev
     dashboard:
       image: ghcr.io/jtlshipping/dashboard:dev
   ```

3. **Restart services**:
   ```bash
   docker compose down
   docker compose up -d
   ```

### Plugin Development

Plugins are mounted from `./karrio/plugins` by default. To use custom plugins:

1. Set `JTL_PLUGINS` in `.env`:
   ```
   JTL_PLUGINS=./custom-plugins
   ```

2. Restart the services:
   ```bash
   docker compose restart api worker
   ```

## Troubleshooting

### Services Won't Start

Check logs:
```bash
docker compose logs
```

### Database Connection Issues

1. Ensure database is running:
   ```bash
   docker compose ps db
   ```

2. Check database logs:
   ```bash
   docker compose logs db
   ```

### Port Already in Use

If ports are already in use, update them in `.env`:
```
JTL_HTTP_PORT=5003
DASHBOARD_PORT=3103
DATABASE_PORT=5433
REDIS_PORT=6380
```

### Reset Everything

```bash
# Stop all services
docker compose down -v

# Remove all JTL containers
docker ps -a | grep jtl | awk '{print $1}' | xargs docker rm -f

# Remove all JTL volumes
docker volume ls | grep shipping-platform | awk '{print $2}' | xargs docker volume rm

# Start fresh
docker compose up -d
```

## Health Checks

The API service has a health check configured. Check status:

```bash
docker compose ps api
```

Healthy status shows `healthy` in the STATUS column.

## OpenTelemetry (Optional)

To enable distributed tracing and metrics:

1. Uncomment and configure in `.env`:
   ```
   OTEL_ENABLED=true
   OTEL_SERVICE_NAME=jtl-api
   OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
   OTEL_EXPORTER_OTLP_PROTOCOL=grpc
   ```

2. Ensure you have an OTLP collector running (Jaeger, Zipkin, etc.)

## Additional Resources

- [Deployment Guide](DEPLOYMENT.md) - Production deployment
- [Docker Documentation](docker/README.md) - Docker-specific details
- [Karrio Documentation](https://docs.karrio.io) - Karrio platform docs

## Support

For issues:
1. Check logs: `docker compose logs`
2. Review this guide's Troubleshooting section
3. Check the main README.md
4. Contact JTL support
