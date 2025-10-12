# Karrio JTL Hub Integration

JTL Hub Single Sign-On (SSO) integration for Karrio shipping platform.

## Features

- JTL Hub OAuth authentication
- EdDSA (Ed25519) JWT verification
- Automatic user and organization provisioning
- Seamless SSO experience for JTL Hub users

## Installation

This module is part of the Karrio platform and is installed automatically when you install Karrio.

## Configuration

Add the following environment variables:

```bash
JTL_HUB_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"
JTL_HUB_OAUTH_AUTHORIZE_URL=https://auth.jtl-cloud.com/oauth/authorize
JTL_HUB_OAUTH_REDIRECT_URI=http://localhost:3000/auth/callback
```

## How It Works

1. User clicks "Sign in with JTL Hub" in the dashboard
2. User is redirected to JTL Hub for authentication
3. JTL Hub redirects back with a JWT token (EdDSA signed)
4. Backend validates the JWT using JTL Hub's public key
5. User and Organization are automatically created (if first login)
6. Karrio JWT is issued for API access

## Token Structure

JTL Hub tokens contain:

```json
{
  "userId": "<UUID>",
  "tenantId": "<UUID>",
  "kid": "<string>",
  "exp": 1234567890
}
```

## Mapping

- `userId` → Karrio `User.username` (format: `jtl-{userId}`)
- `tenantId` → Karrio `Organization.id`
- `kid` → Customer ID (used in org display name)

## License

Apache-2.0
