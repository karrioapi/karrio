"""Deterministic PII / credential scrubbing for Sentry telemetry span bodies.

Replaces the previous Presidio/spaCy NER approach (issue #641). That approach
both **leaked memory** (spaCy interns every unique token into ``vocab.strings``
and never frees it → the long-lived worker grew unbounded → OOM) and **leaked
PII** (NER is only ~41% reliable on names inside JSON values, so many carrier
name fields were never redacted).

The scrubber's input is exclusively the carrier HTTP request/response bodies +
URL attached by the SDK HTTP wrapper (``karrio.core.utils.helpers``'s
``_urlopen_with_span``). Those are **structured** payloads (JSON / XML) from a
known, finite set of connectors — so a deterministic, structural scrubber is
sufficient AND fully testable (no model, no nondeterminism, no memory growth).

Two layers:

1. **Value-shaped PII (field-agnostic)** — applied to every string value and as
   the fallback for non-parseable bodies: email, phone, IBAN, bearer/basic
   tokens, high-entropy secrets. These have a detectable shape, so they're
   caught regardless of the field name.

2. **Structural default-deny** — parse the body (JSON/XML) and walk it. KEEP a
   string value only if it is an obviously-safe shape (number, date, code,
   uuid, country/currency) OR its key is on a small operational allowlist;
   otherwise REDACT. A name in ANY field — known key, unknown key, or buried in
   a free-text ``description`` — is redacted by default. The failure mode is
   over-redaction (safe), never a leak.

This module is intentionally dependency-free (stdlib only): it is imported from
``settings/apm.py`` while Django settings are still being built, and it must
stay standalone-importable.
"""

import json
import logging
import re
import typing
import urllib.parse
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

# Keys in a Sentry span's ``data`` dict whose string values get scrubbed —
# the carrier request/response bodies + URL set by the SDK HTTP wrapper.
_SCRUB_KEYS = frozenset(
    [
        "http.request.body",
        "request.body",
        "http.response.body",
        "response.body",
        "http.url",
    ]
)

# Char cap (matches the SDK's SPAN_BODY_MAX and Sentry's MAX_STRING_LENGTH).
# Oversized payloads (label PDFs, signature images that slipped past upstream
# caps) are dropped wholesale rather than parsed.
_MAX_SCRUB_CHARS = 16384

R_EMAIL = "<REDACTED_EMAIL>"
R_PHONE = "<REDACTED_PHONE>"
R_CREDENTIAL = "<REDACTED_CREDENTIAL>"
R_PII = "<REDACTED_PII>"
R_OVERSIZED = "<REDACTED_OVERSIZED_BODY>"
R_SCRUB_FAILED = "<REDACTED_SCRUB_FAILED>"


# ─────────────────────────────────────────────────────────────────────────────
# Layer 1 — value-shaped PII (field-agnostic)
# ─────────────────────────────────────────────────────────────────────────────
_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
# IBAN: 2-letter country + 2 check digits + 11-30 alphanumerics.
_IBAN_RE = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b")
_BEARER_RE = re.compile(r"(?i)\b(?:bearer|basic)\s+[A-Za-z0-9+/=._\-]{16,}")
# High-entropy secret: a 32+ run of token chars not embedded in a longer word.
_HIGH_ENTROPY_RE = re.compile(r"(?<![A-Za-z0-9+/=])[A-Za-z0-9+/=_\-]{32,}(?![A-Za-z0-9+/=])")
# Phone: requires a '+' or '00' international prefix so bare numeric IDs (which
# default-deny handles structurally anyway) aren't matched as phones.
_PHONE_RE = re.compile(r"(?<!\w)(?:\+|00)\d[\d\s().\-/]{6,}\d")

_VALUE_PII: tuple[tuple[re.Pattern, str], ...] = (
    (_EMAIL_RE, R_EMAIL),
    (_IBAN_RE, R_CREDENTIAL),
    (_BEARER_RE, R_CREDENTIAL),
    (_PHONE_RE, R_PHONE),
    (_HIGH_ENTROPY_RE, R_CREDENTIAL),
)


def _value_pii(text: str) -> str | None:
    """Redact value-shaped PII anywhere in ``text``. Returns the redacted string
    if anything matched, else ``None``."""
    out, hit = text, False
    for rx, rep in _VALUE_PII:
        new = rx.sub(rep, out)
        if new != out:
            out, hit = new, True
    return out if hit else None


# ─────────────────────────────────────────────────────────────────────────────
# Layer 2 — structural default-deny
# ─────────────────────────────────────────────────────────────────────────────
# A canonical UUID is a correlation id (not PII, not a secret) — kept for
# debugging. Checked BEFORE value-PII so the high-entropy rule doesn't eat it.
_UUID_RE = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")

