"""Public-ID encryption for tenant-facing surfaces.

This module provides reversible, server-only encrypted identifiers for
sensitive database primary keys (e.g. ``SystemConnection.id``,
``BrokeredConnection.id``) so that the tenant-scoped GraphQL/REST
surface never returns the raw value. Tenants receive an opaque encrypted
string and pass it back unchanged; the server decrypts on input to
recover the real id.

Two flavors are provided:

* :func:`encrypt_id` / :func:`decrypt_id` — **deterministic**, stable
  encryption for ids that must be the same on every request (React keys,
  mutation inputs that reference the same logical entity). Uses
  ``AES-SIV`` (RFC 5297). Same plaintext + namespace always produces the
  same ciphertext, so the value is safe to use as a stable React key,
  query cache key, etc., while still being opaque to the holder.

* :func:`encrypt_token` / :func:`decrypt_token` — **ephemeral**,
  TTL-bound tokens for one-shot references like ``rate.meta.rate_ref``.
  Uses ``AES-GCM`` with a fresh random nonce per encryption; the
  plaintext carries an ``exp`` claim that decryption enforces.

Key management:
    Both primitives derive their keys from Django's ``SECRET_KEY`` via
    HKDF-SHA256 with distinct ``info`` strings. ``SECRET_KEY`` is
    already shared across every pod in a deployment, so no extra
    secret-distribution work is required for horizontal scaling. To
    rotate, set ``PUBLIC_ID_ROTATION_KEYS`` to a list of previous
    secrets — decryption will try each in order.

Namespacing:
    All functions take a ``namespace`` string (e.g. ``"system_conn"``,
    ``"rate_ref"``). It binds the ciphertext to its expected use so a
    token minted for one surface can't be replayed against another.
"""

from __future__ import annotations

import base64
import json
import secrets
import time
import typing

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, AESSIV
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from django.conf import settings

# Version prefixes — short tags that let us evolve the encoding without
# making old ciphertexts unreadable. Bump on breaking changes only.
_ID_VERSION = b"1"
_TOKEN_VERSION = b"1"

# Namespace prefix that gets stamped onto the encoded output so a
# caller (or an attacker) can't replay a value from one surface against
# another. Bound into the AAD too.
_NAMESPACE_SEP = "_"


def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _b64url_decode(s: str) -> bytes:
    padding = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + padding)


def _derive_keys(info: bytes, length: int) -> list[bytes]:
    """HKDF-derive one key per active secret.

    Returns a list ordered current-first; decrypt tries each in turn so
    rotation can happen without invalidating in-flight tokens.
    """
    secrets_list: list[str] = []
    current = getattr(settings, "SECRET_KEY", None)
    if not current:
        raise RuntimeError("SECRET_KEY must be set to use public_ids")
    secrets_list.append(current)
    secrets_list.extend(getattr(settings, "PUBLIC_ID_ROTATION_KEYS", []) or [])

    return [
        HKDF(algorithm=SHA256(), length=length, salt=None, info=info).derive(s.encode("utf-8")) for s in secrets_list
    ]


def _id_keys() -> list[bytes]:
    # AES-SIV requires a 64-byte key (two 256-bit halves: S2V + CTR).
    return _derive_keys(b"karrio:public_id:siv:v1", 64)


def _token_keys() -> list[bytes]:
    return _derive_keys(b"karrio:public_id:gcm:v1", 32)


def _aad(namespace: str, version: bytes) -> bytes:
    return b"karrio:" + version + b":" + namespace.encode("utf-8")


# ──────────────────────────────────────────────────────────────────────
# Deterministic encrypted IDs (AES-SIV)
# ──────────────────────────────────────────────────────────────────────


def encrypt_id(plaintext: str, namespace: str) -> str:
    """Encrypt a stable identifier with a deterministic AES-SIV.

    Same ``(plaintext, namespace)`` always returns the same ciphertext.
    The ``namespace`` is bound into the AAD so values cannot be replayed
    across surfaces.

    Output format: ``{namespace}_v{ver}_{b64url(ciphertext)}``.
    """
    if not plaintext:
        return ""
    key = _id_keys()[0]
    aad = _aad(namespace, _ID_VERSION)
    ct = AESSIV(key).encrypt(plaintext.encode("utf-8"), [aad])
    return f"{namespace}{_NAMESPACE_SEP}v{_ID_VERSION.decode()}{_NAMESPACE_SEP}{_b64url_encode(ct)}"


