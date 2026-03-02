"""
Sensitive data redaction utilities for karrio tracing.

Used to sanitize HTTP headers and query parameters before they are stored
in TracingRecord.record — ensuring secrets (API keys, auth tokens, passwords)
never reach the database in plaintext.

Redaction format:
  - Authorization: Bearer eyJ...  →  Authorization: Bearer val_xxx
  - Authorization: Basic dXNlc...  →  Authorization: Basic val_xxx
  - X-Api-Key: sk-abc123  →  X-Api-Key: val_xxx
  - client_secret=abc123  →  client_secret=val_xxx
"""

import re
import typing
import urllib.parse


# Header names (lowercase) whose values should be redacted.
SENSITIVE_HEADER_NAMES: typing.FrozenSet[str] = frozenset(
    [
        "authorization",
        "x-api-key",
        "api-key",
        "x-auth-token",
        "x-client-secret",
        "x-password",
        "x-secret",
        "x-access-token",
        "x-token",
        "proxy-authorization",
        "cookie",
        "set-cookie",
    ]
)

# Header name substrings (lowercase) that indicate a sensitive header.
SENSITIVE_HEADER_SUBSTRINGS: typing.Tuple[str, ...] = (
    "secret",
    "password",
    "credential",
    "apikey",
    "api_key",
    "authtoken",
    "auth_token",
    "accesstoken",
    "access_token",
)

# Query parameter names (lowercase) whose values should be redacted.
SENSITIVE_PARAM_NAMES: typing.FrozenSet[str] = frozenset(
    [
        "client_id",
        "client_secret",
        "username",
        "password",
        "api_key",
        "apikey",
        "access_token",
        "token",
        "secret",
        "auth",
        "authorization",
        "key",
    ]
)

# Regex: matches long alphanumeric strings that look like tokens/keys (>20 chars).
_LONG_TOKEN_RE = re.compile(r"[A-Za-z0-9+/=_\-]{21,}")

REDACTED = "val_xxx"


def _is_sensitive_header(name: str) -> bool:
    """Return True if this header name is considered sensitive."""
    lower = name.lower().replace("-", "_")
    if name.lower() in SENSITIVE_HEADER_NAMES:
        return True
    return any(sub in lower for sub in SENSITIVE_HEADER_SUBSTRINGS)


def _redact_header_value(name: str, value: str) -> str:
    """Redact a sensitive header value, preserving scheme prefixes where applicable."""
    if not isinstance(value, str):
        return REDACTED

    lower_name = name.lower()

    if lower_name == "authorization":
        # Keep the scheme prefix: "Bearer val_xxx" or "Basic val_xxx"
        parts = value.split(" ", 1)
        if len(parts) == 2:
            scheme = parts[0]
            return f"{scheme} {REDACTED}"
        return REDACTED

    if lower_name in ("cookie", "set-cookie"):
        # Redact all cookie values
        return REDACTED

    return REDACTED


def redact_headers(headers: typing.Any) -> typing.Dict[str, str]:
    """
    Return a copy of the headers dict with sensitive values redacted.

    Non-dict inputs are returned as an empty dict.
    Non-string values are coerced to strings.
    """
    if not isinstance(headers, dict):
        return {}

    result: typing.Dict[str, str] = {}
    for name, value in headers.items():
        str_value = str(value) if not isinstance(value, str) else value
        if _is_sensitive_header(str(name)):
            result[str(name)] = _redact_header_value(str(name), str_value)
        else:
            result[str(name)] = str_value

    return result


def redact_query_params(params: typing.Union[str, dict, None]) -> typing.Union[str, dict]:
    """
    Redact sensitive query parameter values.

    Accepts either a dict or a URL-encoded query string.
    Returns the same type that was passed in.
    """
    if params is None:
        return {}

    if isinstance(params, dict):
        return {
            k: (REDACTED if k.lower() in SENSITIVE_PARAM_NAMES else v)
            for k, v in params.items()
        }

    if isinstance(params, str):
        try:
            parsed = urllib.parse.parse_qs(params, keep_blank_values=True)
            redacted = {
                k: ([REDACTED] if k.lower() in SENSITIVE_PARAM_NAMES else v)
                for k, v in parsed.items()
            }
            return urllib.parse.urlencode(redacted, doseq=True)
        except Exception:
            return params

    return params
