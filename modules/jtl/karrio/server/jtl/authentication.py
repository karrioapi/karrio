"""
JTL Hub Authentication for Karrio

Implements EdDSA (Ed25519) JWT verification for JTL Hub tokens using JWKS.
"""

import jwt
import logging
from jwt import PyJWKClient
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)

# JWKS client singleton (caches keys)
_jwks_client = None


class JTLHubAuthentication(BaseAuthentication):
    """
    Authenticate requests using JTL Hub JWT tokens.

    JTL Hub uses EdDSA (Ed25519) for JWT signatures.
    Requires public key verification.

    Token structure:
    {
        "header": {"alg": "EdDSA", "typ": "JWT", "kid": "<key-id>"},
        "payload": {
            "userId": "<UUID>",
            "tenantId": "<UUID>",
            "iss": "https://auth.jtl-cloud.com",
            "exp": 1746616503
        }
    }

    Note: kid (key ID) is in the header, not the payload.
    """

    def authenticate(self, request):
        """Authenticate using JTL Hub JWT token."""
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return None

        token = auth_header[7:]

        try:
            # Validate JWT with EdDSA public key
            payload, header = self.validate_token(token)

            # Get or create user and organization
            user, org = self.get_or_create_user_and_org(payload, header)

            # Set request context
            request.user = user
            request.org = org
            request.test_mode = False

            logger.info(f"JTL Hub user authenticated: {payload.get('userId')}")

            return (user, token)

        except jwt.ExpiredSignatureError:
            logger.warning("JTL Hub token has expired")
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JTL Hub token: {e}")
            raise AuthenticationFailed(f'Invalid token: {str(e)}')
        except Exception as e:
            logger.error(f"JTL Hub authentication error: {e}", exc_info=True)
            raise AuthenticationFailed('Authentication failed')

    def validate_token(self, token):
        """
        Validate JWT using JTL Hub's JWKS endpoint.

        Dynamically fetches public keys from JWKS endpoint and verifies EdDSA signature.
        This is the recommended approach as it automatically handles key rotation.

        Returns tuple of (payload, header) to access kid from header.
        """
        global _jwks_client

        # Get JWKS URL from settings with default
        jwks_url = getattr(
            settings,
            'JTL_HUB_JWKS_URL',
            'https://auth.jtl-cloud.com/.well-known/jwks.json'
        )

        try:
            # Initialize JWKS client (cached globally)
            if _jwks_client is None:
                _jwks_client = PyJWKClient(jwks_url)

            # Get signing key from JWKS (automatically fetches and caches)
            signing_key = _jwks_client.get_signing_key_from_jwt(token)

            # Decode and verify JWT signature
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["EdDSA"],
                issuer=getattr(
                    settings,
                    'JTL_HUB_ISSUER',
                    'https://auth.jtl-cloud.com'
                ),
                options={
                    "verify_exp": True,
                    "verify_aud": False  # JTL Hub doesn't include aud claim
                }
            )

            # Get header to access kid (key ID)
            header = jwt.get_unverified_header(token)

            return payload, header

        except jwt.ExpiredSignatureError:
            logger.warning("JTL Hub token has expired")
            raise
        except jwt.InvalidIssuerError:
            logger.warning("Invalid token issuer")
            raise AuthenticationFailed('Invalid token issuer')
        except Exception as e:
            logger.error(f"Token validation error: {e}", exc_info=True)
            raise

    def get_or_create_user_and_org(self, payload, header):
        """
        Auto-provision user and organization from JTL Hub token.

        Mapping:
        - tenantId → Organization.id
        - userId → User.username (format: jtl-{userId})
        - kid (from header) → Key ID for org identification (optional)
        """
        from karrio.server.user.models import User
        from karrio.server.orgs.models import Organization
        from .utils import get_user_email

        tenant_id = payload.get('tenantId')
        user_id = payload.get('userId')
        kid = header.get('kid')  # kid is in JWT header, not payload

        if not tenant_id or not user_id:
            raise AuthenticationFailed('Missing tenantId or userId in token')

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
            logger.info(
                f"JTL Hub provisioning - "
                f"User: {username} (new={user_created}), "
                f"Org: {tenant_id} (new={org_created})"
            )

        return user, org

    def authenticate_header(self, request):
        """Return authentication header for 401 responses."""
        return 'Bearer realm="api"'
