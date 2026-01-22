import karrio.lib as lib
from unittest.mock import ANY
from karrio.server.graph.tests.base import GraphTestCase
import karrio.server.providers.models as providers


class TestRateSheets(GraphTestCase):
    """Tests for Rate Sheet CRUD operations."""

    def setUp(self):
        super().setUp()

        # Create a test rate sheet with shared zones and surcharges
        self.rate_sheet = providers.RateSheet.objects.create(
            name="Test Rate Sheet",
            carrier_name="ups",
            slug="test_rate_sheet",
            zones=[
                {
                    "id": "zone_1",
                    "label": "Zone 1",
                    "cities": ["New York", "Los Angeles"],
                    "country_codes": ["US"],
                }
            ],
            surcharges=[
                {
                    "id": "surch_fuel",
                    "name": "Fuel Surcharge",
                    "amount": 10.0,
                    "surcharge_type": "percentage",
                    "active": True,
                }
            ],
            service_rates=[
                {
                    "service_id": None,  # Will be set after service creation
                    "zone_id": "zone_1",
                    "rate": 10.00,
                    "cost": 8.00,
                }
            ],
            created_by=self.user,
        )

        # Create a test service
        self.service = providers.ServiceLevel.objects.create(
            service_name="UPS Standard",
            service_code="ups_standard",
            carrier_service_code="11",
            currency="USD",
            active=True,
            zone_ids=["zone_1"],
            surcharge_ids=["surch_fuel"],
            created_by=self.user,
        )
        self.rate_sheet.services.add(self.service)

        # Update service_rates with actual service ID
        self.rate_sheet.service_rates = [
            {
                "service_id": self.service.id,
                "zone_id": "zone_1",
                "rate": 10.00,
                "cost": 8.00,
            }
        ]
        self.rate_sheet.save()

    # =========================================================================
    # RATE SHEET QUERY TESTS
    # =========================================================================

    def test_query_rate_sheets(self):
        """Test querying all rate sheets with zones, surcharges, and service_rates."""
        response = self.query(
            """
            query get_rate_sheets {
              rate_sheets {
                edges {
                  node {
                    id
                    name
                    carrier_name
                    slug
                    zones {
                      id
                      label
                      cities
                      country_codes
                      min_weight
                      max_weight
                      weight_unit
                    }
                    surcharges {
                      id
                      name
                      amount
                      surcharge_type
                      active
                    }
                    service_rates {
                      service_id
                      zone_id
                      rate
                      cost
                    }
                    services {
                      id
                      service_name
                      service_code
                      carrier_service_code
                      active
                      currency
                      zone_ids
                      surcharge_ids
                    }
                  }
                }
              }
            }
            """,
            operation_name="get_rate_sheets",
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            lib.to_dict(response_data, clear_empty=False),
            RATE_SHEETS_RESPONSE,
        )

    def test_query_single_rate_sheet(self):
        """Test querying a single rate sheet by ID."""
        response = self.query(
            """
            query get_rate_sheet($id: String!) {
              rate_sheet(id: $id) {
                id
                name
                carrier_name
                zones {
                  id
                  label
                }
                surcharges {
                  id
                  name
                }
                services {
                  id
                  service_name
                }
              }
            }
            """,
            operation_name="get_rate_sheet",
            variables={"id": self.rate_sheet.id},
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(response.data["data"]["rate_sheet"]["name"], "Test Rate Sheet")
        self.assertEqual(response.data["data"]["rate_sheet"]["carrier_name"], "ups")

    def test_query_rate_sheet_not_found(self):
        """Test querying a rate sheet that doesn't exist."""
        response = self.query(
            """
            query get_rate_sheet($id: String!) {
              rate_sheet(id: $id) {
                id
                name
              }
            }
            """,
            operation_name="get_rate_sheet",
            variables={"id": "rsht_nonexistent"},
        )

        self.assertResponseNoErrors(response)
        self.assertIsNone(response.data["data"]["rate_sheet"])

    # =========================================================================
    # RATE SHEET CREATE TESTS
    # =========================================================================

    def test_create_rate_sheet(self):
        """Test creating a new rate sheet with services."""
        response = self.query(
            """
            mutation create_rate_sheet($data: CreateRateSheetMutationInput!) {
              create_rate_sheet(input: $data) {
                rate_sheet {
                  id
                  name
                  carrier_name
                  zones {
                    id
                    label
                    postal_codes
                  }
                  surcharges {
                    id
                    name
                    amount
                    surcharge_type
                  }
                  services {
                    id
                    service_name
                    service_code
                    currency
                    zone_ids
                    surcharge_ids
                  }
                }
              }
            }
            """,
            operation_name="create_rate_sheet",
            variables=CREATE_RATE_SHEET_DATA,
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response_data, CREATE_RATE_SHEET_RESPONSE)

    def test_create_rate_sheet_minimal(self):
        """Test creating a rate sheet with only required fields."""
        response = self.query(
            """
            mutation create_rate_sheet($data: CreateRateSheetMutationInput!) {
              create_rate_sheet(input: $data) {
                rate_sheet {
                  id
                  name
                  carrier_name
                  zones {
                    id
                  }
                  surcharges {
                    id
                  }
                  services {
                    id
                  }
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="create_rate_sheet",
            variables={
                "data": {
                    "name": "Minimal Rate Sheet",
                    "carrier_name": "generic",
                }
            },
        )

        self.assertResponseNoErrors(response)
        rate_sheet = response.data["data"]["create_rate_sheet"]["rate_sheet"]
        self.assertEqual(rate_sheet["name"], "Minimal Rate Sheet")
        self.assertEqual(rate_sheet["zones"], [])
        self.assertEqual(rate_sheet["surcharges"], [])
        self.assertEqual(rate_sheet["services"], [])

    # =========================================================================
    # RATE SHEET UPDATE TESTS
    # =========================================================================

    def test_update_rate_sheet(self):
        """Test updating a rate sheet's basic fields."""
        response = self.query(
            """
            mutation update_rate_sheet($data: UpdateRateSheetMutationInput!) {
              update_rate_sheet(input: $data) {
                rate_sheet {
                  id
                  name
                  services {
                    id
                    service_name
                    zone_ids
                  }
                }
              }
            }
            """,
            operation_name="update_rate_sheet",
            variables={
                "data": {
                    "id": self.rate_sheet.id,
                    "name": "Updated Rate Sheet",
                    "services": [
                        {
                            "id": self.service.id,
                            "service_name": "Updated Service",
                            "zone_ids": ["zone_1"],
                        }
                    ],
                },
            },
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            lib.to_dict(response_data),
            UPDATE_RATE_SHEET_RESPONSE,
        )

    def test_update_rate_sheet_name_only(self):
        """Test updating only the rate sheet name."""
        response = self.query(
            """
            mutation update_rate_sheet($data: UpdateRateSheetMutationInput!) {
              update_rate_sheet(input: $data) {
                rate_sheet {
                  id
                  name
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="update_rate_sheet",
            variables={
                "data": {
                    "id": self.rate_sheet.id,
                    "name": "New Name Only",
                }
            },
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(
            response.data["data"]["update_rate_sheet"]["rate_sheet"]["name"],
            "New Name Only"
        )

    # =========================================================================
    # RATE SHEET DELETE TESTS
    # =========================================================================

    def test_delete_rate_sheet(self):
        """Test deleting a rate sheet."""
        # First create a rate sheet to delete
        new_sheet = providers.RateSheet.objects.create(
            name="To Be Deleted",
            carrier_name="ups",
            slug="to_be_deleted",
            created_by=self.user,
        )

        response = self.query(
            """
            mutation delete_rate_sheet($data: DeleteMutationInput!) {
              delete_rate_sheet(input: $data) {
                id
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="delete_rate_sheet",
            variables={
                "data": {
                    "id": new_sheet.id,
                }
            },
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(response.data["data"]["delete_rate_sheet"]["id"], new_sheet.id)

        # Verify it's deleted
        self.assertFalse(providers.RateSheet.objects.filter(id=new_sheet.id).exists())

    def test_delete_rate_sheet_cascades_services(self):
        """Test that deleting a rate sheet also deletes its services."""
        # Create a rate sheet with a service
        sheet = providers.RateSheet.objects.create(
            name="Sheet With Service",
            carrier_name="ups",
            slug="sheet_with_service",
            created_by=self.user,
        )
        service = providers.ServiceLevel.objects.create(
            service_name="Test Service",
            service_code="test_service",
            carrier_service_code="TEST",
            currency="USD",
            created_by=self.user,
        )
        sheet.services.add(service)
        service_id = service.id

        response = self.query(
            """
            mutation delete_rate_sheet($data: DeleteMutationInput!) {
              delete_rate_sheet(input: $data) {
                id
              }
            }
            """,
            operation_name="delete_rate_sheet",
            variables={"data": {"id": sheet.id}},
        )

        self.assertResponseNoErrors(response)
        # Verify service is also deleted
        self.assertFalse(providers.ServiceLevel.objects.filter(id=service_id).exists())


class TestRateSheetZones(GraphTestCase):
    """Tests for shared zone CRUD operations."""

    def setUp(self):
        super().setUp()

        self.rate_sheet = providers.RateSheet.objects.create(
            name="Zone Test Sheet",
            carrier_name="ups",
            slug="zone_test_sheet",
            zones=[
                {
                    "id": "zone_1",
                    "label": "Zone 1",
                    "cities": ["New York", "Los Angeles"],
                    "country_codes": ["US"],
                    "postal_codes": ["10001", "90001"],
                }
            ],
            created_by=self.user,
        )

        self.service = providers.ServiceLevel.objects.create(
            service_name="Test Service",
            service_code="test_service",
            carrier_service_code="TEST",
            currency="USD",
            zone_ids=["zone_1"],
            created_by=self.user,
        )
        self.rate_sheet.services.add(self.service)

    # =========================================================================
    # ADD ZONE TESTS
    # =========================================================================

    def test_add_shared_zone(self):
        """Test adding a new shared zone."""
        response = self.query(
            """
            mutation add_zone($data: AddSharedZoneMutationInput!) {
              add_shared_zone(input: $data) {
                rate_sheet {
                  id
                  zones {
                    id
                    label
                    country_codes
                  }
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="add_zone",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "zone": {
                        "label": "Zone 2",
                        "country_codes": ["CA", "MX"],
                    },
                },
            },
        )

        self.assertResponseNoErrors(response)
        zones = response.data["data"]["add_shared_zone"]["rate_sheet"]["zones"]
        self.assertEqual(len(zones), 2)
        self.assertEqual(zones[1]["label"], "Zone 2")
        self.assertEqual(zones[1]["country_codes"], ["CA", "MX"])

    def test_add_shared_zone_with_all_fields(self):
        """Test adding a zone with all optional fields."""
        response = self.query(
            """
            mutation add_zone($data: AddSharedZoneMutationInput!) {
              add_shared_zone(input: $data) {
                rate_sheet {
                  id
                  zones {
                    id
                    label
                    country_codes
                    cities
                    postal_codes
                    transit_days
                    transit_time
                    radius
                    latitude
                    longitude
                  }
                }
              }
            }
            """,
            operation_name="add_zone",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "zone": {
                        "label": "Full Zone",
                        "country_codes": ["US"],
                        "cities": ["Seattle", "Portland"],
                        "postal_codes": ["98101", "97201"],
                        "transit_days": 3,
                        "transit_time": 72,
                        "radius": 100.0,
                        "latitude": 47.6062,
                        "longitude": -122.3321,
                    },
                },
            },
        )

        self.assertResponseNoErrors(response)
        zones = response.data["data"]["add_shared_zone"]["rate_sheet"]["zones"]
        new_zone = zones[-1]
        self.assertEqual(new_zone["label"], "Full Zone")
        self.assertEqual(new_zone["cities"], ["Seattle", "Portland"])
        self.assertEqual(new_zone["transit_days"], 3)
        self.assertEqual(new_zone["radius"], 100.0)

    def test_add_shared_zone_with_weight_limits(self):
        """Test adding a zone with weight limits."""
        response = self.query(
            """
            mutation add_zone($data: AddSharedZoneMutationInput!) {
              add_shared_zone(input: $data) {
                rate_sheet {
                  id
                  zones {
                    id
                    label
                    country_codes
                    min_weight
                    max_weight
                    weight_unit
                  }
                }
              }
            }
            """,
            operation_name="add_zone",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "zone": {
                        "label": "Weight Limited Zone",
                        "country_codes": ["US"],
                        "min_weight": 0.0,
                        "max_weight": 30.0,
                        "weight_unit": "KG",
                    },
                },
            },
        )

        self.assertResponseNoErrors(response)
        zones = response.data["data"]["add_shared_zone"]["rate_sheet"]["zones"]
        new_zone = zones[-1]
        self.assertEqual(new_zone["label"], "Weight Limited Zone")
        self.assertEqual(new_zone["min_weight"], 0.0)
        self.assertEqual(new_zone["max_weight"], 30.0)
        self.assertEqual(new_zone["weight_unit"], "KG")

    def test_update_shared_zone_weight_limits(self):
        """Test updating a zone's weight limits."""
        response = self.query(
            """
            mutation update_zone($data: UpdateSharedZoneMutationInput!) {
              update_shared_zone(input: $data) {
                rate_sheet {
                  zones {
                    id
                    label
                    min_weight
                    max_weight
                    weight_unit
                  }
                }
              }
            }
            """,
            operation_name="update_zone",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "zone_id": "zone_1",
                    "zone": {
                        "label": "Zone 1",
                        "min_weight": 0.5,
                        "max_weight": 20.0,
                        "weight_unit": "LB",
                    },
                },
            },
        )

        self.assertResponseNoErrors(response)
        zone = response.data["data"]["update_shared_zone"]["rate_sheet"]["zones"][0]
        self.assertEqual(zone["min_weight"], 0.5)
        self.assertEqual(zone["max_weight"], 20.0)
        self.assertEqual(zone["weight_unit"], "LB")

    def test_add_multiple_zones_sequentially(self):
        """Test adding multiple zones one after another."""
        for i in range(2, 5):
            response = self.query(
                """
                mutation add_zone($data: AddSharedZoneMutationInput!) {
                  add_shared_zone(input: $data) {
                    rate_sheet {
                      zones {
                        id
                        label
                      }
                    }
                  }
                }
                """,
                operation_name="add_zone",
                variables={
                    "data": {
                        "rate_sheet_id": self.rate_sheet.id,
                        "zone": {
                            "label": f"Zone {i}",
                            "country_codes": ["US"],
                        },
                    },
                },
            )
            self.assertResponseNoErrors(response)

        # Verify all zones exist
        self.rate_sheet.refresh_from_db()
        self.assertEqual(len(self.rate_sheet.zones), 4)

    # =========================================================================
    # UPDATE ZONE TESTS
    # =========================================================================

    def test_update_shared_zone(self):
        """Test updating an existing shared zone."""
        response = self.query(
            """
            mutation update_zone($data: UpdateSharedZoneMutationInput!) {
              update_shared_zone(input: $data) {
                rate_sheet {
                  id
                  zones {
                    id
                    label
                    country_codes
                  }
                }
              }
            }
            """,
            operation_name="update_zone",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "zone_id": "zone_1",
                    "zone": {
                        "label": "Updated Zone 1",
                        "country_codes": ["US", "CA"],
                    },
                },
            },
        )

        self.assertResponseNoErrors(response)
        zones = response.data["data"]["update_shared_zone"]["rate_sheet"]["zones"]
        self.assertEqual(zones[0]["label"], "Updated Zone 1")
        self.assertEqual(zones[0]["country_codes"], ["US", "CA"])

    def test_update_zone_partial_fields(self):
        """Test updating only specific fields of a zone."""
        response = self.query(
            """
            mutation update_zone($data: UpdateSharedZoneMutationInput!) {
              update_shared_zone(input: $data) {
                rate_sheet {
                  zones {
                    id
                    label
                    cities
                    country_codes
                  }
                }
              }
            }
            """,
            operation_name="update_zone",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "zone_id": "zone_1",
                    "zone": {
                        "label": "New Label Only",
                    },
                },
            },
        )

        self.assertResponseNoErrors(response)
        zone = response.data["data"]["update_shared_zone"]["rate_sheet"]["zones"][0]
        self.assertEqual(zone["label"], "New Label Only")
        # Other fields might be reset based on implementation

    def test_update_nonexistent_zone(self):
        """Test updating a zone that doesn't exist."""
        response = self.query(
            """
            mutation update_zone($data: UpdateSharedZoneMutationInput!) {
              update_shared_zone(input: $data) {
                rate_sheet {
                  id
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="update_zone",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "zone_id": "nonexistent_zone",
                    "zone": {
                        "label": "Will Fail",
                    },
                },
            },
        )

        # Should have an error
        self.assertIsNotNone(response.data.get("errors") or response.data["data"]["update_shared_zone"].get("errors"))

    # =========================================================================
    # DELETE ZONE TESTS
    # =========================================================================

    def test_delete_shared_zone(self):
        """Test deleting a shared zone."""
        # First add a second zone
        self.rate_sheet.zones.append({
            "id": "zone_2",
            "label": "Zone 2",
            "country_codes": ["CA"],
        })
        self.rate_sheet.save()

        response = self.query(
            """
            mutation delete_zone($data: DeleteSharedZoneMutationInput!) {
              delete_shared_zone(input: $data) {
                rate_sheet {
                  id
                  zones {
                    id
                    label
                  }
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="delete_zone",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "zone_id": "zone_2",
                },
            },
        )

        self.assertResponseNoErrors(response)
        zones = response.data["data"]["delete_shared_zone"]["rate_sheet"]["zones"]
        self.assertEqual(len(zones), 1)
        self.assertEqual(zones[0]["id"], "zone_1")

    def test_delete_zone_removes_from_service_zone_ids(self):
        """Test that deleting a zone removes it from services' zone_ids."""
        # Add zone to service
        self.service.zone_ids = ["zone_1"]
        self.service.save()

        response = self.query(
            """
            mutation delete_zone($data: DeleteSharedZoneMutationInput!) {
              delete_shared_zone(input: $data) {
                rate_sheet {
                  zones {
                    id
                  }
                  services {
                    id
                    zone_ids
                  }
                }
              }
            }
            """,
            operation_name="delete_zone",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "zone_id": "zone_1",
                },
            },
        )

        self.assertResponseNoErrors(response)
        services = response.data["data"]["delete_shared_zone"]["rate_sheet"]["services"]
        self.assertEqual(services[0]["zone_ids"], [])

    def test_delete_zone_removes_service_rates(self):
        """Test that deleting a zone removes associated service_rates."""
        # Add service rate for the zone
        self.rate_sheet.service_rates = [
            {"service_id": self.service.id, "zone_id": "zone_1", "rate": 10.0}
        ]
        self.rate_sheet.save()

        response = self.query(
            """
            mutation delete_zone($data: DeleteSharedZoneMutationInput!) {
              delete_shared_zone(input: $data) {
                rate_sheet {
                  zones {
                    id
                  }
                  service_rates {
                    zone_id
                  }
                }
              }
            }
            """,
            operation_name="delete_zone",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "zone_id": "zone_1",
                },
            },
        )

        self.assertResponseNoErrors(response)
        service_rates = response.data["data"]["delete_shared_zone"]["rate_sheet"]["service_rates"]
        self.assertEqual(service_rates, [])


