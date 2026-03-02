"""Unit tests for karrio.core.utils.redaction."""

import pytest
from karrio.core.utils.redaction import redact_headers, redact_query_params, REDACTED


class TestRedactHeaders:
    def test_authorization_bearer_keeps_scheme(self):
        result = redact_headers({"Authorization": "Bearer eyJhbGciOiJSUzI1NiJ9.abc"})
        assert result["Authorization"] == f"Bearer {REDACTED}"

    def test_authorization_basic_keeps_scheme(self):
        result = redact_headers({"Authorization": "Basic dXNlcjpwYXNzd29yZA=="})
        assert result["Authorization"] == f"Basic {REDACTED}"

    def test_authorization_no_scheme(self):
        result = redact_headers({"Authorization": "rawtoken123"})
        assert result["Authorization"] == REDACTED

    def test_x_api_key_redacted(self):
        result = redact_headers({"X-Api-Key": "sk-live-abc123xyz"})
        assert result["X-Api-Key"] == REDACTED

    def test_api_key_redacted(self):
        result = redact_headers({"Api-Key": "someapikey"})
        assert result["Api-Key"] == REDACTED

    def test_x_client_secret_redacted(self):
        result = redact_headers({"X-Client-Secret": "super_secret_value"})
        assert result["X-Client-Secret"] == REDACTED

    def test_non_sensitive_headers_preserved(self):
        result = redact_headers({
            "Content-Type": "application/json",
            "X-locale": "en_US",
            "Accept": "application/json",
            "X-RateLimit-Remaining": "95",
        })
        assert result["Content-Type"] == "application/json"
        assert result["X-locale"] == "en_US"
        assert result["Accept"] == "application/json"
        assert result["X-RateLimit-Remaining"] == "95"

    def test_mixed_headers(self):
        result = redact_headers({
            "Authorization": "Bearer token123",
            "Content-Type": "application/json",
            "X-Api-Key": "key123",
            "X-Request-Id": "req-abc",
        })
        assert result["Authorization"] == f"Bearer {REDACTED}"
        assert result["Content-Type"] == "application/json"
        assert result["X-Api-Key"] == REDACTED
        assert result["X-Request-Id"] == "req-abc"

    def test_empty_dict(self):
        assert redact_headers({}) == {}

    def test_non_dict_returns_empty(self):
        assert redact_headers(None) == {}
        assert redact_headers("not a dict") == {}
        assert redact_headers(42) == {}

    def test_case_insensitive_header_names(self):
        result = redact_headers({"authorization": "Bearer token"})
        assert result["authorization"] == f"Bearer {REDACTED}"

    def test_secret_substring_match(self):
        result = redact_headers({"X-My-Secret-Key": "verysecret"})
        assert result["X-My-Secret-Key"] == REDACTED

    def test_password_substring_match(self):
        result = redact_headers({"X-Password": "mypassword"})
        assert result["X-Password"] == REDACTED

    def test_cookie_redacted(self):
        result = redact_headers({"Cookie": "session=abc123; token=xyz"})
        assert result["Cookie"] == REDACTED

    def test_non_string_value_coerced(self):
        result = redact_headers({"Content-Length": 1234})
        assert result["Content-Length"] == "1234"


class TestRedactQueryParams:
    def test_dict_client_secret_redacted(self):
        result = redact_query_params({"client_id": "my_id", "client_secret": "super_secret"})
        assert result["client_id"] == REDACTED
        assert result["client_secret"] == REDACTED

    def test_dict_non_sensitive_preserved(self):
        result = redact_query_params({"grant_type": "client_credentials", "scope": "read"})
        assert result["grant_type"] == "client_credentials"
        assert result["scope"] == "read"

    def test_dict_password_redacted(self):
        result = redact_query_params({"username": "admin", "password": "secret"})
        assert result["username"] == REDACTED
        assert result["password"] == REDACTED

    def test_string_query_params(self):
        result = redact_query_params("client_id=myid&client_secret=topsecret&grant_type=cc")
        assert "client_id=val_xxx" in result
        assert "client_secret=val_xxx" in result
        assert "grant_type=cc" in result

    def test_none_returns_empty(self):
        assert redact_query_params(None) == {}

    def test_empty_dict(self):
        assert redact_query_params({}) == {}
