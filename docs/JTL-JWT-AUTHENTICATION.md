# JTL JWT Authentication Guide

This guide explains how to authenticate with the JTL Karrio Shipping Platform using custom JWT tokens. This method allows external systems (like JTL WAWI) to authenticate users without storing passwords.

## Table of Contents

- [Overview](#overview)
- [JWT Token Structure](#jwt-token-structure)
- [Generating JWT Tokens](#generating-jwt-tokens)
- [Using JWT Tokens](#using-jwt-tokens)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)

---

## Overview

The JTL Karrio platform supports custom JWT authentication using HS256 symmetric encryption. This authentication method requires:

1. **Pre-registered users**: Users must be registered via the [JTL Tenant Registration](./JTL-TENANT-REGISTRATION.md) process
2. **Shared secret**: A `JWT_SECRET` known by both JTL WAWI and Karrio
3. **Valid JWT tokens**: Tokens containing the required claims and properly signed

---

## JWT Token Structure

### Header

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### Payload

```json
{
  "tenantId": "23fea40b-5ec7-409a-b7f3-6fa8ed5b2d48",
  "userId": "12ded597-1967-4f7d-84df-c4566c8754aa",
  "iss": "jtl-wawi-api",
  "exp": 1792104666
}
```

### Required Claims

- **`tenantId`**: Your JTL tenant UUID (must match registration)
- **`userId`**: Your JTL user UUID (must match registration)
- **`iss`**: Must be exactly `"jtl-wawi-api"`
- **`exp`**: Token expiration timestamp (Unix timestamp)

---

## Generating JWT Tokens

### Using jwt.io (Web Interface)

1. Go to [https://jwt.io](https://jwt.io)

2. In the **ALGORITHM** dropdown, select **HS256**

3. In the **HEADER** section, paste:
   ```json
   {
     "alg": "HS256",
     "typ": "JWT"
   }
   ```

4. In the **PAYLOAD** section, paste (replace with your values):
   ```json
   {
     "tenantId": "your-tenant-uuid",
     "userId": "your-user-uuid",
     "iss": "jtl-wawi-api",
     "exp": 1792104666
   }
   ```

5. In the **VERIFY SIGNATURE** section:
   - Keep the encoding as **UTF-8**
   - Enter the shared `JWT_SECRET` (contact your administrator)

6. Copy the generated token from the **Encoded** section

### Using Command Line (Bash)

```bash
#!/bin/bash

# Configuration
TENANT_ID="your-tenant-uuid"
USER_ID="your-user-uuid"
JWT_SECRET="your-jwt-secret"
EXP=$(($(date +%s) + 31536000))  # 1 year from now

# Helper functions
base64url() { openssl base64 -e -A | tr '+/' '-_' | tr -d '='; }
hmac_sha256() { echo -n "$2" | openssl dgst -binary -sha256 -mac HMAC -macopt hexkey:"$(echo -n "$1" | xxd -p -c 256)" | base64url; }

# Generate JWT
HEADER='{"alg":"HS256","typ":"JWT"}'
PAYLOAD="{\"tenantId\":\"${TENANT_ID}\",\"userId\":\"${USER_ID}\",\"iss\":\"jtl-wawi-api\",\"exp\":${EXP}}"
HEADER_B64=$(echo -n "$HEADER" | base64url)
PAYLOAD_B64=$(echo -n "$PAYLOAD" | base64url)
UNSIGNED="${HEADER_B64}.${PAYLOAD_B64}"
SIGNATURE=$(hmac_sha256 "$JWT_SECRET" "$UNSIGNED")
JWT="${UNSIGNED}.${SIGNATURE}"

echo "JWT Token:"
echo "$JWT"
```

### Using Python

```python
import jwt
import time

# Configuration
TENANT_ID = "your-tenant-uuid"
USER_ID = "your-user-uuid"
JWT_SECRET = "your-jwt-secret"

# Generate token
payload = {
    "tenantId": TENANT_ID,
    "userId": USER_ID,
    "iss": "jtl-wawi-api",
    "exp": int(time.time()) + 31536000  # 1 year from now
}

token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
print(f"JWT Token: {token}")
```

### Using Node.js

```javascript
const jwt = require('jsonwebtoken');

// Configuration
const TENANT_ID = "your-tenant-uuid";
const USER_ID = "your-user-uuid";
const JWT_SECRET = "your-jwt-secret";

// Generate token
const payload = {
    tenantId: TENANT_ID,
    userId: USER_ID,
    iss: "jtl-wawi-api",
    exp: Math.floor(Date.now() / 1000) + (365 * 24 * 60 * 60) // 1 year from now
};

const token = jwt.sign(payload, JWT_SECRET, { algorithm: 'HS256' });
console.log(`JWT Token: ${token}`);
```

---

## Using JWT Tokens

### Basic API Authentication

Use the JWT token in the `Authorization` header with `Bearer` prefix:

```bash
curl https://api.jtl.karrio.co/graphql \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ user { email full_name } }"}'
```

### Testing Authentication

Verify your token works with a simple user query:

```bash
curl https://api.jtl.karrio.co/graphql \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ user { email } }"}'
```

**Expected Response:**
```json
{
  "data": {
    "user": {
      "email": "your@email.com"
    }
  }
}
```

### Accessing Shipping Methods

```bash
curl https://api.jtl.karrio.co/graphql \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ shipping_methods { edges { node { id carrier_code service_code } } } }"}'
```

### Using with REST API

JWT tokens also work with REST endpoints:

```bash
# Get carrier references
curl https://api.jtl.karrio.co/v1/references \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Get user profile
curl https://api.jtl.karrio.co/v1/user \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## Token Expiration

### Setting Expiration Time

The `exp` claim determines when the token expires and must be a Unix timestamp (seconds since epoch).

**Calculate expiration times:**

```bash
# Current time
date +%s

# 1 hour from now
echo $(($(date +%s) + 3600))

# 1 day from now
echo $(($(date +%s) + 86400))

# 1 week from now
echo $(($(date +%s) + 604800))

# 1 year from now
echo $(($(date +%s) + 31536000))
```

### Token Refresh Strategy

JWT tokens cannot be refreshed like session-based tokens. When a token expires:

1. **Generate a new token** with a fresh expiration time
2. **Use short-lived tokens** for better security (1-24 hours)
3. **Implement automatic renewal** in your application before expiration

---

## Security Considerations

### Critical Security Requirements

⚠️ **IMPORTANT SECURITY NOTES:**

1. **Secret Management**
   - The `JWT_SECRET` must be kept strictly confidential
   - Share the secret only between authorized JTL WAWI and Karrio instances
   - Use environment variables or secure key management systems
   - Never commit secrets to version control

2. **Token Security**
   - JWT tokens grant full access to the user account
   - Treat tokens like passwords - never log or expose them
   - Use HTTPS for all API requests to prevent token interception

3. **Expiration Policy**
   - Set appropriate expiration times based on security requirements
   - Shorter expiration times (1-24 hours) are more secure
   - Consider automatic token rotation for production systems

4. **Transport Security**
   - Always use HTTPS/TLS for API communication
   - Never send tokens over unencrypted connections
   - Validate SSL certificates in production

### Best Practices

- **Environment-specific secrets**: Use different `JWT_SECRET` values for development, staging, and production
- **Logging**: Never log JWT tokens in application logs
- **Storage**: Store tokens securely in your application (encrypted storage, secure memory)
- **Validation**: Always validate token expiration and signature before use
- **Monitoring**: Monitor for suspicious authentication patterns

---

## Troubleshooting

### Authentication Errors

**"Invalid token"**
- ✅ Verify the `JWT_SECRET` matches the server configuration
- ✅ Check that all required claims are present (`tenantId`, `userId`, `iss`, `exp`)
- ✅ Ensure `iss` is exactly `"jtl-wawi-api"` (case-sensitive)
- ✅ Validate the token signature using [jwt.io](https://jwt.io)

**"Token has expired"**
- ✅ Generate a new token with a future `exp` timestamp
- ✅ Check that your system clock is accurate
- ✅ Ensure the expiration time is in seconds (Unix timestamp)

**"User not found"**
- ✅ Complete registration first using the [JTL Tenant Registration](./JTL-TENANT-REGISTRATION.md) process
- ✅ Verify `tenantId` and `userId` match your registration exactly
- ✅ Check that the user account is active and not suspended

**"Invalid issuer"**
- ✅ Ensure the `iss` claim is exactly `"jtl-wawi-api"`
- ✅ Check for extra whitespace or different casing

### Token Validation

Use [jwt.io](https://jwt.io) to debug token issues:

1. Paste your token in the "Encoded" section
2. Verify the header and payload are correct
3. Enter your `JWT_SECRET` in the signature section
4. Check that the signature shows "✅ Signature Verified"

### Network Issues

**Connection refused / timeout**
- ✅ Verify the API endpoint URL: `https://api.jtl.karrio.co`
- ✅ Check your network connectivity and firewall settings
- ✅ Ensure you're using HTTPS, not HTTP

**SSL/TLS errors**
- ✅ Verify SSL certificate validity
- ✅ Update your HTTP client to support modern TLS versions
- ✅ Check for corporate proxy or firewall interference

---

## Complete Example

Here's a complete workflow for generating and using a JWT token:

```bash
#!/bin/bash

# Step 1: Configuration (replace with your values)
TENANT_ID="23fea40b-5ec7-409a-b7f3-6fa8ed5b2d48"
USER_ID="12ded597-1967-4f7d-84df-c4566c8754aa"
JWT_SECRET="your-jwt-secret"
API_URL="https://api.jtl.karrio.co"

# Step 2: Generate JWT token
EXP=$(($(date +%s) + 86400))  # 24 hours from now
base64url() { openssl base64 -e -A | tr '+/' '-_' | tr -d '='; }
hmac_sha256() { echo -n "$2" | openssl dgst -binary -sha256 -mac HMAC -macopt hexkey:"$(echo -n "$1" | xxd -p -c 256)" | base64url; }

HEADER='{"alg":"HS256","typ":"JWT"}'
PAYLOAD="{\"tenantId\":\"${TENANT_ID}\",\"userId\":\"${USER_ID}\",\"iss\":\"jtl-wawi-api\",\"exp\":${EXP}}"
HEADER_B64=$(echo -n "$HEADER" | base64url)
PAYLOAD_B64=$(echo -n "$PAYLOAD" | base64url)
UNSIGNED="${HEADER_B64}.${PAYLOAD_B64}"
SIGNATURE=$(hmac_sha256 "$JWT_SECRET" "$UNSIGNED")
JWT="${UNSIGNED}.${SIGNATURE}"

echo "Generated JWT Token:"
echo "$JWT"
echo ""

# Step 3: Test authentication
echo "Testing authentication..."
RESPONSE=$(curl -s "$API_URL/graphql" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ user { email full_name } }"}')

echo "Response:"
echo "$RESPONSE" | jq .

# Step 4: Test shipping methods access
echo ""
echo "Testing shipping methods access..."
METHODS_RESPONSE=$(curl -s "$API_URL/graphql" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ shipping_methods { edges { node { id carrier_code service_code } } } }"}')

echo "Shipping Methods:"
echo "$METHODS_RESPONSE" | jq .
```

---

## API Reference

For complete API documentation, visit:
- **OpenAPI Documentation**: [https://api.jtl.karrio.co/openapi](https://api.jtl.karrio.co/openapi)
- **GraphQL Playground**: [https://api.jtl.karrio.co/graphql](https://api.jtl.karrio.co/graphql)

---

*Last Updated: October 2025*