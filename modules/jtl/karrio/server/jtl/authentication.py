"""
JTL Authentication for Karrio

Implements symmetric JWT authentication using HS256 algorithm with JWT_SECRET.
"""

import jwt
import logging
import functools
from django.conf import settings
from django.utils.functional import SimpleLazyObject
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)


def catch_auth_exception(func):
    """Decorator to catch and convert authentication exceptions to Karrio API exceptions."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AuthenticationFailed:
            from karrio.server.core.exceptions import APIException
            from rest_framework import status

            raise APIException(
                "Given token not valid for any token type",
                code="invalid_token",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

    return wrapper


def get_request_test_mode(request):
    """Get test mode from request headers."""
    import yaml
    return yaml.safe_load(request.META.get("HTTP_X_TEST_MODE", "")) or False


def get_request_org(request, user, org_id=None, default_org=None):
    """Get organization for request, following Karrio's org resolution pattern."""
    from karrio.server.orgs.models import Organization

    if not settings.MULTI_ORGANIZATIONS:
        return None

    try:
        if default_org is not None:
            org = default_org
        elif user and hasattr(user, 'id') and user.id:
            orgs = Organization.objects.filter(users__id=user.id)
            org = (
                orgs.filter(id=org_id).first()
                if org_id is not None and orgs.filter(id=org_id).exists()
                else orgs.filter(is_active=True).first()
            )
        else:
            org = None

        if org is not None and not org.is_active:
            raise AuthenticationFailed("Organization is inactive")

        if org is None and org_id is not None:
            raise AuthenticationFailed("No active organization found with the given credentials")

        return org
    except Exception:
        return None


