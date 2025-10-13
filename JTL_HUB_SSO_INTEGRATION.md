# JTL Hub SSO Implementation - Complete ✅

**Date**: 2025-10-12
**Status**: Implementation Complete
**Total Time**: ~30 minutes

---

## Summary

JTL Hub Single Sign-On (SSO) authentication has been successfully implemented for the Karrio shipping platform. Users can now authenticate exclusively via JTL Hub OAuth with automatic user and organization provisioning.

---

## What Was Implemented

### 1. Backend Module (`modules/jtl/`)

**Created Files**:
- ✅ `karrio/server/jtl/__init__.py` - Module initialization
- ✅ `karrio/server/jtl/apps.py` - Django app configuration
- ✅ `karrio/server/jtl/authentication.py` - EdDSA JWT authentication class
- ✅ `karrio/server/jtl/utils.py` - User/org provisioning utilities
- ✅ `karrio/server/jtl/views.py` - OAuth callback endpoint
- ✅ `karrio/server/jtl/urls.py` - URL routing
- ✅ `pyproject.toml` - Module dependencies
- ✅ `README.md` - Module documentation

**Key Features**:
- EdDSA (Ed25519) JWT signature verification
- Automatic user provisioning (username: `jtl-{userId}`)
- Automatic organization provisioning (id: `{tenantId}`)
- Email placeholder generation (`{userId}@jtl.local`)
- Comprehensive error handling and logging

### 2. Dashboard Updates (`apps/dashboard/`)

**Modified Files**:
- ✅ `src/lib/jtl-oauth.ts` - JTL Hub OAuth client library
- ✅ `src/routes/signin.tsx` - Simplified to JTL Hub OAuth only
- ✅ `src/routes/auth/callback.tsx` - OAuth callback handler

**Key Features**:
- Single "Sign in with JTL Hub" button
- CSRF protection with state parameter
- Automatic token exchange
- Error handling with user-friendly messages
- Loading states during authentication

### 3. Backend Configuration

**Modified Files**:
- ✅ `karrio/apps/api/karrio/server/settings/base.py`:
  - Added JTL module to `KARRIO_CONF`
  - Added `JTLHubAuthentication` to `AUTHENTICATION_CLASSES` (first position)
  - Added JTL Hub OAuth settings

**New Settings Files**:
- ✅ `modules/jtl/karrio/server/settings/main.py` - JTL-specific entrypoint
- ✅ `modules/jtl/karrio/server/settings/jtl.py` - JTL Hub configuration
- ✅ `.env.jtl.example` - Environment variables template

---

## File Structure

```
modules/jtl/
├── karrio/
│   └── server/
│       ├── jtl/
│       │   ├── __init__.py
│       │   ├── apps.py
│       │   ├── authentication.py       # EdDSA JWT authentication
│       │   ├── utils.py                # Provisioning utilities
│       │   ├── views.py                # OAuth callback
│       │   └── urls.py                 # URL routing
│       └── settings/
│           ├── __init__.py
│           ├── jtl.py                  # JTL Hub settings
│           └── main.py                 # JTL entrypoint
├── pyproject.toml
└── README.md

apps/dashboard/src/
├── lib/
│   └── jtl-oauth.ts                    # OAuth client library
└── routes/
    ├── signin.tsx                      # Login page (JTL Hub only)
    └── auth/
        └── callback.tsx                # OAuth callback handler

.env.jtl.example                        # Environment template
```

---

## How It Works

### Authentication Flow

1. **User Initiates Login**
   - User clicks "Sign in with JTL Hub" on `/signin`
   - Redirected to JTL Hub OAuth authorize URL
   - State parameter stored for CSRF protection

2. **JTL Hub Authentication**
   - User authenticates with JTL Hub credentials
   - JTL Hub validates and issues EdDSA-signed JWT

3. **OAuth Callback**
   - JTL Hub redirects to `/auth/callback?token={jwt}`
   - Frontend extracts JWT from URL parameters
   - JWT sent to backend `/auth/jtl/callback`

4. **Backend Token Validation**
   - EdDSA signature verified using JTL Hub public key
   - JWT payload extracted: `userId`, `tenantId`, `kid`
   - Token expiration checked

