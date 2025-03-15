---
sidebar_position: 2
---

# Carrier Integration

Karrio provides a unified interface to connect with multiple shipping carriers. This guide explains how to set up and manage carrier connections in your Karrio instance.

## Supported Carriers

Karrio supports 30+ carriers globally, including:

| Carrier | Services |
|---------|----------|
| USPS | Priority Mail, First Class, Express |
| FedEx | Ground, Express, Freight |
| UPS | Ground, Express, SurePost |
| DHL | Express, eCommerce |
| Canada Post | Expedited, Regular, Priority |
| Australia Post | Standard, Express, International |
| Royal Mail | 1st Class, 2nd Class, Signed For |
| Purolator | Ground, Express, QuickShip |

## Setting Up Carrier Connections

### Through the Dashboard

1. Log in to your Karrio dashboard
2. Navigate to Settings > Carriers
3. Click "Add Carrier"
4. Select the carrier you want to add
5. Enter your carrier credentials
6. Test the connection
7. Save the connection

### Through the API

You can also set up carrier connections programmatically:

```bash
curl -X POST \
  https://api.karrio.io/v1/connections \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "carrier_name": "fedex",
    "carrier_id": "fedex",
    "test_mode": true,
    "active": true,
    "settings": {
      "user_key": "YOUR_USER_KEY",
      "password": "YOUR_PASSWORD",
      "meter_number": "YOUR_METER_NUMBER",
      "account_number": "YOUR_ACCOUNT_NUMBER"
    }
  }'
```

## Carrier-Specific Configuration

Each carrier requires specific credentials and configuration. Common requirements include:

### FedEx
- Account number
- Meter number
- User key
- Password

### UPS
- Account number
- User ID
- Password
- Access license number

### USPS
- USPS Web Tools User ID
- USPS Web Tools Password

## Using Multiple Carriers

With Karrio, you can:

1. Compare rates across multiple carriers
2. Use custom business rules to select the optimal carrier
3. Maintain carrier-specific configuration (package types, services)
4. Handle carrier-specific requirements automatically

## Extending with Custom Carriers

For advanced users, Karrio allows you to create custom carrier integrations:

1. Create a custom carrier extension
2. Implement the required endpoints (rates, shipping, tracking)
3. Register your custom carrier with Karrio
4. Use your custom carrier alongside official carriers