def decrypt_id(value: str, namespace: str) -> str | None:
    """Reverse :func:`encrypt_id`. Returns ``None`` for invalid input.

    Never raises on tampered input — callers must treat ``None`` as
    "not a valid id" (typically "permission denied" or "not found").
    """
    if not value:
        return None
    expected_prefix = f"{namespace}{_NAMESPACE_SEP}v{_ID_VERSION.decode()}{_NAMESPACE_SEP}"
    if not value.startswith(expected_prefix):
        return None
    try:
        ct = _b64url_decode(value[len(expected_prefix) :])
    except (ValueError, TypeError):
        return None
    aad = _aad(namespace, _ID_VERSION)
    for key in _id_keys():
        try:
            return AESSIV(key).decrypt(ct, [aad]).decode("utf-8")
        except (InvalidTag, ValueError):
            continue
    return None


def encrypt_id_or_passthrough(value: str | None, namespace: str) -> str | None:
    """Encrypt ``value`` only if it isn't already encrypted for this namespace.

    Convenience for resolvers that may receive either form (some call
    paths now encrypt at the source; others still emit raw ids in legacy
    persisted snapshots).
    """
    if value is None:
        return None
    if not value:
        return value
    expected_prefix = f"{namespace}{_NAMESPACE_SEP}v{_ID_VERSION.decode()}{_NAMESPACE_SEP}"
    if value.startswith(expected_prefix):
        return value
    return encrypt_id(value, namespace)


def decrypt_id_or_passthrough(value: str | None, namespace: str) -> str | None:
    """Decrypt ``value`` if it's an encrypted id; otherwise return it unchanged.

    Used at the tenant-input boundary where, during the rollout window,
    a client may still send a raw id (legacy) or the new encrypted form.
    """
    if not value:
        return value
    expected_prefix = f"{namespace}{_NAMESPACE_SEP}v{_ID_VERSION.decode()}{_NAMESPACE_SEP}"
    if not value.startswith(expected_prefix):
        return value
    return decrypt_id(value, namespace)


# ──────────────────────────────────────────────────────────────────────
# Ephemeral encrypted tokens (AES-GCM + TTL)
# ──────────────────────────────────────────────────────────────────────

_DEFAULT_TTL_SECONDS = 30 * 60  # 30 minutes — covers rate → buy window
_MAX_TTL_SECONDS = 24 * 60 * 60


def encrypt_token(
    payload: typing.Mapping[str, typing.Any],
    namespace: str,
    ttl_seconds: int = _DEFAULT_TTL_SECONDS,
) -> str:
    """Mint a short-lived encrypted token carrying ``payload``.

    The token is bound to ``namespace`` and to an ``exp`` timestamp
    (``ttl_seconds`` from now). Decryption enforces both.

    Use this for references that should *not* be stable across requests
    (e.g. a rate-pick reference that's only meaningful for the
    immediately-following purchase call).
    """
    if ttl_seconds <= 0 or ttl_seconds > _MAX_TTL_SECONDS:
        raise ValueError("ttl_seconds out of range")
    key = _token_keys()[0]
    nonce = secrets.token_bytes(12)
    exp = int(time.time()) + ttl_seconds
    body = json.dumps({"d": dict(payload), "exp": exp}, separators=(",", ":")).encode("utf-8")
    ct = AESGCM(key).encrypt(nonce, body, _aad(namespace, _TOKEN_VERSION))
    return f"{namespace}{_NAMESPACE_SEP}v{_TOKEN_VERSION.decode()}{_NAMESPACE_SEP}{_b64url_encode(nonce + ct)}"


