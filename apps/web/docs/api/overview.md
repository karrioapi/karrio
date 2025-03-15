---
title: API Overview
sidebar_position: 1
---

# API Overview

Karrio provides a robust, RESTful API that allows you to integrate shipping functionality into your applications. Our API follows modern best practices with predictable resource-oriented URLs, accepts and returns JSON in request and response bodies, uses standard HTTP response codes, and utilizes OAuth 2.0 for authentication.

## API Versions

The current version of the API is `v1`. All API requests should be made to the base URL:

```
https://api.karrio.io/v1
```

When using a self-hosted Karrio instance, replace the base URL with your instance URL:

```
http://your-karrio-instance:8000/v1
```

## Available Endpoints

Karrio's API is organized around the following main resources:

| Resource | Description |
|----------|-------------|
| Shipping | Create and manage shipments, generate labels, and get rates |
| Tracking | Track packages across multiple carriers |
| Carriers | Manage carrier connections and services |
| Webhooks | Set up event notifications |
| Users | Manage user accounts and permissions |

## Response Format

All API responses are returned in JSON format. A typical successful response will have the following structure:

```json
{
  "data": {
    // Response data specific to the endpoint
  },
  "meta": {
    // Metadata about the response, such as pagination info
  }
}
```

## Error Handling

When an error occurs, the API returns an appropriate HTTP status code along with a descriptive error message:

```json
{
  "error": {
    "code": "invalid_request",
    "message": "The request was unacceptable, often due to missing a required parameter.",
    "details": {
      // Additional details about the error
    }
  }
}
```

Common HTTP status codes returned by the API:

| Status Code | Description |
|-------------|-------------|
| 200 | OK - The request was successful |
| 400 | Bad Request - The request was invalid |
| 401 | Unauthorized - Authentication is required |
| 403 | Forbidden - The API key doesn't have permission |
| 404 | Not Found - The resource doesn't exist |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Server Error - Something went wrong on our end |

## Making Your First API Call

Let's make a simple API call to fetch shipping rates:

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

## Next Steps

- [Authentication](/docs/api/authentication) - Learn how to authenticate with the API
- [Rate Limits](/docs/api/rate-limits) - Understand API rate limiting
- [Shipping API](/docs/api/shipping) - Explore the shipping endpoints
- [Tracking API](/docs/api/tracking) - Learn about package tracking
