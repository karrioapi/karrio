# JTL Shipping Platform

A comprehensive shipping and logistics platform built on top of Karrio, providing enterprise-grade shipping management, carrier integrations, and multi-tenant capabilities.

## Overview

The JTL Shipping Platform is a monorepo-based application that combines a Python/Django backend (Karrio API) with multiple Next.js and React frontends. The platform enables businesses to manage shipping operations, integrate with multiple carriers, track shipments, and provide customer-facing shipping solutions.

### Key Features

- **Multi-Carrier Support** - Integrate with major shipping carriers worldwide
- **Shipment Management** - Create, track, and manage shipments from a unified interface
- **Multi-Tenancy** - Support multiple organizations with isolated data
- **Plugin Architecture** - Extensible system for custom carrier integrations
- **Analytics Dashboard** - Real-time insights into shipping operations
- **Enterprise Auth** - OIDC/OAuth2 authentication support
- **REST API** - Comprehensive API for integration with existing systems
- **GraphQL management API** - Comprehensive API for custom integration

## Architecture

The platform consists of three main layers:

### Backend (Python/Django)

- **Karrio API Server** - Core shipping logic, carrier integrations, and database management
- **GraphQL API** - Modern API layer for flexible data queries
- **Background Workers** - Asynchronous task processing for shipments and tracking
- **Admin Portal** - Django admin for platform management

### Frontend Applications

- **JTL Dashboard** (`@jtl/dashboard`) - Main administrative interface (React + Vite + TanStack Start)

### Shared Packages

- `@karrio/hooks` - Shared React hooks
- `@karrio/ui` - Reusable UI components
- `@karrio/lib` - Common utilities and helpers
- `@karrio/types` - TypeScript type definitions
- `@karrio/core` - Core frontend logic
- `@karrio/admin` - Admin panel components
- `@karrio/app-store` - Plugin marketplace components

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** >= 18.0.0 (we use v18 or higher)
- **npm** >= 11.0.0 (included with Node.js)
- **Python** >= 3.11
- **pip** (Python package installer)
- **Git** (for version control)

### Optional but Recommended

- **PostgreSQL** >= 16 (for production; SQLite used in development)
- **Redis** >= 6.0 (for caching and background jobs)
- **Maildev** (for local email testing, auto-installed via npx)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd shipping-platform
```

### 2. Environment Setup

Copy the sample environment file and configure it:

```bash
cp .env.sample .env
```

Edit `.env` to customize your configuration. Key settings include:

```bash
# Core Settings
DEBUG_MODE=True
SECRET_KEY="your-secret-key-here"

# Database (SQLite for development)
DATABASE_NAME=db.sqlite3

# Authentication
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=demo
ALLOW_SIGNUP=True

# Workers
DETACHED_WORKER=True
WORKER_IMMEDIATE_MODE=True
```

### 3. Backend Setup

The platform uses a custom installation script for the backend:

```bash
# Run the installation script (creates virtual environment and installs dependencies)
./bin/install-dev
```

This script will:

- Create a Python virtual environment in `.venv/karrio`
- Install all Python dependencies
- Run database migrations
- Create a superuser account

### 4. Frontend Setup

Install Node.js dependencies for all workspaces:

```bash
npm install
```

This will install dependencies for:

- Root workspace
- All apps in `apps/`
- All packages in `packages/`
- All Karrio apps in `karrio/apps/`
- All Karrio packages in `karrio/packages/`

## Running the Application

### Quick Start (All Services)

The easiest way to run the entire platform is using the development script:

```bash
./bin/dev up
```

This will start:

- **API Server** on `http://localhost:5002`
- **JTL Dashboard** on `http://localhost:3102`
- **Maildev** (email testing) on `http://localhost:1080`

Access points:

- **API**: http://localhost:5002
- **Admin Panel**: http://localhost:5002/admin
- **JTL Dashboard**: http://localhost:3102
- **Maildev**: http://localhost:1080

### Selective Service Startup

Run specific services only:

```bash
# API server only
./bin/dev up --api-only

# Dashboard only
./bin/dev up --frontend-only

# Skip specific services
./bin/dev up --no-maildev
./bin/dev up --no-api

# Detached mode (start services and exit)
./bin/dev up --detach
```

### Stopping Services

```bash
./bin/dev down
```

### Manual Service Control

If you prefer to run services individually:

#### Backend API

```bash
# Activate virtual environment
source .venv/karrio/bin/activate

# Run the server
karrio runserver
```

