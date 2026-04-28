from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.urls import reverse
from karrio.core.utils.helpers import _resolve_request_id
from karrio.core.utils.tracing import Tracer
from karrio.server.core.middleware import (
    RequestIDMiddleware,
    _generate_request_id,
    _is_valid_request_id,
)
from karrio.server.core.tests.base import APITestCase


class TestRequestIDValidation(TestCase):
    """Test request ID validation and generation utilities."""

    def test_generated_request_id_has_prefix(self):
        request_id = _generate_request_id()
        self.assertTrue(request_id.startswith("req_"))

    def test_generated_request_id_is_valid(self):
        request_id = _generate_request_id()
        self.assertTrue(_is_valid_request_id(request_id))

    def test_generated_request_ids_are_unique(self):
        ids = {_generate_request_id() for _ in range(100)}
        self.assertEqual(len(ids), 100)

    def test_valid_request_id_alphanumeric(self):
        self.assertTrue(_is_valid_request_id("abc123"))

    def test_valid_request_id_with_dashes(self):
        self.assertTrue(_is_valid_request_id("abc-123-def"))

    def test_valid_request_id_with_underscores(self):
        self.assertTrue(_is_valid_request_id("abc_123_def"))

    def test_valid_request_id_with_dots(self):
        self.assertTrue(_is_valid_request_id("abc.123.def"))

    def test_valid_request_id_mixed_chars(self):
        self.assertTrue(_is_valid_request_id("req_abc-123.def_456"))

    def test_invalid_request_id_empty(self):
        self.assertFalse(_is_valid_request_id(""))

    def test_invalid_request_id_spaces(self):
        self.assertFalse(_is_valid_request_id("abc 123"))

    def test_invalid_request_id_special_chars(self):
        self.assertFalse(_is_valid_request_id("abc@123"))
        self.assertFalse(_is_valid_request_id("abc#123"))
        self.assertFalse(_is_valid_request_id("abc$123"))

    def test_invalid_request_id_too_long(self):
        long_id = "a" * 201
        self.assertFalse(_is_valid_request_id(long_id))

    def test_valid_request_id_max_length(self):
        max_id = "a" * 200
        self.assertTrue(_is_valid_request_id(max_id))


class TestRequestIDMiddleware(TestCase):
    """Test the RequestIDMiddleware behavior."""

    def setUp(self):
        self.factory = RequestFactory()
        self.get_response = lambda request: HttpResponse("OK")
        self.middleware = RequestIDMiddleware(self.get_response)

    def test_generates_request_id_when_no_header(self):
        request = self.factory.get("/")
        response = self.middleware(request)

        self.assertTrue(request.request_id.startswith("req_"))
        self.assertEqual(response["X-Request-ID"], request.request_id)

    def test_uses_client_provided_request_id(self):
        request = self.factory.get("/", HTTP_X_REQUEST_ID="my-custom-id-123")
        response = self.middleware(request)

        self.assertEqual(request.request_id, "my-custom-id-123")
        self.assertEqual(response["X-Request-ID"], "my-custom-id-123")

    def test_rejects_invalid_client_request_id(self):
        request = self.factory.get("/", HTTP_X_REQUEST_ID="invalid id with spaces")
        self.middleware(request)

        self.assertTrue(request.request_id.startswith("req_"))
        self.assertNotEqual(request.request_id, "invalid id with spaces")

    def test_rejects_empty_client_request_id(self):
        request = self.factory.get("/", HTTP_X_REQUEST_ID="")
        self.middleware(request)

        self.assertTrue(request.request_id.startswith("req_"))

    def test_strips_whitespace_from_client_id(self):
        request = self.factory.get("/", HTTP_X_REQUEST_ID="  valid-id  ")
        self.middleware(request)

        self.assertEqual(request.request_id, "valid-id")

    def test_response_always_has_x_request_id_header(self):
        request = self.factory.get("/")
        response = self.middleware(request)

        self.assertIn("X-Request-ID", response)
        self.assertTrue(len(response["X-Request-ID"]) > 0)


