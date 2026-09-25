"""Tests for plugin shipment advisors (metadata, registry, runner, invocation)."""

import attr
import unittest
from unittest.mock import patch, MagicMock
import karrio.lib as lib
import karrio.references as references
import karrio.core.advisors as advisors
import karrio.core.metadata as metadata
import karrio.core.models as models
import karrio.core.settings as settings
from karrio.api.interface import Rating, Shipment

import logging

logging.disable(logging.CRITICAL)


def country_advisor(request, context):
    return [
        models.Message(
            carrier_name=context.carrier_name,
            carrier_id=context.carrier_id,
            code="country_advice",
            level="warning",
            message=f"shipper country {request.shipper.country_code}",
        )
    ]


def carrier_integration_metadata(**kwargs) -> metadata.PluginMetadata:
    return metadata.PluginMetadata(
        id="advised_carrier",
        label="Advised Carrier",
        Mapper=MagicMock(),
        Proxy=MagicMock(),
        Settings=MagicMock(),
        **kwargs,
    )


class TestPluginMetadataAdvisors(unittest.TestCase):
    def test_advisor_only_plugin_is_typed_advisor(self):
        plugin = metadata.PluginMetadata(
            id="conventions",
            label="Conventions",
            shipment_advisors=[country_advisor],
        )

        self.assertEqual(plugin.plugin_type, "advisor")
        self.assertListEqual(plugin.plugin_types, ["advisor"])

    def test_carrier_plugin_with_advisors_reports_both_types(self):
        plugin = carrier_integration_metadata(shipment_advisors=[country_advisor])

        self.assertEqual(plugin.plugin_type, "carrier")
        self.assertListEqual(plugin.plugin_types, ["carrier", "advisor"])

    def test_plugins_without_advisors_keep_their_types(self):
        carrier = carrier_integration_metadata()
        bare = metadata.PluginMetadata(id="bare", label="Bare")

        self.assertListEqual(carrier.shipment_advisors, [])
        self.assertListEqual(carrier.plugin_types, ["carrier"])
        self.assertEqual(bare.plugin_type, "unknown")
        self.assertListEqual(bare.plugin_types, ["unknown"])

    def test_advisor_lists_are_not_shared_between_instances(self):
        first = metadata.PluginMetadata(id="first", label="First")
        second = metadata.PluginMetadata(id="second", label="Second")

        first.shipment_advisors.append(country_advisor)

        self.assertListEqual(second.shipment_advisors, [])


def entrypoint_plugins(*plugins: metadata.PluginMetadata) -> dict:
    return {plugin.id: {"entrypoint": {plugin.id: plugin}} for plugin in plugins}


class TestAdvisorRegistry(unittest.TestCase):
    def setUp(self):
        self.advisor_only = metadata.PluginMetadata(
            id="conventions",
            label="Conventions",
            shipment_advisors=[country_advisor],
        )

    def tearDown(self):
        references.import_extensions()

    def import_with(self, *plugins: metadata.PluginMetadata):
        with patch(
            "karrio.core.plugins.discover_entrypoint_plugins",
            return_value=entrypoint_plugins(*plugins),
        ):
            references.import_extensions()

    def test_advisors_are_collected_from_advisor_only_plugins(self):
        self.import_with(self.advisor_only)

        self.assertIn(("conventions", country_advisor), references.get_advisors())
        self.assertNotIn("conventions", references.PROVIDERS)
        self.assertNotIn("conventions", references.LSP_PLUGINS)

    def test_advisors_are_reset_on_reimport(self):
        self.import_with(self.advisor_only)
        self.import_with()

        self.assertNotIn(("conventions", country_advisor), references.get_advisors())

    def test_advisor_only_plugin_is_not_unknown_in_references(self):
        self.import_with(self.advisor_only)

        plugin = references.collect_references(plugin_registry={})["plugins"][
            "conventions"
        ]

        self.assertEqual(plugin["type"], "advisor")
        self.assertListEqual(plugin["types"], ["advisor"])


