# JTL Hub OAuth Authentication - Complete Documentation

> **Purpose**: Understanding JTL Hub's OAuth 2.0 authentication system, available APIs, and what you can accomplish with JTL Hub OAuth credentials.

This document is based on the official JTL Hub Demo Sample and describes the complete OAuth authentication flows and available capabilities.

---

## Table of Contents

1. [Overview](#overview)
2. [OAuth 2.0 Flows](#oauth-20-flows)
3. [JWT Token Structure](#jwt-token-structure)
4. [Authentication Patterns](#authentication-patterns)
5. [JWKS Public Key Verification](#jwks-public-key-verification)
6. [Available APIs](#available-apis)
7. [AppBridge (Embedded Apps)](#appbridge-embedded-apps)
8. [Environment Endpoints](#environment-endpoints)
9. [Code Examples](#code-examples)

---

## Overview

JTL Hub provides OAuth 2.0 authentication for third-party applications. With a CLIENT_ID and CLIENT_SECRET pair, you can:

1. **Authenticate Users**: Let users sign in with their JTL Hub account
2. **Access JTL APIs**: Call JTL Hub APIs on behalf of users or your application
3. **Embed Apps**: Run your app inside JTL Hub as an embedded iframe
4. **Verify Tokens**: Validate user session tokens using EdDSA signatures

### What You Get with CLIENT_ID/CLIENT_SECRET

- **CLIENT_ID**: Public identifier for your application (safe to expose in frontend)
- **CLIENT_SECRET**: Secret key for server-to-server authentication (NEVER expose in frontend)

---

## OAuth 2.0 Flows

JTL Hub supports two primary OAuth 2.0 flows:

### 1. Implicit Flow (Frontend - User Authentication)

**Use Case**: User sign-in, returns JWT directly to browser

**Flow Diagram**:
```
User → Your App → JTL Hub Login → Redirect with JWT → Your App
```

**Authorization Request**:
```
GET https://auth.jtl-cloud.com/oauth/authorize?
  client_id=YOUR_CLIENT_ID
  &response_type=token
  &redirect_uri=https://your-app.com/callback
  &state=random-string-for-csrf
  &scope=openid profile
```

**Parameters**:
- `client_id`: Your application's CLIENT_ID
- `response_type`: `token` (implicit flow - returns JWT directly)
- `redirect_uri`: Where to send user after authentication (must be registered)
- `state`: Random string for CSRF protection (recommended)
- `scope`: Requested permissions (`openid profile` for basic user info)

**Response** (redirect to your callback URL):
```
https://your-app.com/callback?
  token=eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9...
  &state=random-string-for-csrf
```

The `token` is a JWT that contains `userId` and `tenantId`.

### 2. Client Credentials Flow (Backend - Machine-to-Machine)

**Use Case**: Server-to-server API calls without user context

**Request**:
```http
POST https://auth.jtl-cloud.com/oauth2/token
Content-Type: application/x-www-form-urlencoded
Authorization: Basic base64(CLIENT_ID:CLIENT_SECRET)

grant_type=client_credentials
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

This token can be used to call JTL Hub APIs on behalf of your application.

---

## JWT Token Structure

JTL Hub uses **EdDSA (Ed25519)** algorithm for JWT signatures.

### Session Token (User Authentication)

**Header**:
```json
{
  "alg": "EdDSA",
  "typ": "JWT",
  "kid": "key-id-12345"
}
```

**Payload**:
```json
{
  "userId": "550e8400-e29b-41d4-a716-446655440000",
  "tenantId": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "iss": "https://auth.jtl-cloud.com",
  "exp": 1735750000
}
```

**Important Notes**:
- ❌ **No email** in token payload
- ❌ **No username** in token payload
- ❌ **No aud (audience)** claim
- ✅ Only `userId`, `tenantId`, `iss`, and `exp` are guaranteed
- ✅ Algorithm is **EdDSA** (Ed25519 curve), not RS256 or HS256

### Client Credentials Token (Machine-to-Machine)

Similar structure but used for API authentication, not user identity.

---

## Authentication Patterns

JTL Hub supports two application patterns:

### Pattern 1: Standalone Application

Your app runs on its own domain (e.g., `https://your-app.com`).

**Flow**:
1. Redirect user to JTL Hub OAuth
2. User authenticates
3. JTL Hub redirects back with JWT
4. Your backend verifies JWT
5. Your backend creates its own session

**Best For**: SaaS applications, independent services

### Pattern 2: Embedded Application (AppBridge)

Your app runs inside JTL Hub as an iframe.

**Flow**:
1. JTL Hub loads your app in iframe
2. Your app uses AppBridge to communicate with JTL Hub
3. Call `appBridge.method.call('getSessionToken')` to get JWT
4. Send JWT to your backend for verification
5. Backend verifies and processes

**Best For**: Apps deeply integrated with JTL Hub UI

---

## JWKS Public Key Verification

JTL Hub uses **JWKS (JSON Web Key Set)** for public key distribution.

### JWKS Endpoint

```
https://auth.jtl-cloud.com/.well-known/jwks.json
```

**Response**:
```json
{
  "keys": [
    {
      "kty": "OKP",
      "use": "sig",
      "kid": "key-id-12345",
      "alg": "EdDSA",
      "crv": "Ed25519",
      "x": "base64-encoded-public-key-here"
    }
  ]
}
```

### Key Details

- **Algorithm**: EdDSA (Edwards-curve Digital Signature Algorithm)
- **Curve**: Ed25519
- **Key Type**: OKP (Octet string Key Pairs)
- **Use**: Signature verification only

### Why JWKS?

1. **Key Rotation**: JTL Hub can rotate keys without app updates
2. **Security**: No need to hardcode public keys
3. **Standard**: Industry-standard approach (used by Google, Auth0, etc.)
4. **Multiple Keys**: Can have multiple valid keys simultaneously during rotation

### Verifying a Token

**Step 1**: Fetch JWKS from endpoint
**Step 2**: Find key matching `kid` in JWT header
**Step 3**: Import public key from JWKS
**Step 4**: Verify JWT signature with public key
**Step 5**: Validate `iss` (issuer) and `exp` (expiration)

---

## Available APIs

Once authenticated, you can access JTL Hub APIs using the access token.

### 1. Account API (JWKS Endpoint)

**Endpoint**: `https://api.jtl-cloud.com/account/.well-known/jwks.json`

**Authentication**: Bearer token from client credentials flow

**Purpose**: Fetch public keys for JWT verification

**Example**:
```http
GET https://api.jtl-cloud.com/account/.well-known/jwks.json
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### 2. ERP API

**Base URL**: `https://api.jtl-cloud.com/erp`

**Authentication**: Bearer token + `X-Tenant-ID` header

**Purpose**: Access JTL WAWI (ERP) data for a specific tenant

**Example Request**:
```http
GET https://api.jtl-cloud.com/erp/orders
Authorization: Bearer YOUR_ACCESS_TOKEN
X-Tenant-ID: 7c9e6679-7425-40de-944b-e07fc1f90ae7
Content-Type: application/json
```

**Headers Required**:
- `Authorization`: Bearer token from client credentials flow
- `X-Tenant-ID`: The tenant ID from user's session token

**Available Endpoints** (examples from demo):
- `GET /erp/{endpoint}` - Read data
- `POST /erp/{endpoint}` - Create data
- `PUT /erp/{endpoint}` - Update data
- `PATCH /erp/{endpoint}` - Partial update
- `DELETE /erp/{endpoint}` - Delete data

**Note**: Specific endpoints depend on what JTL Hub exposes. The demo sample shows a proxy pattern where you can call various ERP endpoints dynamically.

---

## AppBridge (Embedded Apps)

For apps running inside JTL Hub as iframes, use the AppBridge library.

### Installation

```bash
npm install @jtl-software/cloud-apps-core
```

### Basic Usage

```typescript
import { AppBridge } from '@jtl-software/cloud-apps-core';

// AppBridge is automatically available in embedded context
const appBridge = new AppBridge();
```

### Getting Session Token

```typescript
// Request session token from JTL Hub
const sessionToken = await appBridge.method.call('getSessionToken');

// sessionToken is a JWT containing userId and tenantId
console.log('Session Token:', sessionToken);
```

### Completing Setup Flow

When user first installs your app:

```typescript
// After your setup/onboarding is complete
await appBridge.method.call('setupCompleted');
```

This tells JTL Hub that your app is ready to use.

### AppBridge Methods

From the demo sample, available methods:

1. **`getSessionToken()`**: Get current user's JWT
2. **`setupCompleted()`**: Signal that app setup is complete

**Note**: Additional methods may be available - check JTL Hub documentation.

### AppBridge App Structure

```typescript
// Main app component
const App: React.FC<{ appBridge: AppBridge }> = ({ appBridge }) => {
  // Your app receives appBridge as prop
  // Use it to communicate with JTL Hub

  return (
    <YourAppContent />
  );
};
```

### Modes/Routes

JTL Hub can load your app in different modes:

- `/setup` - Initial app setup/installation
- `/erp` - Main ERP integration view
- `/pane` - Side panel view
- Custom modes as configured in your app manifest

---

## Environment Endpoints

JTL Hub has multiple environments for development and testing.

### Production

- **Auth**: `https://auth.jtl-cloud.com`
- **API**: `https://api.jtl-cloud.com`
- **JWKS**: `https://auth.jtl-cloud.com/.well-known/jwks.json`
- **OAuth**: `https://auth.jtl-cloud.com/oauth/authorize`
- **Token**: `https://auth.jtl-cloud.com/oauth2/token`

### Beta

- **Auth**: `https://auth.beta.jtl-cloud.com`
- **API**: `https://api.beta.jtl-cloud.com`
- **JWKS**: `https://auth.beta.jtl-cloud.com/.well-known/jwks.json`
- **OAuth**: `https://auth.beta.jtl-cloud.com/oauth/authorize`
- **Token**: `https://auth.beta.jtl-cloud.com/oauth2/token`

### Dev

- **Auth**: `https://auth.dev.jtl-cloud.com`
- **API**: `https://api.dev.jtl-cloud.com`
- **JWKS**: `https://auth.dev.jtl-cloud.com/.well-known/jwks.json`
- **OAuth**: `https://auth.dev.jtl-cloud.com/oauth/authorize`
- **Token**: `https://auth.dev.jtl-cloud.com/oauth2/token`

### QA

- **Auth**: `https://auth.qa.jtl-cloud.com`
- **API**: `https://api.qa.jtl-cloud.com`
- **JWKS**: `https://auth.qa.jtl-cloud.com/.well-known/jwks.json`
- **OAuth**: `https://auth.qa.jtl-cloud.com/oauth/authorize`
- **Token**: `https://auth.qa.jtl-cloud.com/oauth2/token`

---

## Code Examples

### Example 1: Client Credentials Flow (Node.js/TypeScript)

```typescript
async function getJwtToken(
  clientId: string,
  clientSecret: string,
  environment: 'prod' | '.beta' | '.dev' | '.qa' = 'prod'
): Promise<string> {
  // Encode credentials
  const authString = Buffer.from(`${clientId}:${clientSecret}`).toString('base64');

  // Determine auth endpoint
  const authEndpoint = environment === 'prod' || environment === '.beta'
    ? 'https://auth.jtl-cloud.com/oauth2/token'
    : `https://auth${environment}.jtl-cloud.com/oauth2/token`;

  // Request token
  const response = await fetch(authEndpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      Authorization: `Basic ${authString}`,
    },
    body: new URLSearchParams({
      grant_type: 'client_credentials',
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(`Failed to get JWT: ${error.error}`);
  }

  const data = await response.json();
  return data.access_token;
}
```

### Example 2: Fetch JWKS and Verify Token (Node.js/TypeScript)

```typescript
import { createRemoteJWKSet, jwtVerify } from 'jose';

async function verifySessionToken(sessionToken: string): Promise<any> {
  // Create JWKS fetcher (automatically caches keys)
  const JWKS = createRemoteJWKSet(
    new URL('https://auth.jtl-cloud.com/.well-known/jwks.json')
  );

  // Verify token
  const { payload, protectedHeader } = await jwtVerify(sessionToken, JWKS, {
    issuer: 'https://auth.jtl-cloud.com',
  });

  console.log('✅ Token is valid');
  console.log('Header:', protectedHeader);
  console.log('Payload:', payload);

  return payload;
}
```

### Example 3: Fetch JWKS Manually (Node.js/TypeScript)

```typescript
async function fetchJwksAndVerifyToken(sessionToken: string): Promise<any> {
  // Step 1: Get client credentials token
  const jwt = await getJwtToken(clientId, clientSecret);

  // Step 2: Fetch JWKS
  const jwksResponse = await fetch(
    'https://api.jtl-cloud.com/account/.well-known/jwks.json',
    {
      headers: {
        Authorization: `Bearer ${jwt}`,
      },
    }
  );
  const jwks = await jwksResponse.json();

  // Step 3: Get the public key
  const key = jwks.keys[0]; // Get first key

  // Step 4: Import key for verification
  const publicKey = await importJWK(key, 'EdDSA');

  // Step 5: Verify token
  const { payload } = await jwtVerify(sessionToken, publicKey);

  return payload;
}
```

### Example 4: Call ERP API (Node.js/TypeScript)

```typescript
async function callErpApi(
  tenantId: string,
  endpoint: string,
  clientId: string,
  clientSecret: string
): Promise<any> {
  // Get access token
  const accessToken = await getJwtToken(clientId, clientSecret);

  // Call ERP API
  const response = await fetch(`https://api.jtl-cloud.com/erp/${endpoint}`, {
    headers: {
      'X-Tenant-ID': tenantId,
      Authorization: `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`ERP API error: ${response.status}`);
  }

  return await response.json();
}

// Usage
const data = await callErpApi(
  '7c9e6679-7425-40de-944b-e07fc1f90ae7',
  'orders',
  'your-client-id',
  'your-client-secret'
);
```

### Example 5: AppBridge Setup Page (React/TypeScript)

```typescript
import { AppBridge } from '@jtl-software/cloud-apps-core';
import { useState } from 'react';

interface SetupPageProps {
  appBridge: AppBridge;
}

const SetupPage: React.FC<SetupPageProps> = ({ appBridge }) => {
  const [isLoading, setIsLoading] = useState(false);

  const handleSetup = async () => {
    try {
      setIsLoading(true);

      // Get session token
      const sessionToken = await appBridge.method.call('getSessionToken');

      // Send to your backend for verification
      const response = await fetch('https://your-api.com/connect-tenant', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ sessionToken }),
      });

      if (response.ok) {
        // Tell JTL Hub setup is complete
        await appBridge.method.call('setupCompleted');
      }
    } catch (error) {
      console.error('Setup failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <h1>Connect Your Account</h1>
      <button onClick={handleSetup} disabled={isLoading}>
        {isLoading ? 'Connecting...' : 'Connect'}
      </button>
    </div>
  );
};
```

### Example 6: Backend Token Verification (Express.js)

```typescript
import express from 'express';
import { createRemoteJWKSet, jwtVerify } from 'jose';

const app = express();
app.use(express.json());

// Middleware to verify JTL Hub tokens
async function verifyJtlToken(req, res, next) {
  try {
    const authHeader = req.headers.authorization || '';
    const token = authHeader.startsWith('Bearer ') ? authHeader.slice(7) : null;

    if (!token) {
      return res.status(401).json({ error: 'No token provided' });
    }

    // Verify using JWKS
    const JWKS = createRemoteJWKSet(
      new URL('https://auth.jtl-cloud.com/.well-known/jwks.json')
    );

    const { payload } = await jwtVerify(token, JWKS, {
      issuer: 'https://auth.jtl-cloud.com',
    });

    // Attach user info to request
    req.user = {
      userId: payload.userId,
      tenantId: payload.tenantId,
    };

    next();
  } catch (err) {
    console.error('Token verification failed:', err);
    res.status(401).json({ error: 'Invalid or expired token' });
  }
}

// Protected endpoint
app.get('/api/protected', verifyJtlToken, (req, res) => {
  res.json({
    message: 'Access granted',
    user: req.user,
  });
});

// Endpoint for embedded apps to connect tenant
app.post('/connect-tenant', async (req, res) => {
  const { sessionToken } = req.body;

  // Verify session token
  const JWKS = createRemoteJWKSet(
    new URL('https://auth.jtl-cloud.com/.well-known/jwks.json')
  );

  const { payload } = await jwtVerify(sessionToken, JWKS, {
    issuer: 'https://auth.jtl-cloud.com',
  });

  // Store mapping between your app's tenant ID and JTL tenant ID
  const myTenantId = new Date().getTime().toString();
  myDatabase.set(myTenantId, payload.tenantId);

  res.json({
    success: true,
    tenantId: myTenantId,
    jtlTenantId: payload.tenantId,
  });
});
```

### Example 7: Python Token Verification

```python
import jwt
from jwt import PyJWKClient

def verify_jtl_token(token: str) -> dict:
    """
    Verify JTL Hub JWT token using JWKS.

    Args:
        token: JWT token from JTL Hub

    Returns:
        Decoded token payload with userId and tenantId
    """
    # Fetch JWKS
    jwks_client = PyJWKClient('https://auth.jtl-cloud.com/.well-known/jwks.json')

    # Get signing key
    signing_key = jwks_client.get_signing_key_from_jwt(token)

    # Verify and decode
    payload = jwt.decode(
        token,
        signing_key.key,
        algorithms=['EdDSA'],
        issuer='https://auth.jtl-cloud.com',
        options={'verify_aud': False}  # JTL Hub doesn't include aud claim
    )

    return payload

# Usage
try:
    payload = verify_jtl_token(session_token)
    user_id = payload['userId']
    tenant_id = payload['tenantId']
    print(f"✅ Token valid - User: {user_id}, Tenant: {tenant_id}")
except jwt.InvalidTokenError as e:
    print(f"❌ Token invalid: {e}")
```

### Example 8: Python Client Credentials Flow

```python
import base64
import requests

def get_jtl_access_token(client_id: str, client_secret: str) -> str:
    """
    Get access token using client credentials flow.

    Args:
        client_id: Your JTL Hub CLIENT_ID
        client_secret: Your JTL Hub CLIENT_SECRET

    Returns:
        Access token for API calls
    """
    # Encode credentials
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = base64.b64encode(auth_string.encode('utf-8'))
    auth_header = f"Basic {auth_bytes.decode('utf-8')}"

    # Request token
    response = requests.post(
        'https://auth.jtl-cloud.com/oauth2/token',
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': auth_header,
        },
        data={'grant_type': 'client_credentials'}
    )

    response.raise_for_status()
    return response.json()['access_token']

# Usage
access_token = get_jtl_access_token('your-client-id', 'your-client-secret')
print(f"Access Token: {access_token[:20]}...")
```

---

## Security Best Practices

### 1. Never Expose CLIENT_SECRET

❌ **Bad** (Frontend):
```javascript
const clientSecret = 'your-secret'; // NEVER do this!
```

✅ **Good** (Backend only):
```javascript
// Server-side only
const clientSecret = process.env.CLIENT_SECRET;
```

### 2. Always Use HTTPS in Production

❌ **Bad**:
```
http://your-app.com/callback
```

✅ **Good**:
```
https://your-app.com/callback
```

### 3. Validate State Parameter

```typescript
// Generate state
const state = crypto.randomBytes(16).toString('hex');
sessionStorage.setItem('oauth_state', state);

// Verify on callback
const returnedState = params.get('state');
if (returnedState !== sessionStorage.getItem('oauth_state')) {
  throw new Error('CSRF attack detected');
}
```

### 4. Verify Token Issuer

```typescript
await jwtVerify(token, JWKS, {
  issuer: 'https://auth.jtl-cloud.com', // Always verify issuer
});
```

### 5. Check Token Expiration

```typescript
const { payload } = await jwtVerify(token, JWKS, {
  // jose automatically checks exp claim
});

// Or manually check
if (Date.now() >= payload.exp * 1000) {
  throw new Error('Token expired');
}
```

---

## What You Can Accomplish with CLIENT_ID/CLIENT_SECRET

### 1. User Authentication
- Let users sign in with JTL Hub account
- Get userId and tenantId for each user
- No need to manage passwords

### 2. Access JTL ERP Data
- Read orders, products, customers from JTL WAWI
- Create and update ERP data
- Sync data between your app and JTL

### 3. Multi-Tenant Applications
- Automatically isolate data by tenantId
- Each JTL organization is a separate tenant
- Scale to many JTL customers

### 4. Embedded Experiences
- Run your app inside JTL Hub
- Seamless user experience
- Access JTL Hub context and data

### 5. Webhook Processing
- Verify webhook signatures from JTL Hub
- Process real-time events
- Keep data in sync

---

## Troubleshooting

### "Invalid signature" Error

**Cause**: Token signed with different key or wrong algorithm

**Solution**:
1. Ensure you're using EdDSA algorithm (not RS256 or HS256)
2. Fetch latest JWKS from correct environment
3. Verify issuer matches token issuer

### "Token expired" Error

**Cause**: Token's `exp` claim is in the past

**Solution**:
1. Request new token from JTL Hub
2. Implement token refresh mechanism
3. Check server clock is synchronized

### "No kid in header" Error

**Cause**: JWT header missing `kid` (key ID)

**Solution**:
1. Ensure you're using correct JWT format
2. Token should come from JTL Hub OAuth flow
3. Check token is not corrupted

### CORS Errors with JWKS

**Cause**: Trying to fetch JWKS from frontend

**Solution**:
- JWKS should be fetched from backend
- Frontend should send token to backend for verification
- Backend verifies and returns session

---

## Summary

**Key Takeaways**:

1. ✅ JTL Hub uses **OAuth 2.0** with **EdDSA (Ed25519)** signatures
2. ✅ Two flows: **Implicit** (user auth) and **Client Credentials** (machine-to-machine)
3. ✅ Tokens contain only **userId** and **tenantId** (no email or username)
4. ✅ Use **JWKS** for dynamic public key fetching (handles key rotation)
5. ✅ **CLIENT_SECRET** must stay on backend - never expose to frontend
6. ✅ Verify **issuer** and **expiration** when validating tokens
7. ✅ AppBridge provides **getSessionToken()** for embedded apps
8. ✅ ERP API requires **Bearer token** + **X-Tenant-ID** header

**With CLIENT_ID/CLIENT_SECRET, you can**:
- ✅ Authenticate JTL Hub users
- ✅ Access JTL ERP/WAWI data
- ✅ Build multi-tenant applications
- ✅ Embed apps in JTL Hub
- ✅ Call JTL Hub APIs

---

## Additional Resources

- **Demo Sample**: `/Users/danielkobina/Workspace/jtl/transfer/FirstTalkWithDanAndMarcel/JTL-Hub-Demo-Sample`
- **JOSE Library**: https://github.com/panva/jose (recommended for JWT verification)
- **PyJWT Documentation**: https://pyjwt.readthedocs.io/
- **EdDSA/Ed25519**: https://ed25519.cr.yp.to/
- **OAuth 2.0 RFC**: https://tools.ietf.org/html/rfc6749

---

**Document Version**: 1.0
**Last Updated**: Based on JTL Hub Demo Sample analysis
**Author**: Generated from official JTL Hub Demo Sample