class TestRateSheetSurcharges(GraphTestCase):
    """Tests for shared surcharge CRUD operations."""

    def setUp(self):
        super().setUp()

        self.rate_sheet = providers.RateSheet.objects.create(
            name="Surcharge Test Sheet",
            carrier_name="ups",
            slug="surcharge_test_sheet",
            surcharges=[
                {
                    "id": "surch_fuel",
                    "name": "Fuel Surcharge",
                    "amount": 10.0,
                    "surcharge_type": "percentage",
                    "active": True,
                    "cost": 8.0,
                }
            ],
            created_by=self.user,
        )

        self.service = providers.ServiceLevel.objects.create(
            service_name="Test Service",
            service_code="test_service",
            carrier_service_code="TEST",
            currency="USD",
            surcharge_ids=["surch_fuel"],
            created_by=self.user,
        )
        self.rate_sheet.services.add(self.service)

    # =========================================================================
    # ADD SURCHARGE TESTS
    # =========================================================================

    def test_add_shared_surcharge(self):
        """Test adding a new shared surcharge."""
        response = self.query(
            """
            mutation add_surcharge($data: AddSharedSurchargeMutationInput!) {
              add_shared_surcharge(input: $data) {
                rate_sheet {
                  id
                  surcharges {
                    id
                    name
                    amount
                    surcharge_type
                    active
                  }
                }
              }
            }
            """,
            operation_name="add_surcharge",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "surcharge": {
                        "name": "Energy Surcharge",
                        "amount": 2.50,
                        "surcharge_type": "fixed",
                    },
                },
            },
        )

        self.assertResponseNoErrors(response)
        surcharges = response.data["data"]["add_shared_surcharge"]["rate_sheet"]["surcharges"]
        self.assertEqual(len(surcharges), 2)
        new_surcharge = surcharges[1]
        self.assertEqual(new_surcharge["name"], "Energy Surcharge")
        self.assertEqual(new_surcharge["amount"], 2.5)
        self.assertEqual(new_surcharge["surcharge_type"], "fixed")
        self.assertTrue(new_surcharge["active"])

    def test_add_surcharge_percentage_type(self):
        """Test adding a percentage-based surcharge."""
        response = self.query(
            """
            mutation add_surcharge($data: AddSharedSurchargeMutationInput!) {
              add_shared_surcharge(input: $data) {
                rate_sheet {
                  surcharges {
                    id
                    name
                    amount
                    surcharge_type
                    cost
                  }
                }
              }
            }
            """,
            operation_name="add_surcharge",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "surcharge": {
                        "name": "Peak Season",
                        "amount": 15.0,
                        "surcharge_type": "percentage",
                        "cost": 12.0,
                    },
                },
            },
        )

        self.assertResponseNoErrors(response)
        surcharges = response.data["data"]["add_shared_surcharge"]["rate_sheet"]["surcharges"]
        new_surcharge = surcharges[-1]
        self.assertEqual(new_surcharge["surcharge_type"], "percentage")
        self.assertEqual(new_surcharge["cost"], 12.0)

    def test_add_inactive_surcharge(self):
        """Test adding a surcharge that starts as inactive."""
        response = self.query(
            """
            mutation add_surcharge($data: AddSharedSurchargeMutationInput!) {
              add_shared_surcharge(input: $data) {
                rate_sheet {
                  surcharges {
                    id
                    name
                    active
                  }
                }
              }
            }
            """,
            operation_name="add_surcharge",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "surcharge": {
                        "name": "Future Surcharge",
                        "amount": 5.0,
                        "active": False,
                    },
                },
            },
        )

        self.assertResponseNoErrors(response)
        surcharges = response.data["data"]["add_shared_surcharge"]["rate_sheet"]["surcharges"]
        new_surcharge = surcharges[-1]
        self.assertFalse(new_surcharge["active"])

    # =========================================================================
    # UPDATE SURCHARGE TESTS
    # =========================================================================

    def test_update_shared_surcharge(self):
        """Test updating an existing shared surcharge."""
        response = self.query(
            """
            mutation update_surcharge($data: UpdateSharedSurchargeMutationInput!) {
              update_shared_surcharge(input: $data) {
                rate_sheet {
                  id
                  surcharges {
                    id
                    name
                    amount
                    surcharge_type
                    active
                  }
                }
              }
            }
            """,
            operation_name="update_surcharge",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "surcharge_id": "surch_fuel",
                    "surcharge": {
                        "name": "Updated Fuel Surcharge",
                        "amount": 12.0,
                        "surcharge_type": "percentage",
                        "active": True,
                    },
                },
            },
        )

        self.assertResponseNoErrors(response)
        surcharges = response.data["data"]["update_shared_surcharge"]["rate_sheet"]["surcharges"]
        self.assertEqual(surcharges[0]["name"], "Updated Fuel Surcharge")
        self.assertEqual(surcharges[0]["amount"], 12.0)

    def test_update_surcharge_toggle_active(self):
        """Test toggling surcharge active status."""
        response = self.query(
            """
            mutation update_surcharge($data: UpdateSharedSurchargeMutationInput!) {
              update_shared_surcharge(input: $data) {
                rate_sheet {
                  surcharges {
                    id
                    active
                  }
                }
              }
            }
            """,
            operation_name="update_surcharge",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "surcharge_id": "surch_fuel",
                    "surcharge": {
                        "name": "Fuel Surcharge",
                        "amount": 10.0,
                        "active": False,
                    },
                },
            },
        )

        self.assertResponseNoErrors(response)
        surcharges = response.data["data"]["update_shared_surcharge"]["rate_sheet"]["surcharges"]
        self.assertFalse(surcharges[0]["active"])

    def test_update_nonexistent_surcharge(self):
        """Test updating a surcharge that doesn't exist."""
        response = self.query(
            """
            mutation update_surcharge($data: UpdateSharedSurchargeMutationInput!) {
              update_shared_surcharge(input: $data) {
                rate_sheet {
                  id
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="update_surcharge",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "surcharge_id": "nonexistent_surcharge",
                    "surcharge": {
                        "name": "Will Fail",
                        "amount": 0,
                    },
                },
            },
        )

        # Should have an error
        self.assertIsNotNone(response.data.get("errors") or response.data["data"]["update_shared_surcharge"].get("errors"))

    # =========================================================================
    # DELETE SURCHARGE TESTS
    # =========================================================================

    def test_delete_shared_surcharge(self):
        """Test deleting a shared surcharge."""
        # Add a second surcharge
        self.rate_sheet.surcharges.append({
            "id": "surch_energy",
            "name": "Energy",
            "amount": 5.0,
            "surcharge_type": "fixed",
            "active": True,
        })
        self.rate_sheet.save()

        response = self.query(
            """
            mutation delete_surcharge($data: DeleteSharedSurchargeMutationInput!) {
              delete_shared_surcharge(input: $data) {
                rate_sheet {
                  id
                  surcharges {
                    id
                    name
                  }
                }
              }
            }
            """,
            operation_name="delete_surcharge",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "surcharge_id": "surch_energy",
                },
            },
        )

        self.assertResponseNoErrors(response)
        surcharges = response.data["data"]["delete_shared_surcharge"]["rate_sheet"]["surcharges"]
        self.assertEqual(len(surcharges), 1)
        self.assertEqual(surcharges[0]["id"], "surch_fuel")

    def test_delete_surcharge_removes_from_service_surcharge_ids(self):
        """Test that deleting a surcharge removes it from services' surcharge_ids."""
        self.service.surcharge_ids = ["surch_fuel"]
        self.service.save()

        response = self.query(
            """
            mutation delete_surcharge($data: DeleteSharedSurchargeMutationInput!) {
              delete_shared_surcharge(input: $data) {
                rate_sheet {
                  surcharges {
                    id
                  }
                  services {
                    id
                    surcharge_ids
                  }
                }
              }
            }
            """,
            operation_name="delete_surcharge",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "surcharge_id": "surch_fuel",
                },
            },
        )

        self.assertResponseNoErrors(response)
        services = response.data["data"]["delete_shared_surcharge"]["rate_sheet"]["services"]
        self.assertEqual(services[0]["surcharge_ids"], [])