@attr.s(auto_attribs=True)
class CredentialSettings(settings.Settings):
    api_key: str = None
    secret: str = None

    @property
    def carrier_name(self):
        return "advised_carrier"


def credential_settings() -> CredentialSettings:
    return CredentialSettings(
        carrier_id="advised_carrier_se",
        account_country_code="SE",
        test_mode=True,
        api_key="API-KEY-VALUE",
        secret="SECRET-VALUE",
        metadata={"token": "METADATA-VALUE"},
        config={"label_type": "PDF", "nested": {"flag": True}},
        id="CONNECTION-ID-VALUE",
    )


RatePayload = {
    "shipper": {"postal_code": "11122", "country_code": "SE"},
    "recipient": {"postal_code": "0150", "country_code": "NO"},
    "parcels": [{"weight": 1.0, "weight_unit": "KG"}],
}


def rate_request() -> models.RateRequest:
    return lib.to_object(models.RateRequest, RatePayload)


class TestAdvisorContext(unittest.TestCase):
    def test_context_exposes_only_allowlisted_fields(self):
        context = advisors.AdvisorContext.from_settings(credential_settings(), "rating")

        self.assertDictEqual(
            attr.asdict(context),
            {
                "carrier_name": "advised_carrier",
                "carrier_id": "advised_carrier_se",
                "account_country_code": "SE",
                "test_mode": True,
                "operation": "rating",
                "config": {"label_type": "PDF", "nested": {"flag": True}},
            },
        )
        self.assertFalse(
            any(
                hasattr(context, name)
                for name in ["api_key", "secret", "metadata", "id", "settings"]
            )
        )

    def test_context_config_is_a_deep_copy(self):
        connection = credential_settings()
        context = advisors.AdvisorContext.from_settings(connection, "shipping")

        context.config["nested"]["flag"] = False

        self.assertTrue(connection.config["nested"]["flag"])

    def test_context_is_immutable(self):
        context = advisors.AdvisorContext.from_settings(credential_settings(), "rating")

        with self.assertRaises(attr.exceptions.FrozenInstanceError):
            context.carrier_id = "other"


def message_advisor(**kwargs):
    return lambda request, context: [
        models.Message(**{**dict(carrier_name=None, carrier_id=None), **kwargs})
    ]


def failing_advisor(request, context):
    raise ValueError("advisor exploded")


def mutating_advisor(request, context):
    request.shipper.country_code = "DK"
    return []


class TestRunAdvisors(unittest.TestCase):
    def run_with(self, *registered, request=None, operation="rating"):
        with patch.object(references, "ADVISORS", list(registered)):
            return advisors.run_advisors(
                request or rate_request(), credential_settings(), operation
            )

    def test_no_advisors_returns_no_messages(self):
        self.assertListEqual(self.run_with(), [])

    def test_levels_above_warning_are_downgraded(self):
        messages = self.run_with(
            ("p1", message_advisor(code="a", level="error", message="A")),
            ("p2", message_advisor(code="b", level="info", message="B")),
            ("p3", message_advisor(code="c", level="warning", message="C")),
            ("p4", message_advisor(code="d", message="D")),
        )

        self.assertListEqual(
            [(m.code, m.level) for m in messages],
            [("a", "warning"), ("b", "info"), ("c", "warning"), ("d", "warning")],
        )

    def test_mutating_advisor_leaves_request_unchanged(self):
        request = rate_request()
        seen = []

        self.run_with(
            ("mutator", mutating_advisor),
            ("observer", lambda req, ctx: seen.append(req.shipper.country_code) or []),
            request=request,
        )

        self.assertEqual(request.shipper.country_code, "SE")
        self.assertListEqual(seen, ["SE"])

    def test_failing_advisor_is_reported_and_others_still_run(self):
        messages = self.run_with(
            ("broken_plugin", failing_advisor),
            ("conventions", country_advisor),
        )

        self.assertListEqual(
            lib.to_dict(messages),
            [
                {
                    "carrier_name": "advised_carrier",
                    "carrier_id": "advised_carrier_se",
                    "code": "shipment_advisor_failed",
                    "level": "warning",
                    "message": "Shipment advisor from plugin 'broken_plugin' failed",
                    "details": {
                        "plugin": "broken_plugin",
                        "error": "advisor exploded",
                    },
                },
                {
                    "carrier_name": "advised_carrier",
                    "carrier_id": "advised_carrier_se",
                    "code": "country_advice",
                    "level": "warning",
                    "message": "shipper country SE",
                },
            ],
        )

    def test_invalid_advisor_output_is_reported_as_failure(self):
        messages = self.run_with(("garbage", lambda req, ctx: [object()]))

        self.assertListEqual(
            [(m.code, m.details["plugin"]) for m in messages],
            [("shipment_advisor_failed", "garbage")],
        )

    def test_message_identity_is_filled_from_context(self):
        messages = self.run_with(
            ("p1", message_advisor(code="a", level="warning")),
            (
                "p2",
                message_advisor(
                    carrier_name="explicit",
                    carrier_id="explicit_id",
                    code="b",
                    level="warning",
                ),
            ),
        )

        self.assertListEqual(
            [(m.carrier_name, m.carrier_id) for m in messages],
            [("advised_carrier", "advised_carrier_se"), ("explicit", "explicit_id")],
        )

    def test_advisor_receives_operation_in_context(self):
        seen = []

        self.run_with(
            ("p1", lambda req, ctx: seen.append(ctx.operation) or []),
            operation="shipping",
        )

        self.assertListEqual(seen, ["shipping"])


