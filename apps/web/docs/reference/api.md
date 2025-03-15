---
sidebar_position: 1
---

# API Reference

The Karrio API allows you to integrate shipping functionality directly into your applications. This reference provides detailed information about the API endpoints, request parameters, and response formats.

## Authentication

All API requests require authentication using API keys. You can obtain your API key from the [Karrio dashboard](https://app.karrio.io/api-keys).

Include your API key in the Authorization header:

```bash
curl -X GET \
  https://api.karrio.io/v1/shipments \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Base URL

The base URL for all API requests is:

```
https://api.karrio.io/v1
```

For self-hosted instances, use your server's URL.

## Rate Limits

API requests are limited to:
- 1000 requests per minute for the Scale plan
- 5000 requests per minute for the Enterprise plan
- 100 requests per minute for self-hosted instances (configurable)

## Endpoints

### Shipments

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/shipments` | GET | List all shipments |
| `/shipments` | POST | Create a new shipment |
| `/shipments/{id}` | GET | Get a specific shipment |
| `/shipments/{id}` | PATCH | Update a shipment |
| `/shipments/{id}` | DELETE | Cancel a shipment |

### Rates

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/rates` | POST | Get shipping rates |

### Trackers

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/trackers` | GET | List all trackers |
| `/trackers` | POST | Create a new tracker |
| `/trackers/{id}` | GET | Get a specific tracker |

## Error Handling

The API uses conventional HTTP response codes to indicate success or failure:
- 2xx: Success
- 4xx: Client error
- 5xx: Server error

Errors include a JSON response body with details:

```json
{
  "error": {
    "code": "invalid_request",
    "message": "The shipment could not be created due to missing required fields",
    "details": {
      "recipient": "This field is required"
    }
  }
}
```