class TestRequestIDInAPI(APITestCase):
    """Test that X-Request-ID flows through API endpoints."""

    def test_response_contains_x_request_id_header(self):
        url = reverse("karrio.server.manager:shipment-list")
        response = self.client.get(url)

        self.assertIn("X-Request-ID", response)
        self.assertTrue(response["X-Request-ID"].startswith("req_"))

    def test_client_provided_request_id_returned(self):
        url = reverse("karrio.server.manager:shipment-list")
        response = self.client.get(url, HTTP_X_REQUEST_ID="test-req-001")

        self.assertEqual(response["X-Request-ID"], "test-req-001")

    def test_invalid_client_request_id_replaced(self):
        url = reverse("karrio.server.manager:shipment-list")
        response = self.client.get(url, HTTP_X_REQUEST_ID="invalid id!")

        self.assertNotEqual(response["X-Request-ID"], "invalid id!")
        self.assertTrue(response["X-Request-ID"].startswith("req_"))


class TestRequestIDPropagation(TestCase):
    """Test request_id propagation from tracer context to SDK HTTP calls."""

    def setUp(self):
        self.maxDiff = None

    def test_resolve_request_id_from_tracer_context(self):
        """Verify request_id is extracted from tracer context via with_metadata."""
        tracer = Tracer()
        tracer.add_context({"request_id": "req_test-123"})
        trace_fn = tracer.with_metadata({})

        result = _resolve_request_id(trace_fn)

        self.assertEqual(result, "req_test-123")

    def test_resolve_request_id_generates_uuid_without_tracer(self):
        """Verify fallback to UUID when trace is None."""
        result = _resolve_request_id(None)

        self.assertRegex(result, r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")

    def test_resolve_request_id_generates_uuid_without_context(self):
        """Verify fallback to UUID when tracer has no request_id in context."""
        tracer = Tracer()
        trace_fn = tracer.with_metadata({})

        result = _resolve_request_id(trace_fn)

        self.assertRegex(result, r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")

    def test_resolve_request_id_with_empty_context(self):
        """Verify fallback when tracer context exists but request_id is empty."""
        tracer = Tracer()
        tracer.add_context({"request_id": ""})
        trace_fn = tracer.with_metadata({})

        result = _resolve_request_id(trace_fn)

        self.assertRegex(result, r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")

    def test_tracer_reference_attached_to_with_metadata(self):
        """Verify _tracer attribute is set on with_metadata return value."""
        tracer = Tracer()
        trace_fn = tracer.with_metadata({"connection": {"carrier_name": "test"}})

        self.assertTrue(hasattr(trace_fn, "_tracer"))
        self.assertIs(trace_fn._tracer, tracer)

    def test_request_id_propagated_through_trace_as(self):
        """Verify request_id survives Settings.trace_as() wrapping chain."""
        # Create a minimal concrete Settings subclass for testing
        import attr
        from karrio.core.settings import Settings

        @attr.s(auto_attribs=True)
        class TestSettings(Settings):
            carrier_id: str = "test"

            @property
            def carrier_name(self):
                return "test_carrier"

        settings = TestSettings(carrier_id="test-carrier")
        tracer = Tracer()
        tracer.add_context({"request_id": "req_through-trace-as"})
        settings.tracer = tracer

        trace_fn = settings.trace_as("json")

        result = _resolve_request_id(trace_fn)

        self.assertEqual(result, "req_through-trace-as")

    def test_trace_as_creates_tracer_if_missing(self):
        """Verify trace_as() creates a tracer when none exists."""
        import attr
        from karrio.core.settings import Settings

        @attr.s(auto_attribs=True)
        class TestSettings(Settings):
            carrier_id: str = "test"

            @property
            def carrier_name(self):
                return "test_carrier"

        settings = TestSettings(carrier_id="test-carrier")
        settings.tracer = None

        trace_fn = settings.trace_as("json")

        self.assertIsNotNone(settings.tracer)
        self.assertTrue(hasattr(trace_fn, "_tracer"))
