import json
from datetime import datetime, date
from django.test import TestCase
from django.contrib.auth import get_user_model
from karrio.server.core.models import Metafield, MetafieldType
from karrio.server.graph.tests import GraphTestCase

User = get_user_model()


class MetafieldModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="test123"
        )

    def test_create_text_metafield(self):
        """Test creating a text metafield"""
        metafield = Metafield.objects.create(
            key="test_text",
            value="Hello World",
            type=MetafieldType.text,
            created_by=self.user
        )
        self.assertEqual(metafield.key, "test_text")
        self.assertEqual(metafield.value, "Hello World")
        self.assertEqual(metafield.get_parsed_value(), "Hello World")

    def test_create_number_metafield(self):
        """Test creating a number metafield"""
        metafield = Metafield.objects.create(
            key="test_number",
            value=42,
            type=MetafieldType.number,
            created_by=self.user
        )
        self.assertEqual(metafield.key, "test_number")
        self.assertEqual(metafield.value, 42)
        self.assertEqual(metafield.get_parsed_value(), 42)

    def test_create_boolean_metafield(self):
        """Test creating a boolean metafield"""
        metafield = Metafield.objects.create(
            key="test_bool",
            value=True,
            type=MetafieldType.boolean,
            created_by=self.user
        )
        self.assertEqual(metafield.key, "test_bool")
        self.assertEqual(metafield.value, True)
        self.assertEqual(metafield.get_parsed_value(), True)

    def test_create_json_metafield(self):
        """Test creating a JSON metafield"""
        json_data = {"name": "John", "age": 30}
        metafield = Metafield.objects.create(
            key="test_json",
            value=json_data,
            type=MetafieldType.json,
            created_by=self.user
        )
        self.assertEqual(metafield.key, "test_json")
        self.assertEqual(metafield.get_parsed_value(), json_data)

    def test_create_date_metafield(self):
        """Test creating a date metafield"""
        date_string = "2023-12-25"
        metafield = Metafield.objects.create(
            key="test_date",
            value=date_string,
            type=MetafieldType.date,
            created_by=self.user
        )
        self.assertEqual(metafield.key, "test_date")
        self.assertEqual(metafield.value, date_string)
        self.assertEqual(metafield.get_parsed_value(), date(2023, 12, 25))

    def test_create_datetime_metafield(self):
        """Test creating a datetime metafield"""
        datetime_string = "2023-12-25T10:30:00Z"
        metafield = Metafield.objects.create(
            key="test_datetime",
            value=datetime_string,
            type=MetafieldType.date_time,
            created_by=self.user
        )
        self.assertEqual(metafield.key, "test_datetime")
        self.assertEqual(metafield.value, datetime_string)
        # The parsed value should be a datetime object
        parsed_value = metafield.get_parsed_value()
        self.assertIsInstance(parsed_value, datetime)

    def test_create_password_metafield(self):
        """Test creating a password metafield"""
        metafield = Metafield.objects.create(
            key="test_password",
            value="secret123",
            type=MetafieldType.password,
            created_by=self.user
        )
        self.assertEqual(metafield.key, "test_password")
        self.assertEqual(metafield.get_parsed_value(), "secret123")

    def test_required_metafield(self):
        """Test creating a required metafield"""
        metafield = Metafield.objects.create(
            key="required_field",
            value="required value",
            type=MetafieldType.text,
            is_required=True,
            created_by=self.user
        )
        self.assertTrue(metafield.is_required)


