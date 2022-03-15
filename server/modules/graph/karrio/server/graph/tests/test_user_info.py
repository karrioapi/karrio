import json
from unittest.mock import ANY
from karrio.server.graph.tests.base import GraphTestCase


class TestUserUpdate(GraphTestCase):
    def test_update_user_info(self):
        response = self.query(
            """
            mutation update_user($data: UpdateUserInput!) {
              update_user(input: $data) {
                user {
                  email
                  full_name
                  is_staff
                  last_login
                  date_joined
                }
              }
            }
            """,
            op_name="update_user",
            variables=USER_UPDATE_DATA,
        )
        response_data = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response_data, USER_UPDATE_RESPONSE)


class TestTokenMutation(GraphTestCase):
    def test_update_token(self):
        current_token = self.token.key
        response = self.query(
            """
            mutation mutate_token($data: TokenMutationInput!) {
              mutate_token(input: $data) {
                token {
                  key
                  created
                }
              }
            }
            """,
            op_name="mutate_token",
            variables=TOKEN_MUTATION_DATA,
        )
        response_data = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertFalse(
            response_data["data"]["mutate_token"]["token"]["key"] == current_token
        )


USER_UPDATE_DATA = {"data": {"full_name": "Marco"}}

USER_UPDATE_RESPONSE = {
    "data": {
        "update_user": {
            "user": {
                "date_joined": ANY,
                "email": "admin@example.com",
                "full_name": "Marco",
                "is_staff": True,
                "last_login": ANY,
            }
        }
    }
}

TOKEN_MUTATION_DATA = {"data": {"refresh": True, "password": "test"}}