class TestServiceRates(GraphTestCase):
    """Tests for service rate (service-zone rate mapping) operations."""

    def setUp(self):
        super().setUp()

        self.rate_sheet = providers.RateSheet.objects.create(
            name="Service Rate Test Sheet",
            carrier_name="ups",
            slug="service_rate_test_sheet",
            zones=[
                {"id": "zone_1", "label": "Zone 1", "country_codes": ["US"]},
                {"id": "zone_2", "label": "Zone 2", "country_codes": ["CA"]},
                {"id": "zone_3", "label": "Zone 3", "country_codes": ["MX"]},
            ],
            created_by=self.user,
        )

        self.service = providers.ServiceLevel.objects.create(
            service_name="Test Service",
            service_code="test_service",
            carrier_service_code="TEST",
            currency="USD",
            zone_ids=["zone_1", "zone_2"],
            created_by=self.user,
        )
        self.rate_sheet.services.add(self.service)

        # Add initial service rates
        self.rate_sheet.service_rates = [
            {"service_id": self.service.id, "zone_id": "zone_1", "rate": 10.00, "cost": 8.00},
            {"service_id": self.service.id, "zone_id": "zone_2", "rate": 15.00, "cost": 12.00},
        ]
        self.rate_sheet.save()

    # =========================================================================
    # UPDATE SERVICE RATE TESTS
    # =========================================================================

    def test_update_service_rate(self):
        """Test updating an existing service rate."""
        response = self.query(
            """
            mutation update_rate($data: UpdateServiceRateMutationInput!) {
              update_service_rate(input: $data) {
                rate_sheet {
                  id
                  service_rates {
                    service_id
                    zone_id
                    rate
                    cost
                  }
                }
              }
            }
            """,
            operation_name="update_rate",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "service_id": self.service.id,
                    "zone_id": "zone_1",
                    "rate": 15.00,
                    "cost": 12.00,
                },
            },
        )

        self.assertResponseNoErrors(response)
        service_rates = response.data["data"]["update_service_rate"]["rate_sheet"]["service_rates"]
        zone_1_rate = next(r for r in service_rates if r["zone_id"] == "zone_1")
        self.assertEqual(zone_1_rate["rate"], 15.0)
        self.assertEqual(zone_1_rate["cost"], 12.0)

    def test_update_service_rate_creates_new(self):
        """Test that updating a non-existent service rate creates it."""
        response = self.query(
            """
            mutation update_rate($data: UpdateServiceRateMutationInput!) {
              update_service_rate(input: $data) {
                rate_sheet {
                  service_rates {
                    service_id
                    zone_id
                    rate
                  }
                }
              }
            }
            """,
            operation_name="update_rate",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "service_id": self.service.id,
                    "zone_id": "zone_3",  # New zone
                    "rate": 20.00,
                },
            },
        )

        self.assertResponseNoErrors(response)
        service_rates = response.data["data"]["update_service_rate"]["rate_sheet"]["service_rates"]
        self.assertEqual(len(service_rates), 3)
        zone_3_rate = next(r for r in service_rates if r["zone_id"] == "zone_3")
        self.assertEqual(zone_3_rate["rate"], 20.0)

    def test_update_service_rate_with_weight_limits(self):
        """Test updating service rate with weight limits."""
        response = self.query(
            """
            mutation update_rate($data: UpdateServiceRateMutationInput!) {
              update_service_rate(input: $data) {
                rate_sheet {
                  service_rates {
                    service_id
                    zone_id
                    rate
                    min_weight
                    max_weight
                  }
                }
              }
            }
            """,
            operation_name="update_rate",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "service_id": self.service.id,
                    "zone_id": "zone_1",
                    "rate": 10.00,
                    "min_weight": 0.0,
                    "max_weight": 50.0,
                },
            },
        )

        self.assertResponseNoErrors(response)
        service_rates = response.data["data"]["update_service_rate"]["rate_sheet"]["service_rates"]
        zone_1_rate = next(r for r in service_rates if r["zone_id"] == "zone_1")
        self.assertEqual(zone_1_rate["min_weight"], 0.0)
        self.assertEqual(zone_1_rate["max_weight"], 50.0)

    # =========================================================================
    # BATCH UPDATE SERVICE RATES TESTS
    # =========================================================================

    def test_batch_update_service_rates(self):
        """Test batch updating multiple service rates."""
        response = self.query(
            """
            mutation batch_update($data: BatchUpdateServiceRatesMutationInput!) {
              batch_update_service_rates(input: $data) {
                rate_sheet {
                  service_rates {
                    service_id
                    zone_id
                    rate
                    cost
                  }
                }
              }
            }
            """,
            operation_name="batch_update",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "rates": [
                        {
                            "service_id": self.service.id,
                            "zone_id": "zone_1",
                            "rate": 11.00,
                            "cost": 9.00,
                        },
                        {
                            "service_id": self.service.id,
                            "zone_id": "zone_2",
                            "rate": 16.00,
                            "cost": 13.00,
                        },
                        {
                            "service_id": self.service.id,
                            "zone_id": "zone_3",
                            "rate": 21.00,
                            "cost": 17.00,
                        },
                    ],
                },
            },
        )

        self.assertResponseNoErrors(response)
        service_rates = response.data["data"]["batch_update_service_rates"]["rate_sheet"]["service_rates"]
        self.assertEqual(len(service_rates), 3)

        # Verify each rate
        rates_by_zone = {r["zone_id"]: r for r in service_rates}
        self.assertEqual(rates_by_zone["zone_1"]["rate"], 11.0)
        self.assertEqual(rates_by_zone["zone_2"]["rate"], 16.0)
        self.assertEqual(rates_by_zone["zone_3"]["rate"], 21.0)


