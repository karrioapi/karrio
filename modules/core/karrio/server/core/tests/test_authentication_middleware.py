"""Regression: middleware must not 500 when the lazy `request.org`
raises AuthenticationFailed.

PR #769 made tenant membership strict: a non-onboarded ORY session that
includes `x-tenant-id` for a tenant the user has not joined returns
`(user, None)` from authentication, with `request.org` wrapped as a
SimpleLazyObject around `get_request_org`. Touching that lazy outside of
DRF view dispatch resolves it, and the resolver raises AuthenticationFailed
because the user is not a member of the requested tenant. Because the
exception is raised in a Django middleware (not a DRF view), DRF cannot
map it to a 401 and Django turns it into a generic 500.

Two middleware touch `request.org` outside view dispatch:

1. `SessionContext._inject_telemetry` (`core/middleware.py`) tags `org_id`
   on the tracer at the *start* of the request, before the view runs.
   This was the live production trigger: `/v1/references` (an AllowAny
   endpoint whose view never touches `request.org`) 500'd purely from
   telemetry resolving the lazy. Sentry recorded 127 events from one user
   in ~10 minutes.
2. `AuthenticationMiddleware.process_response` (`core/authentication.py`)
   writes the `org_id` cookie *after* the view returns.

Both now resolve the lazy defensively (telemetry via `lib.failsafe`,
cookie via try/except). Endpoints that genuinely need org context still
hit the same check during DRF view dispatch (via `access_by`), where it
is correctly converted to a 401.
"""

from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.utils.functional import SimpleLazyObject
from karrio.core.utils import Tracer
from karrio.server.core.authentication import AuthenticationMiddleware
from karrio.server.core.middleware import SessionContext
from rest_framework.exceptions import AuthenticationFailed


def _raise_auth_failed():
    raise AuthenticationFailed("User not authorized for requested tenant organization")


class TestAuthenticationMiddlewareLazyOrgFailure(TestCase):
    """process_response must not crash when `request.org.id` resolution fails."""

    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = AuthenticationMiddleware(get_response=lambda r: HttpResponse("OK"))

    def test_process_response_swallows_authentication_failed_from_lazy_org(self):
        """Non-member with x-tenant-id: lazy `request.org.id` raises ->
        response middleware must not 500."""
        request = self.factory.get("/v1/references", HTTP_X_TENANT_ID="tenant-xyz")
        request.org = SimpleLazyObject(_raise_auth_failed)
        response = HttpResponse("OK", status=200)

        # Must NOT raise — previously this propagated AuthenticationFailed
        # out of the middleware and Django turned it into a 500.
        result = self.middleware.process_response(request, response)

        self.assertEqual(result.status_code, 200)
        self.assertNotIn("org_id", result.cookies)
        self.assertNotIn("X-org-id", result)

    def test_process_response_writes_cookie_for_resolved_org(self):
        """Happy path: resolved org still produces the org_id cookie."""

        class _Org:
            id = "org_resolved_123"

        request = self.factory.get("/v1/references")
        request.org = SimpleLazyObject(_Org)
        response = HttpResponse("OK", status=200)

        result = self.middleware.process_response(request, response)

        self.assertEqual(result.cookies["org_id"].value, "org_resolved_123")
        self.assertEqual(result["X-org-id"], "org_resolved_123")

    def test_process_response_handles_missing_org_attribute(self):
        """No `request.org` at all: middleware skips the cookie cleanly."""
        request = self.factory.get("/v1/references")
        response = HttpResponse("OK", status=200)

        result = self.middleware.process_response(request, response)

        self.assertEqual(result.status_code, 200)
        self.assertNotIn("org_id", result.cookies)

    def test_process_response_still_writes_test_mode_cookie(self):
        """Failure on the org cookie path must not block the test_mode cookie."""
        request = self.factory.get("/v1/references", HTTP_X_TENANT_ID="tenant-xyz")
        request.org = SimpleLazyObject(_raise_auth_failed)
        request.test_mode = True
        response = HttpResponse("OK", status=200)

        result = self.middleware.process_response(request, response)

        self.assertEqual(result.status_code, 200)
        self.assertNotIn("org_id", result.cookies)
        self.assertIn("test_mode", result.cookies)
        self.assertEqual(result["X-test-mode"], "True")


class TestSessionContextTelemetryLazyOrgFailure(TestCase):
    """`_inject_telemetry` must not crash when resolving `request.org` raises.

    This is the live production trigger: telemetry runs at the *start* of
    the request, before the view, so a raised AuthenticationFailed here
    becomes a 500 even on AllowAny endpoints like `/v1/references` whose
    own view never touches `request.org`.
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionContext(get_response=lambda r: HttpResponse("OK"))

    def test_inject_telemetry_swallows_authentication_failed_from_lazy_org(self):
        request = self.factory.get("/v1/references", HTTP_X_TENANT_ID="tenant-xyz")
        request.org = SimpleLazyObject(_raise_auth_failed)
        request.request_id = "req_test_123"
        tracer = Tracer()

        # Must NOT raise — previously the lazy resolve here 500'd the request.
        self.middleware._inject_telemetry(tracer, request)

    def test_inject_telemetry_tags_org_id_for_resolved_org(self):
        class _Org:
            id = "org_resolved_123"

        request = self.factory.get("/v1/references")
        request.org = SimpleLazyObject(_Org)
        request.request_id = "req_test_123"
        tracer = Tracer()

        # Happy path: resolved org is still tagged without raising.
        self.middleware._inject_telemetry(tracer, request)
