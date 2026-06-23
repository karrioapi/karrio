"""Opt-in dynamic carrier metadata.

Some carriers — Parcel.One, Easyship, Eshipper, every aggregator — carry a
per-account catalog that cannot be expressed in compile-time ``units.py``
enums. This module gives those connectors a single, reusable way to publish
their live catalog so the server's reference / metadata endpoints can merge
it on top of the static reference when a caller knows which connection they
care about.

A connector opts in by mixing :class:`DynamicMetadataMixin` into its
``Settings`` subclass and implementing :meth:`fetch_dynamic_metadata`. Cache
layering, timeout enforcement, and negative-caching on failure are provided
by the mixin — callers must always go through :meth:`get_dynamic_metadata`.

The result is a :class:`DynamicMetadata` value object: services, options,
service availability, connection defaults, and an opaque ``raw`` payload for
clients that need vendor-native data.
"""

import concurrent.futures as futures
import datetime
import logging
import typing

import attr
import jstruct

import karrio.core.models as models

logger = logging.getLogger(__name__)


@attr.s(auto_attribs=True)
class OptionDescriptor:
    """A single dynamically-discovered option (ServiceID or similar)."""

    code: str = ""  # vendor wire code, e.g. "SRO"
    name: str = ""  # canonical karrio key, e.g. "parcelone_return_only"
    value_type: str = "bool"  # "bool" | "int" | "float" | "string" | "json"
    meta: dict[str, typing.Any] = {}


@attr.s(auto_attribs=True)
class DynamicMetadata:
    """Live, per-connection carrier catalog.

    Returned by :meth:`DynamicMetadataMixin.get_dynamic_metadata`. The
    server-side orchestrator folds this into the static reference using the
    per-field rules in :mod:`karrio.server.core.dynamic`.

    ``source`` attribution lets clients know whether they're seeing live or
    cached static data:

    - ``"profile"`` — fetched from a vendor profile / catalog endpoint
    - ``"rates"`` — projected from a sample rate quote
    - ``"static"`` — connector did not provide dynamic data; returned empty
    - ``"error"`` — fetch failed; result is empty and short-cached

    ``exclusive`` controls how the server-side merge treats the static
    catalog for this carrier:

    - ``False`` (default) — union semantics: static + dynamic, dynamic wins
      on collision. Right for carriers where the static enum is a stable
      baseline and dynamic data adds rows.
    - ``True`` — replace semantics: the dynamic catalog fully supersedes
      the static one. Right when the live source (e.g. ParcelOne
      ``/profile``) is *authoritative* — anything not in the live catalog
      is genuinely not available to this connection, so surfacing the
      static fallback alongside would mislead the picker.
    """

    services: list[models.ServiceLevel] = jstruct.JList[models.ServiceLevel]
    options: list[OptionDescriptor] = jstruct.JList[OptionDescriptor]
    service_availability: dict[str, list[str]] = {}
    connection_config_defaults: dict[str, typing.Any] = {}
    raw: dict[str, typing.Any] = {}
    source: str = "static"
    fetched_at: datetime.datetime | None = None
    ttl_seconds: int = 3600
    exclusive: bool = False

    @classmethod
    def empty(cls, *, source: str = "static", ttl_seconds: int = 3600) -> "DynamicMetadata":
        """Return an empty result tagged with a source (use for misses / errors)."""
        return cls(
            source=source,
            ttl_seconds=ttl_seconds,
            fetched_at=datetime.datetime.now(datetime.UTC),
        )

    @property
    def is_empty(self) -> bool:
        return not (self.services or self.options or self.service_availability or self.connection_config_defaults)