class TestServiceAssignments(GraphTestCase):
    """Tests for service zone_ids and surcharge_ids assignment operations."""

    def setUp(self):
        super().setUp()

        self.rate_sheet = providers.RateSheet.objects.create(
            name="Assignment Test Sheet",
            carrier_name="ups",
            slug="assignment_test_sheet",
            zones=[
                {"id": "zone_1", "label": "Zone 1", "country_codes": ["US"]},
                {"id": "zone_2", "label": "Zone 2", "country_codes": ["CA"]},
            ],
            surcharges=[
                {"id": "surch_fuel", "name": "Fuel", "amount": 10.0, "surcharge_type": "percentage", "active": True},
                {"id": "surch_energy", "name": "Energy", "amount": 5.0, "surcharge_type": "fixed", "active": True},
            ],
            created_by=self.user,
        )

        self.service = providers.ServiceLevel.objects.create(
            service_name="Test Service",
            service_code="test_service",
            carrier_service_code="TEST",
            currency="USD",
            zone_ids=["zone_1"],
            surcharge_ids=["surch_fuel"],
            created_by=self.user,
        )
        self.rate_sheet.services.add(self.service)

    # =========================================================================
    # UPDATE SERVICE ZONE IDS TESTS
    # =========================================================================

    def test_update_service_zone_ids(self):
        """Test updating service zone_ids."""
        response = self.query(
            """
            mutation update_zone_ids($data: UpdateServiceZoneIdsMutationInput!) {
              update_service_zone_ids(input: $data) {
                rate_sheet {
                  id
                  services {
                    id
                    zone_ids
                  }
                }
              }
            }
            """,
            operation_name="update_zone_ids",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "service_id": self.service.id,
                    "zone_ids": ["zone_1", "zone_2"],
                },
            },
        )

        self.assertResponseNoErrors(response)
        services = response.data["data"]["update_service_zone_ids"]["rate_sheet"]["services"]
        self.assertEqual(services[0]["zone_ids"], ["zone_1", "zone_2"])

    def test_update_service_zone_ids_empty(self):
        """Test clearing service zone_ids."""
        response = self.query(
            """
            mutation update_zone_ids($data: UpdateServiceZoneIdsMutationInput!) {
              update_service_zone_ids(input: $data) {
                rate_sheet {
                  services {
                    id
                    zone_ids
                  }
                }
              }
            }
            """,
            operation_name="update_zone_ids",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "service_id": self.service.id,
                    "zone_ids": [],
                },
            },
        )

        self.assertResponseNoErrors(response)
        services = response.data["data"]["update_service_zone_ids"]["rate_sheet"]["services"]
        self.assertEqual(services[0]["zone_ids"], [])

    # =========================================================================
    # UPDATE SERVICE SURCHARGE IDS TESTS
    # =========================================================================

    def test_update_service_surcharge_ids(self):
        """Test updating service surcharge_ids."""
        response = self.query(
            """
            mutation update_surcharge_ids($data: UpdateServiceSurchargeIdsMutationInput!) {
              update_service_surcharge_ids(input: $data) {
                rate_sheet {
                  id
                  services {
                    id
                    surcharge_ids
                  }
                }
              }
            }
            """,
            operation_name="update_surcharge_ids",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "service_id": self.service.id,
                    "surcharge_ids": ["surch_fuel", "surch_energy"],
                },
            },
        )

        self.assertResponseNoErrors(response)
        services = response.data["data"]["update_service_surcharge_ids"]["rate_sheet"]["services"]
        self.assertEqual(services[0]["surcharge_ids"], ["surch_fuel", "surch_energy"])

    def test_update_service_surcharge_ids_empty(self):
        """Test clearing service surcharge_ids."""
        response = self.query(
            """
            mutation update_surcharge_ids($data: UpdateServiceSurchargeIdsMutationInput!) {
              update_service_surcharge_ids(input: $data) {
                rate_sheet {
                  services {
                    id
                    surcharge_ids
                  }
                }
              }
            }
            """,
            operation_name="update_surcharge_ids",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "service_id": self.service.id,
                    "surcharge_ids": [],
                },
            },
        )

        self.assertResponseNoErrors(response)
        services = response.data["data"]["update_service_surcharge_ids"]["rate_sheet"]["services"]
        self.assertEqual(services[0]["surcharge_ids"], [])


