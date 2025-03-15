---
sidebar_position: 2
---

# API Reference

Karrio provides both REST and GraphQL APIs to integrate shipping functionality into your applications. This reference will help you understand the available endpoints and how to use them.

## Authentication

All API requests require authentication using an API key. You can obtain an API key from your Karrio dashboard.

```bash
# Example API request with authentication
curl -X POST https://api.karrio.io/v1/shipments \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "shipper": {"postal_code": "V6M2V9", "country_code": "CA"},
    "recipient": {"postal_code": "27401", "country_code": "US"},
    "parcels": [{"weight": 1}]
  }'
```

## REST API Endpoints

### Shipments

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/shipments` | POST | Create a new shipment |
| `/v1/shipments/{id}` | GET | Retrieve a shipment |
| `/v1/shipments/{id}` | PATCH | Update a shipment |
| `/v1/shipments/{id}` | DELETE | Cancel a shipment |
| `/v1/shipments` | GET | List shipments |

### Rates

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/rates` | POST | Get shipping rates |

### Trackers

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/trackers` | POST | Create a tracker |
| `/v1/trackers/{id}` | GET | Retrieve a tracker |
| `/v1/trackers` | GET | List trackers |

### Carriers

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/carriers` | GET | List available carriers |
| `/v1/carriers/{carrier_name}/services` | GET | List carrier services |
| `/v1/carriers/{carrier_name}/settings` | GET | Get carrier settings |
| `/v1/carriers/{carrier_name}/settings` | POST | Update carrier settings |

## GraphQL API

Karrio also provides a GraphQL API for more flexible queries. The GraphQL endpoint is available at:

```
https://api.karrio.io/graphql
```

### Example GraphQL Query

```graphql
query {
  shipments(first: 5) {
    edges {
      node {
        id
        status
        createdAt
        trackingNumber
        carrier {
          name
        }
        service
        shipper {
          postalCode
          countryCode
        }
        recipient {
          postalCode
          countryCode
        }
      }
    }
  }
}
```

## Rate Limiting

The Karrio API implements rate limiting to ensure fair usage. The current limits are:

- 100 requests per minute for standard accounts
- 1000 requests per minute for enterprise accounts

If you exceed these limits, you'll receive a `429 Too Many Requests` response.

## Webhooks

Karrio can send webhook notifications for various events. To set up webhooks, go to the Webhooks section in your Karrio dashboard and configure the events you want to receive notifications for.

For more information on webhooks, see the [Webhooks documentation](/docs/webhooks).

## Error Handling

The API returns standard HTTP status codes to indicate success or failure:

- `200 OK`: The request was successful
- `201 Created`: A resource was successfully created
- `400 Bad Request`: The request was invalid
- `401 Unauthorized`: Authentication failed
- `404 Not Found`: The requested resource was not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: An error occurred on the server

Error responses include a JSON body with more details:

```json
{
  "error": {
    "code": "invalid_request",
    "message": "Missing required field: recipient",
    "details": {
      "field": "recipient"
    }
  }
}
```

## SDKs and Client Libraries

Karrio provides official client libraries for several programming languages:

- [JavaScript/TypeScript](https://github.com/karrioapi/karrio-js)
- [Python](https://github.com/karrioapi/karrio-python)
- [Ruby](https://github.com/karrioapi/karrio-ruby)
- [PHP](https://github.com/karrioapi/karrio-php)
- [Go](https://github.com/karrioapi/karrio-go)

These libraries make it easier to integrate with the Karrio API in your preferred language.