def carrier_advisor(request, context):
    return [
        models.Message(
            carrier_name=context.carrier_name,
            carrier_id=context.carrier_id,
            code="carrier_advice",
            level="warning",
            message=f"{context.operation} advice for {context.carrier_id}",
        )
    ]


def mock_gateway(carrier_id: str) -> MagicMock:
    gateway = MagicMock()
    gateway.settings.carrier_name = "test_carrier"
    gateway.settings.carrier_id = carrier_id
    gateway.settings.account_country_code = "SE"
    gateway.settings.test_mode = True
    gateway.settings.config = {}
    gateway.check.return_value = []
    return gateway


def rating_gateway(carrier_id: str, rates: list, messages: list = []) -> MagicMock:
    gateway = mock_gateway(carrier_id)
    gateway.mapper.create_rate_request.return_value = lib.Serializable({})
    gateway.proxy.get_rates.return_value = lib.Deserializable("{}", lib.to_dict)
    gateway.mapper.parse_rate_response.return_value = (rates, messages)
    return gateway


def aborted_gateway(carrier_id: str) -> MagicMock:
    gateway = mock_gateway(carrier_id)
    gateway.check.return_value = [
        models.Message(
            carrier_name="test_carrier",
            carrier_id=carrier_id,
            code="SHIPPING_SDK_NON_SUPPORTED_ERROR",
            message="not supported",
        )
    ]
    return gateway


def rate_details(carrier_id: str) -> models.RateDetails:
    return models.RateDetails(
        carrier_name="test_carrier",
        carrier_id=carrier_id,
        service="standard",
        currency="SEK",
        total_charge=100.0,
    )


def carrier_warning(carrier_id: str) -> models.Message:
    return models.Message(
        carrier_name="test_carrier",
        carrier_id=carrier_id,
        code="carrier_warning",
        level="warning",
        message="carrier says hi",
    )