#### JTL Dashboard

```bash
npm run dev -w @jtl/dashboard
```

## Available Commands

### Root Level

```bash
# Run all apps in development mode
npm run dev

# Build all apps
npm run build

# Lint all code
npm run lint

# Type checking across all workspaces
npm run check-types

# Format code with Prettier
npm run format
```

### Individual Workspace Commands

```bash
# Run specific workspace
npm run dev -w @jtl/dashboard

# Build specific workspace
npm run build -w @jtl/dashboard

# Lint specific workspace
npm run lint -w @jtl/dashboard
```

### Turbo Commands

The project uses Turborepo for build orchestration:

```bash
# Build with caching
turbo build

# Run specific tasks
turbo lint
turbo check-types

# Filter by workspace
turbo build --filter=@jtl/dashboard
turbo dev --filter=@jtl/dashboard
```

## Project Structure

```txt
shipping-platform/
├── apps/                           # JTL Applications
│   └── dashboard/                  # JTL Dashboard (React + Vite + TanStack Start)
├── packages/                       # JTL Shared Packages
│   ├── eslint-config/             # ESLint configurations
│   └── typescript-config/         # TypeScript configurations
├── karrio/                        # Karrio Backend (Git Subtree)
│   ├── apps/
│   │   └── api/                   # Karrio API server (Django)
│   ├── modules/                   # Karrio core modules
│   │   ├── core/                  # Core functionality
│   │   ├── manager/               # Shipment management
│   │   ├── pricing/               # Pricing engine
│   │   ├── documents/             # Document generation
│   │   └── connectors/            # Carrier integrations
│   └── packages/                  # Karrio shared packages
│       ├── hooks/                 # React hooks
│       ├── lib/                   # Utilities
│       ├── types/                 # TypeScript types
│       └── ui/                    # UI components
├── karrio-insiders/               # Karrio Insiders (Git Subtree)
│   └── modules/                   # Premium/private modules
│       ├── apps/                  # Apps module
│       ├── admin/                 # Admin enhancements
│       ├── audit/                 # Audit logging
│       ├── automation/            # Workflow automation
│       └── orgs/                  # Multi-tenancy
├── modules/                       # Custom Python Modules
│   └── shipping/                  # Custom shipping module
│       ├── models.py              # Database models
│       ├── serializers/           # API serializers
│       ├── views.py               # API views
│       └── router.py              # URL routing
├── docker/                        # Docker deployment files
│   ├── server/                    # Server Dockerfile & scripts
│   ├── dashboard/                 # Dashboard Dockerfile & scripts
│   ├── docker-compose.yml         # Local development stack
│   └── Caddyfile                  # Reverse proxy config
├── bin/                           # Development & Deployment Scripts
│   ├── dev                        # Development environment manager
│   ├── install-dev                # Installation script
│   ├── deploy-jtl                 # Production deployment script
│   ├── build-jtl-server-image     # Build server Docker image
│   └── build-jtl-dashboard-image  # Build dashboard Docker image
├── .env.sample                    # Sample environment configuration
├── package.json                   # Root package configuration
├── turbo.json                     # Turborepo configuration
├── requirements.build.txt         # Python build dependencies
└── VERSION                        # Version tracking
```

## Development Workflow

### Adding New Features

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Start development environment**
   ```bash
   ./bin/dev up
   ```

3. **Make your changes** in the appropriate workspace

4. **Test your changes**
   ```bash
   npm run lint
   npm run check-types
   npm run build
   ```

5. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: your feature description"
   git push origin feature/your-feature-name
   ```

### Working with the Backend

```bash
# Activate virtual environment
source .venv/karrio/bin/activate

# Create database migrations
karrio makemigrations

# Apply migrations
karrio migrate

# Create superuser
karrio createsuperuser

# Open Django shell
karrio shell

# Run tests
pytest
```

### Working with Frontend

```bash
# Add dependency to specific workspace
npm install <package> -w @jtl/dashboard

# Run development server with hot reload
npm run dev -w @jtl/dashboard

# Build for production
npm run build -w @jtl/dashboard

# Type check
npm run check-types -w @jtl/dashboard
```

## Database Management

### SQLite (Development)

By default, the platform uses SQLite for development:

```bash
# Database file location
ls db.sqlite3

# View with sqlite3
sqlite3 db.sqlite3
```

### PostgreSQL (Production)

To use PostgreSQL, update your `.env`:

```bash
DATABASE_ENGINE=postgresql
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=yourpassword
DATABASE_NAME=karrio_db
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

