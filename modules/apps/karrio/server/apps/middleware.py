import jwt
import logging
from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class AppJWTMiddleware(MiddlewareMixin):
    """
    Middleware to validate JWT tokens for app authentication.

    Extracts JWT from Authorization header or query parameter,
    validates it using the shared secret, and adds app context
    to the request object.
    """

    def process_request(self, request):
        """Process incoming request and validate JWT if present."""
        # Extract JWT token from request
        jwt_token = self.extract_jwt(request)

        if jwt_token:
            try:
                # Validate JWT and extract app context
                payload = jwt.decode(
                    jwt_token,
                    settings.JWT_APP_SECRET_KEY,
                    algorithms=['HS256'],
                    audience='karrio-api',
                    issuer='karrio-dashboard'
                )

                # Add app context to request
                request.app_context = {
                    'app_id': payload['app_id'],
                    'installation_id': payload['installation_id'],
                    'user_id': payload['user_id'],
                    'org_id': payload['org_id'],
                    'access_scopes': payload['access_scopes']
                }

                logger.debug(f"JWT validated for app {payload['app_id']}")

            except jwt.ExpiredSignatureError:
                logger.warning("JWT token has expired")
                # Don't block request, just don't set app_context

            except jwt.InvalidTokenError as e:
                logger.warning(f"Invalid JWT token: {e}")
                # Don't block request, just don't set app_context

            except Exception as e:
                logger.error(f"JWT validation error: {e}")
                # Don't block request, just don't set app_context

        return None  # Continue processing

    def extract_jwt(self, request):
        """Extract JWT token from Authorization header or query parameter."""
        # Try Authorization header first
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            return auth_header[7:]

        # Try query parameter as fallback (for webhook URLs)
        return request.GET.get('token')


class AppContextMiddleware(MiddlewareMixin):
    """
    Middleware to resolve app installation from JWT context.

    This should be placed after AppJWTMiddleware in MIDDLEWARE setting.
    """

    def process_request(self, request):
        """Resolve app installation if app_context is present."""
        if hasattr(request, 'app_context'):
            try:
                from .models import AppInstallation

                app_context = request.app_context
                installation = AppInstallation.objects.get(
                    id=app_context['installation_id'],
                    app_id=app_context['app_id'],
                    is_active=True
                )

                # Add resolved installation to request
                request.app_installation = installation

                logger.debug(f"App installation resolved: {installation.id}")

            except AppInstallation.DoesNotExist:
                logger.warning(f"App installation not found: {app_context['installation_id']}")
                # Remove invalid app_context
                delattr(request, 'app_context')

            except Exception as e:
                logger.error(f"App installation resolution error: {e}")
                # Remove invalid app_context
                if hasattr(request, 'app_context'):
                    delattr(request, 'app_context')

        return None  # Continue processing


def require_app_context(view_func):
    """
    Decorator to require valid app context for a view.

    Usage:
        @require_app_context
        def my_app_api_view(request):
            # request.app_context and request.app_installation are available
            pass
    """
    def wrapper(request, *args, **kwargs):
        if not hasattr(request, 'app_context'):
            return JsonResponse({'error': 'App authentication required'}, status=401)

        if not hasattr(request, 'app_installation'):
            return JsonResponse({'error': 'App installation not found'}, status=404)

        return view_func(request, *args, **kwargs)

    return wrapper
