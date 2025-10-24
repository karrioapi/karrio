# Shopify Integration - Complete Implementation

## Overview

This document summarizes the complete Shopify embedded app integration with JWT authentication that has been implemented. The integration provides seamless shipping rate calculations and order fulfillment between Shopify stores and Karrio.

## Architecture

### JWT Authentication System
- **Session-Independent Authentication**: Apps can authenticate without user sessions (perfect for webhooks)
- **Cryptographically Signed JWTs**: Using HMAC-SHA256 with shared secret
- **Token Expiration**: 5-minute token expiration for security
- **Installation-Scoped**: Each app installation has its own API key and context

### URL Structure
All Shopify app APIs now use the installation ID in the URL path:
- Carrier Service Rates: `/api/apps/shopify/carrier-service/rates/[installationId]`
- Carrier Service Registration: `/api/apps/shopify/carrier-service/register/[installationId]`
- OAuth Endpoints: `/api/apps/shopify/oauth/authorize` and `/api/apps/shopify/oauth/callback`

## Components Implemented

### 1. JWT Authentication Utilities (`@karrio/hooks/app-auth`)
- **generateAppJWT()**: Creates JWT tokens for app authentication
- **validateAppJWT()**: Server-side JWT validation
- **createAppApiClient()**: Authenticated fetch client for API requests
- **generateWebhookUrl()**: Creates webhook URLs with JWT tokens
- **extractAppContext()**: Extracts app context from JWT tokens

### 2. GraphQL API Extensions
- **API Key Management**: Auto-generation, rotation, and recreation
- **ROTATE_APP_API_KEY**: Mutation to rotate app API keys
- **ENSURE_APP_API_KEY**: Mutation to ensure API key exists

### 3. Shopify App Component (`shopify/component.tsx`)
- **Credential Management**: Support for both environment variables and manual entry
- **OAuth Flow**: Complete OAuth handshake with state management
- **Carrier Service Integration**: Registration and management
- **Beautiful UI**: Modern shadcn/ui components with step-by-step setup

### 4. API Endpoints

#### Carrier Service Rates (`/api/apps/shopify/carrier-service/rates/[installationId]/route.ts`)
- **JWT Authentication**: Validates tokens from query params or headers
- **Installation Verification**: Ensures installation ID matches token
- **Shopify Webhook Validation**: HMAC signature verification
- **Format Conversion**: Shopify ↔ Karrio data transformation
- **Live Rate Calculation**: Real-time shipping rates from Karrio API

#### Carrier Service Registration (`/api/apps/shopify/carrier-service/register/[installationId]/route.ts`)
- **Authenticated Registration**: Uses JWT for secure API calls
- **Dynamic Callback URLs**: Generates URLs with JWT tokens
- **Metafield Updates**: Stores carrier service details
- **Error Handling**: Comprehensive error messages and status codes

### 5. App Container Integration
- **Context Provider**: Sets global user/org context for JWT generation
- **Authentication Ready**: Automatically provides context to embedded apps
- **Session Management**: Handles user and workspace context

## Security Features

### JWT Token Security
- **Shared Secret**: Uses `JWT_APP_SECRET_KEY` environment variable
- **Token Expiration**: 5-minute expiration prevents token reuse
- **Audience/Issuer Validation**: Prevents token misuse
- **Installation Scoping**: Tokens are scoped to specific app installations

### Shopify Integration Security
- **HMAC Validation**: Verifies webhook signatures from Shopify
- **Token Encryption**: Access tokens encrypted before storage
- **Credential Isolation**: Each installation has separate credentials
- **Environment Fallback**: Supports both env vars and manual credentials

## Installation Flow

### 1. App Installation
```typescript
// User installs app from app store
const result = await installApp.mutateAsync({
  app_id: 'shopify',
  access_scopes: [],
  metadata: {},
});
```

### 2. API Key Generation
```typescript
// API key is auto-generated during installation
// Can be rotated or recreated as needed
await rotateAppApiKey.mutateAsync(installationId);
```

### 3. Credential Configuration
- Environment variables (for shared apps)
- Manual entry (for private apps)
- Secure storage in encrypted metafields

### 4. OAuth Authorization
```typescript
// Redirect to OAuth authorization
window.location.href = `/api/apps/shopify/oauth/authorize?installation_id=${installationId}`;
```

### 5. Carrier Service Registration
```typescript
// Register carrier service with authenticated API
const response = await apiClient.post(
  `/api/apps/shopify/carrier-service/register/${installationId}`,
  { installationId }
);
```

## API Endpoints Summary

| Endpoint | Method | Purpose | Authentication |
|----------|--------|---------|----------------|
| `/api/apps/shopify/oauth/authorize` | GET | Initiate OAuth flow | None |
| `/api/apps/shopify/oauth/callback` | GET | Handle OAuth callback | None |
| `/api/apps/shopify/carrier-service/register/[id]` | POST | Register carrier service | JWT |
| `/api/apps/shopify/carrier-service/rates/[id]` | POST | Live shipping rates | JWT |
| `/api/apps/shopify/test-connection/[id]` | POST | Test Shopify connection | JWT |

## Environment Variables

```bash
# JWT Authentication
JWT_APP_SECRET_KEY=your-jwt-secret-key

# Shopify App Credentials (optional - can be set per installation)
SHOPIFY_APP_KEY=your-shopify-app-key
SHOPIFY_APP_SECRET=your-shopify-app-secret

# Karrio API
KARRIO_API_URL=https://api.karrio.io
KARRIO_BASE_URL=https://your-karrio-instance.com
```

## Testing

### Backend Tests
- JWT authentication flow validation
- Token expiration handling
- Installation context verification
- API endpoint security testing

### Frontend Integration
- OAuth flow testing
- Carrier service registration
- Live rate calculation
- Error handling and user feedback

## Key Benefits

1. **Session-Independent**: Apps work without user sessions (perfect for webhooks)
2. **Secure**: Cryptographically signed tokens with expiration
3. **Scalable**: Each installation has its own context and credentials
4. **Flexible**: Supports both environment variables and manual credentials
5. **Complete**: Full OAuth flow, carrier service, and live rates
6. **Modern UI**: Beautiful components with proper loading and error states

## Next Steps

1. **Production Deployment**: Deploy with proper environment variables
2. **Monitoring**: Add logging and monitoring for webhook endpoints
3. **Testing**: Comprehensive testing with real Shopify stores
4. **Documentation**: User-facing setup guides and troubleshooting
5. **Extensions**: Additional Shopify features (fulfillment, tracking, etc.)

This implementation provides a complete, production-ready Shopify integration with modern authentication patterns and security best practices.