# Value shapes that are definitely not a name / free text → kept for debugging.
# A human name (any case, single or multi token) must NOT match any of these —
# note country/currency codes are kept via _SAFE_KEYS, NOT a short-all-caps shape
# (that would keep 2-3 letter surnames like "LEE"/"WU").
_SAFE_VALUE: tuple[re.Pattern, ...] = (
    re.compile(
        r"[-+]?\d{1,5}(\.\d+)?$"
    ),  # short int / decimal (qty, weight, zip); ≥6 digits → redacted (phone/account/id), keyed numerics kept via _SAFE_KEYS
    re.compile(r"(?i)(true|false|null|none|yes|no)$"),  # bool / null
    re.compile(r"\d{4}-\d\d-\d\d([ T][\d:.,+\-Zz]*)?$"),  # ISO date / datetime
    re.compile(r"\d\d:\d\d(:\d\d)?$"),  # time
    # alphanumeric code/id with BOTH a letter AND a digit, no spaces (V01PAK,
    # 1Z999AA10123456784). The letter requirement means pure-digit phone/account
    # numbers are NOT kept here — they fall to the >6-digit redaction above.
    re.compile(r"(?=[A-Za-z0-9._\-]*[A-Za-z])(?=[A-Za-z0-9._\-]*\d)[A-Za-z0-9._\-]{2,}$"),
)

# Operational keys whose free-text values never carry PII → kept for debugging.
# Deliberately conservative: NO *description / *note / *remark / *instruction /
# address keys (those can contain names) — default-deny redacts those.
_SAFE_KEYS = frozenset(
    {
        "service",
        "servicename",
        "servicecode",
        "servicelevel",
        "product",
        "productname",
        "status",
        "statuscode",
        "state",
        "carrier",
        "carriercode",
        "carriername",
        "currency",
        "country",
        "countrycode",
        "weightunit",
        "dimensionunit",
        "method",
        "type",
        "mode",
        "label_type",
        "labeltype",
        "format",
        "trackingnumber",
        "trackingnumbers",
        "barcode",
        # operational numerics (kept regardless of digit count; never PII)
        "weight",
        "height",
        "width",
        "length",
        "quantity",
        "pieces",
        "count",
        "amount",
        "price",
    }
)

# Keys that denote PII / secrets — force-redact regardless of value shape. This
# catches short secrets/accounts/ids that LOOK like safe codes (e.g.
# client_secret=SEKRET123, accountNumber=998877, siteId=AB12CD). Allowlisted
# operational keys (_SAFE_KEYS) are checked first and win, so this only fires on
# non-allowlisted keys. Purely additive: it can only redact MORE, never cause a
# leak — the no-leak guarantee still comes from default-deny.
#
# Derived from a carrier-payload PII audit (see .claude/rules/pii-scrubbing.md +
# the audit-pii skill). Re-run that audit per PRD that adds a PII-bearing
# integration. NOTE: long numeric secrets (meterNumber, routingNumber, …) are
# already covered by the ≥6-digit redaction, and free-text keys (*Description,
# *Note) by default-deny — so this list only needs the SHORT, safe-shaped cases.
# Tokens are matched as substrings, so avoid collision-prone ones (e.g. "meter"
# hits "parameter", "bic" hits "cubic", "routing" hits operational routingCode).
_PII_KEY_RE = re.compile(
    r"(?i)(name|email|mail|phone|fax|mobile|contact|recipient|consignee|shipper"
    r"|sender|signator|signed|attention|customer|holder|account|iban|secret"
    r"|password|token|apikey|api_key|client|auth|ssn|taxid|vat|passport|birth|dob"
    r"|siteid)"
)


def _is_safe_value(value: str) -> bool:
    v = value.strip()
    return v == "" or any(rx.match(v) for rx in _SAFE_VALUE)


def _scrub_value(key: str | None, value: str) -> str:
    """Decide keep/redact for one structured string value.

    Order: keep correlation UUIDs → redact value-shaped PII (field-agnostic) →
    keep explicitly-allowlisted operational keys → force-redact known PII/secret
    keys (catches short secrets/accounts that look like codes) → keep
    obviously-safe value shapes → DEFAULT-DENY redact everything else.
    """
    k = key.lower() if key else ""
    if _UUID_RE.match(value.strip()):  # correlation id — keep (before value-PII)
        return value
    pii = _value_pii(value)
    if pii is not None:  # email / phone / credential / IBAN anywhere
        return pii
    if k in _SAFE_KEYS:  # explicit operational allowlist wins
        return value
    if k and _PII_KEY_RE.search(k):  # known PII/secret key → redact regardless of shape
        return R_PII
    if _is_safe_value(value):  # number / date / alphanumeric code
        return value
    return R_PII  # DEFAULT-DENY: unknown free-text / name → redact


def _walk_json(node: typing.Any, key: str | None = None) -> typing.Any:
    if isinstance(node, dict):
        return {k: _walk_json(v, k) for k, v in node.items()}
    if isinstance(node, list):
        return [_walk_json(v, key) for v in node]
    if isinstance(node, str):
        return _scrub_value(key, node)
    return node  # int / float / bool / None kept as-is


_XML_DTD_RE = re.compile(r"<!\s*(?:DOCTYPE|ENTITY)", re.IGNORECASE)


