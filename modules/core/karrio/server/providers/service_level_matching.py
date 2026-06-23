"""ServiceLevel & rate disambiguation when variants share a `service_code`.

A carrier's API typically defines one code per service family (UPS Standard
is `"11"` whether the package goes Door, Saturday-Door, or Return-Door —
saturday is a request option, return is a return-service option, etc.). The
rate sheet stores each merchant-facing variant as a distinct ServiceLevel
that carries the same `service_code` plus its own `features` and
`carrier_options` describing how the variant differs.

Callers that resolve a (method or rate request) to one variant must NOT just
take the first match by `service_code` — that picks an arbitrary sibling.
There are two scoring entry points here depending on which side of the rate
pipeline the caller is on:

- :func:`pick_best_service_level` — input is the **rate-sheet side**
  (`ServiceLevel` ORM rows, each with a fully-specified `features` dict).
  Use it whenever you are choosing one ServiceLevel before emitting rates.
  Call sites: `RateResolver.get_rate_for_method`,
  `RateResolver._build_account_method_meta`,
  `bridge.commands.recalculate_shipment_rates`.

- :func:`pick_best_rate_for_method` — input is the **rate-response side**
  (post-emission rate dicts whose `meta.service_features` is the SDK's
  list-of-truthy-keys normalization, so absence does not distinguish False
  from "the SDK dropped it"). Use it whenever you have a `list[dict]` of
  emitted rates and need to pick one variant for a given shipping method.
  Call sites: `karrio.server.core.utils.apply_rate_selection`.

Both helpers share `_normalize_features` and `_values_agree` so target-side
inputs (dict / list / attrs) behave identically. They differ in how they
treat **absence on the candidate side** — the ORM side has explicit False,
the rate-meta side does not, so they handle "method says False" differently.
See each function's docstring for the exact rules.

Companion helper for the rates layer (SDK side, post-emission): `karrio.lib
.rate_variant_key` (alias of `karrio.core.utils.rate_variant_key`). It returns
the `(service_code, service_name)` tuple that identifies a rate's variant —
the same notion used here, but applied to emitted `RateDetails` rather than
ServiceLevel ORM rows. Use it whenever rates are grouped, deduped, or matched
across packages or queries — see `karrio.core.utils.to_multi_piece_rates` for
why service_code alone is insufficient.
"""

from __future__ import annotations

import functools
import importlib
import typing


@functools.lru_cache(maxsize=128)
def _carrier_service_code_aliases(carrier_name: str) -> dict[str, str]:
    """Return a `{service_id: wire_code}` map for the carrier, including aliases.

    Some connectors (UPS, Asendia) define a `ServiceCode` enum in
    `karrio.providers.<carrier>.units` where multiple member names point at
    the same wire-code value — e.g. `ups_express_pl = ups_express = "07"`.
    The rate parser may canonicalize zone-suffixed aliases back to the base
    name (see `karrio.providers.ups.units.ServiceZone.find` and the
    `_ZONE_ALIAS_TO_BASE` map), so a user who selected `ups_express_pl`
    will not exact-string-match a returned rate labelled `ups_express`
    even though both resolve to UPS service "07".

    Returning `Enum.__members__` (vs `list(Enum)`) is intentional: aliases
    are dropped by the default iteration order but preserved in
    `__members__`. Carriers without a `ServiceCode` enum return an empty
    dict — callers fall back to exact string matching, so this stays
    behavioural-no-op for the 24/26 connectors that don't follow the
    convention.
    """
    if not carrier_name:
        return {}
    try:
        module = importlib.import_module(f"karrio.providers.{carrier_name}.units")
    except ImportError:
        return {}
    service_code_enum = getattr(module, "ServiceCode", None)
    if service_code_enum is None or not hasattr(service_code_enum, "__members__"):
        return {}
    return {name: str(member.value) for name, member in service_code_enum.__members__.items()}


def _services_alias_equivalent(
    rate_service: str | None,
    target_service: str | None,
    carrier_name: str | None,
) -> bool:
    """True when both service identifiers resolve to the same carrier wire code.

    Used as a fallback when exact `rate.service == target_service` fails.
    Returns False unless BOTH names are present in the carrier's
    `ServiceCode` enum AND map to the same wire-code value. This keeps the
    fallback narrow: it never matches across unrelated services, and never
    fires for carriers that don't expose a `ServiceCode` enum.
    """
    if not (rate_service and target_service and carrier_name):
        return False
    if rate_service == target_service:
        return True
    aliases = _carrier_service_code_aliases(carrier_name)
    rate_code = aliases.get(rate_service)
    target_code = aliases.get(target_service)
    return bool(rate_code) and rate_code == target_code


