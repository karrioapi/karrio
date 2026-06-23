"""Unit tests for karrio.core.utils.redaction."""

import unittest

from karrio.core.utils.redaction import REDACTED, redact_headers, redact_query_params


class TestRedactHeaders(unittest.TestCase):
    def test_authorization_bearer_keeps_scheme(self):
        result = redact_headers({"Authorization": "Bearer eyJhbGciOiJSUzI1NiJ9.abc"})
        self.assertEqual(result["Authorization"], f"Bearer {REDACTED}")

    def test_authorization_basic_keeps_scheme(self):
        result = redact_headers({"Authorization": "Basic dXNlcjpwYXNzd29yZA=="})
        self.assertEqual(result["Authorization"], f"Basic {REDACTED}")

    def test_authorization_no_scheme_redacted(self):
        result = redact_headers({"Authorization": "rawtoken123"})
        self.assertEqual(result["Authorization"], REDACTED)

    def test_x_api_key_redacted(self):
        result = redact_headers({"X-Api-Key": "sk-live-abc123xyz"})
        self.assertEqual(result["X-Api-Key"], REDACTED)

    def test_api_key_redacted(self):
        result = redact_headers({"Api-Key": "someapikey"})
        self.assertEqual(result["Api-Key"], REDACTED)

    def test_x_client_secret_redacted(self):
        result = redact_headers({"X-Client-Secret": "super_secret_value"})
        self.assertEqual(result["X-Client-Secret"], REDACTED)

    def test_non_sensitive_headers_preserved(self):
        result = redact_headers(
            {
                "Content-Type": "application/json",
                "X-locale": "en_US",
                "Accept": "application/json",
                "X-RateLimit-Remaining": "95",
            }
        )
        self.assertEqual(result["Content-Type"], "application/json")
        self.assertEqual(result["X-locale"], "en_US")
        self.assertEqual(result["Accept"], "application/json")
        self.assertEqual(result["X-RateLimit-Remaining"], "95")

    def test_mixed_headers(self):
        result = redact_headers(
            {
                "Authorization": "Bearer token123",
                "Content-Type": "application/json",
                "X-Api-Key": "key123",
                "X-Request-Id": "req-abc",
            }
        )
        self.assertEqual(result["Authorization"], f"Bearer {REDACTED}")
        self.assertEqual(result["Content-Type"], "application/json")
        self.assertEqual(result["X-Api-Key"], REDACTED)
        self.assertEqual(result["X-Request-Id"], "req-abc")

    def test_empty_dict_returns_empty(self):
        self.assertEqual(redact_headers({}), {})

    def test_none_returns_empty(self):
        self.assertEqual(redact_headers(None), {})

    def test_non_dict_returns_empty(self):
        self.assertEqual(redact_headers("not a dict"), {})
        self.assertEqual(redact_headers(42), {})

    def test_case_insensitive_header_name(self):
        result = redact_headers({"authorization": "Bearer token"})
        self.assertEqual(result["authorization"], f"Bearer {REDACTED}")

    def test_secret_substring_in_name_redacted(self):
        result = redact_headers({"X-My-Secret-Key": "verysecret"})
        self.assertEqual(result["X-My-Secret-Key"], REDACTED)

    def test_password_substring_in_name_redacted(self):
        result = redact_headers({"X-Password": "mypassword"})
        self.assertEqual(result["X-Password"], REDACTED)

    def test_cookie_redacted(self):
        result = redact_headers({"Cookie": "session=abc123; token=xyz"})
        self.assertEqual(result["Cookie"], REDACTED)

    def test_non_string_value_coerced_to_string(self):
        result = redact_headers({"Content-Length": 1234})
        self.assertEqual(result["Content-Length"], "1234")


class TestRedactQueryParams(unittest.TestCase):
    def test_dict_client_secret_redacted(self):
        result = redact_query_params({"client_id": "my_id", "client_secret": "super_secret"})
        self.assertEqual(result["client_id"], REDACTED)
        self.assertEqual(result["client_secret"], REDACTED)

    def test_dict_non_sensitive_preserved(self):
        result = redact_query_params({"grant_type": "client_credentials", "scope": "read"})
        self.assertEqual(result["grant_type"], "client_credentials")
        self.assertEqual(result["scope"], "read")

    def test_dict_password_redacted(self):
        result = redact_query_params({"username": "admin", "password": "secret"})
        self.assertEqual(result["username"], REDACTED)
        self.assertEqual(result["password"], REDACTED)

    def test_string_query_params_client_secret_redacted(self):
        result = redact_query_params("client_id=myid&client_secret=topsecret&grant_type=cc")
        self.assertIn("client_id=val_xxx", result)
        self.assertIn("client_secret=val_xxx", result)
        self.assertIn("grant_type=cc", result)

    def test_none_returns_empty_dict(self):
        self.assertEqual(redact_query_params(None), {})

    def test_empty_dict_returns_empty(self):
        self.assertEqual(redact_query_params({}), {})


if __name__ == "__main__":
    unittest.main()


class TestTracerRedactsAtCapture(unittest.TestCase):
    """Verify that Tracer.trace() redacts sensitive headers before creating the Record,
    so data is clean at DB write time without any downstream intervention."""

    def test_request_headers_redacted_in_tracer(self):
        from karrio.core.utils.tracing import Tracer

        tracer = Tracer()
        tracer.trace(
            {
                "request_id": "req_123",
                "url": "https://apis.fedex.com/rate/v1/rates/quotes",
                "request_headers": {
                    "Authorization": "Bearer eyJhbGciOiJSUzI1NiJ9.secret",
                    "Content-Type": "application/json",
                    "X-Api-Key": "sk-live-abc123",
                },
            },
            "request",
        )

        records = tracer.records
        self.assertEqual(len(records), 1)
        headers = records[0].data.get("request_headers", {})
        self.assertEqual(headers["Authorization"], "Bearer val_xxx")
        self.assertEqual(headers["X-Api-Key"], "val_xxx")
        self.assertEqual(headers["Content-Type"], "application/json")

    def test_response_headers_redacted_in_tracer(self):
        from karrio.core.utils.tracing import Tracer

        tracer = Tracer()
        tracer.trace(
            {
                "request_id": "req_123",
                "response": "...",
                "response_headers": {
                    "X-RateLimit-Remaining": "95",
                    "Set-Cookie": "session=abc123",
                },
            },
            "response",
        )

        records = tracer.records
        self.assertEqual(len(records), 1)
        headers = records[0].data.get("response_headers", {})
        self.assertEqual(headers["X-RateLimit-Remaining"], "95")
        self.assertEqual(headers["Set-Cookie"], "val_xxx")

    def test_trace_without_headers_unaffected(self):
        from karrio.core.utils.tracing import Tracer

        tracer = Tracer()
        tracer.trace({"request_id": "req_456", "url": "https://example.com"}, "request")

        records = tracer.records
        self.assertEqual(len(records), 1)
        self.assertNotIn("request_headers", records[0].data)
