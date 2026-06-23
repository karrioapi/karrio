from unittest.mock import ANY

import karrio.lib as lib
import karrio.server.providers.models as providers
from karrio.server.graph.tests.base import GraphTestCase

SYSTEM_CONNECTIONS_COUNTS_QUERY = """
    query get_system_connections_counts {
      system_connections {
        edges {
          node {
            id
            carrier_id
            carrier_name
            user_contracts_count
            user_active_contracts_count
          }
        }
      }
    }
"""


class TestSystemConnections(GraphTestCase):
    def test_query_system_connections(self):
        response = self.query(
            """
            query get_system_connections {
              system_connections {
                edges {
                  node {
                    id
                    carrier_id
                    carrier_name
                    active
                    test_mode
                  }
                }
              }
            }
            """,
            operation_name="get_system_connections",
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            lib.to_dict(response_data),
            SYSTEM_CONNECTIONS,
        )


class TestUserConnections(GraphTestCase):
    def test_query_user_connections(self):
        response = self.query(
            """
            query get_user_connections {
                user_connections {
                edges {
                  node {
                    id
                    carrier_id
                    carrier_name
                    active
                    test_mode
                    credentials
                  }
                }
              }
            }
            """,
            operation_name="get_user_connections",
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            lib.to_dict(response_data),
            USER_CONNECTIONS,
        )

    def test_create_user_connection(self):
        response = self.query(
            """
            mutation create_connection($data: CreateCarrierConnectionMutationInput!) {
              create_carrier_connection(input: $data) {
                connection {
                    id
                    carrier_id
                    carrier_name
                    active
                    test_mode
                    credentials
                }
              }
            }
            """,
            operation_name="create_connection",
            variables=CONNECTION_DATA,
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response_data, CONNECTION_RESPONSE)

    def test_update_user_connection(self):
        response = self.query(
            """
            mutation update_connection($data: UpdateCarrierConnectionMutationInput!) {
              update_carrier_connection(input: $data) {
                connection {
                    carrier_id
                    credentials
                }
              }
            }
            """,
            operation_name="update_connection",
            variables={
                "data": {
                    "id": self.carrier.id,
                    **CONNECTION_UPDATE_DATA["data"],
                },
            },
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            lib.to_dict(response_data),
            lib.to_dict(CONNECTION_UPDATE_RESPONSE),
        )


USER_CONNECTIONS_ORDERING_QUERY = """
    query get_user_connections_ordering {
        user_connections {
          edges {
            node {
              carrier_id
              active
              test_mode
            }
          }
        }
    }
"""


class TestUserConnectionsOrdering(GraphTestCase):
    def setUp(self):
        super().setUp()

    def test_user_connections_orders_active_before_inactive_within_test_mode(self):
        # Flip one base fixture to inactive for this test only (rolls back after).
        self.fedex_carrier.active = False
        self.fedex_carrier.save()

        # Also create a brand-new inactive connection to stress the ordering.
        inactive = providers.CarrierConnection.objects.create(
            carrier_code="canadapost",
            carrier_id="canadapost_inactive",
            test_mode=False,
            active=False,
            created_by=self.user,
            credentials=dict(
                username="x",
                customer_number="x",
                contract_id="x",
                password="x",
            ),
        )

        response = self.query(
            USER_CONNECTIONS_ORDERING_QUERY,
            operation_name="get_user_connections_ordering",
        )
        self.assertResponseNoErrors(response)

        nodes = [
            edge["node"] for edge in response.data["data"]["user_connections"]["edges"] if not edge["node"]["test_mode"]
        ]
        active_indices = [i for i, n in enumerate(nodes) if n["active"]]
        inactive_indices = [i for i, n in enumerate(nodes) if not n["active"]]

        self.assertTrue(active_indices, "Expected at least one active connection")
        self.assertTrue(inactive_indices, "Expected at least one inactive connection")
        self.assertLess(
            max(active_indices),
            min(inactive_indices),
            f"All active connections must appear before inactive ones. "
            f"active_indices={active_indices}, inactive_indices={inactive_indices}",
        )

        inactive.delete()

    def test_user_connections_all_returned_share_same_test_mode_as_token(self):
        # The GraphTestCase token is test_mode=False; the resolver filters to matching
        # test_mode. Verify all returned connections share test_mode=False — this confirms
        # the test_mode primary sort key is honoured at the resolver level.
        response = self.query(
            USER_CONNECTIONS_ORDERING_QUERY,
            operation_name="get_user_connections_ordering",
        )
        self.assertResponseNoErrors(response)

        nodes = [edge["node"] for edge in response.data["data"]["user_connections"]["edges"]]
        self.assertTrue(nodes, "Expected at least one connection in response")
        for node in nodes:
            self.assertFalse(
                node["test_mode"],
                f"Expected all connections to be test_mode=False when using a live token, "
                f"got test_mode=True for carrier_id={node['carrier_id']}",
            )


