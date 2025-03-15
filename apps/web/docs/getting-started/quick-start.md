---
title: Quick Start
sidebar_position: 1
---

# Quick Start

Get started with Karrio in just a few minutes. This guide will help you get up and running quickly with either the Karrio Platform or the self-hosted solution.

## Karrio Platform (Managed Service)

The fastest way to get started with Karrio is to use our managed platform service. This option requires no installation and provides immediate access to our multi-carrier shipping API.

### 1. Create an account

Visit [app.karrio.io](https://app.karrio.io/signup) to create your account.

### 2. Add carrier connections

After creating an account, you can set up your carrier connections:

1. Navigate to the **Connections** section in the dashboard
2. Select the carriers you want to integrate with
3. Enter your carrier account credentials
4. Test the connection to ensure it's working properly

### 3. Make your first API call

You're now ready to make your first API call:

```bash
curl -X POST https://api.karrio.io/v1/shipping/rates \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "shipper": {
      "postal_code": "V6M2V9",
      "city": "Vancouver",
      "country_code": "CA",
      "state_code": "BC"
    },
    "recipient": {
      "postal_code": "10022",
      "city": "New York",
      "country_code": "US",
      "state_code": "NY"
    },
    "parcels": [{
      "weight": 1.0,
      "weight_unit": "KG",
      "packaging_type": "your_packaging"
    }]
  }'
```

## Self-Hosted Solution

If you prefer to self-host Karrio, follow these steps:

### 1. Requirements

Ensure you have the following prerequisites:
- Docker and Docker Compose
- A machine with at least 2GB RAM and 1 CPU
- Basic knowledge of Docker and containerization

### 2. Quick installation

Run the following command to install Karrio:

```bash
curl -sSL https://raw.githubusercontent.com/karrioapi/karrio/main/scripts/install.sh | bash
```

This script will:
- Download the necessary Docker Compose files
- Set up the required environment
- Start the Karrio services

### 3. Access the dashboard

Once installation is complete, you can access the dashboard at:
- UI: `http://localhost:8001`
- API: `http://localhost:8000`

## Next Steps

Now that you have Karrio up and running, here are some recommended next steps:

- [Explore the API Reference](/docs/api)
- [Learn about Carriers](/docs/carriers)
- [See Code Examples](/docs/examples)
- [Set up Webhooks](/docs/webhooks)
- [Self-Hosting with Docker](/docs/self-hosting/docker)
