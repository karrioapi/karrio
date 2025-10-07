# JTL Shipping Platform Docker Setup

This directory contains the Docker configuration and deployment files for the JTL Shipping Platform.

## Directory Structure

```
docker/
├── server/
│   ├── Dockerfile       # Server Docker image
│   ├── entrypoint       # Server entrypoint script
│   └── worker           # Background worker script
├── dashboard/
│   ├── Dockerfile       # Dashboard Docker image
│   └── entrypoint       # Dashboard entrypoint script
├── docker-compose.yml   # Docker Compose configuration
├── Caddyfile           # Caddy reverse proxy configuration
└── README.md           # This file
```

## Services

The platform consists of the following services:

- **api**: The main API server (Karrio server)
- **worker**: Background task worker
- **dashboard**: TanStack Start (React Router v7) dashboard application with Vite
- **caddy**: Reverse proxy for SSL/TLS termination
- **db**: PostgreSQL database
- **redis**: Redis cache and message broker

## Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 4GB+ RAM

### Environment Variables

Create a `.env` file in the `docker` directory with the following variables:

```bash
JTL_TAG=2025.5rc25
DOMAIN=your-domain.com
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret
DASHBOARD_URL=https://app.your-domain.com
KARRIO_PUBLIC_URL=https://api.your-domain.com
```

### Deployment

Use the deployment script:

```bash
./bin/deploy-jtl [version] [domain]
```

Or manually:

```bash
cd docker
docker compose up -d
```

## Building Images

### Server Image

```bash
./bin/build-jtl-server-image <version>
```

### Dashboard Image

The dashboard is built with TanStack Start (React Router v7) and Vite.

```bash
./bin/build-jtl-dashboard-image <version>
```

## Configuration

### Environment Variables

**Server Environment:**
- `JTL_TAG`: Version tag for the Docker images
- `SECRET_KEY`: Django secret key
- `JWT_SECRET`: JWT signing secret
- `DATABASE_HOST`: PostgreSQL host (default: db)
- `DATABASE_NAME`: Database name (default: db)
- `DATABASE_USERNAME`: Database user (default: postgres)
- `DATABASE_PASSWORD`: Database password (default: postgres)
- `REDIS_HOST`: Redis host (default: redis)
- `REDIS_PORT`: Redis port (default: 6379)

**Dashboard Environment:**
- `NODE_ENV`: Node environment (default: production)
- `DASHBOARD_PORT`: Dashboard port (default: 3102)
- `DASHBOARD_URL`: Dashboard public URL
- `KARRIO_PUBLIC_URL`: API public URL
- `VITE_KARRIO_API`: Karrio API endpoint (Vite env var)
- `VITE_KARRIO_OAUTH_CLIENT_ID`: OAuth client ID (Vite env var)
- `VITE_KARRIO_OAUTH_CLIENT_SECRET`: OAuth client secret (Vite env var)
- `VITE_KARRIO_OAUTH_REDIRECT_URI`: OAuth redirect URI (Vite env var)
- `VITE_JTL_CLIENT_ID`: JTL client ID (Vite env var)
- `VITE_JTL_CLIENT_SECRET`: JTL client secret (Vite env var)
- `JTL_CLIENT_ID`: JTL client ID
- `JTL_CLIENT_SECRET`: JTL client secret
- `OAUTH_CLIENT_ID`: OAuth client ID
- `OAUTH_CLIENT_SECRET`: OAuth client secret

### Volumes

- `jtl-static`: Static files for the API server
- `postgres-data`: PostgreSQL data
- `redis-data`: Redis data
- `caddy-data`: Caddy certificates and configuration

## Maintenance

### View Logs

```bash
cd docker
docker compose logs -f [service-name]
```

### Stop Services

```bash
cd docker
docker compose stop
```

### Start Services

```bash
cd docker
docker compose start
```

### Restart Services

```bash
cd docker
docker compose restart [service-name]
```

### Update to New Version

1. Update the `JTL_TAG` in `.env`
2. Pull new images: `docker compose pull`
3. Restart services: `docker compose up -d`

## Troubleshooting

### Database Connection Issues

Check if the database is running:
```bash
docker compose ps db
docker compose logs db
```

### Worker Not Processing Jobs

Check worker logs:
```bash
docker compose logs worker
```

### SSL/TLS Certificate Issues

Check Caddy logs:
```bash
docker compose logs caddy
```

## Support

For issues and questions, please contact the JTL support team.
