"""Tests for `karrio.server.core.rate_dispatcher.dispatch_rates`.

Drop-in replacement for `Rates.fetch(...)` that opts each carrier into
the rate-sheet resolver when its sheet sets
`pricing_config.use_static_rates`.

These tests mock `Rates.fetch` and `Rates.resolve` (the underlying gateway
calls) and use lightweight `SimpleNamespace` carrier shims so the
dispatcher's partition logic can be exercised in pure unit-test mode
without a Django DB roundtrip.
"""

import types
import unittest
from unittest.mock import patch

import karrio.server.core.datatypes as datatypes
import karrio.server.core.exceptions as exceptions
from karrio.core.models import Message
from karrio.server.core.rate_dispatcher import dispatch_rates
from rest_framework.exceptions import NotFound


def _carrier(
    *, carrier_id: str, sheet_pricing_config: dict | None = None, brokered: bool = False
) -> types.SimpleNamespace:
    """Build a minimal carrier-shaped object: either an account/system
    `CarrierConnection` (rate_sheet directly on it) or a brokered
    connection (rate_sheet on `.system_connection`)."""
    sheet = (
        types.SimpleNamespace(pricing_config=dict(sheet_pricing_config)) if sheet_pricing_config is not None else None
    )
    if brokered:
        return types.SimpleNamespace(
            id=carrier_id,
            carrier_id=carrier_id,
            system_connection=types.SimpleNamespace(rate_sheet=sheet),
        )
    return types.SimpleNamespace(id=carrier_id, carrier_id=carrier_id, rate_sheet=sheet)


def _rate_response(*rates: tuple, messages: list | None = None) -> datatypes.RateResponse:
    return datatypes.RateResponse(
        rates=[
            datatypes.Rate(
                carrier_name="test",
                carrier_id=cid,
                service=svc,
                total_charge=amount,
                currency="EUR",
                extra_charges=[],
                meta={},
            )
            for cid, svc, amount in rates
        ],
        messages=messages or [],
    )


_PAYLOAD = {
    "shipper": {"country_code": "DE"},
    "recipient": {"country_code": "DE"},
    "parcels": [{"weight": 1.0, "weight_unit": "KG"}],
}