def _normalize_features(value: typing.Any) -> dict[str, typing.Any]:
    """Coerce a features container (dict, list of strings, or attrs object)
    to a `{key: value}` dict.

    - dict → returned as-is.
    - list[str] → each element treated as a boolean flag set to True.
    - attrs/dataclass-like → fields with non-None values.
    - everything else → empty dict.
    """
    if value is None:
        return {}
    if isinstance(value, dict):
        return {k: v for k, v in value.items() if v is not None}
    if isinstance(value, (list, tuple, set)):
        return {str(item): True for item in value if item}
    # attrs / dataclass support
    try:
        import attr

        if attr.has(type(value)):
            return {k: v for k, v in attr.asdict(value).items() if v is not None}
    except ImportError:
        pass
    if hasattr(value, "__dict__"):
        return {k: v for k, v in vars(value).items() if v is not None and not k.startswith("_")}
    return {}


def _score_candidate(
    service_features: dict[str, typing.Any],
    service_options: dict[str, typing.Any],
    *,
    target_features: dict[str, typing.Any],
    target_options: dict[str, typing.Any],
) -> tuple[int, int, int]:
    """Score how well a ServiceLevel matches a target context.

    Returns a tuple ``(matches, conflicts, distinguishing_off)``:
      - ``matches``: count of feature/option keys present on BOTH sides where
        the values agree (truthy↔truthy, falsy↔falsy, equal strings).
      - ``conflicts``: count of keys present on both sides where values
        disagree. A non-zero conflict count is the strongest negative
        signal; we prefer candidates with fewer conflicts.
      - ``distinguishing_off``: count of "Off" disambiguation flags
        (``saturday_delivery=False`` / ``shipment_type=outbound`` /
        ``last_mile=home_delivery``) carried by the candidate when the
        target didn't ask for the corresponding "On" variant. This is a
        soft preference for the canonical/Door-style variant when the
        target context is silent.

    Comparison rules:
      - Boolean values: agreement = both bool() agree.
      - String values: agreement = equal (case-insensitive).
      - None on either side is treated as "not specified" (skip the key).
    """
    matches = 0
    conflicts = 0
    distinguishing_off = 0

    combined_target = {**target_features, **target_options}
    combined_service = {**service_features, **service_options}

    for key, target_value in combined_target.items():
        if target_value is None:
            continue
        service_value = combined_service.get(key)
        if service_value is None:
            continue
        if _values_agree(target_value, service_value):
            matches += 1
        else:
            conflicts += 1

    # Soft preference: candidate is the canonical "Off" variant for a
    # disambiguation flag the target left unspecified.
    canonical_off_keys = ("saturday_delivery", "sunday_delivery")
    for key in canonical_off_keys:
        if key in combined_target:
            continue  # target spoke explicitly — already scored above
        service_value = combined_service.get(key)
        if service_value is False:
            distinguishing_off += 1

    if combined_service.get("shipment_type") == "outbound" and combined_target.get("shipment_type") is None:
        distinguishing_off += 1
    if combined_service.get("last_mile") == "home_delivery" and combined_target.get("last_mile") is None:
        distinguishing_off += 1

    return matches, conflicts, distinguishing_off


def _values_agree(a: typing.Any, b: typing.Any) -> bool:
    if isinstance(a, bool) or isinstance(b, bool):
        return bool(a) == bool(b)
    if isinstance(a, str) and isinstance(b, str):
        return a.strip().lower() == b.strip().lower()
    return a == b


