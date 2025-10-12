# Product Requirements Document: JTL Hub Single Sign-On Integration

**Project**: JTL Hub OAuth SSO for Karrio Shipping Platform
**Version**: 1.0
**Date**: 2025-10-12
**Status**: Ready for Implementation
**Timeline**: 30 minutes (minimal viable implementation)
**Owner**: Engineering Team

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Problem Statement](#problem-statement)
3. [Goals & Success Criteria](#goals--success-criteria)
4. [Technical Architecture](#technical-architecture)
5. [Implementation Plan](#implementation-plan)
6. [Module Structure](#module-structure)
7. [Configuration](#configuration)
8. [Testing Strategy](#testing-strategy)
9. [Deployment](#deployment)

---

## Executive Summary

Implement single sign-on (SSO) authentication for Karrio using JTL Hub as the identity provider. This integration will enable JTL Hub users to authenticate seamlessly with automatic user and organization provisioning.

### Key Features

- ✅ **JTL Hub OAuth** as the only authentication method
- ✅ **Auto-provisioning** of users and organizations on first login
- ✅ **Tenant mapping**: JTL Hub `tenantId` → Karrio Organization
- ✅ **User mapping**: JTL Hub `userId` → Karrio User
- ✅ **JWT validation**: EdDSA signature verification with public key
- ✅ **Session management**: Reuse existing Karrio JWT infrastructure

### Deliverables

1. New Django module: `modules/jtl/` for JTL Hub authentication
2. Updated dashboard: JTL Hub OAuth only (remove email/password)
3. Auto-provisioning logic: Create User + Organization on first login
4. Custom authentication middleware: JTL Hub JWT validation

**Timeline**: 30 minutes focused implementation
**Risk Level**: Medium (authentication changes)
**User Impact**: High (all users must use JTL Hub SSO)

---

## Problem Statement

### Current State

- Dashboard supports both Karrio OAuth and email/password authentication
- No integration with JTL Hub identity provider
- Manual user and organization creation required
- No SSO for JTL Hub customers
- Multiple authentication methods increase complexity

### Desired State

- **Single authentication method**: JTL Hub OAuth only
- **Automatic provisioning**: Users and organizations created on first login
- **Seamless SSO**: JTL Hub users authenticate once, access Karrio instantly
- **Clean mapping**: JTL `tenantId` → Karrio org, JTL `userId` → Karrio user
- **Minimal code**: Reuse existing JWT infrastructure where possible

---

## Goals & Success Criteria

### Primary Goals

1. **Single Sign-On**: Users authenticate via JTL Hub OAuth
2. **Auto-Provisioning**: First-time users get Karrio accounts automatically
3. **Organization Mapping**: JTL `tenantId` maps 1:1 to Karrio Organization
4. **User Mapping**: JTL `userId` maps uniquely to Karrio User
5. **Session Management**: Karrio JWT issued after successful JTL authentication

### Success Criteria

- ✅ User clicks "Sign in with JTL Hub" → redirected to JTL Hub
- ✅ After JTL authentication → redirected back with JWT token
- ✅ Backend validates JWT using EdDSA public key
- ✅ First login: User + Organization created automatically
- ✅ Returning user: Existing User + Organization loaded
- ✅ Karrio JWT issued for API access
- ✅ All Karrio features work seamlessly with JTL Hub users

---

## Technical Architecture

### Authentication Flow

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Dashboard  │─────▶│   JTL Hub    │─────▶│  Backend API │─────▶│  PostgreSQL  │
│  (React/TS)  │◀─────│  (OAuth IDP) │◀─────│   (Django)   │◀─────│  (User/Org)  │
└──────────────┘      └──────────────┘      └──────────────┘      └──────────────┘
     │                                              │
     │  Karrio JWT (session)                       │
     └──────────────────────────────────────────────┘
```

### Flow Steps

1. **User initiates login** → Dashboard redirects to JTL Hub OAuth authorize URL
2. **User authenticates** → JTL Hub validates credentials
3. **JTL Hub redirects back** → With JWT token (EdDSA signed)
4. **Backend validates JWT** → Using JTL Hub's EdDSA public key
5. **Backend provisions user** → Get or create User and Organization
6. **Backend issues Karrio JWT** → Standard Karrio session token
7. **Dashboard stores JWT** → User is authenticated

### JTL Hub JWT Token Structure

**Source**: [JTL Developer Docs](https://developer.jtl-software.com/products/appregistration/sessiontoken)

```json
{
  "header": {
    "alg": "EdDSA",
    "typ": "JWT"
  },
  "payload": {
    "exp": 1746616503,
    "userId": "<UUID>",
    "tenantId": "<UUID>",
    "kid": "<string>"
  },
  "signature": "..."
}
```

**Field Mapping**:
- `userId` → Karrio `User.username` (format: `jtl-{userId}`)
- `tenantId` → Karrio `Organization.id`
- `kid` → Customer ID (used in org display name)
- `exp` → Token expiration (Unix timestamp)

**Notes**:
- Algorithm: EdDSA (Ed25519) - asymmetric signature
- No email field - must fetch from JTL API or use placeholder
- Public key verification required (not symmetric HS256)

### Component Architecture

#### 1. JTL IDP Module

**Location**: `modules/jtl/karrio/server/jtl/`

**Purpose**: Handle JTL Hub authentication, JWT validation, and user/org provisioning

**Core Components**:
- `authentication.py` - JTLHubAuthentication DRF class (EdDSA verification)
- `views.py` - OAuth callback endpoint
- `utils.py` - User/org provisioning and email fetching
- `urls.py` - `/auth/jtl/callback` route

#### 2. Dashboard Updates

**Location**: `apps/dashboard/src/`

**Changes**:
- Remove email/password login form
- Replace Karrio OAuth with JTL Hub OAuth
- Single button: "Sign in with JTL Hub"
- Callback handler for JTL Hub redirect

#### 3. Backend Integration

**Settings Updates**:
- Add JTL module to `KARRIO_CONF`
- Add `JTLHubAuthentication` to `AUTHENTICATION_CLASSES`
- Configure JTL Hub public key and OAuth URLs

---

## Implementation Plan

### Phase 1: Backend Module (10 minutes)

**Objective**: Create JTL authentication module with EdDSA verification

**Tasks**:
1. Create module structure in `modules/jtl/`
2. Implement `JTLHubAuthentication` class
3. Implement JWT validation with EdDSA public key
4. Implement user/org auto-provisioning
5. Add OAuth callback endpoint
6. Register module in settings

**Key Implementation**:

```python
# modules/jtl/karrio/server/jtl/authentication.py
import jwt
import logging
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)


class JTLHubAuthentication(BaseAuthentication):
    """
    Authenticate requests using JTL Hub JWT tokens.

    JTL Hub uses EdDSA (Ed25519) for JWT signatures.
    Requires public key verification.
    """

    def authenticate(self, request):
        """Authenticate using JTL Hub JWT token."""
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return None

        token = auth_header[7:]

        try:
            # Validate JWT with EdDSA public key
            payload = self.validate_token(token)

            # Get or create user and organization
            user, org = self.get_or_create_user_and_org(payload)

            # Set request context
            request.user = user
            request.org = org
            request.test_mode = False

            logger.info(f"JTL Hub user authenticated: {payload.get('userId')}")

            return (user, token)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed(f'Invalid token: {str(e)}')
        except Exception as e:
            logger.error(f"JTL Hub authentication error: {e}", exc_info=True)
            raise AuthenticationFailed('Authentication failed')

    def validate_token(self, token):
        """Validate JWT using JTL Hub's EdDSA public key."""
        # Load public key from PEM format
        public_key = serialization.load_pem_public_key(
            settings.JTL_HUB_PUBLIC_KEY.encode('utf-8'),
            backend=default_backend()
        )

        # Decode and verify JWT signature
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["EdDSA"],
            options={"verify_exp": True}
        )

        return payload

    def get_or_create_user_and_org(self, payload):
        """Auto-provision user and organization from JTL Hub token."""
        from karrio.server.user.models import User
        from karrio.server.orgs.models import Organization
        from .utils import get_user_email

        tenant_id = payload.get('tenantId')
        user_id = payload.get('userId')
        kid = payload.get('kid')

        if not tenant_id or not user_id:
            raise AuthenticationFailed('Missing tenantId or userId')

        # Get or create organization
        org, org_created = Organization.objects.get_or_create(
            id=tenant_id,
            defaults={
                'name': f'JTL Tenant {kid or tenant_id}',
                'slug': f'jtl-{tenant_id[:8]}',
                'is_active': True,
            }
        )

        # Get or create user
        username = f'jtl-{user_id}'
        email = get_user_email(user_id, tenant_id)

        user, user_created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_active': True,
                'first_name': 'JTL',
                'last_name': 'User',
            }
        )

        # Update email if changed
        if not user_created and user.email != email:
            user.email = email
            user.save(update_fields=['email'])

        # Add user to organization
        if not org.users.filter(id=user.id).exists():
            org.users.add(user)

        if user_created or org_created:
            logger.info(f"Provisioned - User: {username} (new={user_created}), Org: {tenant_id} (new={org_created})")

        return user, org

    def authenticate_header(self, request):
        """Return authentication header for 401 responses."""
        return 'Bearer realm="api"'
```

```python
# modules/jtl/karrio/server/jtl/utils.py
import logging

logger = logging.getLogger(__name__)


def get_user_email(user_id: str, tenant_id: str) -> str:
    """
    Get user email from JTL Hub or generate placeholder.

    JTL tokens don't include email. Options:
    1. Fetch from JTL Hub API (if available)
    2. Use placeholder: {userId}@jtl.local
    """
    # TODO: Implement JTL Hub API call if endpoint available
    # For now, use placeholder email
    email = f'{user_id}@jtl.local'
    logger.debug(f"Generated email for user {user_id}: {email}")
    return email
```

```python
# modules/jtl/karrio/server/jtl/views.py
import jwt
import logging
from django.conf import settings
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .authentication import JTLHubAuthentication

logger = logging.getLogger(__name__)


class JTLCallbackView(APIView):
    """Handle OAuth callback from JTL Hub."""

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        """
        Receive JWT token from JTL Hub after OAuth redirect.
        Exchange for Karrio JWT.
        """
        jtl_token = request.data.get('token') or request.GET.get('token')
        if not jtl_token:
            return Response({'error': 'Missing token'}, status=400)

        try:
            # Validate JTL Hub token
            auth = JTLHubAuthentication()
            payload = auth.validate_token(jtl_token)
            user, org = auth.get_or_create_user_and_org(payload)

            # Issue Karrio JWT
            refresh = RefreshToken.for_user(user)
            refresh['org_id'] = str(org.id)

            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                },
                'org': {
                    'id': str(org.id),
                    'name': org.name,
                }
            })

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired'}, status=401)
        except jwt.InvalidTokenError as e:
            return Response({'error': f'Invalid token: {str(e)}'}, status=401)
        except Exception as e:
            logger.error(f"Callback error: {e}", exc_info=True)
            return Response({'error': 'Authentication failed'}, status=400)
```

```python
# modules/jtl/karrio/server/jtl/urls.py
from django.urls import path
from .views import JTLCallbackView

urlpatterns = [
    path('auth/jtl/callback', JTLCallbackView.as_view(), name='jtl-callback'),
]
```

```python
# modules/jtl/karrio/server/jtl/apps.py
from django.apps import AppConfig


class JTLConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'karrio.server.jtl'
    verbose_name = 'JTL Hub Integration'
```

```python
# modules/jtl/karrio/server/jtl/__init__.py
default_app_config = 'karrio.server.jtl.apps.JTLConfig'
```

### Phase 2: Dashboard OAuth (10 minutes)

**Objective**: Update dashboard to use JTL Hub OAuth exclusively

**Tasks**:
1. Create JTL Hub OAuth client library
2. Update signin page (remove email/password)
3. Add OAuth callback handler
4. Update authentication flow

**Key Implementation**:

```typescript
// apps/dashboard/src/lib/jtl-oauth.ts
interface JTLOAuthConfig {
  authorizeUrl: string
  redirectUri: string
  apiUrl: string
}

class JTLHubOAuth {
  private config: JTLOAuthConfig

  constructor() {
    this.config = {
      authorizeUrl: import.meta.env.VITE_JTL_HUB_AUTHORIZE_URL,
      redirectUri: import.meta.env.VITE_JTL_HUB_REDIRECT_URI,
      apiUrl: import.meta.env.VITE_KARRIO_API,
    }
  }

  /**
   * Redirect to JTL Hub for authentication
   */
  login(): void {
    const state = this.generateState()
    const params = new URLSearchParams({
      response_type: 'token',
      redirect_uri: this.config.redirectUri,
      state,
    })

    window.location.href = `${this.config.authorizeUrl}?${params.toString()}`
  }

  /**
   * Handle callback from JTL Hub
   */
  async handleCallback(token: string): Promise<AuthResponse> {
    const response = await fetch(`${this.config.apiUrl}/auth/jtl/callback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token }),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || 'Authentication failed')
    }

    const data = await response.json()

    // Store Karrio JWT
    this.storeTokens(data)

    return data
  }

  private storeTokens(data: AuthResponse): void {
    localStorage.setItem('karrio_access_token', data.access_token)
    localStorage.setItem('karrio_refresh_token', data.refresh_token)
    localStorage.setItem('karrio_user', JSON.stringify(data.user))
    localStorage.setItem('karrio_org', JSON.stringify(data.org))
  }

  private generateState(): string {
    const state = Math.random().toString(36).substring(2, 15)
    sessionStorage.setItem('jtl_oauth_state', state)
    return state
  }

  private verifyState(state: string): boolean {
    const stored = sessionStorage.getItem('jtl_oauth_state')
    sessionStorage.removeItem('jtl_oauth_state')
    return stored === state
  }
}

export const jtlOAuth = new JTLHubOAuth()

interface AuthResponse {
  access_token: string
  refresh_token: string
  user: {
    id: number
    email: string
    username: string
  }
  org: {
    id: string
    name: string
  }
}
```

```tsx
// apps/dashboard/src/routes/signin.tsx
import { createFileRoute } from '@tanstack/react-router'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { jtlOAuth } from '@/lib/jtl-oauth'

export const Route = createFileRoute('/signin')({
  component: SignInPage,
})

function SignInPage() {
  const handleJTLLogin = () => {
    jtlOAuth.login()
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-gray-900">JTL Shipping</h1>
          <p className="text-sm text-gray-600 mt-2">
            Sign in with your JTL Hub account
          </p>
        </div>

        <Card className="border border-gray-200 shadow-sm">
          <CardContent className="p-8">
            <Button
              onClick={handleJTLLogin}
              className="w-full bg-blue-600 hover:bg-blue-700"
            >
              Sign in with JTL Hub
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
```

```tsx
// apps/dashboard/src/routes/auth/callback.tsx
import { useEffect, useState } from 'react'
import { createFileRoute, useRouter } from '@tanstack/react-router'
import { jtlOAuth } from '@/lib/jtl-oauth'

export const Route = createFileRoute('/auth/callback')({
  component: CallbackPage,
})

function CallbackPage() {
  const router = useRouter()
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const handleCallback = async () => {
      try {
        // Extract JWT token from URL (query or hash)
        const params = new URLSearchParams(window.location.search)
        const hash = new URLSearchParams(window.location.hash.substring(1))

        const token = params.get('token') || hash.get('token')
        const state = params.get('state') || hash.get('state')

        if (!token) {
          throw new Error('No token received from JTL Hub')
        }

        // Exchange for Karrio JWT
        await jtlOAuth.handleCallback(token)

        // Redirect to dashboard
        router.navigate({ to: '/dashboard' })
      } catch (err) {
        console.error('Authentication error:', err)
        setError(err instanceof Error ? err.message : 'Authentication failed')
      }
    }

    handleCallback()
  }, [router])

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-red-600 mb-2">
            Authentication Failed
          </h2>
          <p className="text-gray-600">{error}</p>
          <button
            onClick={() => router.navigate({ to: '/signin' })}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded"
          >
            Try Again
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto" />
        <p className="mt-4 text-gray-600">Authenticating...</p>
      </div>
    </div>
  )
}
```

### Phase 3: Backend Configuration (5 minutes)

**Objective**: Register JTL module and configure settings

**Tasks**:
1. Add JTL module to `KARRIO_CONF`
2. Add `JTLHubAuthentication` to `AUTHENTICATION_CLASSES`
3. Configure environment variables
4. Update URL routing

**Settings Updates**:

```python
# karrio/apps/api/karrio/server/settings/base.py

# Add to KARRIO_CONF
KARRIO_CONF = [
    {
        "app": "karrio.server.jtl",
        "module": "karrio.server.jtl",
        "urls": "karrio.server.jtl.urls",
    },
    # ... existing modules
]

# JTL Hub Settings
JTL_HUB_PUBLIC_KEY = config("JTL_HUB_PUBLIC_KEY", default="")
JTL_HUB_OAUTH_AUTHORIZE_URL = config(
    "JTL_HUB_OAUTH_AUTHORIZE_URL",
    default="https://auth.jtl-cloud.com/oauth/authorize"
)
JTL_HUB_OAUTH_REDIRECT_URI = config(
    "JTL_HUB_OAUTH_REDIRECT_URI",
    default="http://localhost:3000/auth/callback"
)

# Add to AUTHENTICATION_CLASSES (first position)
AUTHENTICATION_CLASSES = [
    "karrio.server.jtl.authentication.JTLHubAuthentication",  # NEW
    "karrio.server.core.authentication.TokenBasicAuthentication",
    "karrio.server.core.authentication.TokenAuthentication",
    "karrio.server.core.authentication.OAuth2Authentication",
    "karrio.server.core.authentication.JWTAuthentication",
    "rest_framework.authentication.SessionAuthentication",
]
```

### Phase 4: Testing (5 minutes)

**Objective**: Verify end-to-end authentication flow

**Test Cases**:
1. First-time login creates User and Organization
2. Returning login reuses existing User and Organization
3. Invalid token returns appropriate error
4. Expired token returns appropriate error
5. Karrio JWT works for API access

---

## Module Structure

```
modules/jtl/
├── karrio/
│   └── server/
│       └── jtl/
│           ├── __init__.py
│           ├── apps.py                    # Django app configuration
│           ├── authentication.py          # JTLHubAuthentication class
│           ├── views.py                   # OAuth callback endpoint
│           ├── urls.py                    # URL routing
│           └── utils.py                   # Helper functions
├── pyproject.toml
└── README.md

apps/dashboard/src/
├── lib/
│   └── jtl-oauth.ts                       # JTL Hub OAuth client
└── routes/
    ├── signin.tsx                         # Login page (JTL Hub only)
    └── auth/
        └── callback.tsx                   # OAuth callback handler
```

---

## Configuration

### Environment Variables

**Backend (.env)**:
```bash
# JTL Hub OAuth Configuration
JTL_HUB_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEA...
-----END PUBLIC KEY-----"

JTL_HUB_OAUTH_AUTHORIZE_URL=https://auth.jtl-cloud.com/oauth/authorize
JTL_HUB_OAUTH_REDIRECT_URI=http://localhost:3000/auth/callback
```

**Dashboard (.env)**:
```bash
# JTL Hub OAuth Configuration
VITE_JTL_HUB_AUTHORIZE_URL=https://auth.jtl-cloud.com/oauth/authorize
VITE_JTL_HUB_REDIRECT_URI=http://localhost:3000/auth/callback

# Karrio API
VITE_KARRIO_API=http://localhost:8000
```

### Required from JTL Hub Team

1. **EdDSA Public Key** (PEM format)
   - Used to verify JWT signatures
   - Should be Ed25519 public key

2. **OAuth URLs**
   - Authorization endpoint
   - Token delivery method (URL param or POST body)

3. **Optional: User API**
   - Endpoint to fetch user email (if available)
   - Otherwise use placeholder: `{userId}@jtl.local`

---

## Testing Strategy

### Unit Tests

```python
# modules/jtl/karrio/server/jtl/tests/test_authentication.py
from django.test import TestCase
from unittest.mock import Mock, patch
from karrio.server.jtl.authentication import JTLHubAuthentication


class JTLHubAuthenticationTest(TestCase):

    def setUp(self):
        self.auth = JTLHubAuthentication()
        self.valid_token = "eyJhbGc..."  # Sample JTL token

    @patch('karrio.server.jtl.authentication.jwt.decode')
    def test_validate_token_success(self, mock_decode):
        """Test successful token validation."""
        mock_decode.return_value = {
            'userId': 'user-123',
            'tenantId': 'tenant-456',
            'kid': 'customer-789',
            'exp': 9999999999
        }

        payload = self.auth.validate_token(self.valid_token)

        self.assertEqual(payload['userId'], 'user-123')
        self.assertEqual(payload['tenantId'], 'tenant-456')

    def test_get_or_create_user_first_time(self):
        """Test user provisioning on first login."""
        payload = {
            'userId': 'new-user-123',
            'tenantId': 'new-tenant-456',
            'kid': 'customer-789'
        }

        user, org = self.auth.get_or_create_user_and_org(payload)

        self.assertEqual(user.username, 'jtl-new-user-123')
        self.assertEqual(str(org.id), 'new-tenant-456')
        self.assertTrue(org.users.filter(id=user.id).exists())

    def test_get_or_create_user_existing(self):
        """Test user reuse on returning login."""
        # Create user first
        payload = {
            'userId': 'existing-user',
            'tenantId': 'existing-tenant',
            'kid': 'customer-789'
        }

        user1, org1 = self.auth.get_or_create_user_and_org(payload)
        user2, org2 = self.auth.get_or_create_user_and_org(payload)

        self.assertEqual(user1.id, user2.id)
        self.assertEqual(org1.id, org2.id)
```

### Manual Testing Checklist

- [ ] Obtain real JTL Hub JWT token from JTL team
- [ ] Verify token can be decoded with provided public key
- [ ] Test login flow: click "Sign in with JTL Hub"
- [ ] Verify redirect to JTL Hub authorize URL
- [ ] Complete authentication on JTL Hub
- [ ] Verify redirect back to callback URL with token
- [ ] Verify User created with username `jtl-{userId}`
- [ ] Verify Organization created with id `{tenantId}`
- [ ] Verify Karrio JWT issued
- [ ] Verify API access with Karrio JWT works
- [ ] Test second login reuses existing User/Org
- [ ] Test expired token error handling
- [ ] Test invalid token error handling

---

## Deployment

### Pre-Deployment Checklist

- [ ] Get EdDSA public key from JTL Hub team
- [ ] Add `JTL_HUB_PUBLIC_KEY` to production environment
- [ ] Configure production OAuth redirect URI
- [ ] Run migrations (if any)
- [ ] Deploy backend changes
- [ ] Deploy dashboard changes
- [ ] Test in staging environment

### Deployment Steps

1. **Backend**:
   ```bash
   # Add environment variables
   export JTL_HUB_PUBLIC_KEY="..."
   export JTL_HUB_OAUTH_AUTHORIZE_URL="..."
   export JTL_HUB_OAUTH_REDIRECT_URI="..."

   # Deploy
   python manage.py migrate
   python manage.py collectstatic --noinput
   gunicorn karrio.server.wsgi:application
   ```

2. **Dashboard**:
   ```bash
   # Build with environment variables
   VITE_JTL_HUB_AUTHORIZE_URL="..." \
   VITE_JTL_HUB_REDIRECT_URI="..." \
   VITE_KARRIO_API="..." \
   npm run build

   # Deploy static files
   ```

3. **Verify**:
   - Test login flow in production
   - Monitor logs for authentication errors
   - Verify user provisioning works

### Rollback Plan

If issues arise:
1. Remove `JTLHubAuthentication` from `AUTHENTICATION_CLASSES`
2. Revert dashboard to previous version
3. Investigate logs and fix issues
4. Re-deploy with fixes

---

## Summary

This PRD outlines a **minimal, focused** implementation of JTL Hub SSO:

✅ **30-minute implementation** (if focused)
✅ **Reuses existing infrastructure** (JWT, User, Organization models)
✅ **Minimal new code** (~400 lines total)
✅ **Auto-provisioning** (no manual user management)
✅ **Clean architecture** (dedicated module, clear separation)
✅ **EdDSA verification** (industry-standard asymmetric JWT)

### Next Steps

1. ✅ PRD approved
2. Get EdDSA public key from JTL Hub team (PEM format)
3. Confirm OAuth redirect flow details
4. Implement Phase 1: Backend module
5. Implement Phase 2: Dashboard updates
6. Implement Phase 3: Configuration
7. Execute Phase 4: Testing
8. Deploy to production

---

**Document Version**: 1.0
**Last Updated**: 2025-10-12
**Status**: Ready for Implementation
