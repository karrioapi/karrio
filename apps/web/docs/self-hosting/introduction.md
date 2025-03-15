---
title: Introduction to Self-Hosting
sidebar_position: 1
---

# Introduction to Self-Hosting

Karrio is available as a fully open-source solution that you can deploy and manage on your own infrastructure. Self-hosting Karrio gives you complete control over your shipping data, infrastructure, and customizations.

## Why Self-Host Karrio?

There are several compelling reasons to self-host Karrio:

### Complete Data Control

When you self-host Karrio, all your shipping data stays within your infrastructure. This is particularly important for businesses with strict data privacy requirements or regulatory compliance needs.

### Unlimited Customization

Self-hosting enables you to modify the codebase to fit your specific business requirements. You can customize the UI, add new features, or integrate with internal systems that may not be supported by the hosted platform.

### Cost Control

For high-volume shipping operations, self-hosting can be more cost-effective than a SaaS solution with per-transaction pricing. You control the infrastructure costs and can optimize for your specific usage patterns.

### Infrastructure Integration

Integrate Karrio with your existing infrastructure, security systems, and monitoring tools to create a seamless part of your technology stack.

## Karrio Architecture

The self-hosted version of Karrio consists of several components:

<!-- Removing image reference that doesn't exist -->
<!-- ![Karrio Architecture](/img/docs/karrio-architecture.png) -->

- **API Server**: Handles all API requests and business logic
- **Web UI**: Provides a user interface for managing shipments
- **Database**: Stores shipping data, user accounts, and settings
- **Worker**: Processes background tasks like label generation and tracking updates
- **Redis**: Used for caching and as a message broker
- **Carrier Extensions**: Plug-ins for connecting to different shipping carriers

## Deployment Options

Karrio can be deployed in various ways depending on your needs:

### Docker Compose (Recommended for Development)

The simplest way to deploy Karrio for development or small-scale production use is with Docker Compose. This requires minimal setup and can be running in minutes.

```bash
curl -sSL https://raw.githubusercontent.com/karrioapi/karrio/main/scripts/install.sh | bash
```

### Kubernetes (Recommended for Production)

For production deployments, we recommend using Kubernetes for better scalability, reliability, and maintainability.

```bash
# Apply the Kubernetes manifests
kubectl apply -f https://raw.githubusercontent.com/karrioapi/karrio/main/k8s/karrio.yaml
```

### Manual Installation

For advanced users who need complete control over the installation process, you can also install Karrio manually by following our step-by-step guide.

## System Requirements

To run Karrio effectively, your system should meet these minimum requirements:

- **CPU**: 2 cores
- **RAM**: 4GB
- **Disk**: 20GB
- **Operating System**: Linux (Ubuntu 18.04+ recommended), macOS, or Windows with Docker
- **Docker**: Version 19.03 or later
- **Docker Compose**: Version 1.25 or later (for Docker Compose deployment)
- **Kubernetes**: Version 1.16 or later (for Kubernetes deployment)

## Next Steps

- **[Self-Hosting with Docker](/docs/self-hosting/docker)**: Get started with Docker deployment
