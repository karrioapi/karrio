# Karrio Insiders

The enterprise-ready shipping integration platform built on top of [Karrio](https://github.com/karrioapi/karrio).

## Features

Additional features on top of Karrio:

- Multi-Tenancy and team collaboration
- Advanced shipping addons
- Customizable dashboard
- Billing management
- Priority support

## Prerequisites

- Docker and Docker Compose
- Git installed on your system
- Valid Karrio Insiders license
- GitHub account with access to karrio-insiders repository

## Authentication Setup

### GitHub Personal Access Token (PAT) - Required for Docker

All Docker deployments require a GitHub PAT to pull Insiders images from the GitHub Container Registry:

1. Create a GitHub Personal Access Token with `read:packages` scope:
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Click "Generate new token (classic)"
   - Select `read:packages` scope
   - Generate and save the token

2. Login to GitHub Container Registry:
```bash
echo YOUR_PAT | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin
```

### SSH Authentication - Required for Cloning Repositories

Only needed if you're cloning the karrio-insiders repository:

1. **Generate an SSH key** (if you don't have one):
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

2. **Add the SSH key to your SSH agent**:
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

3. **Copy your public key**:
```bash
cat ~/.ssh/id_ed25519.pub
```

4. **Add the key to your GitHub account**:
   - Go to GitHub Settings → SSH and GPG keys
   - Click "New SSH key"
   - Paste your public key and save

5. **Test your connection**:
```bash
ssh -T git@github.com
```
You should see: "Hi username! You've successfully authenticated..."

## Setup Options

### Option 1: Local Docker Deployment (Quick Start)

The fastest way to run Karrio Insiders locally using pre-built Docker images.

1. Clone the main repository and initialize submodules:
```bash
# Clone the main Karrio repository
git clone --depth 1 https://github.com/karrioapi/karrio
cd karrio

# Initialize the required submodules
git submodule update --init community
git submodule update --init ee/insiders
```

2. Start the Insiders environment:
```bash
# Navigate to the docker directory
cd docker

# Login to GitHub Container Registry (if not already logged in)
echo YOUR_PAT | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin

# Start the services
docker compose -f docker-compose.insiders.local.yml up -d
```

3. Access the services:
- Dashboard: http://localhost:3002
- API: http://localhost:5002

Default login: `admin@example.com` | `demo`

### Option 2: Local Development Environment

For developers who want to modify and run Karrio Insiders code locally.

1. Clone and setup the repository (same as Option 1):
```bash
git clone git@github.com:karrioapi/karrio.git
cd karrio
git submodule update --init community
git submodule update --init ee/insiders
```

2. Set up the development environment:
```bash
# Run the setup script
./bin/setup-dev-env
# activate python env
source ./bin/activate-env
```

3. Follow the local development guide:
   - Documentation: https://www.karrio.io/docs/developing/local-development
   - This setup allows you to run the server locally and make code changes

### Option 3: Hobby Deployment (Cloud)

Deploy a production-ready Karrio Insiders instance on your server.

**Prerequisites:**
- Linux server with Docker installed
- Domain name pointed to your server
- GitHub PAT with `read:packages` scope

**Deployment:**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/karrioapi/karrio/HEAD/bin/deploy-insiders)"
```

This script will:
- Set up SSL certificates with Let's Encrypt
- Configure proper domain routing
- Set up a production-ready PostgreSQL database
- Configure Redis for caching
- Set up proper Docker networking

## Troubleshooting

### SSH Authentication Issues

**Permission denied when cloning insiders submodule:**
- Ensure your GitHub account has been granted access to the karrio-insiders repository
- Verify SSH authentication is working: `ssh -T git@github.com`
- Check that you're using the SSH agent: `ssh-add -l`

**"Host key verification failed" error:**
- Add GitHub to known hosts: `ssh-keyscan github.com >> ~/.ssh/known_hosts`

### Docker Registry Issues

**Failed to pull images from ghcr.io:**
- Ensure you're logged in: `docker login ghcr.io`
- Verify your PAT has `read:packages` scope
- Check your GitHub username and PAT are correct

### General Issues

**Still having problems?**
- Contact support@karrio.io with your GitHub username to verify access
- Include error messages and steps you've taken

## Support

For support, please contact:

- Email: support@karrio.io
- Discord: [Karrio Discord Server](https://discord.gg/gS88uE7sEx)
