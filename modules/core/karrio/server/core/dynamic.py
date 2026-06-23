"""Server-side glue for :mod:`karrio.core.dynamic`.

Wraps the per-connection dynamic-metadata fetch behind the merge rules that
the carrier-detail REST endpoints need. Only used when a caller passes
``?connection_id=<uuid>`` — see ``PRDs/CARRIER_DYNAMIC_METADATA.md``.
"""

import copy
import logging

import karrio.core.dynamic as core_dynamic
import karrio.lib as lib
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.request import Request

logger = logging.getLogger(__name__)


def merge_dynamic_metadata(
    reference: dict,
    *,
    connection_id: str,
    request: Request,
    carrier_name: str,
) -> dict:
    """Return a copy of ``reference`` merged with the connection's live dynamic metadata.

    No-ops (returns the input reference) when the connector hasn't opted into
    :class:`~karrio.core.dynamic.DynamicMetadataMixin` or when the live
    fetch returns nothing.

    ``connection_id`` may refer to a tenant-owned :class:`CarrierConnection`
    OR a :class:`BrokeredConnection` enabled for the tenant — both expose the
    same ``.gateway`` / ``.ext`` surface, so the dynamic-metadata path is
    uniform. System carriers that the tenant has not enabled are not
    reachable here (no leak across tenants).

    Raises:
        rest_framework.exceptions.NotFound: connection unknown or not accessible.
        rest_framework.exceptions.ValidationError: connection / URL carrier mismatch.
    """
    from karrio.server.core.gateway import Connections

    connection = Connections.first(context=request, carrier_id=connection_id)
    if connection is None:
        raise NotFound(f"Connection '{connection_id}' not found")

    if connection.ext != carrier_name:
        raise ValidationError(f"Connection '{connection_id}' is for carrier '{connection.ext}', not '{carrier_name}'.")

    settings = lib.failsafe(lambda: connection.gateway.settings)
    if not isinstance(settings, core_dynamic.DynamicMetadataMixin):
        return reference

    dyn = lib.failsafe(lambda: settings.get_dynamic_metadata())
    if dyn is None or dyn.is_empty:
        return reference

    return _merge(reference, dyn, carrier_name)


def carriers_with_dynamic_metadata() -> set[str]:
    """Return the set of carrier names whose Settings opts into DynamicMetadataMixin.

    Drives the ``has_dynamic_metadata`` flag in REST responses so the shipping
    app can decide up-front whether passing ``?connection_id=`` is worthwhile
    for a given carrier — non-dynamic carriers serve only static catalogs
    regardless of the query param.

    Walks the installed SDK ``gateway.providers`` once per process; cheap
    enough that we don't bother memoising.
    """
    import karrio.sdk as karrio

    discovered: set[str] = set()
    for carrier_name, provider in (karrio.gateway.providers or {}).items():
        # PluginMetadata exposes the settings class as `Settings` (capital S).
        # See karrio.core.metadata.PluginMetadata and references._register_carrier.
        settings_cls = lib.failsafe(lambda p=provider: getattr(p, "Settings", None))
        if (
            settings_cls is not None
            and isinstance(settings_cls, type)
            and issubclass(settings_cls, core_dynamic.DynamicMetadataMixin)
        ):
            discovered.add(carrier_name)
    return discovered


def invalidate(connection_id: str) -> None:
    """Drop the cached dynamic metadata for one connection (account or brokered).

    Wired on connection post_save / post_delete so a credential change or
    carrier removal busts the cache immediately. ``connection_id`` may refer
    to either a :class:`CarrierConnection` (account) or a
    :class:`BrokeredConnection` — both produce a Settings object with the
    connection's primary key, which is what the SDK cache keys on.
    """
    import karrio.server.providers.models as providers_models

    connection = (
        providers_models.CarrierConnection.objects.filter(pk=connection_id).first()
        or providers_models.BrokeredConnection.objects.filter(pk=connection_id).first()
    )
    if connection is None:
        return

    _invalidate_connection(connection)


def invalidate_for_system_connection(system_connection_id: str) -> None:
    """Drop the cached dynamic metadata for every brokered connection layered on a system connection.

    System credentials / config changes flow through to every brokered
    enablement (their Settings inherits via ``_get_credentials`` /
    ``config``), so the per-brokered cache entries must be busted too. The
    brokered id is what the SDK cache keys on (see
    :meth:`karrio.core.dynamic.DynamicMetadataMixin.dynamic_cache_key`).
    """
    import karrio.server.providers.models as providers_models

    brokered = providers_models.BrokeredConnection.objects.filter(system_connection_id=system_connection_id)
    for connection in brokered.iterator():
        _invalidate_connection(connection)


def _invalidate_connection(connection) -> None:
    settings = lib.failsafe(lambda: connection.gateway.settings)
    if isinstance(settings, core_dynamic.DynamicMetadataMixin):
        lib.failsafe(settings.invalidate_dynamic_metadata)


def _merge(
    reference: dict,
    dyn: core_dynamic.DynamicMetadata,
    carrier_name: str,
) -> dict:
    """Fold dynamic metadata into the static reference.

    ``dyn.exclusive`` selects the policy:

    - ``False`` (default): union of static + dynamic per carrier, with
      dynamic values winning on key collision.
    - ``True``: the dynamic catalog *replaces* the static one for this
      carrier. Use when the live source is authoritative (e.g. ParcelOne
      ``/profile`` — anything not in the live catalog isn't available to
      this connection, so surfacing the static fallback alongside would
      mislead the picker).
    """
    out = copy.deepcopy(reference)
    exclusive = bool(getattr(dyn, "exclusive", False))

    # services[carrier] : dict[service_code -> service_code]
    static_services = (out.get("services") or {}).get(carrier_name, {}) or {}
    dyn_services = {s.service_code: s.service_code for s in (dyn.services or []) if getattr(s, "service_code", None)}
    out.setdefault("services", {})[carrier_name] = dyn_services if exclusive else {**static_services, **dyn_services}

    # service_names[carrier] : dict[service_code -> human name]
    static_names = (out.get("service_names") or {}).get(carrier_name, {}) or {}
    dyn_names = {
        s.service_code: getattr(s, "service_name", None) or s.service_code
        for s in (dyn.services or [])
        if getattr(s, "service_code", None)
    }
    out.setdefault("service_names", {})[carrier_name] = dyn_names if exclusive else {**static_names, **dyn_names}

    # options[carrier] : dict[option_key -> meta]
    static_options = (out.get("options") or {}).get(carrier_name, {}) or {}
    dyn_options: dict[str, dict] = {
        (opt.name or opt.code): {
            "code": opt.code,
            "type": opt.value_type,
            **(opt.meta or {}),
        }
        for opt in (dyn.options or [])
        if (opt.name or opt.code)
    }
    out.setdefault("options", {})[carrier_name] = dyn_options if exclusive else {**static_options, **dyn_options}

    # connection_configs[carrier][key]["default"] overridden per defaults
    if dyn.connection_config_defaults:
        configs = out.setdefault("connection_configs", {}).setdefault(carrier_name, {})
        for key, default in dyn.connection_config_defaults.items():
            cfg = configs.setdefault(key, {})
            cfg["default"] = default

    # service_availability is brand-new — emit as-is under the carrier key.
    if dyn.service_availability:
        out.setdefault("service_availability", {})[carrier_name] = dict(dyn.service_availability)

    # Attribution so clients can tell when they're seeing live data.
    out.setdefault("_dynamic_metadata_sources", {})[carrier_name] = dyn.source

    return out