class TestRateSheetServices(GraphTestCase):
    """Tests for rate sheet service operations."""

    def setUp(self):
        super().setUp()

        self.rate_sheet = providers.RateSheet.objects.create(
            name="Service Test Sheet",
            carrier_name="ups",
            slug="service_test_sheet",
            zones=[
                {"id": "zone_1", "label": "Zone 1", "country_codes": ["US"]},
            ],
            created_by=self.user,
        )

        self.service1 = providers.ServiceLevel.objects.create(
            service_name="Service 1",
            service_code="service_1",
            carrier_service_code="S1",
            currency="USD",
            zone_ids=["zone_1"],
            created_by=self.user,
        )
        self.service2 = providers.ServiceLevel.objects.create(
            service_name="Service 2",
            service_code="service_2",
            carrier_service_code="S2",
            currency="USD",
            zone_ids=["zone_1"],
            created_by=self.user,
        )
        self.rate_sheet.services.add(self.service1, self.service2)

    def test_delete_rate_sheet_service(self):
        """Test deleting a service from a rate sheet."""
        response = self.query(
            """
            mutation delete_service($data: DeleteRateSheetServiceMutationInput!) {
              delete_rate_sheet_service(input: $data) {
                rate_sheet {
                  id
                  services {
                    id
                    service_name
                  }
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="delete_service",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "service_id": self.service2.id,
                },
            },
        )

        self.assertResponseNoErrors(response)
        services = response.data["data"]["delete_rate_sheet_service"]["rate_sheet"]["services"]
        self.assertEqual(len(services), 1)
        self.assertEqual(services[0]["service_name"], "Service 1")

class TestRateSheetModelMethods(GraphTestCase):
    """Tests for RateSheet model methods (rate calculation, etc.)."""

    def setUp(self):
        super().setUp()

        self.rate_sheet = providers.RateSheet.objects.create(
            name="Calculation Test Sheet",
            carrier_name="ups",
            slug="calculation_test_sheet",
            zones=[
                {"id": "zone_1", "label": "Zone 1", "country_codes": ["US"]},
                {"id": "zone_2", "label": "Zone 2", "country_codes": ["CA"], "transit_days": 5},
            ],
            surcharges=[
                {"id": "surch_fuel", "name": "Fuel", "amount": 10.0, "surcharge_type": "percentage", "active": True, "cost": 8.0},
                {"id": "surch_handling", "name": "Handling", "amount": 5.0, "surcharge_type": "fixed", "active": True, "cost": 3.0},
                {"id": "surch_inactive", "name": "Inactive", "amount": 100.0, "surcharge_type": "fixed", "active": False},
            ],
            service_rates=[],
            created_by=self.user,
        )

        self.service = providers.ServiceLevel.objects.create(
            service_name="Test Service",
            service_code="test_service",
            carrier_service_code="TEST",
            currency="USD",
            zone_ids=["zone_1", "zone_2"],
            surcharge_ids=["surch_fuel", "surch_handling", "surch_inactive"],
            created_by=self.user,
        )
        self.rate_sheet.services.add(self.service)

        # Add service rates
        self.rate_sheet.service_rates = [
            {"service_id": self.service.id, "zone_id": "zone_1", "rate": 100.00, "cost": 80.00},
            {"service_id": self.service.id, "zone_id": "zone_2", "rate": 150.00, "cost": 120.00},
        ]
        self.rate_sheet.save()

    def test_get_zone(self):
        """Test getting a zone by ID."""
        zone = self.rate_sheet.get_zone("zone_1")
        self.assertIsNotNone(zone)
        self.assertEqual(zone["label"], "Zone 1")

        zone_none = self.rate_sheet.get_zone("nonexistent")
        self.assertIsNone(zone_none)

    def test_get_surcharge(self):
        """Test getting a surcharge by ID."""
        surcharge = self.rate_sheet.get_surcharge("surch_fuel")
        self.assertIsNotNone(surcharge)
        self.assertEqual(surcharge["name"], "Fuel")

        surcharge_none = self.rate_sheet.get_surcharge("nonexistent")
        self.assertIsNone(surcharge_none)

    def test_get_service_rate(self):
        """Test getting a service rate by service_id and zone_id."""
        rate = self.rate_sheet.get_service_rate(self.service.id, "zone_1")
        self.assertIsNotNone(rate)
        self.assertEqual(rate["rate"], 100.00)

        rate_none = self.rate_sheet.get_service_rate(self.service.id, "nonexistent")
        self.assertIsNone(rate_none)

    def test_apply_surcharges_to_rate_percentage(self):
        """Test applying percentage surcharges."""
        # 10% of 100 = 10
        total, breakdown = self.rate_sheet.apply_surcharges_to_rate(100.0, ["surch_fuel"])
        self.assertEqual(total, 110.0)
        self.assertEqual(len(breakdown), 1)
        self.assertEqual(breakdown[0]["amount"], 10.0)
        self.assertEqual(breakdown[0]["surcharge_type"], "percentage")

    def test_apply_surcharges_to_rate_fixed(self):
        """Test applying fixed surcharges."""
        total, breakdown = self.rate_sheet.apply_surcharges_to_rate(100.0, ["surch_handling"])
        self.assertEqual(total, 105.0)
        self.assertEqual(len(breakdown), 1)
        self.assertEqual(breakdown[0]["amount"], 5.0)
        self.assertEqual(breakdown[0]["surcharge_type"], "fixed")

    def test_apply_surcharges_to_rate_combined(self):
        """Test applying multiple surcharges."""
        # 100 + 10% (10) + 5 fixed = 115
        total, breakdown = self.rate_sheet.apply_surcharges_to_rate(100.0, ["surch_fuel", "surch_handling"])
        self.assertEqual(total, 115.0)
        self.assertEqual(len(breakdown), 2)

    def test_apply_surcharges_skips_inactive(self):
        """Test that inactive surcharges are skipped."""
        total, breakdown = self.rate_sheet.apply_surcharges_to_rate(100.0, ["surch_fuel", "surch_inactive"])
        self.assertEqual(total, 110.0)  # Only fuel applied
        self.assertEqual(len(breakdown), 1)  # Only one active surcharge

    def test_calculate_rate(self):
        """Test full rate calculation with surcharges."""
        total, breakdown = self.rate_sheet.calculate_rate(self.service.id, "zone_1")
        # Base: 100, Fuel (10%): 10, Handling (fixed): 5 = 115
        self.assertEqual(total, 115.0)
        self.assertEqual(breakdown["base_rate"], 100.0)
        self.assertEqual(breakdown["base_cost"], 80.0)
        self.assertEqual(len(breakdown["surcharges"]), 2)  # Only active surcharges

    def test_get_service_zones_for_rating(self):
        """Test getting zones with rates for SDK rating."""
        zones = self.rate_sheet.get_service_zones_for_rating(self.service.id)
        self.assertEqual(len(zones), 2)

        zone_1 = next(z for z in zones if z["id"] == "zone_1")
        self.assertEqual(zone_1["rate"], 100.0)
        self.assertEqual(zone_1["cost"], 80.0)

        zone_2 = next(z for z in zones if z["id"] == "zone_2")
        self.assertEqual(zone_2["rate"], 150.0)
        self.assertEqual(zone_2["transit_days"], 5)  # From zone definition

    def test_get_surcharges_for_rating(self):
        """Test getting surcharges for SDK rating."""
        surcharges = self.rate_sheet.get_surcharges_for_rating(["surch_fuel", "surch_handling", "surch_inactive"])
        # Should only return active surcharges
        self.assertEqual(len(surcharges), 2)

        fuel = next(s for s in surcharges if s["id"] == "surch_fuel")
        self.assertEqual(fuel["amount"], 10.0)
        self.assertEqual(fuel["cost"], 8.0)


class TestRateSheetEdgeCases(GraphTestCase):
    """Tests for edge cases and error handling."""

    def setUp(self):
        super().setUp()

        self.rate_sheet = providers.RateSheet.objects.create(
            name="Edge Case Sheet",
            carrier_name="ups",
            slug="edge_case_sheet",
            zones=[],
            surcharges=[],
            service_rates=[],
            created_by=self.user,
        )

    def test_operations_on_empty_rate_sheet(self):
        """Test that operations work on an empty rate sheet."""
        # Add first zone
        response = self.query(
            """
            mutation add_zone($data: AddSharedZoneMutationInput!) {
              add_shared_zone(input: $data) {
                rate_sheet {
                  zones {
                    id
                    label
                  }
                }
              }
            }
            """,
            operation_name="add_zone",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "zone": {
                        "label": "First Zone",
                        "country_codes": ["US"],
                    },
                },
            },
        )

        self.assertResponseNoErrors(response)
        zones = response.data["data"]["add_shared_zone"]["rate_sheet"]["zones"]
        self.assertEqual(len(zones), 1)

    def test_operations_on_nonexistent_rate_sheet(self):
        """Test that operations fail gracefully on nonexistent rate sheet."""
        response = self.query(
            """
            mutation add_zone($data: AddSharedZoneMutationInput!) {
              add_shared_zone(input: $data) {
                rate_sheet {
                  id
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="add_zone",
            variables={
                "data": {
                    "rate_sheet_id": "rsht_nonexistent",
                    "zone": {
                        "label": "Will Fail",
                    },
                },
            },
        )

        # Should have an error
        self.assertIsNotNone(response.data.get("errors") or response.data["data"]["add_shared_zone"].get("errors"))

    def test_zone_with_empty_arrays(self):
        """Test zone with empty country_codes, cities, postal_codes."""
        response = self.query(
            """
            mutation add_zone($data: AddSharedZoneMutationInput!) {
              add_shared_zone(input: $data) {
                rate_sheet {
                  zones {
                    id
                    label
                    country_codes
                    cities
                    postal_codes
                  }
                }
              }
            }
            """,
            operation_name="add_zone",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "zone": {
                        "label": "Empty Zone",
                        "country_codes": [],
                        "cities": [],
                        "postal_codes": [],
                    },
                },
            },
        )

        self.assertResponseNoErrors(response)
        zone = response.data["data"]["add_shared_zone"]["rate_sheet"]["zones"][0]
        self.assertEqual(zone["country_codes"], [])
        self.assertEqual(zone["cities"], [])
        self.assertEqual(zone["postal_codes"], [])

    def test_surcharge_with_zero_amount(self):
        """Test adding a surcharge with zero amount."""
        response = self.query(
            """
            mutation add_surcharge($data: AddSharedSurchargeMutationInput!) {
              add_shared_surcharge(input: $data) {
                rate_sheet {
                  surcharges {
                    id
                    name
                    amount
                  }
                }
              }
            }
            """,
            operation_name="add_surcharge",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "surcharge": {
                        "name": "Zero Surcharge",
                        "amount": 0.0,
                    },
                },
            },
        )

        self.assertResponseNoErrors(response)
        surcharge = response.data["data"]["add_shared_surcharge"]["rate_sheet"]["surcharges"][0]
        self.assertEqual(surcharge["amount"], 0.0)

    def test_service_rate_with_null_cost(self):
        """Test service rate with null cost."""
        # First add a zone and service
        self.rate_sheet.zones = [{"id": "zone_1", "label": "Zone 1", "country_codes": ["US"]}]
        self.rate_sheet.save()

        service = providers.ServiceLevel.objects.create(
            service_name="Test Service",
            service_code="test_service",
            carrier_service_code="TEST",
            currency="USD",
            created_by=self.user,
        )
        self.rate_sheet.services.add(service)

        response = self.query(
            """
            mutation update_rate($data: UpdateServiceRateMutationInput!) {
              update_service_rate(input: $data) {
                rate_sheet {
                  service_rates {
                    service_id
                    zone_id
                    rate
                    cost
                  }
                }
              }
            }
            """,
            operation_name="update_rate",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "service_id": service.id,
                    "zone_id": "zone_1",
                    "rate": 10.00,
                    # cost is not provided
                },
            },
        )

        self.assertResponseNoErrors(response)
        service_rate = response.data["data"]["update_service_rate"]["rate_sheet"]["service_rates"][0]
        self.assertEqual(service_rate["rate"], 10.0)
        # cost should be null or default