class DynamicMetadataMixin:
    """Mixin on a connector's ``Settings`` to publish dynamic metadata.

    Carriers that opt in must:

    1. Mix this class into their ``Settings`` (alongside ``core.Settings``).
    2. Implement :meth:`fetch_dynamic_metadata`.

    The mixin handles cache layering, single-flight protection (via the
    underlying ``lib.Cache._values`` futures), per-call timeout enforcement,
    and short negative caching on failure. Callers must call
    :meth:`get_dynamic_metadata` — never the raw fetch.

    Class-level knobs (override as class attributes on the connector's
    Settings):

    ``dynamic_ttl_seconds``
        How long a successful fetch stays cached. Default 3600 (1h).
    ``dynamic_timeout_seconds``
        Hard wall-clock timeout on the vendor fetch. Default 0.8 (800 ms).
        Note: Python cannot forcibly stop a running thread, so the fetch
        thread may continue past this deadline; the caller is unblocked
        immediately but the connector should still set a network-level
        timeout on its outbound request.
    ``dynamic_negative_ttl_seconds``
        How long an error/timeout result is cached. Keeps us from
        hammering a flaky vendor while still recovering quickly when they
        come back. Default 60.
    """

    dynamic_ttl_seconds: int = 3600
    dynamic_timeout_seconds: float = 0.8
    dynamic_negative_ttl_seconds: int = 60

    # ------------------------------------------------------------------ #
    # Subclass contract                                                  #
    # ------------------------------------------------------------------ #
    def fetch_dynamic_metadata(self) -> DynamicMetadata:
        """Hit the vendor API and return a :class:`DynamicMetadata`.

        Subclasses must override. The base implementation raises
        ``NotImplementedError`` — discovered via ``isinstance`` check on
        the server side so we don't break carriers that subclass the mixin
        without implementing fetch yet.
        """
        raise NotImplementedError(
            f"{type(self).__name__} mixes in DynamicMetadataMixin but does not implement fetch_dynamic_metadata()"
        )

    def dynamic_cache_key(self) -> str:
        """Cache key for this connection's dynamic metadata.

        Default keys on ``carrier_name`` + connection id (or username when
        no id is present, as in fixture-driven tests). Override on the
        connector if multiple settings dimensions (mandator, sub-account)
        materially change the returned catalog.
        """
        carrier = getattr(self, "carrier_name", None) or getattr(self, "carrier_id", "") or "unknown"
        ident = (
            getattr(self, "id", None) or getattr(self, "username", None) or getattr(self, "carrier_id", "") or "default"
        )
        return f"karrio.dynamic.{carrier}.{ident}"

    # ------------------------------------------------------------------ #
    # Public entry point                                                 #
    # ------------------------------------------------------------------ #
    def get_dynamic_metadata(self) -> DynamicMetadata:
        """Return the cached or freshly-fetched dynamic metadata."""
        cache = self._dynamic_cache()
        cache_key = self.dynamic_cache_key()

        cached = cache.get(cache_key)
        if cached is not None and self._is_cache_fresh(cached):
            return cached

        metadata = self._fetch_with_timeout()
        cache.set(cache_key, metadata, timeout=metadata.ttl_seconds)
        return metadata

    def invalidate_dynamic_metadata(self) -> None:
        """Drop the cached value (e.g. after settings changed)."""
        self._dynamic_cache().delete(self.dynamic_cache_key())

    # ------------------------------------------------------------------ #
    # Internals                                                          #
    # ------------------------------------------------------------------ #
    def _dynamic_cache(self):
        """Return the underlying cache (the gateway-injected one when present)."""
        cache = getattr(self, "connection_cache", None) or getattr(self, "cache", None)
        if cache is None:
            import karrio.lib as lib

            cache = lib.Cache()
        return cache

    def _fetch_with_timeout(self) -> DynamicMetadata:
        """Run ``fetch_dynamic_metadata`` with a wall-clock deadline.

        On timeout or exception, return an empty result tagged ``error`` and
        short-TTL'd via ``dynamic_negative_ttl_seconds`` so the next call
        retries soon rather than blocking on the same flaky vendor.
        """
        pool = futures.ThreadPoolExecutor(max_workers=1)
        try:
            future = pool.submit(self.fetch_dynamic_metadata)
            metadata = future.result(timeout=self.dynamic_timeout_seconds)
        except futures.TimeoutError:
            logger.warning(
                "dynamic metadata fetch timed out",
                extra=dict(
                    carrier_name=getattr(self, "carrier_name", None),
                    carrier_id=getattr(self, "carrier_id", None),
                    timeout_seconds=self.dynamic_timeout_seconds,
                ),
            )
            metadata = DynamicMetadata.empty(source="error", ttl_seconds=self.dynamic_negative_ttl_seconds)
            metadata.raw = {"error": "timeout"}
        except Exception as exc:  # noqa: BLE001 — failsafe, falls back to static
            logger.exception(
                "dynamic metadata fetch failed",
                extra=dict(
                    carrier_name=getattr(self, "carrier_name", None),
                    carrier_id=getattr(self, "carrier_id", None),
                ),
            )
            metadata = DynamicMetadata.empty(source="error", ttl_seconds=self.dynamic_negative_ttl_seconds)
            metadata.raw = {"error": str(exc)}
        finally:
            # Best-effort: pending tasks are cancelled; an in-flight fetch may
            # leak the worker thread until its own HTTP timeout fires. This is
            # an accepted limitation of Python's thread model — connectors
            # must set network-level timeouts on outbound requests.
            pool.shutdown(wait=False, cancel_futures=True)

        # Backfill fields the subclass may have left blank.
        if metadata.fetched_at is None:
            metadata.fetched_at = datetime.datetime.now(datetime.UTC)
        if not metadata.ttl_seconds:
            metadata.ttl_seconds = self.dynamic_ttl_seconds
        return metadata

    @staticmethod
    def _is_cache_fresh(metadata: DynamicMetadata) -> bool:
        if not metadata.fetched_at or not metadata.ttl_seconds:
            return False
        age = (datetime.datetime.now(datetime.UTC) - metadata.fetched_at).total_seconds()
        return age < metadata.ttl_seconds
