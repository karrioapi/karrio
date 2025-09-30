from unittest.mock import ANY
import karrio.server.automation.models as models
import karrio.server.automation.tests.base as base


class TestShippingRulesGraphQL(base.WorkflowTestCase):
    """Test GraphQL CRUD operations for shipping rules."""

    def setUp(self):
        super().setUp()
        # Create test shipping rule with correct field names
        self.shipping_rule = models.ShippingRule.objects.create(
            name="Test US Cheapest Rule",
            slug="test_us_cheapest_rule",
            description="Select cheapest rate for US destinations",
            priority=1,
            is_active=True,
            conditions={"destination": {"country_code": "US"}, "weight": {"max": 50}},
            actions={"select_service": {"strategy": "cheapest"}},
            metadata={"created_for": "testing"},
            created_by=self.user,
        )

    def test_query_shipping_rules_list(self):
        """Test querying list of shipping rules."""
        response = self.query(
            """
            query GetShippingRules($filter: ShippingRuleFilter) {
              shipping_rules(filter: $filter) {
                edges {
                  node {
                    id
                    name
                    slug
                    description
                    priority
                    is_active
                    conditions {
                      destination {
                        country_code
                      }
                      weight {
                        max
                      }
                    }
                    actions {
                      select_service {
                        strategy
                      }
                    }
                  }
                }
              }
            }
            """,
            variables={"filter": {"first": 10}},
        )

        expected_response = {
            "data": {
                "shipping_rules": {
                    "edges": [
                        {
                            "node": {
                                "id": self.shipping_rule.id,
                                "name": "Test US Cheapest Rule",
                                "slug": "test_us_cheapest_rule",
                                "description": "Select cheapest rate for US destinations",
                                "priority": 1,
                                "is_active": True,
                                "conditions": {
                                    "destination": {"country_code": "US"},
                                    "weight": {"max": 50},
                                },
                                "actions": {"select_service": {"strategy": "cheapest"}},
                            }
                        }
                    ]
                }
            }
        }

        self.assertDictEqual(response.data, expected_response)

    def test_query_single_shipping_rule(self):
        """Test querying a single shipping rule by ID."""
        response = self.query(
            """
            query GetShippingRule($id: String!) {
              shipping_rule(id: $id) {
                id
                name
                slug
                description
                priority
                is_active
                conditions {
                  destination {
                    country_code
                  }
                  weight {
                    max
                  }
                }
                actions {
                  select_service {
                    strategy
                  }
                }
                metadata
              }
            }
            """,
            variables={"id": self.shipping_rule.id},
        )

        expected_response = {
            "data": {
                "shipping_rule": {
                    "id": self.shipping_rule.id,
                    "name": "Test US Cheapest Rule",
                    "slug": "test_us_cheapest_rule",
                    "description": "Select cheapest rate for US destinations",
                    "priority": 1,
                    "is_active": True,
                    "conditions": {
                        "destination": {"country_code": "US"},
                        "weight": {"max": 50},
                    },
                    "actions": {"select_service": {"strategy": "cheapest"}},
                    "metadata": {"created_for": "testing"},
                }
            }
        }

        self.assertDictEqual(response.data, expected_response)

    def test_create_basic_shipping_rule(self):
        """Test creating a basic shipping rule."""
        response = self.query(
            """
            mutation CreateShippingRule($data: CreateShippingRuleMutationInput!) {
              create_shipping_rule(input: $data) {
                shipping_rule {
                  id
                  name
                  slug
                  priority
                  is_active
                  conditions {
                    destination {
                      country_code
                    }
                  }
                  actions {
                    select_service {
                      strategy
                    }
                  }
                }
              }
            }
            """,
            variables={
                "data": {
                    "name": "Canada Express Rule",
                    "description": "Select fastest service for Canada",
                    "priority": 2,
                    "conditions": {"destination": {"country_code": "CA"}},
                    "actions": {"select_service": {"strategy": "fastest"}},
                    "is_active": True,
                }
            },
        )

        expected_response = {
            "data": {
                "create_shipping_rule": {
                    "shipping_rule": {
                        "id": ANY,
                        "name": "Canada Express Rule",
                        "slug": ANY,
                        "priority": 2,
                        "is_active": True,
                        "conditions": {"destination": {"country_code": "CA"}},
                        "actions": {"select_service": {"strategy": "fastest"}},
                    }
                }
            }
        }

        self.assertDictEqual(response.data, expected_response)

    def test_create_shipstation_style_weight_rule(self):
        """Test creating ShipStation-style weight threshold rule."""
        response = self.query(
            """
            mutation CreateShippingRule($data: CreateShippingRuleMutationInput!) {
              create_shipping_rule(input: $data) {
                shipping_rule {
                  id
                  name
                  conditions {
                    weight {
                      max
                    }
                    destination {
                      country_code
                    }
                  }
                  actions {
                    select_service {
                      carrier_code
                      service_code
                    }
                  }
                }
              }
            }
            """,
            variables={
                "data": {
                    "name": "USPS First Class Under 1lb",
                    "priority": 1,
                    "conditions": {
                        "destination": {"country_code": "US"},
                        "weight": {"max": 1.0},
                    },
                    "actions": {
                        "select_service": {
                            "carrier_code": "usps",
                            "service_code": "usps_first_class",
                        }
                    },
                }
            },
        )

        expected_response = {
            "data": {
                "create_shipping_rule": {
                    "shipping_rule": {
                        "id": ANY,
                        "name": "USPS First Class Under 1lb",
                        "conditions": {
                            "weight": {"max": 1.0},
                            "destination": {"country_code": "US"},
                        },
                        "actions": {
                            "select_service": {
                                "carrier_code": "usps",
                                "service_code": "usps_first_class",
                            }
                        },
                    }
                }
            }
        }

        self.assertDictEqual(response.data, expected_response)

    def test_create_rule_with_rate_comparison(self):
        """Test creating rule with rate comparison conditions."""
        response = self.query(
            """
            mutation CreateShippingRule($data: CreateShippingRuleMutationInput!) {
              create_shipping_rule(input: $data) {
                shipping_rule {
                  id
                  name
                  conditions {
                    destination {
                      country_code
                    }
                    rate_comparison {
                      compare
                      operator
                      value
                    }
                  }
                  actions {
                    select_service {
                      carrier_code
                    }
                  }
                }
              }
            }
            """,
            variables={
                "data": {
                    "name": "UPS for Expensive Shipments",
                    "priority": 3,
                    "conditions": {
                        "destination": {"country_code": "US"},
                        "rate_comparison": {
                            "compare": "total_charge",
                            "operator": "gte",
                            "value": 150.0,
                        },
                    },
                    "actions": {"select_service": {"carrier_code": "ups"}},
                }
            },
        )

        expected_response = {
            "data": {
                "create_shipping_rule": {
                    "shipping_rule": {
                        "id": ANY,
                        "name": "UPS for Expensive Shipments",
                        "conditions": {
                            "destination": {"country_code": "US"},
                            "rate_comparison": {
                                "compare": "total_charge",
                                "operator": "gte",
                                "value": 150.0,
                            },
                        },
                        "actions": {"select_service": {"carrier_code": "ups"}},
                    }
                }
            }
        }

        self.assertDictEqual(response.data, expected_response)

    def test_update_shipping_rule(self):
        """Test updating an existing shipping rule."""
        response = self.query(
            """
            mutation UpdateShippingRule($data: UpdateShippingRuleMutationInput!) {
              update_shipping_rule(input: $data) {
                shipping_rule {
                  id
                  name
                  priority
                  is_active
                }
              }
            }
            """,
            variables={
                "data": {
                    "id": self.shipping_rule.id,
                    "name": "Updated US Cheapest Rule",
                    "priority": 5,
                    "is_active": False,
                }
            },
        )

        expected_response = {
            "data": {
                "update_shipping_rule": {
                    "shipping_rule": {
                        "id": self.shipping_rule.id,
                        "name": "Updated US Cheapest Rule",
                        "priority": 5,
                        "is_active": False,
                    }
                }
            }
        }

        self.assertDictEqual(response.data, expected_response)

    def test_delete_shipping_rule(self):
        """Test deleting a shipping rule."""
        response = self.query(
            """
            mutation DeleteShippingRule($data: DeleteMutationInput!) {
              delete_shipping_rule(input: $data) {
                id
              }
            }
            """,
            variables={"data": {"id": self.shipping_rule.id}},
        )

        expected_response = {
            "data": {"delete_shipping_rule": {"id": self.shipping_rule.id}}
        }

        self.assertDictEqual(response.data, expected_response)
        # Verify rule is deleted
        self.assertFalse(
            models.ShippingRule.objects.filter(id=self.shipping_rule.id).exists()
        )
