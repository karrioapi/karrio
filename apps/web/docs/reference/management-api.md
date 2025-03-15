---
sidebar_position: 3
---

# Management API

The Karrio Management API allows you to programmatically manage your Karrio organization, users, and settings. This is separate from the Shipping API which handles shipping operations.

## Authentication

Management API requests require a Management API key, which is different from your regular API key. You can generate a Management API key in the Karrio dashboard under Settings > API Keys > Management.

Include your Management API key in the Authorization header:

```bash
curl -X GET \
  https://api.karrio.io/v1/management/users \
  -H "Authorization: Bearer YOUR_MANAGEMENT_API_KEY"
```

## Base URL

Management API endpoints are all under:

```
https://api.karrio.io/v1/management
```

## Organizations

### List Organizations

```bash
GET /organizations
```

### Get Organization

```bash
GET /organizations/{org_id}
```

### Update Organization

```bash
PATCH /organizations/{org_id}
```

Example request:

```bash
curl -X PATCH \
  https://api.karrio.io/v1/management/organizations/org_123 \
  -H "Authorization: Bearer YOUR_MANAGEMENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Organization Name",
    "address": {
      "street1": "123 Main St",
      "city": "Boston",
      "state_code": "MA",
      "postal_code": "02108",
      "country_code": "US"
    }
  }'
```

## Users

### List Users

```bash
GET /users
```

### Create User

```bash
POST /users
```

Example request:

```bash
curl -X POST \
  https://api.karrio.io/v1/management/users \
  -H "Authorization: Bearer YOUR_MANAGEMENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe",
    "role": "member"
  }'
```

### Get User

```bash
GET /users/{user_id}
```

### Update User

```bash
PATCH /users/{user_id}
```

### Delete User

```bash
DELETE /users/{user_id}
```

## API Keys

### List API Keys

```bash
GET /api-keys
```

### Create API Key

```bash
POST /api-keys
```

Example request:

```bash
curl -X POST \
  https://api.karrio.io/v1/management/api-keys \
  -H "Authorization: Bearer YOUR_MANAGEMENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Development API Key",
    "permissions": ["read:shipments", "write:shipments"]
  }'
```

### Revoke API Key

```bash
DELETE /api-keys/{key_id}
```

## Webhooks

### List Webhooks

```bash
GET /webhooks
```

### Create Webhook

```bash
POST /webhooks
```

Example request:

```bash
curl -X POST \
  https://api.karrio.io/v1/management/webhooks \
  -H "Authorization: Bearer YOUR_MANAGEMENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-server.com/webhook",
    "events": ["shipment.created", "tracker.updated"],
    "active": true
  }'
```

### Update Webhook

```bash
PATCH /webhooks/{webhook_id}
```

### Delete Webhook

```bash
DELETE /webhooks/{webhook_id}
```