def pick_best_service_level(
    services: typing.Iterable,
    service_code: str,
    *,
    service_name: str | None = None,
    target_features: typing.Any = None,
    target_options: typing.Any = None,
):
    """Return the ServiceLevel that best matches the caller's context.

    Args:
        services: Iterable of ServiceLevel-like objects with `service_code`,
            `service_name`, `features`, and `carrier_options` attributes.
        service_code: The carrier service code to filter by.
        service_name: Optional exact service_name to prefer (e.g. when an
            already-emitted rate carries `meta.service_name`).
        target_features: The caller's features (dict / list / attrs).
        target_options: The caller's carrier_options (dict).

    Returns:
        The single best-matching ServiceLevel, or None.

    Selection order:
        1. service_code match required.
        2. If `service_name` is provided and matches one candidate, return it.
        3. Score remaining candidates by feature/option overlap with the
           target. Pick the candidate with the most matches, then the
           fewest conflicts, then the most "canonical-off" disambiguation
           flags. Stable for a given input.
        4. If no scoring context is provided, return the first candidate
           by service_name (preserves a deterministic fallback).
    """
    candidates = [s for s in services if getattr(s, "service_code", None) == service_code]
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]

    if service_name:
        named = next(
            (s for s in candidates if (getattr(s, "service_name", None) or "").strip() == service_name.strip()),
            None,
        )
        if named is not None:
            return named

    target_feat = _normalize_features(target_features)
    target_opts = _normalize_features(target_options)

    if not target_feat and not target_opts:
        # Deterministic fallback: alphabetical service_name.
        return min(candidates, key=lambda s: getattr(s, "service_name", "") or "")

    scored = []
    for svc in candidates:
        svc_features = _normalize_features(getattr(svc, "features", None))
        svc_options = _normalize_features(getattr(svc, "carrier_options", None))
        matches, conflicts, distinguishing_off = _score_candidate(
            svc_features,
            svc_options,
            target_features=target_feat,
            target_options=target_opts,
        )
        scored.append((matches, -conflicts, distinguishing_off, svc))

    # Highest matches, fewest conflicts, most canonical-off, deterministic by name.
    scored.sort(key=lambda t: (t[0], t[1], t[2], -len(getattr(t[3], "service_name", "") or "")), reverse=True)
    return scored[0][3]


def _score_rate_candidate(
    rate_features: dict[str, typing.Any],
    rate_options: dict[str, typing.Any],
    *,
    target_features: dict[str, typing.Any],
    target_options: dict[str, typing.Any],
) -> tuple[int, int, int]:
    """Score how well an emitted rate matches a target context.

    Mirrors :func:`_score_candidate` but adapts to the rate-meta input shape.
    The SDK's universal rating proxy normalizes `ServiceLevel.features` into
    `service_features` as a **list of truthy keys** (false/None values are
    dropped). That means absence on the rate side is genuinely ambiguous —
    we can't tell "False" from "the SDK didn't carry it". The scoring rules
    differ from `_score_candidate` accordingly:

      - target True  + rate truthy    → match  (rate confirms positive flag)
      - target True  + rate absent    → ignored (rate doesn't know)
      - target False + rate truthy    → conflict (rate advertises a flag
        the method opts out of — the smoking gun for the witness shipment)
      - target False + rate absent    → match  (absence confirms False)
      - target str   + rate str equal → match
      - target str   + rate disagrees → conflict
      - target str   + rate absent    → ignored

    Returns ``(matches, conflicts, distinguishing_off)`` with the same
    shape as the ServiceLevel scorer so callers can sort by the same key.
    """
    matches = 0
    conflicts = 0
    distinguishing_off = 0

    combined_target = {**target_features, **target_options}
    combined_rate = {**rate_features, **rate_options}

    for key, target_value in combined_target.items():
        if target_value is None:
            continue
        rate_value = combined_rate.get(key)
        if isinstance(target_value, bool):
            if target_value:
                if rate_value:
                    matches += 1
                # absent on rate: ignored — the SDK list-normaliser drops it.
            else:
                if rate_value:
                    conflicts += 1
                else:
                    matches += 1
            continue
        if isinstance(target_value, str):
            if rate_value is None:
                continue
            if _values_agree(target_value, rate_value):
                matches += 1
            else:
                conflicts += 1
            continue
        # Other types (numbers, etc.) — strict equality.
        if rate_value is None:
            continue
        if rate_value == target_value:
            matches += 1
        else:
            conflicts += 1

    # Soft preference parity with the ServiceLevel scorer: when the target
    # is silent on a canonical "Off" disambiguator and the rate doesn't
    # advertise it either, treat the rate as the canonical sibling. For
    # emitted rates we can only infer this from absence (the SDK drops
    # falsy keys), so the bonus fires whenever the key is missing from
    # combined_rate AND the target left it unspecified.
    canonical_off_keys = ("saturday_delivery", "sunday_delivery")
    for key in canonical_off_keys:
        if key in combined_target:
            continue
        if combined_rate.get(key):
            continue
        distinguishing_off += 1

    return matches, conflicts, distinguishing_off


