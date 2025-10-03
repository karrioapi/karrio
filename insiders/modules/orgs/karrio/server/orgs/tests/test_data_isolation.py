from django.urls import reverse
from karrio.server.user.models import Token
from django.contrib.auth import get_user_model
from karrio.server.core.tests import APITestCase
from karrio.server.graph.tests.base import GraphTestCase


CREATE_ORGANIZATION_MUTATION = """
mutation CreateOrganization($data: CreateOrganizationMutationInput!) {
    create_organization(input: $data) {
        organization { id name slug }
        errors { field messages }
    }
}
"""

CREATE_CARRIER_CONNECTION_MUTATION = """
mutation CreateCarrierConnection($data: CreateCarrierConnectionMutationInput!) {
    create_carrier_connection(input: $data) {
        connection { id carrier_id }
        errors { field messages }
    }
}
"""

PARTIAL_SHIPMENT_UPDATE_MUTATION = """
mutation PartialShipmentUpdate($data: PartialShipmentMutationInput!) {
    partial_shipment_update(input: $data) {
        shipment { id status }
        errors { field messages }
    }
}
"""

CREATE_ORDER_MUTATION = """
mutation CreateOrder($data: CreateOrderMutationInput!) {
    create_order(input: $data) {
        order { id }
        errors { field messages }
    }
}
"""


class TestDataIsolation(GraphTestCase):
    def setUp(self):
        super().setUp()

        self.user2 = get_user_model().objects.create_user(
            email="admin2@example.com", password="test123"
        )
        self.token2 = Token.objects.create(user=self.user2, test_mode=False)

        # Create Org 1 with User 1
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        org1_response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "Organization 1"}},
        )
        self.assertResponseNoErrors(org1_response)
        self.org1 = org1_response.data["data"]["create_organization"]["organization"]

        # Create Org 2 with User 2
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        org2_response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "Organization 2"}},
        )
        self.assertResponseNoErrors(org2_response)
        self.org2 = org2_response.data["data"]["create_organization"]["organization"]

        # Re-authenticate as User 1 for tests
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")


class TestCarrierDataIsolation(TestDataIsolation):
    def setUp(self):
        super().setUp()
        # Create carrier for Org 1
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        carrier1_response = self.query(
            CREATE_CARRIER_CONNECTION_MUTATION,
            variables={
                "data": {
                    "carrier_name": "sendle",
                    "carrier_id": "sendle",
                    "credentials": {"sendle_id": "test", "api_key": "test"},
                }
            },
        )
        self.assertResponseNoErrors(carrier1_response)
        self.org1_carrier = carrier1_response.data["data"]["create_carrier_connection"]["connection"]

        # Create carrier for Org 2
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        carrier2_response = self.query(
            CREATE_CARRIER_CONNECTION_MUTATION,
            variables={
                "data": {
                    "carrier_name": "canadapost",
                    "carrier_id": "canadapost",
                    "credentials": {
                        "username": "test",
                        "password": "test",
                        "customer_number": "test",
                        "contract_id": "test",
                    },
                }
            },
        )
        self.assertResponseNoErrors(carrier2_response)
        self.org2_carrier = carrier2_response.data["data"]["create_carrier_connection"]["connection"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_carrier_query_isolation(self):
        response = self.query("{ user_connections { edges { node { id carrier_id } } } }")
        self.assertResponseNoErrors(response)
        carriers = response.data["data"]["user_connections"]["edges"]
        self.assertIn(self.org1_carrier["id"], [c["node"]["id"] for c in carriers])

    def test_carrier_query_isolation_org2(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        response = self.query("{ user_connections { edges { node { id carrier_id } } } }")
        self.assertResponseNoErrors(response)
        carriers = response.data["data"]["user_connections"]["edges"]
        self.assertIn(self.org2_carrier["id"], [c["node"]["id"] for c in carriers])


class TestShipmentDataIsolation(TestDataIsolation, APITestCase):
    def setUp(self):
        super().setUp()
        # Create shipment for Org 1
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.post(reverse("karrio.server.manager:shipment-list"), SHIPMENT_DATA("shipper", "recipient"))
        self.assertEqual(response.status_code, 201)
        self.org1_shipment = response.data

        # Create shipment for Org 2
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        response = self.client.post(reverse("karrio.server.manager:shipment-list"), SHIPMENT_DATA("shipper2", "recipient2"))
        self.assertEqual(response.status_code, 201)
        self.org2_shipment = response.data

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")


class TestOrderDataIsolation(TestDataIsolation):
    def setUp(self):
        super().setUp()
        # Create order for Org 1
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        order1_response = self.query(
            CREATE_ORDER_MUTATION,
            variables={"data": ORDER_DATA("order1")},
        )
        self.assertResponseNoErrors(order1_response)
        self.org1_order = order1_response.data["data"]["create_order"]["order"]

        # Create order for Org 2
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        order2_response = self.query(
            CREATE_ORDER_MUTATION,
            variables={"data": ORDER_DATA("order2")},
        )
        self.assertResponseNoErrors(order2_response)
        self.org2_order = order2_response.data["data"]["create_order"]["order"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_order_query_isolation(self):
        response = self.query("{ orders { edges { node { id } } } }")
        self.assertResponseNoErrors(response)
        orders = response.data["data"]["orders"]["edges"]
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0]["node"]["id"], self.org1_order["id"])

    def test_same_order_id_different_orgs_allowed(self):
        # Create order with same order_id in Org 2 (should succeed since different org)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        response = self.query(
            CREATE_ORDER_MUTATION,
            variables={"data": ORDER_DATA("order1")},  # Same order_id as org1
        )
        self.assertResponseNoErrors(response)
        
        # Verify both orgs now have an order with order_id "order1"
        # Check Org 1
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        org1_response = self.query("{ orders { edges { node { id order_id } } } }")
        self.assertResponseNoErrors(org1_response)
        org1_orders = org1_response.data["data"]["orders"]["edges"]
        self.assertEqual(len(org1_orders), 1)
        self.assertEqual(org1_orders[0]["node"]["order_id"], "order1")
        
        # Check Org 2  
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        org2_response = self.query("{ orders { edges { node { id order_id } } } }")
        self.assertResponseNoErrors(org2_response)
        org2_orders = org2_response.data["data"]["orders"]["edges"]
        self.assertEqual(len(org2_orders), 2)  # order1 and order2
        order_ids = [order["node"]["order_id"] for order in org2_orders]
        self.assertIn("order1", order_ids)
        self.assertIn("order2", order_ids)

    def test_duplicate_order_same_org_rest_api_prevented(self):
        # Test REST API collision detection within same organization
        from django.urls import reverse
        from rest_framework import status
        import json

        url = reverse("karrio.server.orders:order-list")
        order_data = {
            "order_id": "rest_collision_test",
            "source": "shopify",
            "shipping_to": {
                "company_name": "recipient",
                "address_line1": "456 Oak Ave", 
                "city": "Somewhere",
                "postal_code": "67890",
                "country_code": "US",
            },
            "line_items": [{"sku": "item1", "quantity": 1, "weight": 1, "weight_unit": "KG"}],
        }

        # Create first order in Org 1 via REST API
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response1 = self.client.post(url, order_data)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # Attempt to create duplicate order in same org (should fail)
        response2 = self.client.post(url, order_data)
        self.assertEqual(response2.status_code, status.HTTP_409_CONFLICT)

        # Create order with same order_id + source in different org (should succeed)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        response3 = self.client.post(url, order_data)
        self.assertEqual(response3.status_code, status.HTTP_201_CREATED)

        # Attempt duplicate in Org 2 (should fail)
        response4 = self.client.post(url, order_data)
        self.assertEqual(response4.status_code, status.HTTP_409_CONFLICT)


