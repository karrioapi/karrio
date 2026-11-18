"""Links the server puts into emails (password reset, sign-up, email change).

Each of those emails carries a one-time token, so where its link points is a
security decision. A client may still choose the page (``redirect_url``), but
only on a frontend the operator listed: ``DASHBOARD_URL`` and
``EMAIL_LINK_ALLOWED_ORIGINS``. Without ``redirect_url`` the link is built
from ``DASHBOARD_URL``. Nothing configured means no link, so no email.
"""

import typing
import urllib.parse
import django.core.exceptions as exceptions

from karrio.server.conf import settings
from karrio.server.core.logging import logger

# Dashboard routes the emails link to when the client does not choose one.
CONFIRM_EMAIL_ROUTE = "email"
CHANGE_EMAIL_ROUTE = "email/change"
RESET_PASSWORD_ROUTE = "password/reset"  # noqa: S105 - a URL path, not a credential

DEFAULT_PORTS = {"http": 80, "https": 443}
REFUSED_MESSAGE = (
    "redirect_url is not on an allowed frontend. The server operator must list it "
    "in DASHBOARD_URL or EMAIL_LINK_ALLOWED_ORIGINS."
)
UNCONFIGURED_MESSAGE = (
    "Email links are not configured. The server operator must set DASHBOARD_URL "
    "(or EMAIL_LINK_ALLOWED_ORIGINS) on the API."
)


def build_link(base_url: str, route: str, **query: str) -> str:
    """Join `route` onto the app's `base_url`, with `query` appended when given."""
    url = f"{base_url.rstrip('/')}/{route.lstrip('/')}"

    return f"{url}?{urllib.parse.urlencode(query)}" if query else url


def normalize_origin(url: typing.Any) -> typing.Optional[str]:
    """``scheme://host[:port]`` of an absolute http(s) URL, or None.

    Lower-cases scheme and host, drops a default port and a trailing dot on
    the host. Anything a browser and this parser could read differently is
    refused: userinfo, backslashes, whitespace, control characters, a
    missing scheme (``//host``) and invalid ports.
    """
    if not isinstance(url, str) or not url:
        return None
    if any(c.isspace() or c == "\\" or ord(c) < 0x20 or ord(c) == 0x7F for c in url):
        return None

    try:  # malformed authorities ("https://[x/", NFKC look-alikes) raise ValueError
        parts = urllib.parse.urlsplit(url)
        scheme = parts.scheme.lower()
        if scheme not in DEFAULT_PORTS or not parts.netloc or "@" in parts.netloc:
            return None
        port = parts.port or DEFAULT_PORTS[scheme]
        host = (parts.hostname or "").rstrip(".")
    except ValueError:
        return None

    if not host:
        return None
    if ":" in host:  # IPv6 literal
        host = f"[{host}]"

    return f"{scheme}://{host}" + ("" if port == DEFAULT_PORTS[scheme] else f":{port}")


def _plain_base(url: typing.Any) -> typing.Optional[urllib.parse.SplitResult]:
    """`url` split, when it is an http(s) URL without query or fragment: the
    email appends its own query or token, so neither may be in the base."""
    if normalize_origin(url) is None:
        return None
    parts = urllib.parse.urlsplit(url)
    return None if parts.query or parts.fragment else parts


def allowed_origins() -> typing.Set[str]:
    """Origins of the configured frontends. A configured value that is not a
    plain http(s) URL (one with a query or fragment, say) is treated as not
    configured: it authorises nothing, whether or not redirect_url is given."""
    configured = [
        getattr(settings, "DASHBOARD_URL", None),
        *(getattr(settings, "EMAIL_LINK_ALLOWED_ORIGINS", None) or []),
    ]
    return {normalize_origin(url) for url in configured if _plain_base(url)}


def _refuse(message: str, **details) -> typing.NoReturn:
    logger.warning("Email link refused", reason=message, **details)
    raise exceptions.ValidationError(message, code="invalid_redirect_url")


def email_link(route: str, redirect_url: typing.Optional[str] = None) -> str:
    """The base URL an email links to; the email appends its token to it.

    Raises ValidationError when the link would leave the configured
    frontends, so the caller sends nothing and creates nothing.
    """
    if not redirect_url:
        dashboard = getattr(settings, "DASHBOARD_URL", None)
        if _plain_base(dashboard) is None:
            _refuse(UNCONFIGURED_MESSAGE)
        return build_link(dashboard, route)

    parts = _plain_base(redirect_url)
    origin = normalize_origin(redirect_url)
    if parts is None:
        _refuse(REFUSED_MESSAGE, origin=origin)
    if origin not in allowed_origins():
        _refuse(
            UNCONFIGURED_MESSAGE if not allowed_origins() else REFUSED_MESSAGE,
            origin=origin,
        )

    return f"{origin}{parts.path}"
