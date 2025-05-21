import karrio.lib as lib
from unittest.mock import ANY
from karrio.server.graph.tests.base import GraphTestCase


class TestSystemConnections(GraphTestCase):
    def test_query_system_connections(self):
        response = self.query(
            """
            query get_system_connections {
              system_connections {
                id
                carrier_id
                carrier_name
                test_mode
                active
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
                    id
                    carrier_id
                    carrier_name
                    test_mode
                    active
                    credentials
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
                    test_mode
                    active
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


SYSTEM_CONNECTIONS = {
    "data": {
        "system_connections": [
            {
                "active": True,
                "carrier_id": "dhl_universal",
                "carrier_name": "dhl_universal",
                "id": ANY,
                "test_mode": False,
            },
            {
                "active": True,
                "carrier_id": "fedex_express",
                "carrier_name": "fedex",
                "id": ANY,
                "test_mode": False,
            },
        ]
    }
}

USER_CONNECTIONS = {
    "data": {
        "user_connections": [
            {
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
            },
            {
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
            },
        ]
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