def _scrub_xml(text: str) -> str | None:
    """Walk XML, redacting element text + attribute values by tag/attr name.
    Returns ``None`` if the body isn't safe, parseable XML."""
    # Reject DTD / entity declarations BEFORE parsing — they're what enables
    # "billion laughs" / XXE expansion attacks (a small body that explodes memory
    # on parse; the upstream size cap doesn't protect against expansion). Carrier
    # XML never uses a DTD, so such a body falls back to the freeform path.
    # stdlib ElementTree additionally resolves no external entities by default.
    if _XML_DTD_RE.search(text):
        return None
    try:
        root = ET.fromstring(text)  # noqa: S314 — DTD/entity bodies rejected above; no external-entity resolution
    except ET.ParseError:
        return None
    for el in root.iter():
        tag = el.tag.split("}")[-1]  # strip namespace
        if el.text and el.text.strip():
            el.text = _scrub_value(tag, el.text)
        for attr, av in list(el.attrib.items()):
            el.attrib[attr] = _scrub_value(attr, av)
    return ET.tostring(root, encoding="unicode")


# URLs (http.url): redact sensitive query-param values + any value-shaped PII.
_SENSITIVE_QUERY = re.compile(
    r"(?i)([?&][^=&]*(?:key|secret|token|password|account|auth|sig|signature)[^=&]*=)([^&#]+)"
)


def _scrub_url(url: str) -> str:
    url = _SENSITIVE_QUERY.sub(lambda m: m.group(1) + R_CREDENTIAL, url)
    return _value_pii(url) or url


# application/x-www-form-urlencoded bodies (OAuth token requests + some carrier
# APIs). Form-shaped = key=value pairs with no raw whitespace (spaces are + / %20).
_FORM_RE = re.compile(r"^[^\s=&]+=[^\s&]*(?:&[^\s=&]+=[^\s&]*)*$")


def _scrub_form(text: str) -> str | None:
    """Scrub a form-urlencoded body per-pair (default-deny). Returns None if the
    body isn't form-shaped (so the caller falls through to the freeform path)."""
    stripped = text.strip()
    if not _FORM_RE.match(stripped):
        return None
    pairs = urllib.parse.parse_qsl(stripped, keep_blank_values=True)
    if not pairs:
        return None
    return urllib.parse.urlencode([(k, _scrub_value(k, v)) for k, v in pairs])


# Fallback for truncated / malformed JSON (the 16KB cap can cut JSON mid-object):
# redact complete "key":"value" string pairs via default-deny, then value-PII.
_JSON_PAIR_RE = re.compile(r'("(?:[^"\\]|\\.)*")\s*:\s*("(?:[^"\\]|\\.)*")')


def _scrub_freeform(text: str) -> str:
    if '":' in text:

        def _repl(m: re.Match) -> str:
            try:
                k = json.loads(m.group(1))
                v = json.loads(m.group(2))
            except ValueError:
                return m.group(0)
            return f"{m.group(1)}: {json.dumps(_scrub_value(k, v), ensure_ascii=False)}"

        text = _JSON_PAIR_RE.sub(_repl, text)
    return _value_pii(text) or text


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────
def scrub_text(text: typing.Any) -> typing.Any:
    """Redact PII / credentials from a carrier body or URL string.

    Non-strings and empty strings pass through. Oversized bodies are dropped.
    JSON and XML bodies are walked structurally (default-deny); URLs get
    query-param redaction; anything else falls back to per-pair + value-shaped
    redaction.
    """
    if not isinstance(text, str) or not text:
        return text
    if len(text) > _MAX_SCRUB_CHARS:
        return R_OVERSIZED

    if text.lstrip().startswith(("http://", "https://")):
        return _scrub_url(text)

    try:
        return json.dumps(_walk_json(json.loads(text)), ensure_ascii=False)
    except (ValueError, TypeError):
        pass

    xml = _scrub_xml(text)
    if xml is not None:
        return xml

    form = _scrub_form(text)
    if form is not None:
        return form

    return _scrub_freeform(text)


def scrub_span_data(data: dict | None) -> dict:
    """Scrub PII from span data; only touches ``_SCRUB_KEYS`` string values.

    Per-key try/except so a failure on one field doesn't discard scrubbing
    already done on the others. On a scrub error we **fail closed** — the field
    is replaced with ``R_SCRUB_FAILED`` rather than passed through raw, so an
    unexpected error can never leak an un-redacted carrier body to Sentry. If
    the dict iteration itself fails, the exception propagates to the caller
    (``_sentry_before_send_transaction``), whose own try/except drops to
    returning the event unchanged — a residual fail-open the caller owns.
    """
    if data is None:
        return {}
    if not isinstance(data, dict):
        return data

    result = {}
    for key, value in data.items():
        if key in _SCRUB_KEYS and isinstance(value, str):
            try:
                result[key] = scrub_text(value)
            except Exception:
                # Fail CLOSED: never emit a raw payload because scrubbing errored.
                logger.warning(
                    "telemetry_scrubbing: scrub_text failed for key=%r; failing closed (redacted)",
                    key,
                    exc_info=True,
                )
                result[key] = R_SCRUB_FAILED
        else:
            result[key] = value
    return result
