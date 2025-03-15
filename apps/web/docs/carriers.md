---
sidebar_position: 4
---

# Carrier Integration

Karrio supports integration with 30+ shipping carriers worldwide. This guide provides information about the supported carriers and how to set them up.

## Supported Carriers

Karrio integrates with the following carriers:

### North America

- **USPS** (United States Postal Service)
- **UPS** (United Parcel Service)
- **FedEx**
- **DHL Express**
- **Canada Post**
- **Purolator**
- **Canpar**
- **DHL eCommerce**
- **APC Postal**
- **Sendle**

### Europe

- **DPD**
- **Royal Mail**
- **Parcelforce**
- **Evri (formerly Hermes)**
- **Deutsche Post**
- **DHL Germany**
- **La Poste**
- **Colissimo**
- **PostNL**
- **GLS**

### Asia Pacific

- **Australia Post**
- **Aramex**
- **SF Express**
- **Japan Post**
- **Yamato**
- **Toll**
- **StarTrack**
- **YunExpress**

### Global

- **DHL Express**
- **FedEx**
- **UPS**
- **Aramex**

## Carrier Setup

Each carrier requires specific credentials to connect with Karrio. This section explains how to set up each carrier.

### UPS

UPS requires the following credentials:

- **Username**: Your UPS account username
- **Password**: Your UPS account password
- **Access License Number**: Your UPS API access license number
- **Account Number**: Your UPS account number

To obtain these credentials:

1. Register for a UPS account at [ups.com](https://www.ups.com)
2. Apply for API access through the UPS Developer Portal
3. Once approved, you'll receive your Access License Number

### FedEx

FedEx requires the following credentials:

- **Account Number**: Your FedEx account number
- **Meter Number**: Your FedEx meter number
- **User Key**: Your FedEx user key
- **Password**: Your FedEx password

To obtain these credentials:

1. Register for a FedEx account at [fedex.com](https://www.fedex.com)
2. Apply for API access through the FedEx Developer Portal
3. Once approved, you'll receive your credentials

### USPS

USPS requires the following credentials:

- **Username**: Your USPS Web Tools username
- **Password**: Your USPS Web Tools password

To obtain these credentials:

1. Register for a USPS Web Tools account at [usps.com/business/web-tools-apis](https://www.usps.com/business/web-tools-apis.htm)
2. Complete the registration form
3. You'll receive your credentials via email

### DHL Express

DHL Express requires the following credentials:

- **Site ID**: Your DHL Express site ID
- **Password**: Your DHL Express password
- **Account Number**: Your DHL Express account number

To obtain these credentials:

1. Contact your DHL Express account representative
2. Request API access for your account
3. You'll receive your credentials once approved

## Setting Up Carriers in Karrio

You can set up carriers in Karrio through the dashboard or via the API.

### Using the Dashboard

1. Log in to your Karrio dashboard
2. Navigate to Settings > Carriers
3. Select the carrier you want to set up
4. Enter your credentials
5. Click "Save"

### Using the API

```bash
curl -X POST https://api.karrio.io/v1/carriers/ups/settings \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your-ups-username",
    "password": "your-ups-password",
    "access_license_number": "your-ups-license",
    "account_number": "your-ups-account"
  }'
```

## Testing Carrier Connections

After setting up a carrier, you can test the connection:

1. In the Karrio dashboard, go to Settings > Carriers
2. Select the carrier you want to test
3. Click "Test Connection"

This will verify that your credentials are valid and that Karrio can communicate with the carrier's API.

## Carrier-Specific Features

Each carrier supports different features and services. Here's a summary of what's available:

| Carrier | Rating | Label Generation | Tracking | Address Validation | Pickup | International |
|---------|--------|------------------|----------|-------------------|--------|---------------|
| UPS | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| FedEx | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| USPS | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| DHL Express | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Canada Post | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Australia Post | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| Royal Mail | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |

## Carrier Service Mapping

Karrio provides a standardized service mapping across carriers. This allows you to use consistent service names regardless of the carrier.

For example, the following service types are available across multiple carriers:

- `standard`: Standard ground service
- `express`: Express or priority service
- `international_standard`: Standard international service
- `international_express`: Express international service

You can use these standardized service names when creating shipments, or you can use carrier-specific service codes if you prefer.

## Troubleshooting Carrier Issues

If you encounter issues with a carrier integration, check:

1. That your credentials are correct
2. That your account is in good standing with the carrier
3. That you have the necessary permissions and add-ons for the services you're trying to use
4. That the carrier's API is operational (check the carrier's status page)

For more help, contact Karrio support or join our [Discord community](https://discord.gg/karrio).
