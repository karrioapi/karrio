---
title: Shipping Overview
sidebar_position: 1
---

# Shipping Overview

Karrio's shipping functionality provides a complete solution for integrating multi-carrier shipping capabilities into your applications. Whether you're building an e-commerce platform, a logistics system, or any application that requires shipping functionality, Karrio offers a unified API to access multiple carrier services.

## Core Shipping Capabilities

### Rate Shopping

Fetch and compare shipping rates from multiple carriers with a single API call. This allows you to offer your customers the best shipping options based on price, delivery time, or other preferences.

```bash
POST /v1/shipping/rates
```

### Label Generation

Generate shipping labels from any supported carrier. Once you've selected a shipping service, you can create a shipment and generate the corresponding label.

```bash
POST /v1/shipping/labels
```

### Package Tracking

Track packages across all integrated carriers through a unified tracking interface. This allows you to provide consistent tracking updates to your customers, regardless of which carrier is handling the shipment.

```bash
GET /v1/tracking/:tracking_number
```

### Returns Management

Create return labels and manage the returns process for your customers. This allows you to streamline the returns process and provide a better customer experience.

```bash
POST /v1/shipping/returns
```

## Supported Carriers

Karrio integrates with a wide range of carriers, including:

- DHL Express
- FedEx
- UPS
- USPS
- Canada Post
- Australia Post
- Royal Mail
- And many more...

For a complete list of supported carriers, see the [Carriers](/docs/shipping/carriers) page.

## Integration Patterns

There are several common patterns for integrating Karrio's shipping functionality into your applications:

### Direct API Integration

For maximum flexibility, you can integrate directly with Karrio's API. This approach allows for complete control over the shipping process and user experience.

### Webhook-Based Integration

Set up webhooks to receive notifications about shipping events, such as when a label is created or a package status changes. This approach is useful for maintaining synchronization between your system and Karrio.

### SDK Integration

Karrio provides SDKs for various programming languages to simplify the integration process. These SDKs handle authentication, error handling, and provide a more convenient interface for interacting with the API.

## Next Steps

- [Carrier Integration](/docs/shipping/carriers) - Learn how to connect with specific carriers
- [Shipping Rates](/docs/shipping/rates) - Understand how to fetch and compare shipping rates
- [Shipping Labels](/docs/shipping/labels) - Learn how to generate shipping labels
- [Package Tracking](/docs/shipping/tracking) - Explore the package tracking functionality
