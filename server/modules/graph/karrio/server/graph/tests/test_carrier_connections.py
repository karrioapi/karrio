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
        self.assertDictEqual(response_data, SYSTEM_CONNECTIONS)


class TestUserConnections(GraphTestCase):
    def test_query_user_connections(self):
        response = self.query(
            """
            query get_user_connections {
                user_connections {
                  __typename
                  ... on CanadaPostSettingsType {
                    id
                    carrier_id
                    carrier_name
                    test_mode
                    active
                    username
                    password
                  }
                  ... on UPSSettingsType {
                    id
                    carrier_id
                    carrier_name
                    test_mode
                    active
                    username
                    password
                    access_license_number
                    account_number
                  }
                }
              }
            """,
            operation_name="get_user_connections",
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response_data, USER_CONNECTIONS)

    def test_create_user_connection(self):
        response = self.query(
            """
            mutation create_connection($data: CreateCarrierConnectionMutationInput!) {
              create_carrier_connection(input: $data) {
                connection {
                    ... on SendleSettingsType {
                        id
                        test_mode
                        active
                        carrier_id
                        sendle_id
                        api_key
                    }
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
                    ... on CanadaPostSettingsType {
                        carrier_id
                        username
                        customer_number
                        contract_id
                        password
                    }
                }
              }
            }
            """,
            operation_name="update_connection",
            variables={
                "data": {
                    "canadapost": {
                        "id": self.carrier.id,
                        **CONNECTION_UPDATE_DATA["data"]["canadapost"],
                    }
                },
            },
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response_data, CONNECTION_UPDATE_RESPONSE)


SYSTEM_CONNECTIONS = {
    "data": {
        "system_connections": [
            {
                "id": ANY,
                "carrier_id": "dhl_universal",
                "carrier_name": "dhl_universal",
                "test_mode": False,
                "active": True,
            },
            {
                "id": ANY,
                "carrier_id": "fedex_express",
                "carrier_name": "fedex",
                "test_mode": False,
                "active": True,
            },
        ]
    }
}

USER_CONNECTIONS = {
    "data": {
        "user_connections": [
            {
                "__typename": "UPSSettingsType",
                "id": ANY,
                "carrier_id": "ups_package",
                "carrier_name": "ups",
                "test_mode": False,
                "active": True,
                "username": "test",
                "password": "test",
                "access_license_number": "000000",
                "account_number": "000000",
            },
            {
                "__typename": "CanadaPostSettingsType",
                "id": ANY,
                "carrier_id": "canadapost",
                "carrier_name": "canadapost",
                "test_mode": False,
                "active": True,
                "username": "6e93d53968881714",
                "password": "0bfa9fcb9853d1f51ee57a",
            },
        ]
    }
}

CONNECTION_DATA = {
    "data": {
        "sendle": {
            "test_mode": False,
            "carrier_id": "sendle",
            "sendle_id": "test_sendle_id",
            "api_key": "test_api_key",
        }
    }
}

CONNECTION_RESPONSE = {
    "data": {
        "create_carrier_connection": {
            "connection": {
                "active": True,
                "api_key": "test_api_key",
                "carrier_id": "sendle",
                "id": ANY,
                "sendle_id": "test_sendle_id",
                "test_mode": False,
            }
        }
    }
}

CONNECTION_UPDATE_DATA = {
    "data": {
        "canadapost": {
            "carrier_id": "canadapost_updated",
            "username": "6e93d53968881714_updated",
            "customer_number": "2004381_updated",
            "contract_id": "42708517_updated",
            "password": "0bfa9fcb9853d1f51ee57a_updated",
        }
    }
}

CONNECTION_UPDATE_RESPONSE = {
    "data": {
        "update_carrier_connection": {
            "connection": {
                "carrier_id": "canadapost_updated",
                "contract_id": "42708517_updated",
                "customer_number": "2004381_updated",
                "password": "0bfa9fcb9853d1f51ee57a_updated",
                "username": "6e93d53968881714_updated",
            }
        }
    }
}