SYSTEM_CONNECTIONS = {
    "data": {
        "system_connections": {
            "edges": [
                {
                    "node": {
                        "active": True,
                        "carrier_id": "fedex_express",
                        "carrier_name": "fedex",
                        "id": ANY,
                        "test_mode": False,
                    }
                },
                {
                    "node": {
                        "active": True,
                        "carrier_id": "dhl_universal",
                        "carrier_name": "dhl_universal",
                        "id": ANY,
                        "test_mode": False,
                    }
                },
            ]
        }
    }
}

USER_CONNECTIONS = {
    "data": {
        "user_connections": {
            "edges": [
                {
                    "node": {
                        "active": True,
                        "carrier_id": "canadapost",
                        "carrier_name": "canadapost",
                        "credentials": {
                            "contract_id": "42708517",
                            "customer_number": "2004381",
                            "password": "0bfa9fcb9853d1f51ee57a",
                            "username": "6e93d53968881714",
                        },
                        "id": ANY,
                        "test_mode": False,
                    }
                },
                {
                    "node": {
                        "active": True,
                        "carrier_id": "dhl_universal",
                        "carrier_name": "dhl_universal",
                        "credentials": {
                            "consumer_key": "test",
                            "consumer_secret": "password",
                        },
                        "id": ANY,
                        "test_mode": False,
                    }
                },
                {
                    "node": {
                        "active": True,
                        "carrier_id": "fedex_express",
                        "carrier_name": "fedex",
                        "credentials": {
                            "account_number": "000000",
                            "api_key": "test",
                            "secret_key": "password",
                            "track_api_key": "test",
                            "track_secret_key": "password",
                        },
                        "id": ANY,
                        "test_mode": False,
                    }
                },
                {
                    "node": {
                        "active": True,
                        "carrier_id": "ups_package",
                        "carrier_name": "ups",
                        "credentials": {
                            "account_number": "000000",
                            "client_id": "test",
                            "client_secret": "test",
                        },
                        "id": ANY,
                        "test_mode": False,
                    }
                },
            ]
        }
    }
}

CONNECTION_DATA = {
    "data": {
        "carrier_name": "sendle",
        "carrier_id": "sendle",
        "credentials": {
            "sendle_id": "test_sendle_id",
            "api_key": "test_api_key",
        },
    }
}

CONNECTION_RESPONSE = {
    "data": {
        "create_carrier_connection": {
            "connection": {
                "id": ANY,
                "active": True,
                "carrier_id": "sendle",
                "carrier_name": "sendle",
                "test_mode": False,
                "credentials": {
                    "api_key": "test_api_key",
                    "sendle_id": "test_sendle_id",
                    "account_country_code": None,
                },
            }
        }
    }
}

CONNECTION_UPDATE_DATA = {
    "data": {
        "carrier_id": "canadapost_updated",
        "credentials": {
            "username": "6e93d53968881714_updated",
            "customer_number": "2004381_updated",
            "contract_id": "42708517_updated",
            "password": "0bfa9fcb9853d1f51ee57a_updated",
        },
    }
}

CONNECTION_UPDATE_RESPONSE = {
    "data": {
        "update_carrier_connection": {
            "connection": {
                "carrier_id": "canadapost_updated",
                "credentials": {
                    "account_country_code": "CA",
                    "contract_id": "42708517_updated",
                    "customer_number": "2004381_updated",
                    "password": "0bfa9fcb9853d1f51ee57a_updated",
                    "username": "6e93d53968881714_updated",
                },
            }
        }
    }
}


SYSTEM_CONNECTIONS_FILTER_QUERY = """
    query get_system_connections_filtered($filter: CarrierFilter) {
      system_connections(filter: $filter) {
        edges {
          node {
            carrier_id
            account_country_code
          }
        }
      }
    }
"""


