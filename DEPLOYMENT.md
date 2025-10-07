# JTL Shipping Platform - Custom Deployment Guide

This document describes the custom deployment setup for the JTL Shipping Platform.

## Overview

The JTL Shipping Platform is built on top of Karrio and includes custom deployment configurations for containerized deployments.

## Directory Structure

```
.
├── docker/                         # Docker configuration
│   ├── server/                     # Server Docker setup
│   │   ├── Dockerfile             # Server image
│   │   ├── entrypoint             # Server startup script
│   │   └── worker                 # Background worker script
│   ├── dashboard/                 # Dashboard Docker setup
│   │   ├── Dockerfile             # Dashboard image
│   │   └── entrypoint             # Dashboard startup script
│   ├── docker-compose.yml         # Deployment configuration
│   ├── Caddyfile                  # Reverse proxy config
│   └── README.md                  # Docker documentation
├── bin/                           # Build and deployment scripts
│   ├── deploy-jtl                 # Main deployment script
│   ├── build-jtl-server-image     # Server image build script
│   ├── build-jtl-dashboard-image  # Dashboard image build script
│   ├── update-version             # Version update script
│   ├── update-package-versions    # Package version sync script
│   └── update-source-version      # Source requirements generator
├── .github/workflows/             # CI/CD workflows
│   └── jtl-build.yml             # Docker image build workflow
├── requirements.build.txt         # Build requirements (editable installs)
├── requirements.source.txt        # Source requirements (file:// paths)
└── VERSION                        # Version file
```

## Version Management

The platform version is managed centrally in the `VERSION` file at the root of the repository.

### Update Version

```bash
# Update from old version to new version
./bin/update-version 2025.5rc25 2025.5rc26
```

This updates:
- `VERSION`
- `docker/docker-compose.yml`
- `bin/deploy-jtl`
- `.github/workflows/jtl-build.yml`

### Update Package Versions

Sync all Python package versions with the central version:

```bash
./bin/update-package-versions [version]
```

### Generate Source Requirements

Convert build requirements to source requirements:

```bash
./bin/update-source-version
```

## Building Docker Images

### Server Image

Build the server image locally:

```bash
./bin/build-jtl-server-image <version>
```

Environment variables:
- `JTL_IMAGE`: Image name (default: `ghcr.io/jtl/shipping-platform-server`)
- `REQUIREMENTS`: Requirements file (default: `./requirements.build.txt`)
- `SOURCE`: Source repository URL

Example:
```bash
JTL_IMAGE=my-registry/jtl-server ./bin/build-jtl-server-image 2025.5rc25
```

### Dashboard Image

Build the dashboard image locally:

```bash
./bin/build-jtl-dashboard-image <version>
```

Environment variables:
- `JTL_IMAGE`: Image name (default: `ghcr.io/jtl/shipping-platform-dashboard`)
- `SOURCE`: Source repository URL

## Deployment

### Automated Deployment

Use the deployment script for a guided setup:

```bash
./bin/deploy-jtl [version] [domain] [staging]
```

Arguments:
- `version`: Version to deploy (optional, default: 2025.5rc25)
- `domain`: Domain name (optional, will prompt if not provided)
- `staging`: Any value to use Let's Encrypt staging (optional)

Example:
```bash
./bin/deploy-jtl 2025.5rc25 jtl.example.com
```

### Manual Deployment

1. **Create environment file**:
   ```bash
   cd docker
   cat > .env <<EOF
   JTL_TAG=2025.5rc25
   SECRET_KEY=$(head -c 28 /dev/urandom | sha224sum -b | head -c 56)
   JWT_SECRET=$(head -c 28 /dev/urandom | sha224sum -b | head -c 56)
   DOMAIN=your-domain.com
   DASHBOARD_URL=https://app.your-domain.com
   KARRIO_PUBLIC_URL=https://api.your-domain.com
   EOF
   ```

2. **Configure Caddyfile** (update domain):
   ```bash
   # Edit docker/Caddyfile with your domain
   ```

3. **Start services**:
   ```bash
   docker compose up -d
   ```

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/jtl-build.yml`) automatically builds and pushes Docker images when:
- Changes are pushed to the `main` branch
- The `VERSION` file is modified
- Manually triggered via workflow dispatch

### Workflow Jobs

1. **changes**: Detects version file changes
2. **jtl-server-build**: Builds and pushes server image
3. **jtl-dashboard-build**: Builds and pushes dashboard image

### Required Secrets

Configure these in your GitHub repository:
- `GITHUB_TOKEN`: Automatically provided by GitHub Actions

### Image Registry

Images are pushed to GitHub Container Registry (ghcr.io):
- Server: `ghcr.io/jtl/shipping-platform-server:<version>`
- Dashboard: `ghcr.io/jtl/shipping-platform-dashboard:<version>`

## Requirements Files

### requirements.build.txt

Used for building Docker images. Contains editable installs (`-e ./path/to/package`) that reference local source code.

### requirements.source.txt

Used for local development. Contains file:// URLs that reference local packages.

These files are synchronized and should reference the same packages.

## Environment Variables

### Server Environment

- `DEBUG_MODE`: Enable debug mode (default: False)
- `USE_HTTPS`: Enable HTTPS (default: False)
- `SECRET_KEY`: Django secret key (required)
- `DATABASE_HOST`: PostgreSQL host
- `DATABASE_NAME`: Database name
- `DATABASE_USERNAME`: Database username
- `DATABASE_PASSWORD`: Database password
- `REDIS_HOST`: Redis host
- `REDIS_PORT`: Redis port
- `DETACHED_WORKER`: Run worker as separate container (default: True)

### Dashboard Environment

The dashboard is built with **TanStack Start** (React Router v7) and **Vite**.

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

## Maintenance

### View Logs

```bash
cd docker
docker compose logs -f [service]
```

### Database Migrations

Migrations run automatically on container startup. To run manually:

```bash
docker compose exec api karrio migrate
```

### Backup Database

```bash
docker compose exec db pg_dump -U postgres db > backup.sql
```

### Restore Database

```bash
docker compose exec -T db psql -U postgres db < backup.sql
```

## Troubleshooting

### Container Won't Start

Check logs:
```bash
docker compose logs [service]
```

### Database Connection Issues

1. Check if database is running:
   ```bash
   docker compose ps db
   ```

2. Verify connection settings in `.env`

3. Check database logs:
   ```bash
   docker compose logs db
   ```

### Worker Not Processing Jobs

1. Check worker logs:
   ```bash
   docker compose logs worker
   ```

2. Verify Redis connection:
   ```bash
   docker compose exec api redis-cli -h redis ping
   ```

### SSL Certificate Issues

1. Check Caddy logs:
   ```bash
   docker compose logs caddy
   ```

2. Verify DNS records point to your server

3. Check firewall allows ports 80 and 443

## Support

For issues and questions:
- Check the [docker/README.md](docker/README.md) for Docker-specific information
- Review the Karrio documentation at [https://docs.karrio.io](https://docs.karrio.io)
- Contact the JTL support team

## License

Refer to the main LICENSE file in the repository root.