def decrypt_token(value: str, namespace: str) -> dict | None:
    """Reverse :func:`encrypt_token`. Returns ``None`` if invalid or expired."""
    if not value:
        return None
    expected_prefix = f"{namespace}{_NAMESPACE_SEP}v{_TOKEN_VERSION.decode()}{_NAMESPACE_SEP}"
    if not value.startswith(expected_prefix):
        return None
    try:
        blob = _b64url_decode(value[len(expected_prefix) :])
    except (ValueError, TypeError):
        return None
    if len(blob) < 13:
        return None
    nonce, ct = blob[:12], blob[12:]
    aad = _aad(namespace, _TOKEN_VERSION)
    plaintext: bytes | None = None
    for key in _token_keys():
        try:
            plaintext = AESGCM(key).decrypt(nonce, ct, aad)
            break
        except (InvalidTag, ValueError):
            continue
    if plaintext is None:
        return None
    try:
        decoded = json.loads(plaintext.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return None
    if not isinstance(decoded, dict) or "d" not in decoded or "exp" not in decoded:
        return None
    if int(decoded.get("exp", 0)) < int(time.time()):
        return None
    payload = decoded.get("d")
    return payload if isinstance(payload, dict) else None


# ──────────────────────────────────────────────────────────────────────
# Common namespaces (centralized so a typo can't silently break a
# round-trip — encryption and decryption must use the same constant).
# ──────────────────────────────────────────────────────────────────────


class Namespaces:
    """Canonical namespace identifiers for public-id encryption."""

    SYSTEM_CONNECTION = "scn"
    BROKERED_CONNECTION = "bcn"
    CARRIER_CONNECTION = "ccn"
    RATE_REF = "rate"


# ──────────────────────────────────────────────────────────────────────
# Rate-meta redaction
#
# `rate.meta.carrier_connection_id` is server-internal — the pricing
# module and other server-side enrichment paths read it. But it round-
# trips back to the tenant inside `selected_rate` and through GraphQL
# `rates` queries, where it leaks the DB primary key of a SystemConnection
# or BrokeredConnection. The helpers below build the tenant-facing view
# of a rate meta dict by stripping the raw PK and replacing it with an
# encrypted `rate_ref` that the server can decrypt at buy-label time.
#
# Connection kinds (`account`, `system`, `brokered`) match
# `karrio.server.core.utils.ConnectionType` — kept as strings to avoid
# an import cycle.
# ──────────────────────────────────────────────────────────────────────


def _is_account_kind(kind: str | None) -> bool:
    # Missing / empty kind defaults to account (legacy rates pre-dating
    # the connection_kind discriminator). The redaction docstring
    # promises "account or missing → pass through".
    if not kind:
        return True
    return kind.lower() == "account"


def redact_rate_meta_for_tenant(meta: dict | None) -> dict | None:
    """Return a tenant-safe copy of a rate meta dict.

    Behavior, keyed by ``meta["connection_kind"]``:

    * ``account`` (or missing): pass through unchanged. The merchant
      already owns the connection so ``carrier_connection_id`` is not a
      leak.
    * ``system`` / ``brokered``: drop ``carrier_connection_id`` and add
      a ``rate_ref`` ephemeral token carrying ``{cid, kind}`` encrypted
      with the rate-ref namespace. The server reverses this in
      :func:`resolve_rate_ref` during buy-label.

    Does not mutate ``meta``.
    """
    if not meta:
        return meta
    out = dict(meta)
    kind = out.get("connection_kind")

    if _is_account_kind(kind):
        return out

    raw_cid = out.pop("carrier_connection_id", None)
    if raw_cid and kind:
        out["rate_ref"] = encrypt_token(
            {"cid": raw_cid, "kind": kind},
            Namespaces.RATE_REF,
        )
    return out


def resolve_rate_ref(meta: dict | None) -> dict | None:
    """Reverse :func:`redact_rate_meta_for_tenant` for the buy-label path.

    Returns ``{"connection_id": str, "connection_type": str}`` suitable
    for passing to ``karrio.server.core.utils.resolve_carrier``, or
    ``None`` if no reference can be recovered.

    Accepted forms (in priority order):

    1. ``meta.rate_ref`` — encrypted token from ``redact_rate_meta_for_tenant``.
    2. ``meta.carrier_connection_id`` for ``account`` kind — trusted directly
       (merchant owns the connection).
    3. ``meta.carrier_connection_id`` for any kind — *legacy* path for rates
       persisted before this PR. Sunset planned: the data migration that
       lands alongside this change will rewrite these into ``rate_ref``.
    """
    if not meta:
        return None
    kind = meta.get("connection_kind")

    rate_ref = meta.get("rate_ref")
    if rate_ref:
        decoded = decrypt_token(rate_ref, Namespaces.RATE_REF)
        if decoded and decoded.get("cid"):
            return {
                "connection_id": decoded["cid"],
                "connection_type": decoded.get("kind") or "system",
            }

    cid = meta.get("carrier_connection_id")
    if cid:
        return {
            "connection_id": cid,
            "connection_type": kind or "account",
        }

    return None