class TestRatingAdvisors(unittest.TestCase):
    def fetch(self, *gateways):
        with patch.object(references, "ADVISORS", [("conventions", carrier_advisor)]):
            return Rating.fetch(RatePayload).from_(*gateways).parse()

    def test_advisor_runs_once_per_carrier_with_rates(self):
        rates, messages = self.fetch(
            rating_gateway("carrier_a", [rate_details("carrier_a")]),
            rating_gateway("carrier_b", [rate_details("carrier_b")]),
        )

        self.assertEqual(len(rates), 2)
        self.assertListEqual(
            lib.to_dict(messages),
            [
                {
                    "carrier_name": "test_carrier",
                    "carrier_id": "carrier_a",
                    "code": "carrier_advice",
                    "level": "warning",
                    "message": "rating advice for carrier_a",
                },
                {
                    "carrier_name": "test_carrier",
                    "carrier_id": "carrier_b",
                    "code": "carrier_advice",
                    "level": "warning",
                    "message": "rating advice for carrier_b",
                },
            ],
        )

    def test_no_advice_for_gateways_without_rates_or_aborted(self):
        rates, messages = self.fetch(
            rating_gateway(
                "carrier_a", [rate_details("carrier_a")], [carrier_warning("carrier_a")]
            ),
            rating_gateway("carrier_c", [], [carrier_warning("carrier_c")]),
            aborted_gateway("carrier_d"),
        )

        self.assertEqual(len(rates), 1)
        self.assertListEqual(
            [(m.carrier_id, m.code) for m in messages],
            [
                ("carrier_a", "carrier_warning"),
                ("carrier_a", "carrier_advice"),
                ("carrier_c", "carrier_warning"),
                ("carrier_d", "SHIPPING_SDK_NON_SUPPORTED_ERROR"),
            ],
        )


ShipmentPayload = {
    "shipper": {
        "person_name": "Merchant",
        "address_line1": "Storgatan 1",
        "city": "Stockholm",
        "postal_code": "11122",
        "country_code": "SE",
    },
    "recipient": {
        "person_name": "Customer",
        "address_line1": "Karl Johans gate 1",
        "city": "Oslo",
        "postal_code": "0150",
        "country_code": "NO",
    },
    "parcels": [{"weight": 1.0, "weight_unit": "KG"}],
    "service": "standard",
}


def shipment_details(carrier_id: str) -> models.ShipmentDetails:
    return models.ShipmentDetails(
        carrier_id=carrier_id,
        carrier_name="test_carrier",
        tracking_number="TRK123",
        shipment_identifier="TRK123",
        docs=dict(label="base64label"),
    )


def shipping_gateway(carrier_id: str, result: tuple) -> MagicMock:
    gateway = mock_gateway(carrier_id)
    gateway.mapper.create_shipment_request.return_value = lib.Serializable({})
    gateway.proxy.create_shipment.return_value = lib.Deserializable("{}", lib.to_dict)
    gateway.mapper.parse_shipment_response.return_value = result
    gateway.mapper.create_return_shipment_request.return_value = lib.Serializable({})
    gateway.proxy.create_return_shipment.return_value = lib.Deserializable(
        "{}", lib.to_dict
    )
    gateway.mapper.parse_return_shipment_response.return_value = result
    return gateway


class TestShipmentAdvisors(unittest.TestCase):
    def create(self, gateway, advisor=carrier_advisor, **payload):
        with patch.object(references, "ADVISORS", [("conventions", advisor)]):
            return (
                Shipment.create({**ShipmentPayload, **payload}).from_(gateway).parse()
            )

    def test_advisor_message_is_added_to_successful_shipment(self):
        details, messages = self.create(
            shipping_gateway(
                "carrier_a",
                (shipment_details("carrier_a"), [carrier_warning("carrier_a")]),
            )
        )

        self.assertEqual(details, shipment_details("carrier_a"))
        self.assertListEqual(
            lib.to_dict(messages),
            [
                lib.to_dict(carrier_warning("carrier_a")),
                {
                    "carrier_name": "test_carrier",
                    "carrier_id": "carrier_a",
                    "code": "carrier_advice",
                    "level": "warning",
                    "message": "shipping advice for carrier_a",
                },
            ],
        )

    def test_no_advice_for_failed_shipment(self):
        details, messages = self.create(
            shipping_gateway("carrier_a", (None, [carrier_warning("carrier_a")]))
        )

        self.assertIsNone(details)
        self.assertListEqual(messages, [carrier_warning("carrier_a")])

    def test_no_advice_for_aborted_shipment(self):
        details, messages = self.create(aborted_gateway("carrier_a"))

        self.assertIsNone(details)
        self.assertListEqual(
            [m.code for m in messages], ["SHIPPING_SDK_NON_SUPPORTED_ERROR"]
        )

    def test_return_shipment_is_advised_on_swapped_request(self):
        details, messages = self.create(
            shipping_gateway("carrier_a", (shipment_details("carrier_a"), [])),
            advisor=country_advisor,
            is_return=True,
        )

        self.assertListEqual([m.message for m in messages], ["shipper country NO"])