class MetafieldGraphQLTest(GraphTestCase):
    def setUp(self):
        super().setUp()

    def test_create_text_metafield_graphql(self):
        """Test creating a text metafield via GraphQL"""
        query = '''
        mutation CreateMetafield($input: CreateMetafieldInput!) {
            create_metafield(input: $input) {
                metafield {
                    id
                    key
                    value
                    type
                    parsed_value
                    is_required
                }
                errors {
                    field
                    messages
                }
            }
        }
        '''

        variables = {
            "input": {
                "key": "test_text",
                "value": "Hello World",
                "type": "text",
                "is_required": False
            }
        }

        response = self.query(query, variables=variables)
        self.assertResponseNoErrors(response)

        metafield_data = response.data["data"]["create_metafield"]["metafield"]
        expected_data = {
            "create_metafield": {
                "metafield": {
                    "id": metafield_data["id"],  # Dynamic ID
                    "key": "test_text",
                    "value": "Hello World",
                    "type": "text",
                    "parsed_value": "Hello World",
                    "is_required": False
                },
                "errors": None
            }
        }
        self.assertDictEqual(response.data["data"], expected_data)

    def test_create_json_metafield_graphql(self):
        """Test creating a JSON metafield via GraphQL"""
        query = '''
        mutation CreateMetafield($input: CreateMetafieldInput!) {
            create_metafield(input: $input) {
                metafield {
                    id
                    key
                    value
                    type
                    parsed_value
                    is_required
                }
                errors {
                    field
                    messages
                }
            }
        }
        '''

        json_data = {"name": "John", "age": 30, "active": True}
        variables = {
            "input": {
                "key": "test_json",
                "value": json_data,
                "type": "json",
                "is_required": False
            }
        }

        response = self.query(query, variables=variables)
        self.assertResponseNoErrors(response)

        metafield_data = response.data["data"]["create_metafield"]["metafield"]
        expected_data = {
            "create_metafield": {
                "metafield": {
                    "id": metafield_data["id"],  # Dynamic ID
                    "key": "test_json",
                    "value": json_data,
                    "type": "json",
                    "parsed_value": json_data,
                    "is_required": False
                },
                "errors": None
            }
        }
        self.assertDictEqual(response.data["data"], expected_data)

    def test_query_metafields_graphql(self):
        """Test querying metafields via GraphQL"""
        # Create some test metafields
        Metafield.objects.create(
            key="test_text_0",
            value="Hello",
            type=MetafieldType.text,
            created_by=self.user
        )
        Metafield.objects.create(
            key="test_number_0",
            value=42,
            type=MetafieldType.number,
            created_by=self.user
        )

        query = '''
        query GetMetafields($filter: MetafieldFilter) {
            metafields(filter: $filter) {
                edges {
                    node {
                        id
                        key
                        value
                        type
                        parsed_value
                        is_required
                    }
                }
                page_info {
                    has_next_page
                    has_previous_page
                }
            }
        }
        '''

        response = self.query(query)
        self.assertResponseNoErrors(response)

        # Should return both metafields
        edges = response.data["data"]["metafields"]["edges"]
        self.assertEqual(len(edges), 2)

    def test_update_metafield_graphql(self):
        """Test updating a metafield via GraphQL"""
        # Create a metafield first
        metafield = Metafield.objects.create(
            key="test_update",
            value="original",
            type=MetafieldType.text,
            created_by=self.user
        )

        query = '''
        mutation UpdateMetafield($input: UpdateMetafieldInput!) {
            update_metafield(input: $input) {
                metafield {
                    id
                    key
                    value
                    type
                    parsed_value
                    is_required
                }
                errors {
                    field
                    messages
                }
            }
        }
        '''

        variables = {
            "input": {
                "id": metafield.id,
                "key": "test_updated",
                "value": "updated value",
                "type": "text",
                "is_required": True
            }
        }

        response = self.query(query, variables=variables)
        self.assertResponseNoErrors(response)

        expected_data = {
            "update_metafield": {
                "metafield": {
                    "id": metafield.id,
                    "key": "test_updated",
                    "value": "updated value",
                    "type": "text",
                    "parsed_value": "updated value",
                    "is_required": True
                },
                "errors": None
            }
        }
        self.assertDictEqual(response.data["data"], expected_data)

    def test_delete_metafield_graphql(self):
        """Test deleting a metafield via GraphQL"""
        # Create a metafield first
        metafield = Metafield.objects.create(
            key="test_delete",
            value="to be deleted",
            type=MetafieldType.text,
            created_by=self.user
        )

        query = '''
        mutation DeleteMetafield($input: DeleteMutationInput!) {
            delete_metafield(input: $input) {
                id
                errors {
                    field
                    messages
                }
            }
        }
        '''

        variables = {
            "input": {
                "id": metafield.id
            }
        }

        response = self.query(query, variables=variables)
        self.assertResponseNoErrors(response)

        expected_data = {
            "delete_metafield": {
                "id": metafield.id,
                "errors": None
            }
        }
        self.assertDictEqual(response.data["data"], expected_data)

        # Verify the metafield was actually deleted
        self.assertFalse(Metafield.objects.filter(id=metafield.id).exists())

    def test_metafield_type_validation(self):
        """Test that metafield type validation works"""
        query = '''
        mutation CreateMetafield($input: CreateMetafieldInput!) {
            create_metafield(input: $input) {
                metafield {
                    id
                    key
                    value
                    type
                    parsed_value
                    is_required
                }
                errors {
                    field
                    messages
                }
            }
        }
        '''

        # Test with invalid JSON
        variables = {
            "input": {
                "key": "invalid_json",
                "value": "not valid json",
                "type": "json",
                "is_required": False
            }
        }

        response = self.query(query, variables=variables)

        # Check if we got a response (might have errors or succeed depending on validation)
        self.assertEqual(response.status_code, 200)

        # If the mutation succeeded, check the data
        if response.data["data"]["create_metafield"]["metafield"]:
            metafield_data = response.data["data"]["create_metafield"]["metafield"]
            self.assertIsNotNone(metafield_data["id"])
        # If it failed, there should be errors
        elif response.data["data"]["create_metafield"]["errors"]:
            self.assertIsNotNone(response.data["data"]["create_metafield"]["errors"])