class TestSystemConnectionsCountryFilter(GraphTestCase):
    """Regression: ensure `account_country_code` filter is applied server-side so
    the dashboard isn't relying on a client-side filter applied to a page that's
    already been truncated by `paginated_connection`'s default `first=25`."""

    def setUp(self):
        super().setUp()
        self.dhl_system_connection.credentials = {
            **(self.dhl_system_connection.credentials or {}),
            "account_country_code": "DE",
        }
        self.dhl_system_connection.save()
        self.fedex_system_connection.credentials = {
            **(self.fedex_system_connection.credentials or {}),
            "account_country_code": "US",
        }
        self.fedex_system_connection.save()

    def test_filter_by_account_country_code_returns_only_matching(self):
        response = self.query(
            SYSTEM_CONNECTIONS_FILTER_QUERY,
            operation_name="get_system_connections_filtered",
            variables={"filter": {"account_country_code": ["DE"]}},
        )
        self.assertResponseNoErrors(response)

        nodes = [edge["node"] for edge in response.data["data"]["system_connections"]["edges"]]
        self.assertTrue(nodes, "Expected at least one connection for DE")
        for node in nodes:
            self.assertEqual(node["account_country_code"], "DE")

    def test_filter_by_account_country_code_supports_multiple(self):
        response = self.query(
            SYSTEM_CONNECTIONS_FILTER_QUERY,
            operation_name="get_system_connections_filtered",
            variables={"filter": {"account_country_code": ["DE", "US"]}},
        )
        self.assertResponseNoErrors(response)

        country_codes = sorted(
            edge["node"]["account_country_code"] for edge in response.data["data"]["system_connections"]["edges"]
        )
        self.assertEqual(country_codes, ["DE", "US"])

    def test_filter_omitted_returns_all_active_connections(self):
        response = self.query(
            SYSTEM_CONNECTIONS_FILTER_QUERY,
            operation_name="get_system_connections_filtered",
            variables={"filter": {}},
        )
        self.assertResponseNoErrors(response)

        country_codes = sorted(
            edge["node"]["account_country_code"] for edge in response.data["data"]["system_connections"]["edges"]
        )
        self.assertEqual(country_codes, ["DE", "US"])


class TestSystemConnectionsUserContractsCount(GraphTestCase):
    """Regression: the scalar Subquery in `SystemConnectionType.resolve_list` must not
    inherit `CarrierConnectionManager`'s ORDER BY, otherwise Django widens the implicit
    GROUP BY and Postgres raises "more than one row returned by a subquery"."""

    def setUp(self):
        super().setUp()
        # OuterRef in resolve_list correlates on credentials__account_country_code.
        self.dhl_system_connection.credentials = {
            **(self.dhl_system_connection.credentials or {}),
            "account_country_code": "DE",
        }
        self.dhl_system_connection.save()

        # 3 user connections: same carrier_code/country, varying active+created_at — the
        # exact shape that breaks the broken GROUP BY (would split into 3 groups).
        for carrier_id, active in [
            ("dhl_universal_extra_inactive", False),
            ("dhl_universal_extra_active_1", True),
            ("dhl_universal_extra_active_2", True),
        ]:
            providers.CarrierConnection.objects.create(
                carrier_code="dhl_universal",
                carrier_id=carrier_id,
                test_mode=False,
                active=active,
                created_by=self.user,
                credentials={
                    "consumer_key": carrier_id,
                    "consumer_secret": "p",
                    "account_country_code": "DE",
                },
                capabilities=["tracking"],
            )

    def test_user_contracts_count_with_multiple_connections_same_carrier(self):
        response = self.query(
            SYSTEM_CONNECTIONS_COUNTS_QUERY,
            operation_name="get_system_connections_counts",
        )
        self.assertResponseNoErrors(response)

        dhl_node = next(
            (
                e["node"]
                for e in response.data["data"]["system_connections"]["edges"]
                if e["node"]["carrier_id"] == "dhl_universal"
            ),
            None,
        )
        self.assertIsNotNone(dhl_node)
        self.assertEqual(dhl_node["user_contracts_count"], 3)
        self.assertEqual(dhl_node["user_active_contracts_count"], 2)
