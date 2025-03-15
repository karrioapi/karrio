---
sidebar_position: 2
---

# Deploying Karrio with Docker

This guide walks through deploying Karrio using Docker Compose, the recommended method for most users.

## Prerequisites

- Docker Engine 20.10.0 or newer
- Docker Compose 2.0.0 or newer
- Git (optional, for cloning the repository)

## Quick Start

The fastest way to get Karrio running is to use our official Docker Compose configuration:

```bash
# Clone the repository (or download the docker-compose.yml file)
git clone https://github.com/karrioapi/karrio.git
cd karrio/deploy

# Start the services
docker-compose up -d
```

This will start all the necessary services:
- Karrio API server
- Web interface
- PostgreSQL database
- Redis cache

Once started, you can access the Karrio dashboard at `http://localhost:8000`.

## Configuration Options

You can customize your Karrio deployment by editing the `.env` file:

```bash
# Create a .env file from the template
cp .env.sample .env

# Edit the .env file with your preferred settings
nano .env
```

Key configuration options include:
- Database credentials
- API keys for carriers
- Webhook URLs
- Authentication settings

## Upgrading

To upgrade to a newer version of Karrio:

```bash
# Pull the latest changes
git pull

# Restart the services with the new version
docker-compose down
docker-compose up -d
```

## Backup and Restore

It's important to regularly backup your Karrio data:

```bash
# Backup the database
docker-compose exec postgres pg_dump -U postgres karrio > karrio_backup.sql

# Restore from backup
cat karrio_backup.sql | docker-compose exec -T postgres psql -U postgres karrio
```
