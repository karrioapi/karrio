"""Tests for the `connection_message_builders` hook list used by the
carrier-connection mutations in `graph.schemas.base.mutations`.

The hook lives in karrio core so extension modules (entitlements,
specifically) can register custom message-building logic without karrio
importing from them.
"""

from unittest import TestCase

from karrio.server.graph.schemas.base import mutations as graph_mutations


class _FakeConnection:
    def __init__(self, carrier_name="ups", carrier_id="ups_test"):
        self.carrier_name = carrier_name
        self.carrier_id = carrier_id


class TestConnectionMessageBuilders(TestCase):
    def test_falls_back_to_generic_success_when_no_builder_registered(self):
        original = list(graph_mutations.connection_message_builders)
        graph_mutations.connection_message_builders[:] = []
        try:
            messages = graph_mutations._build_connection_messages(_FakeConnection(), requested_active=True)
        finally:
            graph_mutations.connection_message_builders[:] = original

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].code, "success")
        self.assertEqual(messages[0].carrier_name, "ups")

    def test_first_builder_with_messages_wins(self):
        def builder_a(connection, requested_active):
            return [
                dict(
                    carrier_name=connection.carrier_name,
                    carrier_id=connection.carrier_id,
                    message="From builder A",
                    code="upgrade_required",
                    level="info",
                )
            ]

        def builder_b(connection, requested_active):
            return [
                dict(
                    carrier_name=connection.carrier_name,
                    carrier_id=connection.carrier_id,
                    message="From builder B",
                    code="success",
                    level="success",
                )
            ]

        original = list(graph_mutations.connection_message_builders)
        graph_mutations.connection_message_builders[:] = [builder_a, builder_b]
        try:
            messages = graph_mutations._build_connection_messages(_FakeConnection(), requested_active=True)
        finally:
            graph_mutations.connection_message_builders[:] = original

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].code, "upgrade_required")
        self.assertEqual(messages[0].message, "From builder A")

    def test_empty_builder_output_skipped(self):
        """A builder returning None or [] lets the next builder run, then
        falls back to the generic default if nothing produced messages."""

        def builder_empty(connection, requested_active):
            return []

        def builder_none(connection, requested_active):
            return None

        original = list(graph_mutations.connection_message_builders)
        graph_mutations.connection_message_builders[:] = [builder_empty, builder_none]
        try:
            messages = graph_mutations._build_connection_messages(_FakeConnection(), requested_active=True)
        finally:
            graph_mutations.connection_message_builders[:] = original

        self.assertEqual(messages[0].code, "success")  # fell back to generic

    def test_failing_builder_is_isolated(self):
        """A broken extension shouldn't break the mutation response."""

        def boom(connection, requested_active):
            raise RuntimeError("builder crashed")

        def good(connection, requested_active):
            return [
                dict(
                    carrier_name=connection.carrier_name,
                    carrier_id=connection.carrier_id,
                    message="Recovered",
                    code="success",
                    level="success",
                )
            ]

        original = list(graph_mutations.connection_message_builders)
        graph_mutations.connection_message_builders[:] = [boom, good]
        try:
            messages = graph_mutations._build_connection_messages(_FakeConnection(), requested_active=True)
        finally:
            graph_mutations.connection_message_builders[:] = original

        self.assertEqual(messages[0].message, "Recovered")