Then run migrations:

```bash
source .venv/karrio/bin/activate
karrio migrate
```

## Managing Git Subtrees

The project uses git subtrees to include upstream Karrio code. The `karrio/` and `insiders/` directories are managed as subtrees from their respective upstream repositories.

### Understanding Subtrees

Git subtrees allow us to:

- Include external repositories as subdirectories
- Track upstream changes while maintaining our own modifications
- Keep all code in a single repository for easier development

### Updating Subtrees

To pull the latest changes from upstream Karrio repositories:

```bash
# Update both karrio and insiders subtrees
./bin/update-subtrees

# Update only karrio
./bin/update-subtrees --karrio-only

# Update only insiders
./bin/update-subtrees --insiders-only

# Update from a specific branch
./bin/update-subtrees --branch develop
```

### Manual Subtree Operations

If you need to perform manual subtree operations:

```bash
# Add a new subtree (already done in this repo)
git subtree add --prefix=karrio karrio main --squash

# Pull updates from upstream
git subtree pull --prefix=karrio karrio main --squash
git subtree pull --prefix=insiders insiders main --squash

# Push local changes to upstream (if you have write access)
git subtree push --prefix=karrio karrio main
```

### Subtree Remotes

The project has two git remotes for subtrees:

```bash
# View configured remotes
git remote -v

# karrio -> git@github.com:jtlshipping/karrio.git
# insiders -> git@github.com:jtlshipping/karrio-insiders.git
```

### Handling Merge Conflicts

If you encounter merge conflicts when updating subtrees:

1. **Review the conflicts**

   ```bash
   git status
   ```

2. **Resolve conflicts manually** in the affected files

3. **Stage the resolved files**

   ```bash
   git add <resolved-files>
   ```

4. **Complete the merge**
   ```bash
   git commit
   ```

## Email Testing

The platform includes Maildev for local email testing:

1. **Access Maildev**: http://localhost:1080
2. **View sent emails** from the application
3. **Test email notifications** without sending real emails

Configure email in `.env`:

```bash
EMAIL_PORT=1025
EMAIL_USE_TLS=false
EMAIL_HOST=localhost
EMAIL_HOST_USER=admin@example.com
```

## Environment Variables

Key environment variables you can configure:

| Variable                        | Default             | Description                |
| ------------------------------- | ------------------- | -------------------------- |
| `DEBUG_MODE`                    | `True`              | Enable debug mode          |
| `ADMIN_DASHBOARD`               | `True`              | Enable admin dashboard     |
| `ALLOWED_HOSTS`                 | `*,localhost`       | Allowed hosts              |
| `SECRET_KEY`                    | (sample key)        | Django secret key          |
| `DATABASE_NAME`                 | `db.sqlite3`        | Database name              |
| `ADMIN_EMAIL`                   | `admin@example.com` | Admin email                |
| `ADMIN_PASSWORD`                | `demo`              | Admin password             |
| `ALLOW_SIGNUP`                  | `True`              | Allow user registration    |
| `DETACHED_WORKER`               | `True`              | Run workers in background  |
| `ENABLE_ALL_PLUGINS_BY_DEFAULT` | `True`              | Enable all carrier plugins |

## Troubleshooting

### Port Already in Use

If you see port conflicts:

```bash
# Kill processes on specific ports
lsof -ti:5002 | xargs kill -9  # API
lsof -ti:3102 | xargs kill -9  # Foundation
lsof -ti:3002 | xargs kill -9  # Dashboard
lsof -ti:1080 | xargs kill -9  # Maildev
```

### Python Virtual Environment Issues

```bash
# Remove and recreate virtual environment
rm -rf .venv/karrio
./bin/install-dev
```

### Node Modules Issues

```bash
# Clean install
rm -rf node_modules
rm -rf apps/*/node_modules
rm -rf karrio/apps/*/node_modules
rm package-lock.json
npm install
```

### Database Migration Issues