class TestWebhookDataIsolation(TestDataIsolation, APITestCase):
    def setUp(self):
        super().setUp()
        # Create webhook for Org 1
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.post(reverse("karrio.server.events:webhook-list"), WEBHOOK_DATA("https://org1.com"))
        self.assertEqual(response.status_code, 201)
        self.org1_webhook = response.data

        # Create webhook for Org 2
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        response = self.client.post(reverse("karrio.server.events:webhook-list"), WEBHOOK_DATA("https://org2.com"))
        self.assertEqual(response.status_code, 201)
        self.org2_webhook = response.data

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_webhook_query_isolation(self):
        response = self.query("{ webhooks { edges { node { id } } } }")
        self.assertResponseNoErrors(response)
        webhooks = response.data["data"]["webhooks"]["edges"]
        self.assertEqual(len(webhooks), 1)
        self.assertEqual(webhooks[0]["node"]["id"], self.org1_webhook["id"])


# Helpers for test data
def SHIPMENT_DATA(shipper, recipient):
    return {
        "shipper": {
            "company_name": shipper,
            "address_line1": "123 Main St",
            "city": "Anytown",
            "postal_code": "12345",
            "country_code": "US",
        },
        "recipient": {
            "company_name": recipient,
            "address_line1": "456 Oak Ave",
            "city": "Somewhere",
            "postal_code": "67890",
            "country_code": "US",
        },
        "parcels": [{"weight": 1, "weight_unit": "KG"}],
    }

def ORDER_DATA(order_id):
    return {
        "order_id": order_id,
        "shipping_to": {
            "company_name": "recipient",
            "address_line1": "456 Oak Ave",
            "city": "Somewhere",
            "postal_code": "67890",
            "country_code": "US",
        },
        "line_items": [{"sku": "item1", "quantity": 1, "weight": 1, "weight_unit": "KG"}],
    }

def WEBHOOK_DATA(url):
    return {
        "url": url,
        "enabled_events": ["shipment_purchased", "shipment_cancelled"],
    }

DHL_EXPRESS_PAYLOAD = {
    "carrier_name": "dhl_express",
    "carrier_id": "dhl_express",
    "credentials": {
        "site_id": "test_site_id",
        "password": "test_password",
        "account_number": "123456789",
    },
}