# =========================================================================
# EXPECTED RESPONSES
# =========================================================================

RATE_SHEETS_RESPONSE = {
    "data": {
        "rate_sheets": {
            "edges": [
                {
                    "node": {
                        "carrier_name": "ups",
                        "id": ANY,
                        "name": "Test Rate Sheet",
                        "slug": "test_rate_sheet",
                        "zones": [
                            {
                                "id": "zone_1",
                                "label": "Zone 1",
                                "cities": ["New York", "Los Angeles"],
                                "country_codes": ["US"],
                                "min_weight": None,
                                "max_weight": None,
                                "weight_unit": None,
                            }
                        ],
                        "surcharges": [
                            {
                                "id": "surch_fuel",
                                "name": "Fuel Surcharge",
                                "amount": 10.0,
                                "surcharge_type": "percentage",
                                "active": True,
                            }
                        ],
                        "service_rates": [
                            {
                                "service_id": ANY,
                                "zone_id": "zone_1",
                                "rate": 10.0,
                                "cost": 8.0,
                            }
                        ],
                        "services": [
                            {
                                "active": True,
                                "carrier_service_code": "11",
                                "currency": "USD",
                                "id": ANY,
                                "service_code": "ups_standard",
                                "service_name": "UPS Standard",
                                "zone_ids": ["zone_1"],
                                "surcharge_ids": ["surch_fuel"],
                            }
                        ],
                    }
                }
            ]
        }
    }
}

