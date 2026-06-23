"""Rate-request dispatcher.

Routes a rate request to `Rates.fetch` (live carrier API) or `Rates.resolve`
(rate-sheet only, no carrier HTTP) based on each carrier's attached rate
sheet `pricing_config.use_static_rates` flag.

When no carrier opts in, the underlying call is `Rates.fetch(...)` exactly
as before — same payload, same response shape, same after-hooks fire. When
all carriers opt in, only `Rates.resolve(...)` runs (no carrier API). When
the request straddles both, the dispatcher partitions the carrier list and
merges the two responses transparently.

The pricing module's `apply_custom_markups` after-hook is registered on
both `Rates.fetch` and `Rates.resolve`, so plan markups + plan_costs
enrichment apply uniformly regardless of which path produced a rate.
"""

from __future__ import annotations

import typing

import karrio.server.core.datatypes as datatypes
import karrio.server.core.exceptions as exceptions
from karrio.server.core.gateway import Carriers, Rates
from karrio.server.providers.rate_sheet_datatypes import RateSheetPricingConfig
from rest_framework import status
from rest_framework.exceptions import NotFound


def dispatch_rates(
    payload: dict,
    *,
    context: typing.Any = None,
    carriers: list | None = None,
    raise_on_error: bool = True,
    **carrier_filters,
) -> datatypes.RateResponse:
    """Drop-in replacement for `Rates.fetch(...)` that opts each carrier
    into the rate-sheet resolver when its sheet sets
    `pricing_config.use_static_rates`.
    """
    resolved_carriers = (
        list(carriers)
        if carriers is not None
        else _default_carrier_list(payload=payload, context=context, **carrier_filters)
    )
    static_carriers, live_carriers = _partition_by_static_flag(resolved_carriers)

    static_response = (
        Rates.resolve(
            payload,
            context=context,
            carriers=static_carriers,
            raise_on_error=False,
        )
        if static_carriers
        else None
    )
    live_response = (
        Rates.fetch(
            payload,
            context=context,
            carriers=live_carriers,
            raise_on_error=False,
        )
        if live_carriers
        else None
    )

    merged = _merge_rate_responses(static_response, live_response)

    if raise_on_error and not resolved_carriers:
        raise NotFound("No active carrier connection found to process the request")
    if raise_on_error and not merged.rates and merged.messages:
        raise exceptions.APIException(
            detail=merged.messages,
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
        )
    return merged


def _default_carrier_list(
    *,
    payload: dict,
    context: typing.Any,
    **carrier_filters,
) -> list:
    """Mirror `Rates.fetch`'s default carrier-listing filters so the
    dispatcher is byte-equivalent to a direct fetch when nothing opts in.
    """
    return Carriers.list(
        context=context,
        **{
            "active": True,
            "capability": "rating",
            "carrier_ids": payload.get("carrier_ids", []),
            "services": payload.get("services", []),
            **carrier_filters,
        },
    )


def _partition_by_static_flag(carriers: list) -> tuple[list, list]:
    """Split carriers into (static, live).

    A carrier goes to the static bucket only when (a) it has a rate
    sheet attached AND (b) that sheet's
    `pricing_config.use_static_rates` resolves to True (default). Sheet-
    less carriers (account `CarrierConnection`s without a rate sheet)
    always go live — there's no sheet for the resolver to consult.
    """
    static: list = []
    live: list = []
    for carrier in carriers:
        sheet = _carrier_rate_sheet(carrier)
        if sheet is None:
            live.append(carrier)
            continue
        cfg = RateSheetPricingConfig.from_dict(getattr(sheet, "pricing_config", None) or {})
        (static if cfg.use_static_rates else live).append(carrier)
    return static, live


def _carrier_rate_sheet(carrier) -> typing.Any:
    """Return the rate sheet attached to a carrier, if any.

    Brokered: the rate sheet lives on the wrapped SystemConnection.
    Direct system / account carriers: the rate sheet is on the carrier itself.
    """
    direct = getattr(carrier, "rate_sheet", None)
    if direct is not None:
        return direct
    sysconn = getattr(carrier, "system_connection", None)
    if sysconn is not None:
        return getattr(sysconn, "rate_sheet", None)
    return None


def _merge_rate_responses(
    *responses: datatypes.RateResponse | None,
) -> datatypes.RateResponse:
    """Concatenate `rates` and `messages` across non-None responses."""
    rates: list = []
    messages: list = []
    for response in responses:
        if response is None:
            continue
        rates.extend(response.rates or [])
        messages.extend(response.messages or [])
    return datatypes.RateResponse(rates=rates, messages=messages)
