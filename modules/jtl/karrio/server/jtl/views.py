"""
JTL Hub OAuth callback endpoint.
"""

import jwt
import logging
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .authentication import JTLHubAuthentication

logger = logging.getLogger(__name__)


class JTLCallbackView(APIView):
    """
    Handle OAuth callback from JTL Hub.

    After user authenticates with JTL Hub, they are redirected back
    with a JWT token. This endpoint validates the token and issues
    a Karrio JWT for API access.
    """

    authentication_classes = []  # Public endpoint
    permission_classes = []  # No permissions required

    def post(self, request):
        """
        Receive JWT token from JTL Hub and exchange for Karrio JWT.

        Request body:
            {
                "token": "eyJhbGc..."  # JTL Hub JWT
            }

        Response:
            {
                "access_token": "...",   # Karrio JWT access token
                "refresh_token": "...",  # Karrio JWT refresh token
                "user": {...},           # User info
                "org": {...}             # Organization info
            }
        """
        # Get JTL Hub token from request
        jtl_token = request.data.get('token') or request.GET.get('token')

        if not jtl_token:
            logger.warning("Callback received without token")
            return Response(
                {'error': 'Missing token parameter'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Validate JTL Hub token and provision user/org
            auth = JTLHubAuthentication()
            payload, header = auth.validate_token(jtl_token)
            user, org = auth.get_or_create_user_and_org(payload, header)

            # Issue Karrio JWT tokens
            refresh = RefreshToken.for_user(user)
            refresh['org_id'] = str(org.id)
            refresh['is_verified'] = True  # Verified by JTL Hub

            logger.info(
                f"JTL Hub callback successful - "
                f"User: {user.username}, Org: {org.id}"
            )

            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'org': {
                    'id': str(org.id),
                    'name': org.name,
                    'slug': org.slug,
                }
            }, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            logger.warning("JTL Hub token expired")
            return Response(
                {'error': 'Token has expired'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JTL Hub token: {e}")
            return Response(
                {'error': f'Invalid token: {str(e)}'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        except Exception as e:
            logger.error(f"JTL Hub callback error: {e}", exc_info=True)
            return Response(
                {'error': 'Authentication failed'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request):
        """
        Handle GET requests (for URL-based token delivery).

        Some OAuth flows may pass the token as a URL parameter.
        """
        return self.post(request)