CREATE_RATE_SHEET_DATA = {
    "data": {
        "name": "New Rate Sheet",
        "carrier_name": "fedex",
        "services": [
            {
                "service_name": "FedEx Ground",
                "service_code": "fedex_ground",
                "carrier_service_code": "FEDEX_GROUND",
                "currency": "USD",
                "zone_ids": [],
                "surcharge_ids": [],
            }
        ],
    }
}

CREATE_RATE_SHEET_RESPONSE = {
    "data": {
        "create_rate_sheet": {
            "rate_sheet": {
                "id": ANY,
                "name": "New Rate Sheet",
                "carrier_name": "fedex",
                "zones": [],
                "surcharges": [],
                "services": [
                    {
                        "id": ANY,
                        "service_name": "FedEx Ground",
                        "service_code": "fedex_ground",
                        "currency": "USD",
                        "zone_ids": [],
                        "surcharge_ids": [],
                    }
                ],
            }
        }
    }
}

UPDATE_RATE_SHEET_RESPONSE = {
    "data": {
        "update_rate_sheet": {
            "rate_sheet": {
                "id": ANY,
                "name": "Updated Rate Sheet",
                "services": [
                    {
                        "id": ANY,
                        "service_name": "Updated Service",
                        "zone_ids": ["zone_1"],
                    }
                ],
            }
        }
    }
}