class TestDispatchRatesPartition(unittest.TestCase):
    """Unit tests for the fetch-vs-resolve partition logic.

    Mocks `Rates.fetch` and `Rates.resolve` at the dispatcher's import
    site (`karrio.server.core.rate_dispatcher.Rates`) so we can assert
    exactly which path is taken for each carrier.
    """

    def test_default_flag_is_static_when_sheet_attached(self):
        """When a sheet is attached but doesn't explicitly set the flag,
        the dataclass default (`use_static_rates=True`) applies — the
        carrier routes to `Rates.resolve`. Sheets pre-dating the field
        get the new behaviour automatically."""
        carriers = [
            _carrier(carrier_id="c1", sheet_pricing_config={}),
            _carrier(carrier_id="c2", sheet_pricing_config={"excluded_markup_ids": []}),
        ]
        with patch("karrio.server.core.rate_dispatcher.Rates") as rates_mock:
            rates_mock.resolve.return_value = _rate_response(("c1", "svc", 5.00), ("c2", "svc", 6.00))

            response = dispatch_rates(_PAYLOAD, carriers=carriers)

        rates_mock.resolve.assert_called_once()
        rates_mock.fetch.assert_not_called()
        resolve_carriers = rates_mock.resolve.call_args.kwargs["carriers"]
        self.assertEqual([c.carrier_id for c in resolve_carriers], ["c1", "c2"])
        self.assertEqual(len(response.rates), 2)

    def test_explicit_false_opts_back_to_live(self):
        """Sheets that explicitly set `use_static_rates: false` opt back
        into the live carrier API at quote time."""
        carriers = [_carrier(carrier_id="c1", sheet_pricing_config={"use_static_rates": False})]
        with patch("karrio.server.core.rate_dispatcher.Rates") as rates_mock:
            rates_mock.fetch.return_value = _rate_response(("c1", "svc", 5.00))

            dispatch_rates(_PAYLOAD, carriers=carriers)

        rates_mock.fetch.assert_called_once()
        rates_mock.resolve.assert_not_called()

    def test_all_static_routes_to_resolve_only_no_carrier_proxy(self):
        """Every sheet has `use_static_rates=True` — `Rates.fetch` is never called."""
        carriers = [
            _carrier(carrier_id="c1", sheet_pricing_config={"use_static_rates": True}),
            _carrier(carrier_id="c2", sheet_pricing_config={"use_static_rates": True}, brokered=True),
        ]
        with patch("karrio.server.core.rate_dispatcher.Rates") as rates_mock:
            rates_mock.resolve.return_value = _rate_response(("c1", "svc", 4.75), ("c2", "svc", 5.50))

            response = dispatch_rates(_PAYLOAD, carriers=carriers)

        rates_mock.resolve.assert_called_once()
        rates_mock.fetch.assert_not_called()
        resolve_carriers = rates_mock.resolve.call_args.kwargs["carriers"]
        self.assertEqual([c.carrier_id for c in resolve_carriers], ["c1", "c2"])
        self.assertEqual(len(response.rates), 2)

    def test_mixed_partitions_correctly(self):
        """One carrier opts out, the other keeps the default — both paths run on disjoint subsets."""
        carriers = [
            _carrier(carrier_id="static", sheet_pricing_config={"use_static_rates": True}),
            _carrier(carrier_id="live", sheet_pricing_config={"use_static_rates": False}),
        ]
        with patch("karrio.server.core.rate_dispatcher.Rates") as rates_mock:
            rates_mock.resolve.return_value = _rate_response(("static", "svc", 4.75))
            rates_mock.fetch.return_value = _rate_response(("live", "svc", 5.00))

            response = dispatch_rates(_PAYLOAD, carriers=carriers)

        rates_mock.resolve.assert_called_once()
        rates_mock.fetch.assert_called_once()
        self.assertEqual([c.carrier_id for c in rates_mock.resolve.call_args.kwargs["carriers"]], ["static"])
        self.assertEqual([c.carrier_id for c in rates_mock.fetch.call_args.kwargs["carriers"]], ["live"])
        # Merged response carries rates from both buckets.
        self.assertEqual({r.carrier_id for r in response.rates}, {"static", "live"})

    def test_brokered_flag_read_from_system_connection_rate_sheet(self):
        """Brokered carriers carry `rate_sheet` on `system_connection`, not directly."""
        brokered_static = _carrier(
            carrier_id="brokered",
            sheet_pricing_config={"use_static_rates": True},
            brokered=True,
        )
        with patch("karrio.server.core.rate_dispatcher.Rates") as rates_mock:
            rates_mock.resolve.return_value = _rate_response(("brokered", "svc", 4.75))

            dispatch_rates(_PAYLOAD, carriers=[brokered_static])

        rates_mock.resolve.assert_called_once()
        rates_mock.fetch.assert_not_called()

    def test_carrier_without_rate_sheet_routes_live(self):
        """Account carriers without a rate sheet always go through `fetch`."""
        carriers = [_carrier(carrier_id="account_no_sheet")]
        with patch("karrio.server.core.rate_dispatcher.Rates") as rates_mock:
            rates_mock.fetch.return_value = _rate_response(("account_no_sheet", "svc", 5.00))

            dispatch_rates(_PAYLOAD, carriers=carriers)

        rates_mock.fetch.assert_called_once()
        rates_mock.resolve.assert_not_called()

    def test_invalid_flag_value_coerces_to_false(self):
        """`{"use_static_rates": "yes"}` → bool('yes') == True. `{"use_static_rates": 0}` → False.

        The dataclass coerces via `bool(...)` so any truthy value opts in.
        This test pins the truthy/falsy semantics so a misconfigured sheet
        doesn't crash the dispatcher.
        """
        truthy = _carrier(carrier_id="truthy", sheet_pricing_config={"use_static_rates": "yes"})
        falsy = _carrier(carrier_id="falsy", sheet_pricing_config={"use_static_rates": 0})
        with patch("karrio.server.core.rate_dispatcher.Rates") as rates_mock:
            rates_mock.resolve.return_value = _rate_response(("truthy", "svc", 4.75))
            rates_mock.fetch.return_value = _rate_response(("falsy", "svc", 5.00))

            dispatch_rates(_PAYLOAD, carriers=[truthy, falsy])

        rates_mock.resolve.assert_called_once()
        rates_mock.fetch.assert_called_once()
        self.assertEqual([c.carrier_id for c in rates_mock.resolve.call_args.kwargs["carriers"]], ["truthy"])
        self.assertEqual([c.carrier_id for c in rates_mock.fetch.call_args.kwargs["carriers"]], ["falsy"])

    def test_merged_response_concatenates_rates_and_messages(self):
        carriers = [
            _carrier(carrier_id="s", sheet_pricing_config={"use_static_rates": True}),
            _carrier(carrier_id="l"),
        ]
        with patch("karrio.server.core.rate_dispatcher.Rates") as rates_mock:
            rates_mock.resolve.return_value = _rate_response(
                ("s", "svc", 4.75),
                messages=[Message(carrier_id="s", carrier_name="test", code="info", message="static-info")],
            )
            rates_mock.fetch.return_value = _rate_response(
                ("l", "svc", 5.00),
                messages=[Message(carrier_id="l", carrier_name="test", code="info", message="live-info")],
            )

            response = dispatch_rates(_PAYLOAD, carriers=carriers)

        self.assertEqual(len(response.rates), 2)
        self.assertEqual(
            sorted(m.message for m in response.messages),
            ["live-info", "static-info"],
        )

    def test_raise_on_error_when_no_carriers(self):
        with patch("karrio.server.core.rate_dispatcher.Rates"), self.assertRaises(NotFound):
            dispatch_rates(_PAYLOAD, carriers=[], raise_on_error=True)

    def test_no_raise_on_empty_carriers_when_flag_off(self):
        with patch("karrio.server.core.rate_dispatcher.Rates"):
            response = dispatch_rates(_PAYLOAD, carriers=[], raise_on_error=False)
        self.assertEqual(response.rates, [])
        self.assertEqual(response.messages, [])

    def test_raise_on_error_424_when_no_rates_only_messages(self):
        carriers = [_carrier(carrier_id="c1")]
        with patch("karrio.server.core.rate_dispatcher.Rates") as rates_mock:
            rates_mock.fetch.return_value = _rate_response(
                messages=[Message(carrier_id="c1", carrier_name="test", code="error", message="boom")],
            )
            with self.assertRaises(exceptions.APIException):
                dispatch_rates(_PAYLOAD, carriers=carriers, raise_on_error=True)

    def test_subcalls_passed_raise_on_error_false(self):
        """Subcalls to fetch/resolve must use `raise_on_error=False` so the
        dispatcher itself is the only place that raises — otherwise a
        partial-success (one bucket fails, the other returns rates)
        would erroneously bubble an exception."""
        carriers = [
            _carrier(carrier_id="s", sheet_pricing_config={"use_static_rates": True}),
            _carrier(carrier_id="l"),
        ]
        with patch("karrio.server.core.rate_dispatcher.Rates") as rates_mock:
            rates_mock.resolve.return_value = _rate_response(("s", "svc", 4.75))
            rates_mock.fetch.return_value = _rate_response(("l", "svc", 5.00))

            dispatch_rates(_PAYLOAD, carriers=carriers, raise_on_error=True)

        self.assertIs(rates_mock.resolve.call_args.kwargs["raise_on_error"], False)
        self.assertIs(rates_mock.fetch.call_args.kwargs["raise_on_error"], False)


if __name__ == "__main__":
    unittest.main()
