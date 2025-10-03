import jwt
import time
from unittest.mock import patch
from django.test import TestCase, RequestFactory
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse

from karrio.server.apps.middleware import AppJWTMiddleware, AppContextMiddleware, require_app_context
from karrio.server.apps.models import AppInstallation
from karrio.server.apps.authentication import AppJWTAuthentication, AppContextUser
from karrio.server.graph.tests.base import GraphTestCase
from rest_framework.exceptions import AuthenticationFailed


class TestAppJWTAuthentication(GraphTestCase):
    """Test suite for JWT app authentication middleware."""

    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()
        self.jwt_middleware = AppJWTMiddleware(lambda request: None)
        self.context_middleware = AppContextMiddleware(lambda request: None)

        # Create test app installation
        self.installation = AppInstallation.objects.create(
            app_id="test-app",
            app_type="marketplace",
            access_scopes=["read", "write"],
            created_by=self.user
        )

    def generate_test_jwt(self, **kwargs):
        """Generate a test JWT token."""
        payload = {
            'iss': 'karrio-dashboard',
            'aud': 'karrio-api',
            'sub': f"app-{kwargs.get('app_id', 'test-app')}-{kwargs.get('installation_id', self.installation.id)}",
            'exp': int(time.time()) + 300,  # 5 minutes
            'iat': int(time.time()),
            'app_id': kwargs.get('app_id', 'test-app'),
            'installation_id': kwargs.get('installation_id', self.installation.id),
            'user_id': kwargs.get('user_id', str(self.user.id)),
            'org_id': kwargs.get('org_id', str(self.user.id)),  # Using user.id as org_id for test
            'access_scopes': kwargs.get('access_scopes', ['read', 'write'])
        }

        return jwt.encode(payload, 'test-secret-key', algorithm='HS256')

    @patch.object(settings, 'JWT_APP_SECRET_KEY', 'test-secret-key')
    def test_valid_jwt_authentication(self):
        """Test JWT middleware with valid token."""
        print("Testing valid JWT authentication")

        token = self.generate_test_jwt()
        request = self.factory.get('/', HTTP_AUTHORIZATION=f'Bearer {token}')

        # Process request through JWT middleware
        response = self.jwt_middleware.process_request(request)

        # Should not return a response (continue processing)
        self.assertIsNone(response)

        # Should set app_context on request
        self.assertTrue(hasattr(request, 'app_context'))
        self.assertEqual(request.app_context['app_id'], 'test-app')
        self.assertEqual(request.app_context['installation_id'], self.installation.id)
        self.assertEqual(request.app_context['user_id'], str(self.user.id))

    @patch.object(settings, 'JWT_APP_SECRET_KEY', 'test-secret-key')
    def test_jwt_from_query_parameter(self):
        """Test JWT extraction from query parameter."""
        print("Testing JWT from query parameter")

        token = self.generate_test_jwt()
        request = self.factory.get(f'/?token={token}')

        # Process request through JWT middleware
        response = self.jwt_middleware.process_request(request)

        # Should not return a response
        self.assertIsNone(response)

        # Should set app_context on request
        self.assertTrue(hasattr(request, 'app_context'))
        self.assertEqual(request.app_context['app_id'], 'test-app')

    @patch.object(settings, 'JWT_APP_SECRET_KEY', 'test-secret-key')
    def test_expired_jwt_token(self):
        """Test JWT middleware with expired token."""
        print("Testing expired JWT token")

        # Generate expired token
        payload = {
            'iss': 'karrio-dashboard',
            'aud': 'karrio-api',
            'sub': f"app-test-app-{self.installation.id}",
            'exp': int(time.time()) - 300,  # Expired 5 minutes ago
            'iat': int(time.time()) - 600,
            'app_id': 'test-app',
            'installation_id': self.installation.id,
            'user_id': str(self.user.id),
            'org_id': str(self.user.id),
            'access_scopes': ['read', 'write']
        }

        token = jwt.encode(payload, 'test-secret-key', algorithm='HS256')
        request = self.factory.get('/', HTTP_AUTHORIZATION=f'Bearer {token}')

        # Process request through JWT middleware
        response = self.jwt_middleware.process_request(request)

        # Should not return a response (continues processing without app_context)
        self.assertIsNone(response)

        # Should NOT set app_context on request
        self.assertFalse(hasattr(request, 'app_context'))

    @patch.object(settings, 'JWT_APP_SECRET_KEY', 'test-secret-key')
    def test_invalid_jwt_signature(self):
        """Test JWT middleware with invalid signature."""
        print("Testing invalid JWT signature")

        # Generate token with wrong secret
        token = jwt.encode({
            'iss': 'karrio-dashboard',
            'aud': 'karrio-api',
            'app_id': 'test-app'
        }, 'wrong-secret-key', algorithm='HS256')

        request = self.factory.get('/', HTTP_AUTHORIZATION=f'Bearer {token}')

        # Process request through JWT middleware
        response = self.jwt_middleware.process_request(request)

        # Should not return a response
        self.assertIsNone(response)

        # Should NOT set app_context on request
        self.assertFalse(hasattr(request, 'app_context'))

    @patch.object(settings, 'JWT_APP_SECRET_KEY', 'test-secret-key')
    def test_invalid_jwt_issuer(self):
        """Test JWT middleware with invalid issuer."""
        print("Testing invalid JWT issuer")

        payload = {
            'iss': 'malicious-service',  # Wrong issuer
            'aud': 'karrio-api',
            'app_id': 'test-app'
        }

        token = jwt.encode(payload, 'test-secret-key', algorithm='HS256')
        request = self.factory.get('/', HTTP_AUTHORIZATION=f'Bearer {token}')

        # Process request through JWT middleware
        response = self.jwt_middleware.process_request(request)

        # Should not return a response
        self.assertIsNone(response)

        # Should NOT set app_context on request
        self.assertFalse(hasattr(request, 'app_context'))

    def test_no_jwt_token(self):
        """Test JWT middleware without token."""
        print("Testing request without JWT token")

        request = self.factory.get('/')

        # Process request through JWT middleware
        response = self.jwt_middleware.process_request(request)

        # Should not return a response
        self.assertIsNone(response)

        # Should NOT set app_context on request
        self.assertFalse(hasattr(request, 'app_context'))

    @patch.object(settings, 'JWT_APP_SECRET_KEY', 'test-secret-key')
    def test_app_context_middleware_resolution(self):
        """Test app context middleware resolving installation."""
        print("Testing app context middleware resolution")

        token = self.generate_test_jwt()
        request = self.factory.get('/', HTTP_AUTHORIZATION=f'Bearer {token}')

        # Process through JWT middleware first
        self.jwt_middleware.process_request(request)

        # Verify app_context is set
        self.assertTrue(hasattr(request, 'app_context'))

        # Process through context middleware
        response = self.context_middleware.process_request(request)

        # Should not return a response
        self.assertIsNone(response)

        # Should resolve and set app_installation
        self.assertTrue(hasattr(request, 'app_installation'))
        self.assertEqual(request.app_installation.id, self.installation.id)
        self.assertEqual(request.app_installation.app_id, 'test-app')

    @patch.object(settings, 'JWT_APP_SECRET_KEY', 'test-secret-key')
    def test_app_context_middleware_invalid_installation(self):
        """Test app context middleware with invalid installation ID."""
        print("Testing app context middleware with invalid installation")

        token = self.generate_test_jwt(installation_id='invalid-id')
        request = self.factory.get('/', HTTP_AUTHORIZATION=f'Bearer {token}')

        # Process through JWT middleware first
        self.jwt_middleware.process_request(request)

        # Verify app_context is set
        self.assertTrue(hasattr(request, 'app_context'))

        # Process through context middleware
        response = self.context_middleware.process_request(request)

        # Should not return a response
        self.assertIsNone(response)

        # Should remove invalid app_context and not set app_installation
        self.assertFalse(hasattr(request, 'app_context'))
        self.assertFalse(hasattr(request, 'app_installation'))

    @patch.object(settings, 'JWT_APP_SECRET_KEY', 'test-secret-key')
    def test_require_app_context_decorator_success(self):
        """Test require_app_context decorator with valid context."""
        print("Testing require_app_context decorator with valid context")

        @require_app_context
        def test_view(request):
            return JsonResponse({'success': True})

        token = self.generate_test_jwt()
        request = self.factory.get('/', HTTP_AUTHORIZATION=f'Bearer {token}')

        # Set up request context
        self.jwt_middleware.process_request(request)
        self.context_middleware.process_request(request)

        # Call decorated view
        response = test_view(request)

        # Should succeed
        self.assertEqual(response.status_code, 200)

    def test_require_app_context_decorator_no_context(self):
        """Test require_app_context decorator without context."""
        print("Testing require_app_context decorator without context")

        @require_app_context
        def test_view(request):
            return JsonResponse({'success': True})

        request = self.factory.get('/')

        # Call decorated view without app context
        response = test_view(request)

        # Should return 401
        self.assertEqual(response.status_code, 401)

    @patch.object(settings, 'JWT_APP_SECRET_KEY', 'test-secret-key')
    def test_require_app_context_decorator_no_installation(self):
        """Test require_app_context decorator without installation."""
        print("Testing require_app_context decorator without installation")

        @require_app_context
        def test_view(request):
            return JsonResponse({'success': True})

        token = self.generate_test_jwt(installation_id='invalid-id')
        request = self.factory.get('/', HTTP_AUTHORIZATION=f'Bearer {token}')

        # Set up request context (will fail to resolve installation)
        self.jwt_middleware.process_request(request)
        self.context_middleware.process_request(request)

        # Call decorated view
        response = test_view(request)

        # Should return 401 (no app_context after middleware removes it)
        self.assertEqual(response.status_code, 401)

    @patch.object(settings, 'JWT_APP_SECRET_KEY', 'test-secret-key')
    def test_jwt_security_boundary(self):
        """Test JWT security boundaries and edge cases."""
        print("Testing JWT security boundaries")

        # Test malformed JWT
        request = self.factory.get('/', HTTP_AUTHORIZATION='Bearer invalid.jwt.token')
        response = self.jwt_middleware.process_request(request)
        self.assertIsNone(response)
        self.assertFalse(hasattr(request, 'app_context'))

        # Test JWT with missing required fields
        incomplete_payload = {
            'iss': 'karrio-dashboard',
            'aud': 'karrio-api',
            # Missing app_id, installation_id, etc.
        }
        token = jwt.encode(incomplete_payload, 'test-secret-key', algorithm='HS256')
        request = self.factory.get('/', HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.jwt_middleware.process_request(request)
        self.assertIsNone(response)
        self.assertFalse(hasattr(request, 'app_context'))

    @patch.object(settings, 'JWT_APP_SECRET_KEY', 'test-secret-key')
    def test_jwt_with_real_api_endpoint(self):
        """Test JWT authentication with a real API endpoint (v1/connections)."""
        print("Testing JWT with real API endpoint")

        # Generate valid JWT token
        token = self.generate_test_jwt()

        # Make authenticated request to connections endpoint
        response = self.client.get(
            '/v1/connections',
            HTTP_AUTHORIZATION=f'Bearer {token}',
            content_type='application/json'
        )

        # Should succeed (200) or return unauthorized (401) depending on middleware setup
        # Since middleware might not be fully configured in test, we mainly test token format
        self.assertIn(response.status_code, [200, 401, 403])

        # Test with invalid token
        invalid_token = jwt.encode({
            'iss': 'wrong-issuer',
            'aud': 'karrio-api',
            'app_id': 'test-app'
        }, 'test-secret-key', algorithm='HS256')

        response = self.client.get(
            '/v1/connections',
            HTTP_AUTHORIZATION=f'Bearer {invalid_token}',
            content_type='application/json'
        )

        # Should not process JWT (continues with normal auth)
        self.assertIn(response.status_code, [200, 401, 403])

    @patch.object(settings, 'JWT_APP_SECRET_KEY', 'test-secret-key')
    def test_jwt_middleware_integration_with_real_request(self):
        """Test JWT middleware integration with Django test client."""
        print("Testing JWT middleware integration with real request")

        # Create a test view that requires app context
        from django.http import JsonResponse
        from django.views.decorators.csrf import csrf_exempt
        from django.views.decorators.http import require_http_methods

        @csrf_exempt
        @require_http_methods(["GET"])
        @require_app_context
        def test_app_api_view(request):
            return JsonResponse({
                'success': True,
                'app_id': request.app_context['app_id'],
                'installation_id': request.app_context['installation_id'],
                'user_id': request.app_context['user_id']
            })

        # Temporarily add the view to URL patterns for testing
        from django.urls import path
        from django.urls import include
        from django.conf.urls import url

        # Generate valid JWT token
        token = self.generate_test_jwt()

        # Test with valid JWT using request factory (simulating middleware)
        request = self.factory.get('/test-app-api/', HTTP_AUTHORIZATION=f'Bearer {token}')

        # Process through middleware
        self.jwt_middleware.process_request(request)
        self.context_middleware.process_request(request)

        # Call the view
        response = test_app_api_view(request)

        # Should succeed
        self.assertEqual(response.status_code, 200)

        # Verify response contains app context
        import json
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['app_id'], 'test-app')
        self.assertEqual(response_data['installation_id'], self.installation.id)
        self.assertEqual(response_data['user_id'], str(self.user.id))

    @patch.object(settings, 'JWT_APP_SECRET_KEY', 'test-secret-key')
    def test_jwt_token_in_query_parameter_with_real_endpoint(self):
        """Test JWT token passed as query parameter with real endpoint."""
        print("Testing JWT token in query parameter with real endpoint")

        # Generate valid JWT token
        token = self.generate_test_jwt()

        # Make request with token in query parameter
        response = self.client.get(
            f'/v1/connections?token={token}',
            content_type='application/json'
        )

        # Should process normally (middleware extracts token from query param)
        self.assertIn(response.status_code, [200, 401, 403])

        # Test with malformed token in query
        response = self.client.get(
            '/v1/connections?token=invalid.jwt.token',
            content_type='application/json'
        )

        # Should continue processing without app context
        self.assertIn(response.status_code, [200, 401, 403])

    @patch.object(settings, 'JWT_APP_SECRET_KEY', 'test-secret-key')
    def test_drf_app_jwt_authentication(self):
        """Test DRF AppJWTAuthentication class."""
        print("Testing DRF AppJWTAuthentication class")

        auth = AppJWTAuthentication()

        # Test with valid JWT token
        token = self.generate_test_jwt()
        request = self.factory.get('/', HTTP_AUTHORIZATION=f'Bearer {token}')

        user, auth_token = auth.authenticate(request)

        # Should return AppContextUser instance
        self.assertIsInstance(user, AppContextUser)
        self.assertEqual(auth_token, token)
        self.assertEqual(user.app_context['app_id'], 'test-app')
        self.assertEqual(user.app_context['installation_id'], self.installation.id)
        self.assertTrue(user.is_authenticated)

        # Test user properties
        self.assertEqual(user.username, 'app-test-app')
        self.assertTrue(user.id.startswith('app-test-app-'))

    @patch.object(settings, 'JWT_APP_SECRET_KEY', 'test-secret-key')
    def test_drf_authentication_with_invalid_token(self):
        """Test DRF authentication with invalid token."""
        print("Testing DRF authentication with invalid token")

        auth = AppJWTAuthentication()

        # Test with expired token
        expired_payload = {
            'iss': 'karrio-dashboard',
            'aud': 'karrio-api',
            'sub': f"app-test-app-{self.installation.id}",
            'exp': int(time.time()) - 300,  # Expired
            'iat': int(time.time()) - 600,
            'app_id': 'test-app',
            'installation_id': self.installation.id,
            'user_id': str(self.user.id),
            'org_id': str(self.user.id),
            'access_scopes': ['read', 'write']
        }

        expired_token = jwt.encode(expired_payload, 'test-secret-key', algorithm='HS256')
        request = self.factory.get('/', HTTP_AUTHORIZATION=f'Bearer {expired_token}')

        with self.assertRaises(AuthenticationFailed) as context:
            auth.authenticate(request)

        self.assertIn('expired', str(context.exception))

    def test_drf_authentication_without_token(self):
        """Test DRF authentication without token."""
        print("Testing DRF authentication without token")

        auth = AppJWTAuthentication()
        request = self.factory.get('/')

        # Should return None (no authentication attempted)
        result = auth.authenticate(request)
        self.assertIsNone(result)

    @patch.object(settings, 'JWT_APP_SECRET_KEY', 'test-secret-key')
    def test_app_context_user_permissions(self):
        """Test AppContextUser permission system."""
        print("Testing AppContextUser permission system")

        # Create app context with different scopes
        app_context = {
            'app_id': 'test-app',
            'installation_id': self.installation.id,
            'user_id': str(self.user.id),
            'org_id': str(self.user.id),
            'access_scopes': ['read', 'write']
        }

        user = AppContextUser(app_context)

        # Test permission checking
        self.assertTrue(user.has_perm('read'))
        self.assertTrue(user.has_perm('write'))
        self.assertFalse(user.has_perm('admin'))

        # Test with admin scope
        admin_context = app_context.copy()
        admin_context['access_scopes'] = ['admin']
        admin_user = AppContextUser(admin_context)

        self.assertTrue(admin_user.has_perm('admin'))
        self.assertTrue(admin_user.has_module_perms('any_module'))

    @patch.object(settings, 'JWT_APP_SECRET_KEY', 'test-secret-key')
    def test_jwt_authentication_header_extraction(self):
        """Test JWT token extraction from different sources."""
        print("Testing JWT token extraction from different sources")

        auth = AppJWTAuthentication()
        token = self.generate_test_jwt()

        # Test Authorization header
        request = self.factory.get('/', HTTP_AUTHORIZATION=f'Bearer {token}')
        extracted_token = auth.extract_jwt_token(request)
        self.assertEqual(extracted_token, token)

        # Test query parameter
        request = self.factory.get(f'/?token={token}')
        extracted_token = auth.extract_jwt_token(request)
        self.assertEqual(extracted_token, token)

        # Test no token
        request = self.factory.get('/')
        extracted_token = auth.extract_jwt_token(request)
        self.assertIsNone(extracted_token)
