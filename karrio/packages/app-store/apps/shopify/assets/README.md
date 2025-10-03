# Shopify Integration for Karrio

Connect your Shopify store to Karrio for automated shipping rate calculations, label generation, and order fulfillment.

## Features

- **Real-time Shipping Rates**: Provide accurate shipping rates to customers during checkout
- **Automatic Label Generation**: Generate shipping labels directly from Shopify orders
- **Multi-carrier Support**: Access to 50+ shipping carriers through Karrio
- **Rate Customization**: Apply markup percentages and custom rules
- **Order Synchronization**: Automatically sync orders and tracking information
- **Webhook Integration**: Real-time updates between Shopify and Karrio

## Getting Started

### Prerequisites

- A Shopify store (any plan)
- A Karrio account with API access
- Admin access to your Shopify store

### Installation Steps

1. **Install the App**: Click "Install" in the Karrio dashboard
2. **Configure Connection**: Choose between OAuth or manual setup
3. **Set Up Carrier Service**: Configure shipping rate calculation
4. **Test Integration**: Verify rates are appearing in checkout
5. **Go Live**: Enable for production use

### Setup Options

#### Option 1: OAuth Setup (Recommended)
If OAuth environment variables are configured:
1. Enter your shop domain (e.g., `mystore.myshopify.com`)
2. Click "Connect with Shopify"
3. Authorize the connection in Shopify
4. Configure rate settings

#### Option 2: Manual Setup
If OAuth is not available:
1. Create a private app in Shopify Admin
2. Generate access token with required scopes
3. Enter shop domain and access token manually
4. Test connection and configure settings

### Required Shopify Permissions

- `read_orders`: Read order information
- `write_shipping`: Create carrier services and shipping rates

### Configuration Options

- **Shop Domain**: Your Shopify store URL
- **Carrier Service Name**: Name displayed in checkout
- **Default Package Weight**: Fallback weight for items without weight
- **Rate Markup**: Percentage markup applied to shipping rates
- **Rate Calculation**: Enable/disable real-time rate requests

## How It Works

1. **Customer Checkout**: Customer enters shipping address in Shopify checkout
2. **Rate Request**: Shopify sends rate request to Karrio via carrier service
3. **Rate Calculation**: Karrio calculates rates from multiple carriers
4. **Rate Display**: Rates are displayed to customer in checkout
5. **Order Creation**: When order is placed, it's synced to Karrio
6. **Label Generation**: Generate shipping labels through Karrio dashboard

## Troubleshooting

### Common Issues

**Rates not appearing in checkout:**
- Verify carrier service is enabled in Shopify
- Check that rate calculation is enabled in app settings
- Ensure default package weight is set for weightless items

**Connection test failing:**
- Verify shop domain format (must end with `.myshopify.com`)
- Check access token has required permissions
- Ensure private app is enabled in Shopify

**OAuth authorization failing:**
- Verify OAuth environment variables are configured
- Check that callback URLs are properly set
- Ensure shop domain is correct

### Support

For additional support:
- Check the [Karrio Documentation](https://docs.karrio.io)
- Contact support at support@karrio.io
- Visit the [Community Forum](https://community.karrio.io)

## API Endpoints

This app provides several API endpoints:

- `POST /test-connection`: Test Shopify API connection
- `GET /oauth/check-support`: Check OAuth configuration
- `GET /oauth/authorize`: Initiate OAuth flow
- `POST /oauth/callback`: Handle OAuth callback

## Screenshots

*Screenshots will be displayed here showing the configuration interface, rate calculation, and order management features.*

## Version History

### v1.0.0
- Initial release
- OAuth and manual connection support
- Real-time rate calculation
- Basic order synchronization
- Webhook integration

---

*This integration is built and maintained by the Karrio team. For technical issues or feature requests, please contact our support team.*