class TestWithoutAdvisors(unittest.TestCase):
    def setUp(self):
        patcher = patch.object(references, "ADVISORS", [])
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_rate_response_is_unchanged(self):
        rates, messages = (
            Rating.fetch(RatePayload)
            .from_(
                rating_gateway(
                    "carrier_a",
                    [rate_details("carrier_a")],
                    [carrier_warning("carrier_a")],
                ),
                rating_gateway("carrier_b", [rate_details("carrier_b")]),
                rating_gateway("carrier_c", [], [carrier_warning("carrier_c")]),
                aborted_gateway("carrier_d"),
            )
            .parse()
        )

        self.assertListEqual(
            rates, [rate_details("carrier_a"), rate_details("carrier_b")]
        )
        self.assertListEqual(
            [(m.carrier_id, m.code) for m in messages],
            [
                ("carrier_a", "carrier_warning"),
                ("carrier_c", "carrier_warning"),
                ("carrier_d", "SHIPPING_SDK_NON_SUPPORTED_ERROR"),
            ],
        )

    def test_shipment_response_is_unchanged(self):
        parsed = (shipment_details("carrier_a"), [carrier_warning("carrier_a")])

        result = (
            Shipment.create(ShipmentPayload)
            .from_(shipping_gateway("carrier_a", parsed))
            .parse()
        )

        self.assertIs(result, parsed)

    def test_return_shipment_response_is_unchanged(self):
        parsed = (shipment_details("carrier_a"), [])

        result = (
            Shipment.create({**ShipmentPayload, "is_return": True})
            .from_(shipping_gateway("carrier_a", parsed))
            .parse()
        )

        self.assertIs(result, parsed)


# Mirrors the example plugin in apps/www/docs/carriers/sdk/advisors.mdx
def invoice_email_advisor(request, context):
    if context.operation != "shipping":
        return []

    if (request.shipper.country_code, request.recipient.country_code) != ("SE", "NO"):
        return []

    return [
        models.Message(
            carrier_name=None,
            carrier_id=None,
            code="commercial_invoice_email",
            level="warning",
            message="Email the commercial invoice to the recipient",
        )
    ]


LANE_CONVENTIONS_METADATA = metadata.PluginMetadata(
    id="lane_conventions",
    label="Lane Conventions",
    shipment_advisors=[invoice_email_advisor],
)


class TestDocumentedAdvisorPlugin(unittest.TestCase):
    def setUp(self):
        patcher = patch.object(
            references,
            "ADVISORS",
            [
                (LANE_CONVENTIONS_METADATA.id, advisor)
                for advisor in LANE_CONVENTIONS_METADATA.shipment_advisors
            ],
        )
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_documented_plugin_is_typed_advisor(self):
        self.assertEqual(LANE_CONVENTIONS_METADATA.plugin_type, "advisor")

    def test_documented_advisor_advises_shipments_only(self):
        _, rate_messages = (
            Rating.fetch(RatePayload)
            .from_(rating_gateway("carrier_a", [rate_details("carrier_a")]))
            .parse()
        )
        _, shipment_messages = (
            Shipment.create(ShipmentPayload)
            .from_(shipping_gateway("carrier_a", (shipment_details("carrier_a"), [])))
            .parse()
        )

        self.assertListEqual(rate_messages, [])
        self.assertListEqual(
            lib.to_dict(shipment_messages),
            [
                {
                    "carrier_name": "test_carrier",
                    "carrier_id": "carrier_a",
                    "code": "commercial_invoice_email",
                    "level": "warning",
                    "message": "Email the commercial invoice to the recipient",
                }
            ],
        )


if __name__ == "__main__":
    unittest.main()