ADD_SHARED_ZONE_RESPONSE = {
    "data": {
        "add_shared_zone": {
            "rate_sheet": {
                "id": ANY,
                "zones": [
                    {
                        "id": "zone_1",
                        "label": "Zone 1",
                        "country_codes": ["US"],
                    },
                    {
                        "id": ANY,
                        "label": "Zone 2",
                        "country_codes": ["CA", "MX"],
                    },
                ],
            }
        }
    }
}

UPDATE_SHARED_ZONE_RESPONSE = {
    "data": {
        "update_shared_zone": {
            "rate_sheet": {
                "id": ANY,
                "zones": [
                    {
                        "id": "zone_1",
                        "label": "Updated Zone 1",
                        "country_codes": ["US", "CA"],
                    },
                ],
            }
        }
    }
}

ADD_SHARED_SURCHARGE_RESPONSE = {
    "data": {
        "add_shared_surcharge": {
            "rate_sheet": {
                "id": ANY,
                "surcharges": [
                    {
                        "id": "surch_fuel",
                        "name": "Fuel Surcharge",
                        "amount": 10.0,
                        "surcharge_type": "percentage",
                        "active": True,
                    },
                    {
                        "id": ANY,
                        "name": "Energy Surcharge",
                        "amount": 2.5,
                        "surcharge_type": "fixed",
                        "active": True,
                    },
                ],
            }
        }
    }
}

UPDATE_SERVICE_RATE_RESPONSE = {
    "data": {
        "update_service_rate": {
            "rate_sheet": {
                "id": ANY,
                "service_rates": [
                    {
                        "service_id": ANY,
                        "zone_id": "zone_1",
                        "rate": 15.0,
                        "cost": 12.0,
                    },
                ],
            }
        }
    }
}

UPDATE_SERVICE_ZONE_IDS_RESPONSE = {
    "data": {
        "update_service_zone_ids": {
            "rate_sheet": {
                "id": ANY,
                "services": [
                    {
                        "id": ANY,
                        "zone_ids": ["zone_1", "zone_2"],
                    },
                ],
            }
        }
    }
}

UPDATE_SERVICE_SURCHARGE_IDS_RESPONSE = {
    "data": {
        "update_service_surcharge_ids": {
            "rate_sheet": {
                "id": ANY,
                "services": [
                    {
                        "id": ANY,
                        "surcharge_ids": ["surch_fuel", "surch_energy"],
                    },
                ],
            }
        }
    }
}
