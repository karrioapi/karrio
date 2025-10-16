# JTL Tenant Registration Guide

This guide explains how to register with the JTL Karrio Shipping Platform using your JTL tenant and user identifiers.

## Table of Contents

- [Registration](#registration)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)

---

## Registration

### Prerequisites

- JTL Tenant ID (UUID format)
- JTL User ID (UUID format)
- Email address
- Password (minimum 8 characters)

### Registration Process

1. Navigate to [https://app.jtl.karrio.co/register](https://app.jtl.karrio.co/register)

2. Fill in the registration form:
   - **Tenant ID**: Your JTL tenant UUID (e.g., `23fea40b-5ec7-409a-b7f3-6fa8ed5b2d48`)
   - **User ID**: Your JTL user UUID (e.g., `12ded597-1967-4f7d-84df-c4566c8754aa`)
   - **Email**: Your email address for login
   - **Password**: Create a secure password (min. 8 characters)
   - **Confirm Password**: Re-enter your password

3. Click "Create Account"

4. After successful registration, you'll be redirected to the [sign-in page](https://app.jtl.karrio.co/signin)

![Registration Form](./registration-screenshot.png)

### Using the Registration API

You can also register programmatically via the API:

```bash
curl -X POST https://api.jtl.karrio.co/jtl/tenants/onboarding \
  -H "Content-Type: application/json" \
  -d '{
    "tenantId": "your-tenant-uuid",
    "userId": "your-user-uuid",
    "email": "your@email.com",
    "password": "your-password"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGci...",
  "refresh_token": "eyJhbGci...",
  "user": {
    "id": 2,
    "email": "your@email.com",
    "full_name": "Your Name"
  },
  "org": {
    "id": "org_...",
    "name": "Your Organization",
    "slug": "your-org-slug"
  },
  "org_user": {
    "id": "usr_...",
    "is_owner": true,
    "roles": ["member", "developer", "admin"]
  }
}
```

---

## Authentication

After successful registration, you can authenticate using JWT tokens. For detailed JWT authentication instructions, including token generation and usage, see the [JTL JWT Authentication Guide](./JTL-JWT-AUTHENTICATION.md).

---

## API Endpoints

### Base URLs

- **Frontend**: [https://app.jtl.karrio.co](https://app.jtl.karrio.co)
- **API**: [https://api.jtl.karrio.co](https://api.jtl.karrio.co)
- **OpenAPI Docs**: [https://api.jtl.karrio.co/openapi](https://api.jtl.karrio.co/openapi)

### Authentication Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/jtl/tenants/onboarding` | POST | Register a new JTL tenant |
| `/api/token` | POST | Login with email/password |
| `/api/token/refresh` | POST | Refresh access token |
| `/graphql` | POST | GraphQL API (requires auth) |

### Testing Your Registration

After registration, you can test authentication using JWT tokens. See the [JTL JWT Authentication Guide](./JTL-JWT-AUTHENTICATION.md) for detailed testing instructions.

---

## Troubleshooting

### Registration Issues

**"Organization not found"**
- Ensure you've completed registration first via `/jtl/tenants/onboarding`
- Check that tenantId and userId are correct UUIDs

### JWT Authentication Issues

For JWT authentication troubleshooting, see the [JTL JWT Authentication Guide](./JTL-JWT-AUTHENTICATION.md#troubleshooting).

### Getting Help

- **API Documentation**: [https://api.jtl.karrio.co/openapi](https://api.jtl.karrio.co/openapi)
- **Issues**: Contact your system administrator
- **JWT Debugging**: Use [jwt.io](https://jwt.io) to decode and verify tokens

---

## Quick Reference

### Complete Registration Flow

```bash
# Register tenant/user
curl -X POST https://api.jtl.karrio.co/jtl/tenants/onboarding \
  -H "Content-Type: application/json" \
  -d '{
    "tenantId": "23fea40b-5ec7-409a-b7f3-6fa8ed5b2d48",
    "userId": "12ded597-1967-4f7d-84df-c4566c8754aa",
    "email": "user@example.com",
    "password": "securepass123"
  }'
```

For JWT token generation and authentication examples, see the [JTL JWT Authentication Guide](./JTL-JWT-AUTHENTICATION.md#complete-example).

---

*Last Updated: October 2025*
