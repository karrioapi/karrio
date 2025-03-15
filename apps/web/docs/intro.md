---
title: Introduction
slug: /
sidebar_position: 1
---

# Introduction

Welcome to the Karrio documentation! Here you'll find comprehensive guides and documentation to help you start working with Karrio as quickly as possible.

## What is Karrio?

Karrio is a modern, headless shipping platform that provides a unified API to integrate multiple shipping carriers. It enables developers to build powerful shipping experiences in their applications with minimal effort.

### Key Features

- **Universal Shipping API**: Connect to 30+ shipping carriers through a single API
- **Rate Shopping**: Compare shipping rates across multiple carriers
- **Label Generation**: Create shipping labels with ease
- **Package Tracking**: Track shipments across all carriers
- **Webhooks**: Receive real-time notifications for shipping events
- **Flexible Deployment**: Use our managed platform or self-host

## Why Karrio?

Shipping integration is often complex and time-consuming. Each carrier has its own API, credentials, and peculiarities. Karrio solves this by providing:

1. **Simplified Integration**: One API for all carriers
2. **Developer-Friendly**: Modern RESTful API with comprehensive documentation
3. **Flexibility**: Use our managed platform or self-host with full control
4. **Cost-Effective**: Open-source core with transparent pricing
5. **Extensibility**: Customize and extend to meet your specific needs

## Quick Start

You can get started with Karrio in two ways:

### Option 1: Karrio Platform (Hosted)

The fastest way to start using Karrio:

1. [Sign up](https://app.karrio.io/signup) for a Karrio account
2. Add your carrier connections in the dashboard
3. Generate API keys and start shipping!

```bash
# Example API call to create a shipment
curl -X POST https://api.karrio.io/v1/shipping/rates \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "shipper": {
      "postal_code": "V6M2V9",
      "country_code": "CA"
    },
    "recipient": {
      "postal_code": "10022",
      "country_code": "US"
    },
    "parcels": [{
      "weight": 1.0,
      "weight_unit": "KG"
    }]
  }'
```

### Option 2: Self-Hosting (Open Source)

For complete control and customization:

1. Clone the [Karrio repository](https://github.com/karrioapi/karrio)
2. Deploy using Docker Compose or Kubernetes
3. Configure your carriers and start shipping!

```bash
# Quick installation
curl -sSL https://raw.githubusercontent.com/karrioapi/karrio/main/scripts/install.sh | bash
```

## Where to Go Next

- **[Getting Started](/docs/getting-started/quick-start)**: Detailed setup instructions
- **[API Reference](/docs/api/overview)**: Explore the API endpoints
- **[Shipping Integration](/docs/shipping/overview)**: Learn about core shipping features
- **[Developer Guides](/docs/guides/sdk-usage)**: Advanced usage and customization
- **[Self-Hosting](/docs/self-hosting/introduction)**: Deploy and manage your own instance