def pick_best_rate_for_method(
    rates: typing.Iterable[typing.Mapping[str, typing.Any]],
    service_code: str,
    *,
    service_name: str | None = None,
    target_features: typing.Any = None,
    target_options: typing.Any = None,
) -> typing.Mapping[str, typing.Any] | None:
    """Return the rate dict whose variant best matches a shipping method.

    Companion to :func:`pick_best_service_level`. Use this at rate-selection
    time, when you have a `list[dict]` of emitted rates and the method's
    `features` / `carrier_options` / preferred `service_name`. The SDK
    universal rating proxy emits one rate per active `ServiceLevel`, so
    sibling variants of the same `service_code` all appear in `rates` and a
    bare `next(r for r in rates if r["service"] == code)` picks an
    arbitrary one (see `shp_cc0d0501e93c4dc1850f53d5212b7b53` for the
    witness — UPS Saturday-vs-Standard).

    Args:
        rates: Iterable of rate dicts. Each dict is expected to have a
            top-level ``service`` key (the carrier service code) and a
            ``meta`` dict whose ``service_features`` (list of truthy keys)
            and ``service_name`` carry the variant identity.
        service_code: The carrier service code to filter by.
        service_name: Optional exact service_name to prefer (case-
            insensitive, trim-stripped). When provided and at least one
            candidate matches, returns that candidate immediately.
        target_features: The method's features (dict / list / attrs).
        target_options: The method's carrier_options (dict).

    Returns:
        The best-matching rate dict, or None when no rate has the given
        service code.

    Selection order:
        1. service_code match required.
        2. service_name exact (case-insensitive) match short-circuits.
        3. Score remaining candidates via :func:`_score_rate_candidate`.
        4. If no scoring context (no features / options / name), fall back
           to alphabetical by ``meta.service_name`` for determinism.

    Price is intentionally NOT a sort key. The picker's job is variant
    identity (which ServiceLevel matches the method's intent); once that
    variant is chosen, the per-(zone, weight-bracket) price is unique
    and price-vs-price comparisons across variants are the wrong layer
    to do that comparison at — that's what ``_deduplicate_by_bucket``
    (in shipping/services/rate_resolver.py) is for, and what the rules
    engine "cheapest" strategy does explicitly.
    """
    rate_list = [r for r in rates if isinstance(r, typing.Mapping)]
    candidates = [r for r in rate_list if r.get("service") == service_code]
    if not candidates:
        # Alias fallback — match rates whose `service` resolves to the same
        # carrier wire code as `service_code` via the carrier's `ServiceCode`
        # enum. Closes the gap where the rate parser canonicalizes
        # zone-suffixed aliases (e.g. UPS `ups_express_pl` → `ups_express`)
        # before string-compare here. See
        # `_carrier_service_code_aliases` for the convention.
        candidates = [
            r for r in rate_list if _services_alias_equivalent(r.get("service"), service_code, r.get("carrier_name"))
        ]
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]

    if service_name:
        target_name = service_name.strip().lower()
        named = [
            r for r in candidates if ((r.get("meta") or {}).get("service_name") or "").strip().lower() == target_name
        ]
        if len(named) == 1:
            return named[0]
        if named:
            # Multiple candidates share the requested name — narrow scoring to them.
            candidates = named

    target_feat = _normalize_features(target_features)
    target_opts = _normalize_features(target_options)

    if not target_feat and not target_opts:
        # Deterministic fallback: alphabetical by service_name.
        return min(
            candidates,
            key=lambda r: ((r.get("meta") or {}).get("service_name") or "") or "",
        )

    scored = []
    for rate in candidates:
        meta = rate.get("meta") or {}
        rate_features = _normalize_features(meta.get("service_features"))
        rate_options = _normalize_features(meta.get("carrier_options"))
        # Hoist enum-shaped meta keys (last_mile, shipment_type, ...) that
        # the SDK doesn't fold into service_features but the rate-resolver
        # path does write onto meta directly.
        for key in ("last_mile", "first_mile", "shipment_type", "form_factor"):
            value = meta.get(key)
            if value is not None and key not in rate_features:
                rate_features[key] = value
        matches, conflicts, distinguishing_off = _score_rate_candidate(
            rate_features,
            rate_options,
            target_features=target_feat,
            target_options=target_opts,
        )
        scored.append((matches, -conflicts, distinguishing_off, rate))

    # Highest matches, fewest conflicts, most canonical-off, deterministic
    # by service_name length (shorter wins — canonical Door beats variant
    # names like "to Door - Saturday" when the score is otherwise tied).
    scored.sort(
        key=lambda t: (
            t[0],
            t[1],
            t[2],
            -len((t[3].get("meta") or {}).get("service_name") or ""),
        ),
        reverse=True,
    )
    return scored[0][3]
