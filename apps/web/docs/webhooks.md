---
sidebar_position: 3
---

# Webhooks

Karrio uses webhooks to notify your application when events happen in your account. This guide explains how to set up and use webhooks with Karrio.

## What are Webhooks?

Webhooks are HTTP callbacks that are triggered by specific events in Karrio. When an event occurs, Karrio sends an HTTP POST request to the URL you've configured, containing information about the event.

## Available Events

Karrio supports the following webhook events:

| Event | Description |
|-------|-------------|
| `shipment.created` | Triggered when a new shipment is created |
| `shipment.purchased` | Triggered when a shipping label is purchased |
| `shipment.cancelled` | Triggered when a shipment is cancelled |
| `shipment.updated` | Triggered when a shipment is updated |
| `tracker.created` | Triggered when a new tracker is created |
| `tracker.updated` | Triggered when a tracker status is updated |
| `rate.fetched` | Triggered when shipping rates are fetched |

## Setting Up Webhooks

You can set up webhooks through the Karrio dashboard or via the API.

### Using the Dashboard

1. Log in to your Karrio dashboard
2. Navigate to Settings > Webhooks
3. Click "Add Webhook"
4. Enter the URL where you want to receive webhook events
5. Select the events you want to subscribe to
6. Click "Save"

### Using the API

```bash
curl -X POST https://api.karrio.io/v1/webhooks \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-app.com/webhooks/karrio",
    "events": ["shipment.created", "shipment.purchased", "tracker.updated"],
    "description": "Production webhook endpoint"
  }'
```

## Webhook Payload

When an event occurs, Karrio sends an HTTP POST request to your webhook URL with a JSON payload. The payload includes:

- `id`: A unique identifier for the webhook event
- `event`: The type of event that occurred
- `created_at`: The timestamp when the event occurred
- `data`: The data associated with the event

Example payload for a `shipment.created` event:

```json
{
  "id": "evt_123456789",
  "event": "shipment.created",
  "created_at": "2023-06-15T14:30:00Z",
  "data": {
    "id": "shp_987654321",
    "status": "created",
    "carrier": {
      "name": "ups"
    },
    "service": "ups_express",
    "shipper": {
      "name": "Sender Name",
      "company_name": "Sender Company",
      "address_line1": "123 Sender St",
      "city": "Sender City",
      "postal_code": "12345",
      "country_code": "US",
      "phone_number": "123-456-7890",
      "email": "sender@example.com"
    },
    "recipient": {
      "name": "Recipient Name",
      "company_name": "Recipient Company",
      "address_line1": "456 Recipient St",
      "city": "Recipient City",
      "postal_code": "67890",
      "country_code": "US",
      "phone_number": "098-765-4321",
      "email": "recipient@example.com"
    },
    "parcels": [
      {
        "weight": 1.5,
        "weight_unit": "kg",
        "length": 10,
        "width": 15,
        "height": 5,
        "dimension_unit": "cm"
      }
    ],
    "created_at": "2023-06-15T14:30:00Z"
  }
}
```

## Verifying Webhook Signatures

To ensure that webhook requests are coming from Karrio, you should verify the signature included in each request. Karrio signs webhook requests using HMAC with SHA-256.

The signature is included in the `X-Karrio-Signature` header of the request. To verify the signature:

1. Get the webhook secret from your Karrio dashboard
2. Compute an HMAC with the SHA-256 hash function
3. Use your webhook secret as the key and the request body as the message
4. Compare the computed signature with the value in the `X-Karrio-Signature` header

### Example Verification in Node.js

```javascript
const crypto = require('crypto');
const express = require('express');
const app = express();

app.use(express.json({
  verify: (req, res, buf) => {
    req.rawBody = buf;
  }
}));

app.post('/webhooks/karrio', (req, res) => {
  const signature = req.headers['x-karrio-signature'];
  const webhookSecret = 'your_webhook_secret';

  const hmac = crypto.createHmac('sha256', webhookSecret);
  const computedSignature = hmac.update(req.rawBody).digest('hex');

  if (crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(computedSignature)
  )) {
    // Signature is valid, process the webhook
    console.log('Webhook verified:', req.body);
    res.status(200).send('Webhook received');
  } else {
    // Signature is invalid
    console.error('Invalid webhook signature');
    res.status(403).send('Invalid signature');
  }
});

app.listen(3000, () => {
  console.log('Webhook server listening on port 3000');
});
```

## Best Practices

1. **Respond quickly**: Your webhook endpoint should respond with a 2xx status code as quickly as possible. Process the webhook asynchronously if needed.

2. **Implement retries**: Karrio will retry failed webhook deliveries with an exponential backoff schedule.

3. **Verify signatures**: Always verify webhook signatures to ensure the requests are coming from Karrio.

4. **Idempotency**: Implement idempotent webhook handling to avoid processing duplicate events.

5. **Logging**: Log webhook requests for debugging and auditing purposes.

## Testing Webhooks

You can test your webhook implementation using the Karrio dashboard:

1. Go to Settings > Webhooks
2. Select the webhook you want to test
3. Click "Send Test Event"
4. Select an event type
5. Click "Send"

This will send a test webhook with sample data to your endpoint.

## Troubleshooting

If you're not receiving webhook events, check:

1. That your webhook URL is publicly accessible
2. That your server is responding with a 2xx status code
3. That you've subscribed to the correct events
4. Your server logs for any errors processing the webhook

For more help, contact Karrio support or join our [Discord community](https://discord.gg/karrio).