class JTLJWTAuthentication(BaseAuthentication):
    """
    Authenticate requests using JTL JWT tokens with HS256 symmetric encryption.

    Token structure:
    {
        "header": {"alg": "HS256", "typ": "JWT"},
        "payload": {
            "tenantId": "<UUID>",
            "userId": "<UUID>",
            "iss": "jtl-wawi-api",
            "exp": 1746616503
        }
    }
    """

    def authenticate(self, request):
        """Authenticate using JTL JWT token."""
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        logger.info(f"JTL JWT Auth called. Header: {auth_header[:50] if auth_header else 'NONE'}")

        if not auth_header.startswith('Bearer '):
            logger.info("No Bearer token found, skipping JTL auth")
            return None

        token = auth_header[7:]
        logger.info(f"Processing JTL JWT token: {token[:20]}...")

        try:
            # First, check if this is likely a JTL token before full validation
            if not self.is_jtl_token(token):
                logger.info("Token is not a JTL token, skipping")
                return None

            # Validate JWT with HS256 symmetric key (only for JTL tokens)
            payload = self.validate_token(token)

            # Get user and organization (must exist from onboarding)
            user, default_org, org_user = self.get_user_and_org(payload)

            # Set request context following Karrio patterns
            request.user = user
            request.token = payload
            request.test_mode = get_request_test_mode(request)
            request.otp_is_verified = True  # JTL tokens are pre-verified
            request.org = SimpleLazyObject(
                functools.partial(
                    get_request_org,
                    request,
                    user,
                    org_id=request.META.get("HTTP_X_ORG_ID"),
                    default_org=default_org,
                )
            )

            logger.info(f"JTL user authenticated: {payload.get('userId')}")

            return (user, payload)

        except jwt.ExpiredSignatureError:
            logger.warning("JTL token has expired")
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JTL token: {e}")
            raise AuthenticationFailed(f'Invalid token: {str(e)}')
        except Exception as e:
            logger.error(f"JTL authentication error: {e}", exc_info=True)
            # For JTL tokens that fail validation, still raise an exception
            # But for non-JTL tokens, we should have returned None earlier
            raise AuthenticationFailed('Authentication failed')

    def is_jtl_token(self, token):
        """
        Check if a JWT token is intended for JTL authentication without full validation.
        
        This method safely decodes the token payload to check for JTL-specific fields
        or issuer without validating the signature or expiration.
        
        Returns True if this looks like a JTL token, False otherwise.
        """
        try:
            # Decode without verification to peek at the payload
            payload = jwt.decode(
                token,
                options={
                    "verify_signature": False,
                    "verify_exp": False,
                    "verify_aud": False,
                    "verify_iss": False
                }
            )
            
            # Check for JTL-specific indicators
            # JTL tokens should have both tenantId and userId, and optionally issuer
            has_tenant_id = 'tenantId' in payload
            has_user_id = 'userId' in payload
            has_jtl_issuer = payload.get('iss') == 'jtl-wawi-api'
            
            # Consider it a JTL token if it has JTL fields OR JTL issuer
            is_jtl = has_jtl_issuer or (has_tenant_id and has_user_id)
            
            if is_jtl:
                logger.info(f"Detected JTL token with tenantId: {has_tenant_id}, userId: {has_user_id}, issuer: {payload.get('iss', 'none')}")
            
            return is_jtl
            
        except Exception as e:
            # If we can't decode the token at all, it's probably not valid JWT
            logger.debug(f"Could not decode token for JTL check: {e}")
            return False

    def validate_token(self, token):
        """
        Validate JWT using JWT_SECRET with HS256 algorithm.

        Returns payload dictionary.
        """
        try:
            # Get JWT secret from Django settings (loaded via decouple)
            jwt_secret = getattr(settings, 'JWT_SECRET', None)
            if not jwt_secret:
                raise AuthenticationFailed('JWT_SECRET not configured')

            # Decode and verify JWT signature
            payload = jwt.decode(
                token,
                jwt_secret,
                algorithms=["HS256"],
                issuer="jtl-wawi-api",
                options={
                    "verify_exp": True,
                    "verify_aud": False
                }
            )

            return payload

        except jwt.ExpiredSignatureError:
            logger.warning("JTL token has expired")
            raise
        except jwt.InvalidIssuerError:
            logger.warning("Invalid token issuer")
            raise AuthenticationFailed('Invalid token issuer')
        except Exception as e:
            logger.error(f"Token validation error: {e}", exc_info=True)
            raise

    def get_user_and_org(self, payload):
        """
        Retrieve user and organization from JTL token.

        Authentication will fail if tenant or user doesn't exist.
        Users must be onboarded via the onboarding API first.

        Mapping:
        - tenantId → Organization (metadata.tenantId = tenantId)
        - userId → OrganizationUser (metadata.userId = userId)
        """
        from karrio.server.user.models import User
        from karrio.server.orgs.models import Organization, OrganizationUser

        tenant_id = payload.get('tenantId')
        user_id = payload.get('userId')

        if not tenant_id or not user_id:
            raise AuthenticationFailed('Missing tenantId or userId in token')

        # Get organization by metadata.tenantId
        org = Organization.objects.filter(
            metadata__tenantId=tenant_id
        ).first()

        if not org:
            logger.warning(f"Organization not found for tenantId: {tenant_id[:8]}")
            raise AuthenticationFailed('Organization not found. Please complete onboarding first.')

        # Get organization user by metadata.userId
        org_user = OrganizationUser.objects.filter(
            organization=org,
            metadata__userId=user_id
        ).first()

        if not org_user:
            logger.warning(f"User not found for userId: {user_id[:8]} in organization: {org.id}")
            raise AuthenticationFailed('User not found. Please complete onboarding first.')

        user = org_user.user

        if not user.is_active:
            logger.warning(f"Inactive user attempted authentication: {user_id[:8]}")
            raise AuthenticationFailed('User account is inactive.')

        logger.info(f"Authenticated user: {user_id[:8]} for organization: {tenant_id[:8]}")

        return user, org, org_user

    def authenticate_header(self, request):
        """Return authentication header for 401 responses."""
        return 'Bearer realm="api"'