```bash
source .venv/karrio/bin/activate

# Reset migrations (caution: destroys data)
rm db.sqlite3
karrio migrate

# Or create fresh migrations
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
karrio makemigrations
karrio migrate
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

[Your License Here]

## Support

For support, email [your-email] or open an issue in the repository.

## Production Deployment

### Prerequisites for Deployment

- **Server**: Ubuntu 22.04+ with minimum 4GB RAM (8GB recommended)
- **Domain**: DNS A records configured for `api.yourdomain.com` and `app.yourdomain.com`
- **GitHub PAT**: Personal Access Token with `read:packages` scope to pull Docker images

### Setting Up GitHub Personal Access Token (PAT)

The deployment pulls private Docker images from GitHub Container Registry, so you need a PAT:

1. **Go to GitHub Settings**
   - Visit: https://github.com/settings/tokens
   - Or: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)

2. **Generate New Token**
   - Click "Generate new token (classic)"
   - Give it a name: e.g., "JTL Deployment"
   - Select expiration: "No expiration" or custom period
   - **Required scope**: Check `read:packages` (allows downloading Docker images)
   - Click "Generate token"

3. **Save Your Token**
   - **Copy the token immediately** - you won't see it again!
   - Store it securely (password manager, secure notes, etc.)
   - Example token format: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

4. **Use the Token**
   - The deployment script will prompt you for it
   - Or set it as an environment variable: `export GITHUB_TOKEN=ghp_your_token_here`

**Note**: If you lose your token, you'll need to generate a new one.

### One-Line Cloud Deployment

Deploy to Digital Ocean, AWS, or any Ubuntu server:

```bash
export GITHUB_TOKEN=ghp_your_token_here
/bin/bash -c "$(curl -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github.v3.raw" -L https://api.github.com/repos/jtlshipping/shipping-platform/contents/bin/install-jtl?ref=main)"
```

**What the script does:**
1. Downloads deployment files from private repository using GitHub API
2. Asks for version to deploy (defaults to latest from `VERSION` file)
3. Asks for your domain name
4. Installs Docker and Docker Compose (if not present)
5. Logs into GitHub Container Registry
6. Generates secure secrets automatically (SECRET_KEY, OAuth credentials, etc.)
7. Creates SSL certificates with Let's Encrypt
8. Pulls and starts all Docker containers
9. Runs database migrations
10. Creates admin user

**Manual deployment with arguments:**

```bash
# SSH into your server
ssh root@YOUR_SERVER_IP

# Set your GitHub token
export GITHUB_TOKEN=ghp_your_token_here

# Run deployment with version and domain
/bin/bash -c "$(curl -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github.v3.raw" -L https://api.github.com/repos/jtlshipping/shipping-platform/contents/bin/install-jtl?ref=main)" -- 2025.1.0 yourdomain.com

# For staging SSL (Let's Encrypt staging)
/bin/bash -c "$(curl -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github.v3.raw" -L https://api.github.com/repos/jtlshipping/shipping-platform/contents/bin/install-jtl?ref=main)" -- 2025.1.0 yourdomain.com staging
```

**After deployment (5-10 minutes):**
- Dashboard: `https://app.yourdomain.com`
- API: `https://api.yourdomain.com`
- API Docs: `https://api.yourdomain.com/docs`
- Default login: `admin@example.com` / `demo`

### Managing Production Deployment

**View logs:**
```bash
docker compose logs -f api
docker compose logs -f dashboard
```

**Stop services:**
```bash
docker compose stop
```

**Start services:**
```bash
docker compose start
```

**Upgrade to latest version:**
```bash
# Automated upgrade with safety checks
/bin/bash -c "$(curl -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github.v3.raw" -L https://api.github.com/repos/jtlshipping/shipping-platform/contents/bin/upgrade-jtl?ref=main)"
```

The upgrade script will:
1. Check for postgres volume to prevent data loss
2. Back up your Caddyfile
3. Download latest docker-compose.yml
4. Pull new Docker images
5. Gracefully stop services
6. Apply any necessary configuration updates
7. Restart with new version

**Manual upgrade:**
```bash
# Set your GitHub token in .env file or export it
export GITHUB_TOKEN=your_token_here

# Pull latest images
docker compose pull

# Restart services
docker compose up -d
```

### Local Docker Deployment

For testing with Docker locally:

```bash
# Login to GitHub Container Registry
echo YOUR_PAT | docker login ghcr.io -u YOUR_USERNAME --password-stdin

# Start services
docker compose up -d
```

Access at:
- Dashboard: http://localhost:3102
- API: http://localhost:5002

## Useful Links

- [Karrio Documentation](https://docs.karrio.io)
- [Turborepo Documentation](https://turborepo.com/docs)
- [TanStack Start Documentation](https://tanstack.com/start/latest)
- [Django Documentation](https://docs.djangoproject.com)