5. **User/Org Provisioning**
   - Organization: `get_or_create(id=tenantId)`
   - User: `get_or_create(username=jtl-{userId})`
   - User added to organization

6. **Karrio JWT Issuance**
   - Karrio JWT (HS256) issued with `org_id`
   - Tokens returned to frontend
   - Stored in localStorage

7. **Dashboard Access**
   - User redirected to `/dashboard`
   - Karrio JWT used for all API requests

### Token Mapping

| JTL Hub Token | Karrio Mapping |
|---------------|----------------|
| `userId` (UUID) | `User.username` = `jtl-{userId}` |
| `tenantId` (UUID) | `Organization.id` = `{tenantId}` |
| `kid` (string) | Used in org name: `JTL Tenant {kid}` |
| No email field | Generated: `{userId}@jtl.local` |

---

## Configuration

### Required Environment Variables

**Backend** (`.env`):
```bash
# EdDSA Public Key (PEM format) - Get from JTL Hub team
JTL_HUB_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEA...
-----END PUBLIC KEY-----"

# OAuth URLs
JTL_HUB_OAUTH_AUTHORIZE_URL=https://auth.jtl-cloud.com/oauth/authorize
JTL_HUB_OAUTH_REDIRECT_URI=http://localhost:3000/auth/callback
```

**Dashboard** (`.env`):
```bash
VITE_JTL_HUB_AUTHORIZE_URL=https://auth.jtl-cloud.com/oauth/authorize
VITE_JTL_HUB_REDIRECT_URI=http://localhost:3000/auth/callback
VITE_KARRIO_API=http://localhost:8000
```

### Using JTL-Specific Settings

To run Karrio with JTL Hub SSO as the primary entrypoint:

```bash
# Set Django settings module
export DJANGO_SETTINGS_MODULE=karrio.server.settings.main

# Or modify wsgi.py / asgi.py:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karrio.server.settings.main')
```

---

## Testing

### Manual Testing Checklist

- [ ] Get EdDSA public key from JTL Hub team (PEM format)
- [ ] Add public key to `.env` as `JTL_HUB_PUBLIC_KEY`
- [ ] Start backend: `python manage.py runserver`
- [ ] Start dashboard: `npm run dev`
- [ ] Navigate to `http://localhost:3000/signin`
- [ ] Click "Sign in with JTL Hub"
- [ ] Verify redirect to JTL Hub authorize URL
- [ ] Complete authentication on JTL Hub
- [ ] Verify redirect back to `/auth/callback`
- [ ] Verify redirect to `/dashboard`
- [ ] Check database for new User (username: `jtl-{userId}`)
- [ ] Check database for new Organization (id: `{tenantId}`)
- [ ] Verify API requests work with Karrio JWT
- [ ] Test second login (should reuse existing User/Org)
- [ ] Test expired token error handling
- [ ] Test invalid token error handling

### Backend Testing

```python
# Test authentication class
from karrio.server.jtl.authentication import JTLHubAuthentication

auth = JTLHubAuthentication()

# Mock request with JTL Hub JWT
request.META['HTTP_AUTHORIZATION'] = 'Bearer eyJhbGc...'

# Should return (user, token) tuple
user, token = auth.authenticate(request)

assert user.username == 'jtl-{userId}'
assert request.org.id == '{tenantId}'
```

### Frontend Testing

```typescript
// Test OAuth client
import { jtlOAuth } from '@/lib/jtl-oauth'

// Initiate login
jtlOAuth.login()

// Handle callback
const auth = await jtlOAuth.handleCallback(jtlToken)

console.log(auth.user)  // { id, email, username, ... }
console.log(auth.org)   // { id, name, slug }
```

---

## Dependencies

**Python** (`pyproject.toml`):
- `PyJWT >= 2.8.0` - JWT encoding/decoding
- `cryptography >= 41.0.0` - EdDSA signature verification
- `karrio-server-core` - Core Karrio dependencies

**TypeScript**:
- No additional dependencies (uses fetch API)

---

## Security Considerations

### Implemented

✅ **EdDSA Signature Verification**: All JTL tokens verified with public key
✅ **CSRF Protection**: State parameter validated on callback
✅ **Token Expiration**: JWT `exp` claim checked
✅ **HTTPS Ready**: Supports secure cookie settings
✅ **Organization Isolation**: Users scoped to tenants
✅ **Logging**: All auth events logged for audit

