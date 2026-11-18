"""Webhook destination policy and DNS-pinned direct delivery."""

import ipaddress
import json
import socket
import re
from urllib.parse import urlsplit, urlunsplit

import requests
import urllib3
from django.conf import settings
from django.core.exceptions import ValidationError

ERROR = "Webhook destination must resolve to an allowed address."
# Metadata endpoints never become reachable through an operator exception.
METADATA = tuple(
    map(
        ipaddress.ip_network,
        (
            "169.254.0.0/16",
            "fd00:ec2::254/128",
            "fd20:ce::254/128",
            "100.100.100.200/32",
        ),
    )
)

# Deny transition mechanisms rather than trusting how a particular network
# routes their embedded IPv4 addresses (including metadata addresses).
IPV4_TRANSITION = tuple(
    map(
        ipaddress.ip_network,
        (
            "64:ff9b::/96",
            "64:ff9b:1::/48",
            "::/96",
            "::ffff:0:0:0/96",
            "2002::/16",
            "2001::/32",  # Teredo
        ),
    )
)
# ISATAP (RFC 5214 section 6.1) embeds an IPv4 address in the interface
# identifier, under any /64: 0000:5efe or 0200:5efe in bits 64-95.
ISATAP_MARKERS = (0x00005EFE, 0x02005EFE)
# An IPv6 destination must be global unicast: inside this block and is_global.
IPV6_GLOBAL_UNICAST = ipaddress.ip_network("2000::/3")
HOST_LABEL = re.compile(r"[a-z0-9-]{1,63}")
URI_CHARACTERS = re.compile(r"^[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+$")


def canonical_host(host):
    """Return the IDNA-canonical host, or raise ValueError.

    The check runs on the canonical form (the one DNS, Host, SNI and a proxy
    will see), not on the input: IDNA folds look-alike characters such as the
    full-width percent sign into ASCII. Only an IP literal or lower-case
    letter-digit-hyphen labels (1-63 each, 253 in total) are accepted.
    """
    host = host.encode("idna").decode("ascii").lower()
    if "%" not in host:  # a zone identifier is not part of a destination
        try:
            ipaddress.ip_address(host)
            return host
        except ValueError:
            pass
    name = host[:-1] if host.endswith(".") else host  # absolute name
    if len(name) > 253 or not all(
        HOST_LABEL.fullmatch(label) for label in name.split(".")
    ):
        raise ValueError(ERROR)
    return host


def resolve_destination(url):
    try:
        parsed = urlsplit(url)
        host = parsed.hostname
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        if (
            parsed.scheme not in ("http", "https")
            or not host
            or parsed.username is not None
            or parsed.password is not None
            or parsed.fragment
            or any(c.isspace() or ord(c) < 32 or ord(c) == 127 for c in url)
        ):
            raise ValueError(ERROR)
        # Only the hostname may be Unicode. Canonicalize it before DNS, Host,
        # TLS SNI and proxy delivery, so every parser sees the same authority.
        host = canonical_host(host)
        authority = f"[{host}]" if ":" in host else host
        if parsed.port is not None:
            authority += f":{port}"
        canonical = urlunsplit(
            (parsed.scheme, authority, parsed.path or "/", parsed.query, "")
        )
        if (
            not URI_CHARACTERS.fullmatch(canonical)
            or re.search(r"%(?![0-9A-Fa-f]{2})", canonical)
            or urllib3.util.parse_url(canonical).host.strip("[]") != host
        ):
            raise ValueError(ERROR)
        parsed = urlsplit(canonical)
        answers = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
        addresses = list(dict.fromkeys(answer[4][0] for answer in answers))
        if not addresses:
            raise ValueError(ERROR)
        exceptions = getattr(settings, "WEBHOOK_ALLOWED_DESTINATIONS", [])
        for address in addresses:
            ip = ipaddress.ip_address(address)
            ip = getattr(ip, "ipv4_mapped", None) or ip
            if ip.version == 6 and (
                any(ip in network for network in IPV4_TRANSITION)
                or (int(ip) >> 32) & 0xFFFFFFFF in ISATAP_MARKERS
            ):
                raise ValueError(ERROR)
            if any(
                ip in network for network in METADATA if ip.version == network.version
            ):
                raise ValueError(ERROR)
            allowed = host.lower() in [value.lower() for value in exceptions]
            for value in exceptions:
                try:
                    allowed = allowed or ip in ipaddress.ip_network(value, strict=False)
                except ValueError:
                    pass  # Exact hostname entries are handled above, never suffix matches.
            global_unicast = ip.is_global and (
                ip.version == 4 or ip in IPV6_GLOBAL_UNICAST
            )
            if (
                not global_unicast or ip.is_multicast or ip.is_unspecified
            ) and not allowed:
                raise ValueError(ERROR)
        return parsed, addresses[0], port
    except (
        ValueError,
        OSError,
        TypeError,
        urllib3.exceptions.LocationParseError,
    ) as error:
        raise ValidationError(ERROR) from error


def post_webhook(url, payload, headers):
    parsed, address, port = resolve_destination(url)
    url = parsed.geturl()
    proxies = requests.utils.get_environ_proxies(url)
    if requests.utils.select_proxy(url, proxies):
        # Operators control the egress proxy: it resolves the validated hostname
        # itself. DNS pinning applies only to direct connections.
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=(5, 15),
            allow_redirects=False,
            proxies=proxies,
            stream=True,
        )
        response.close()
    else:
        secure = parsed.scheme == "https"
        pool_class = (
            urllib3.HTTPSConnectionPool if secure else urllib3.HTTPConnectionPool
        )
        tls = (
            dict(
                server_hostname=parsed.hostname,
                assert_hostname=parsed.hostname,
                cert_reqs="CERT_REQUIRED",
                ca_certs=requests.certs.where(),
            )
            if secure
            else {}
        )
        pool = pool_class(
            address, port=port, timeout=urllib3.Timeout(connect=5, read=15), **tls
        )
        host = f"[{parsed.hostname}]" if ":" in parsed.hostname else parsed.hostname
        authority = f"{host}:{port}" if parsed.port else host
        path = parsed.path or "/"
        if parsed.query:
            path += "?" + parsed.query
        try:
            result = pool.urlopen(
                "POST",
                path,
                body=json.dumps(payload).encode(),
                headers={**headers, "Host": authority},
                redirect=False,
                retries=False,
                preload_content=False,
            )
            response = requests.Response()
            response.status_code = result.status
            # Webhook bodies are not consumed by any caller; bound memory usage.
            result.close()
        finally:
            pool.close()
    # requests considers 3xx "ok", but a redirect is a failed webhook delivery.
    if 300 <= response.status_code < 400:
        response.status_code = 502
    return response
