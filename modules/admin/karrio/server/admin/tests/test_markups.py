from unittest.mock import ANY
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase as BaseAPITestCase, APIClient
from karrio.server.admin.tests.base import AdminGraphTestCase
from karrio.server.user.models import Token
import karrio.server.providers.models as providers

class TestAdminMarkups(AdminGraphTestCase):
    """Tests for Admin Markup CRUD operations including meta field."""

    def setUp(self):
        super().setUp()
        import karrio.server.pricing.models as pricing

        self.pricing = pricing

        # Create a test markup with meta field
        self.markup = pricing.Markup.objects.create(
            name="Brokerage Fee - Scale",
            amount=0.85,
            markup_type="PERCENTAGE",
            active=True,
            is_visible=True,
            meta={
                "type": "brokerage-fee",
                "plan": "scale",
                "show_in_preview": True,
            },
            metadata={"notes": "Default brokerage fee"},
        )

    def test_query_markups(self):
        """Test querying all markups through admin API."""
        response = self.query(
            """
            query get_markups {
              markups {
                edges {
                  node {
                    id
                    name
                    active
                    amount
                    markup_type
                    is_visible
                    meta
                    metadata
                    carrier_codes
                    service_codes
                    connection_ids
                  }
                }
              }
            }
            """,
            operation_name="get_markups",
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["markups"]["edges"]
        self.assertEqual(len(edges), 1)

        node = edges[0]["node"]
        self.assertEqual(node["name"], "Brokerage Fee - Scale")
        self.assertEqual(node["amount"], 0.85)
        self.assertEqual(node["markup_type"], "PERCENTAGE")
        self.assertTrue(node["active"])
        self.assertTrue(node["is_visible"])
        self.assertEqual(node["meta"]["type"], "brokerage-fee")
        self.assertEqual(node["meta"]["plan"], "scale")
        self.assertTrue(node["meta"]["show_in_preview"])
        self.assertEqual(node["metadata"]["notes"], "Default brokerage fee")

    def test_query_single_markup(self):
        """Test querying a single markup by ID."""
        response = self.query(
            """
            query get_markup($id: String!) {
              markup(id: $id) {
                id
                name
                amount
                markup_type
                meta
                metadata
              }
            }
            """,
            operation_name="get_markup",
            variables={"id": self.markup.id},
        )

        self.assertResponseNoErrors(response)
        markup = response.data["data"]["markup"]
        self.assertEqual(markup["name"], "Brokerage Fee - Scale")
        self.assertEqual(markup["meta"]["type"], "brokerage-fee")
        self.assertEqual(markup["meta"]["plan"], "scale")

    def test_create_markup_with_meta(self):
        """Test creating a markup with meta field (category, plan, show_in_preview)."""
        response = self.query(
            """
            mutation create_markup($input: CreateMarkupMutationInput!) {
              create_markup(input: $input) {
                errors {
                  field
                  messages
                }
                markup {
                  id
                  name
                  active
                  amount
                  markup_type
                  is_visible
                  meta
                  metadata
                  carrier_codes
                  service_codes
                  connection_ids
                }
              }
            }
            """,
            operation_name="create_markup",
            variables={
                "input": {
                    "name": "Insurance - Basic",
                    "amount": 50.00,
                    "markup_type": "AMOUNT",
                    "active": True,
                    "is_visible": True,
                    "meta": {
                        "type": "insurance",
                        "plan": "basic",
                        "show_in_preview": True,
                    },
                    "metadata": {"coverage": "up to $500"},
                }
            },
        )

        self.assertResponseNoErrors(response)
        result = response.data["data"]["create_markup"]
        self.assertIsNone(result["errors"])

        markup = result["markup"]
        self.assertEqual(markup["name"], "Insurance - Basic")
        self.assertEqual(markup["amount"], 50.00)
        self.assertEqual(markup["markup_type"], "AMOUNT")
        self.assertTrue(markup["active"])
        self.assertTrue(markup["is_visible"])
        self.assertEqual(markup["meta"]["type"], "insurance")
        self.assertEqual(markup["meta"]["plan"], "basic")
        self.assertTrue(markup["meta"]["show_in_preview"])
        self.assertEqual(markup["metadata"]["coverage"], "up to $500")

    def test_create_markup_percentage_type(self):
        """Test creating a percentage-based markup."""
        response = self.query(
            """
            mutation create_markup($input: CreateMarkupMutationInput!) {
              create_markup(input: $input) {
                errors {
                  field
                  messages
                }
                markup {
                  id
                  name
                  amount
                  markup_type
                  meta
                }
              }
            }
            """,
            operation_name="create_markup",
            variables={
                "input": {
                    "name": "Brokerage Fee - Launch",
                    "amount": 1.5,
                    "markup_type": "PERCENTAGE",
                    "meta": {
                        "type": "brokerage-fee",
                        "plan": "launch",
                        "show_in_preview": True,
                    },
                }
            },
        )

        self.assertResponseNoErrors(response)
        markup = response.data["data"]["create_markup"]["markup"]
        self.assertEqual(markup["amount"], 1.5)
        self.assertEqual(markup["markup_type"], "PERCENTAGE")
        self.assertEqual(markup["meta"]["type"], "brokerage-fee")
        self.assertEqual(markup["meta"]["plan"], "launch")

    def test_create_markup_without_meta(self):
        """Test creating a markup without meta field (defaults to empty dict)."""
        response = self.query(
            """
            mutation create_markup($input: CreateMarkupMutationInput!) {
              create_markup(input: $input) {
                errors {
                  field
                  messages
                }
                markup {
                  id
                  name
                  amount
                  markup_type
                  meta
                }
              }
            }
            """,
            operation_name="create_markup",
            variables={
                "input": {
                    "name": "Simple Surcharge",
                    "amount": 5.0,
                    "markup_type": "AMOUNT",
                }
            },
        )

        self.assertResponseNoErrors(response)
        markup = response.data["data"]["create_markup"]["markup"]
        self.assertEqual(markup["name"], "Simple Surcharge")
        # meta should default to empty dict
        self.assertEqual(markup["meta"], {})

    def test_create_markup_with_filters(self):
        """Test creating a markup with carrier/service/connection filters."""
        response = self.query(
            """
            mutation create_markup($input: CreateMarkupMutationInput!) {
              create_markup(input: $input) {
                errors {
                  field
                  messages
                }
                markup {
                  id
                  name
                  amount
                  markup_type
                  carrier_codes
                  service_codes
                  connection_ids
                  meta
                }
              }
            }
            """,
            operation_name="create_markup",
            variables={
                "input": {
                    "name": "DHL Only Surcharge",
                    "amount": 2.0,
                    "markup_type": "AMOUNT",
                    "carrier_codes": ["dhl_express", "dhl_parcel_de"],
                    "service_codes": ["dhl_express_worldwide"],
                    "meta": {
                        "type": "surcharge",
                        "show_in_preview": False,
                    },
                }
            },
        )

        self.assertResponseNoErrors(response)
        markup = response.data["data"]["create_markup"]["markup"]
        self.assertEqual(markup["carrier_codes"], ["dhl_express", "dhl_parcel_de"])
        self.assertEqual(markup["service_codes"], ["dhl_express_worldwide"])
        self.assertEqual(markup["meta"]["type"], "surcharge")
        self.assertFalse(markup["meta"]["show_in_preview"])

    def test_update_markup_meta(self):
        """Test updating a markup's meta field."""
        response = self.query(
            """
            mutation update_markup($input: UpdateMarkupMutationInput!) {
              update_markup(input: $input) {
                errors {
                  field
                  messages
                }
                markup {
                  id
                  name
                  amount
                  markup_type
                  meta
                  metadata
                }
              }
            }
            """,
            operation_name="update_markup",
            variables={
                "input": {
                    "id": self.markup.id,
                    "meta": {
                        "type": "brokerage-fee",
                        "plan": "enterprise",
                        "show_in_preview": False,
                    },
                }
            },
        )

        self.assertResponseNoErrors(response)
        markup = response.data["data"]["update_markup"]["markup"]
        self.assertEqual(markup["meta"]["plan"], "enterprise")
        self.assertFalse(markup["meta"]["show_in_preview"])
        # Original fields should be preserved
        self.assertEqual(markup["name"], "Brokerage Fee - Scale")
        self.assertEqual(markup["amount"], 0.85)

    def test_update_markup_amount_and_type(self):
        """Test updating markup amount and type."""
        response = self.query(
            """
            mutation update_markup($input: UpdateMarkupMutationInput!) {
              update_markup(input: $input) {
                errors {
                  field
                  messages
                }
                markup {
                  id
                  name
                  amount
                  markup_type
                  active
                  is_visible
                }
              }
            }
            """,
            operation_name="update_markup",
            variables={
                "input": {
                    "id": self.markup.id,
                    "amount": 25.0,
                    "markup_type": "AMOUNT",
                    "active": False,
                    "is_visible": False,
                }
            },
        )

        self.assertResponseNoErrors(response)
        markup = response.data["data"]["update_markup"]["markup"]
        self.assertEqual(markup["amount"], 25.0)
        self.assertEqual(markup["markup_type"], "AMOUNT")
        self.assertFalse(markup["active"])
        self.assertFalse(markup["is_visible"])

    def test_update_markup_filters(self):
        """Test updating markup carrier/service filters."""
        response = self.query(
            """
            mutation update_markup($input: UpdateMarkupMutationInput!) {
              update_markup(input: $input) {
                errors {
                  field
                  messages
                }
                markup {
                  id
                  carrier_codes
                  service_codes
                  connection_ids
                }
              }
            }
            """,
            operation_name="update_markup",
            variables={
                "input": {
                    "id": self.markup.id,
                    "carrier_codes": ["ups", "fedex"],
                    "service_codes": ["ups_ground"],
                }
            },
        )

        self.assertResponseNoErrors(response)
        markup = response.data["data"]["update_markup"]["markup"]
        self.assertEqual(markup["carrier_codes"], ["ups", "fedex"])
        self.assertEqual(markup["service_codes"], ["ups_ground"])

    def test_delete_markup(self):
        """Test deleting a markup through admin API."""
        # Create a markup to delete
        to_delete = self.pricing.Markup.objects.create(
            name="To Be Deleted",
            amount=1.0,
            markup_type="AMOUNT",
            meta={"type": "surcharge"},
        )

        response = self.query(
            """
            mutation delete_markup($input: DeleteMutationInput!) {
              delete_markup(input: $input) {
                errors {
                  field
                  messages
                }
                id
              }
            }
            """,
            operation_name="delete_markup",
            variables={"input": {"id": to_delete.id}},
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(
            response.data["data"]["delete_markup"]["id"], to_delete.id
        )
        self.assertFalse(
            self.pricing.Markup.objects.filter(id=to_delete.id).exists()
        )

    def test_query_markups_returns_all(self):
        """Test querying markups returns all markups."""
        # Create a second markup
        self.pricing.Markup.objects.create(
            name="Inactive Fee",
            amount=3.0,
            markup_type="AMOUNT",
            active=False,
            meta={"type": "notification"},
        )

        response = self.query(
            """
            query get_markups {
              markups {
                edges {
                  node {
                    id
                    name
                    active
                    markup_type
                    meta
                  }
                }
              }
            }
            """,
            operation_name="get_markups",
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["markups"]["edges"]
        self.assertEqual(len(edges), 2)
        names = {e["node"]["name"] for e in edges}
        self.assertIn("Brokerage Fee - Scale", names)
        self.assertIn("Inactive Fee", names)

    def test_filter_markups_by_meta_key_value(self):
        """Test filtering markups by generic meta key/value."""
        self.pricing.Markup.objects.create(
            name="Insurance Fee",
            amount=5.0,
            markup_type="AMOUNT",
            active=True,
            meta={"type": "insurance", "plan": "pro"},
        )
        self.pricing.Markup.objects.create(
            name="Notification Fee",
            amount=0.5,
            markup_type="AMOUNT",
            active=True,
            meta={"type": "notification"},
        )

        response = self.query(
            """
            query get_markups($filter: MarkupFilter) {
              markups(filter: $filter) {
                edges {
                  node {
                    id
                    name
                    meta
                  }
                }
              }
            }
            """,
            operation_name="get_markups",
            variables={"filter": {"meta_key": "type", "meta_value": "insurance"}},
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["markups"]["edges"]
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0]["node"]["name"], "Insurance Fee")
        self.assertEqual(edges[0]["node"]["meta"]["type"], "insurance")

    def test_filter_markups_by_meta_plan(self):
        """Test filtering markups by meta plan using generic key/value."""
        self.pricing.Markup.objects.create(
            name="Pro Brokerage",
            amount=2.0,
            markup_type="PERCENTAGE",
            active=True,
            meta={"type": "brokerage-fee", "plan": "pro"},
        )
        self.pricing.Markup.objects.create(
            name="Enterprise Brokerage",
            amount=1.5,
            markup_type="PERCENTAGE",
            active=True,
            meta={"type": "brokerage-fee", "plan": "enterprise"},
        )

        response = self.query(
            """
            query get_markups($filter: MarkupFilter) {
              markups(filter: $filter) {
                edges {
                  node {
                    id
                    name
                    meta
                  }
                }
              }
            }
            """,
            operation_name="get_markups",
            variables={"filter": {"meta_key": "plan", "meta_value": "enterprise"}},
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["markups"]["edges"]
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0]["node"]["name"], "Enterprise Brokerage")
        self.assertEqual(edges[0]["node"]["meta"]["plan"], "enterprise")

    def test_filter_markups_by_meta_key_only(self):
        """Test filtering markups by meta key existence (no value)."""
        self.pricing.Markup.objects.create(
            name="Has Plan",
            amount=2.0,
            markup_type="PERCENTAGE",
            active=True,
            meta={"type": "brokerage-fee", "plan": "pro"},
        )
        self.pricing.Markup.objects.create(
            name="No Plan",
            amount=0.5,
            markup_type="AMOUNT",
            active=True,
            meta={"type": "notification"},
        )

        response = self.query(
            """
            query get_markups($filter: MarkupFilter) {
              markups(filter: $filter) {
                edges {
                  node {
                    id
                    name
                    meta
                  }
                }
              }
            }
            """,
            operation_name="get_markups",
            variables={"filter": {"meta_key": "plan"}},
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["markups"]["edges"]
        # setUp markup has plan="scale", plus "Has Plan" with plan="pro"
        names = {e["node"]["name"] for e in edges}
        self.assertIn("Has Plan", names)
        self.assertIn("Brokerage Fee - Scale", names)
        self.assertNotIn("No Plan", names)

    def test_filter_markups_by_metadata_key_value(self):
        """Test filtering markups by generic metadata key/value."""
        self.pricing.Markup.objects.create(
            name="With Coverage",
            amount=50.0,
            markup_type="AMOUNT",
            active=True,
            metadata={"coverage": "up to $500"},
        )
        self.pricing.Markup.objects.create(
            name="With Region",
            amount=3.0,
            markup_type="AMOUNT",
            active=True,
            metadata={"region": "north-america"},
        )

        response = self.query(
            """
            query get_markups($filter: MarkupFilter) {
              markups(filter: $filter) {
                edges {
                  node {
                    id
                    name
                    metadata
                  }
                }
              }
            }
            """,
            operation_name="get_markups",
            variables={"filter": {"metadata_key": "coverage", "metadata_value": "up to $500"}},
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["markups"]["edges"]
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0]["node"]["name"], "With Coverage")

    def test_filter_markups_by_meta_value_icontains(self):
        """Test that meta_value uses case-insensitive partial matching."""
        self.pricing.Markup.objects.create(
            name="Brokerage Pro",
            amount=2.0,
            markup_type="PERCENTAGE",
            active=True,
            meta={"type": "brokerage-fee", "plan": "Pro-Enterprise"},
        )

        # Search with partial lowercase value
        response = self.query(
            """
            query get_markups($filter: MarkupFilter) {
              markups(filter: $filter) {
                edges {
                  node {
                    id
                    name
                    meta
                  }
                }
              }
            }
            """,
            operation_name="get_markups",
            variables={"filter": {"meta_key": "plan", "meta_value": "enterprise"}},
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["markups"]["edges"]
        names = {e["node"]["name"] for e in edges}
        self.assertIn("Brokerage Pro", names)

    def test_filter_markups_by_metadata_value_icontains(self):
        """Test that metadata_value uses case-insensitive partial matching."""
        self.pricing.Markup.objects.create(
            name="Regional Fee",
            amount=3.0,
            markup_type="AMOUNT",
            active=True,
            metadata={"region": "North-America"},
        )

        response = self.query(
            """
            query get_markups($filter: MarkupFilter) {
              markups(filter: $filter) {
                edges {
                  node {
                    id
                    name
                    metadata
                  }
                }
              }
            }
            """,
            operation_name="get_markups",
            variables={"filter": {"metadata_key": "region", "metadata_value": "north"}},
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["markups"]["edges"]
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0]["node"]["name"], "Regional Fee")

    def test_filter_markups_by_active(self):
        """Test filtering markups by active status."""
        self.pricing.Markup.objects.create(
            name="Inactive Surcharge",
            amount=3.0,
            markup_type="AMOUNT",
            active=False,
            meta={"type": "surcharge"},
        )

        response = self.query(
            """
            query get_markups($filter: MarkupFilter) {
              markups(filter: $filter) {
                edges {
                  node {
                    id
                    name
                    active
                  }
                }
              }
            }
            """,
            operation_name="get_markups",
            variables={"filter": {"active": True}},
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["markups"]["edges"]
        for edge in edges:
            self.assertTrue(edge["node"]["active"])

    def test_filter_markups_by_markup_type(self):
        """Test filtering markups by markup_type."""
        self.pricing.Markup.objects.create(
            name="Flat Fee",
            amount=10.0,
            markup_type="AMOUNT",
            active=True,
        )

        response = self.query(
            """
            query get_markups($filter: MarkupFilter) {
              markups(filter: $filter) {
                edges {
                  node {
                    id
                    name
                    markup_type
                  }
                }
              }
            }
            """,
            operation_name="get_markups",
            variables={"filter": {"markup_type": "PERCENTAGE"}},
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["markups"]["edges"]
        for edge in edges:
            self.assertEqual(edge["node"]["markup_type"], "PERCENTAGE")

    def test_filter_markups_combined(self):
        """Test combining meta key/value and active filters."""
        self.pricing.Markup.objects.create(
            name="Active Insurance",
            amount=5.0,
            markup_type="AMOUNT",
            active=True,
            meta={"type": "insurance"},
        )
        self.pricing.Markup.objects.create(
            name="Inactive Insurance",
            amount=3.0,
            markup_type="AMOUNT",
            active=False,
            meta={"type": "insurance"},
        )

        response = self.query(
            """
            query get_markups($filter: MarkupFilter) {
              markups(filter: $filter) {
                edges {
                  node {
                    id
                    name
                    active
                    meta
                  }
                }
              }
            }
            """,
            operation_name="get_markups",
            variables={"filter": {"meta_key": "type", "meta_value": "insurance", "active": True}},
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["markups"]["edges"]
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0]["node"]["name"], "Active Insurance")
        self.assertTrue(edges[0]["node"]["active"])
        self.assertEqual(edges[0]["node"]["meta"]["type"], "insurance")

    def test_create_markup_all_meta_categories(self):
        """Test creating markups for each meta category type."""
        categories = [
            ("brokerage-fee", "Brokerage Fee - Pro", "PERCENTAGE", 1.2),
            ("insurance", "Coverage - Premium", "AMOUNT", 100.0),
            ("surcharge", "Handling Surcharge", "AMOUNT", 3.50),
            ("notification", "SMS Notification", "AMOUNT", 0.50),
            ("address-validation", "Address Validation", "AMOUNT", 1.00),
        ]

        for meta_type, name, markup_type, amount in categories:
            response = self.query(
                """
                mutation create_markup($input: CreateMarkupMutationInput!) {
                  create_markup(input: $input) {
                    errors {
                      field
                      messages
                    }
                    markup {
                      id
                      name
                      meta
                    }
                  }
                }
                """,
                operation_name="create_markup",
                variables={
                    "input": {
                        "name": name,
                        "amount": amount,
                        "markup_type": markup_type,
                        "meta": {
                            "type": meta_type,
                            "show_in_preview": True,
                        },
                    }
                },
            )

            self.assertResponseNoErrors(response)
            markup = response.data["data"]["create_markup"]["markup"]
            self.assertEqual(markup["name"], name)
            self.assertEqual(markup["meta"]["type"], meta_type)


class TestMarkupFeatureGating(BaseAPITestCase):
    """Tests for feature-gated markup applicability logic."""

    def setUp(self):
        super().setUp()
        import karrio.server.pricing.models as pricing
        import karrio.server.core.datatypes as datatypes
        import karrio.core.models as karrio_models

        self.pricing = pricing
        self.datatypes = datatypes
        self.karrio_models = karrio_models

        # Create feature-gated markups (using meta.feature_gate)
        self.insurance_markup = pricing.Markup.objects.create(
            name="Insurance Fee",
            amount=50.0,
            markup_type="AMOUNT",
            active=True,
            is_visible=True,
            meta={"type": "insurance", "feature_gate": "insurance", "show_in_preview": True},
        )
        self.notification_markup = pricing.Markup.objects.create(
            name="Notification Fee",
            amount=2.0,
            markup_type="AMOUNT",
            active=True,
            is_visible=True,
            meta={"type": "notification", "feature_gate": "notification", "show_in_preview": True},
        )
        self.address_validation_markup = pricing.Markup.objects.create(
            name="Address Validation Fee",
            amount=1.5,
            markup_type="AMOUNT",
            active=True,
            is_visible=True,
            meta={"type": "address-validation", "feature_gate": "address_validation", "show_in_preview": True},
        )

        # Create feature-gated surcharge (conditional at runtime, unconditional in CSV preview)
        self.surcharge_markup = pricing.Markup.objects.create(
            name="Fuel Surcharge",
            amount=3.0,
            markup_type="AMOUNT",
            active=True,
            is_visible=True,
            meta={"type": "surcharge", "feature_gate": "fuel_surcharge"},
        )

        # Create unconditional markups (no feature_gate)
        self.brokerage_markup = pricing.Markup.objects.create(
            name="Brokerage Fee",
            amount=0.85,
            markup_type="PERCENTAGE",
            active=True,
            is_visible=True,
            meta={"type": "brokerage-fee", "show_in_preview": True},
        )

        # Helper: build a rate with given meta
        def make_rate(service_features=None, **kwargs):
            meta = {"service_features": service_features or []}
            meta.update(kwargs.get("extra_meta", {}))
            return self.datatypes.Rate(
                carrier_name="generic",
                carrier_id="car_test",
                currency="USD",
                total_charge=100.0,
                service="test_service",
                extra_charges=[],
                meta=meta,
            )

        self.make_rate = make_rate

        # Helper: build a rate response
        def make_response(rates):
            return self.datatypes.RateResponse(
                messages=[],
                rates=rates,
            )

        self.make_response = make_response

    def test_insurance_markup_skips_when_service_lacks_feature(self):
        """Insurance markup should NOT apply when service doesn't have insurance feature."""
        rate = self.make_rate(service_features=["tracked", "express"])
        result = self.insurance_markup._is_applicable(rate, options={"insurance": True})

        self.assertFalse(result)

    def test_insurance_markup_skips_when_option_not_requested(self):
        """Insurance markup should NOT apply when option not in request."""
        rate = self.make_rate(service_features=["insurance", "tracked"])
        result = self.insurance_markup._is_applicable(rate, options={})

        self.assertFalse(result)

    def test_insurance_markup_applies_when_feature_and_option_present(self):
        """Insurance markup should apply when service has feature AND option is requested."""
        rate = self.make_rate(service_features=["insurance", "tracked"])
        result = self.insurance_markup._is_applicable(rate, options={"insurance": True})

        self.assertTrue(result)

    def test_notification_markup_feature_gate(self):
        """Notification markup requires 'notification' feature and option."""
        rate_with = self.make_rate(service_features=["notification"])
        rate_without = self.make_rate(service_features=["tracked"])

        self.assertTrue(self.notification_markup._is_applicable(rate_with, options={"notification": True}))
        self.assertFalse(self.notification_markup._is_applicable(rate_with, options={}))
        self.assertFalse(self.notification_markup._is_applicable(rate_without, options={"notification": True}))

    def test_address_validation_markup_feature_gate(self):
        """Address validation markup requires 'address_validation' feature and option."""
        rate_with = self.make_rate(service_features=["address_validation"])
        rate_without = self.make_rate(service_features=["tracked"])

        result_applies = self.address_validation_markup._is_applicable(
            rate_with, options={"address_validation": True}
        )
        result_no_feature = self.address_validation_markup._is_applicable(
            rate_without, options={"address_validation": True}
        )

        self.assertTrue(result_applies)
        self.assertFalse(result_no_feature)

    def test_brokerage_markup_always_applies(self):
        """Brokerage-fee markup should always apply regardless of features/options."""
        rate = self.make_rate(service_features=[])
        result = self.brokerage_markup._is_applicable(rate, options={})

        self.assertTrue(result)

    def test_surcharge_with_feature_gate_is_conditional(self):
        """Surcharge with meta.feature_gate is conditional during live rates."""
        rate_with = self.make_rate(service_features=["fuel_surcharge"])
        rate_without = self.make_rate(service_features=["tracked"])

        result_applies = self.surcharge_markup._is_applicable(
            rate_with, options={"fuel_surcharge": True}
        )
        result_no_feature = self.surcharge_markup._is_applicable(
            rate_without, options={"fuel_surcharge": True}
        )
        result_no_option = self.surcharge_markup._is_applicable(
            rate_with, options={}
        )

        self.assertTrue(result_applies)
        self.assertFalse(result_no_feature)
        self.assertFalse(result_no_option)

    def test_surcharge_without_feature_gate_always_applies(self):
        """Surcharge without meta.feature_gate should always apply."""
        unconditional_surcharge = self.pricing.Markup.objects.create(
            name="Unconditional Surcharge",
            amount=2.0,
            markup_type="AMOUNT",
            active=True,
            is_visible=True,
            meta={"type": "surcharge"},
        )
        rate = self.make_rate(service_features=[])
        result = unconditional_surcharge._is_applicable(rate, options={})

        self.assertTrue(result)

    def test_apply_charge_passes_options(self):
        """apply_charge should pass options to _is_applicable for feature-gating."""
        rate = self.make_rate(service_features=["insurance"])
        response = self.make_response([rate])

        # Without insurance option: markup should not be applied
        result_without = self.insurance_markup.apply_charge(response, options={})
        self.assertEqual(result_without.rates[0].total_charge, 100.0)

        # With insurance option: markup should be applied
        result_with = self.insurance_markup.apply_charge(response, options={"insurance": True})
        self.assertEqual(result_with.rates[0].total_charge, 150.0)

    def test_brokerage_apply_charge_ignores_options(self):
        """Brokerage markup should apply regardless of options."""
        rate = self.make_rate(service_features=[])
        response = self.make_response([rate])

        result = self.brokerage_markup.apply_charge(response, options={})
        # 100.0 * 0.85% = 0.85, total = 100.85
        self.assertEqual(result.rates[0].total_charge, 100.85)

    def test_markup_without_feature_gate_always_applies(self):
        """A markup with no meta.feature_gate should always apply (unconditional)."""
        no_gate_markup = self.pricing.Markup.objects.create(
            name="Generic Markup",
            amount=5.0,
            markup_type="AMOUNT",
            active=True,
            is_visible=True,
            meta={"type": "insurance"},  # has type but no feature_gate
        )
        rate = self.make_rate(service_features=[])
        result = no_gate_markup._is_applicable(rate, options={})

        self.assertTrue(result)