### Best Practices

- Store public key in environment variables (never in code)
- Use HTTPS in production for all OAuth redirects
- Rotate public keys periodically if JTL Hub updates
- Monitor authentication logs for suspicious activity
- Implement rate limiting on callback endpoint

---

## Troubleshooting

### Common Issues

**1. "JTL Hub public key not configured"**
- Ensure `JTL_HUB_PUBLIC_KEY` is set in `.env`
- Verify key format (PEM with `\n` for newlines)

**2. "Invalid token"**
- Check token is from correct JTL Hub environment (beta/prod)
- Verify public key matches JTL Hub's current key
- Check token hasn't expired (`exp` claim)

**3. "No token received from JTL Hub"**
- Verify redirect URI matches JTL Hub configuration
- Check browser console for errors
- Verify OAuth authorize URL is correct

**4. "Missing tenantId or userId"**
- Token payload may be incorrect format
- Verify you're using JTL Hub session tokens (not other token types)

**5. "User/Org not created"**
- Check database permissions
- Check backend logs for errors
- Verify `MULTI_ORGANIZATIONS` feature flag is enabled

---

## Next Steps

### Required Before Production

1. **Get Production Credentials**
   - [ ] EdDSA public key from JTL Hub team
   - [ ] Production OAuth authorize URL
   - [ ] Production redirect URI (HTTPS)

2. **Update Configuration**
   - [ ] Set production environment variables
   - [ ] Update CORS settings for production domains
   - [ ] Configure HTTPS settings (`USE_HTTPS=True`)

3. **Testing**
   - [ ] Test with real JTL Hub accounts
   - [ ] Verify user provisioning works correctly
   - [ ] Test error scenarios (expired tokens, invalid tokens)

4. **Documentation**
   - [ ] Document for JTL Hub users
   - [ ] Create admin guide for user management
   - [ ] Document troubleshooting steps

### Optional Enhancements

- [ ] Implement email fetching from JTL Hub API (if available)
- [ ] Add user profile sync from JTL Hub
- [ ] Add JTL Hub logout callback
- [ ] Implement token refresh flow
- [ ] Add monitoring/metrics for auth events

---

## Support

### Getting Help

- **JTL Hub Documentation**: https://developer.jtl-software.com/products/appregistration
- **Karrio Documentation**: Check internal docs
- **JTL Hub Team**: Contact for public key and OAuth configuration

### Reporting Issues

If you encounter issues:
1. Check logs: `karrio.server.jtl` logger
2. Verify configuration: All environment variables set
3. Test with curl: Direct API calls to `/auth/jtl/callback`
4. Check database: User and Org records created

---

## Implementation Checklist

### Backend ✅
- [x] JTL module structure created
- [x] EdDSA authentication class implemented
- [x] User/org provisioning logic implemented
- [x] OAuth callback endpoint implemented
- [x] Settings configuration updated
- [x] JTL-specific settings entrypoint created

### Frontend ✅
- [x] JTL OAuth client library created
- [x] Sign-in page updated (JTL Hub only)
- [x] OAuth callback handler created
- [x] Error handling implemented
- [x] Loading states implemented

### Configuration ✅
- [x] Environment variables documented
- [x] `.env.jtl.example` created
- [x] Settings module registered
- [x] Authentication classes configured

### Documentation ✅
- [x] Module README created
- [x] Implementation guide created
- [x] PRD documented
- [x] Testing checklist created

---

## Summary

The JTL Hub SSO integration is **complete and ready for testing**. All core functionality has been implemented following the PRD requirements:

- ✅ JTL Hub OAuth as the only authentication method
- ✅ EdDSA JWT verification with public key
- ✅ Automatic user and organization provisioning
- ✅ Clean tenant mapping (tenantId → Organization)
- ✅ Seamless SSO user experience
- ✅ Comprehensive error handling
- ✅ JTL-specific settings entrypoint

**Next action**: Obtain EdDSA public key from JTL Hub team and test with real credentials.

---

**Implementation Complete** ✅
**Ready for Testing** ✅
**Ready for Production** ⏳ (pending JTL Hub credentials)
