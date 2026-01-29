"""GraphQL pickup query tests following AGENTS.md patterns."""

import karrio.lib as lib
from karrio.server.graph.tests.base import GraphTestCase
from karrio.server.core.utils import create_carrier_snapshot
import karrio.server.manager.models as models


class TestPickupQueries(GraphTestCase):
    def setUp(self):
        super().setUp()
        self.maxDiff = None

        # Create a shipment for the pickup
        self.shipment = models.Shipment.objects.create(
            shipper={
                "postal_code": "E1C4Z8",
                "city": "Moncton",
                "person_name": "John Doe",
                "company_name": "A corp.",
                "country_code": "CA",
                "phone_number": "514 000 0000",
                "state_code": "NB",
                "address_line1": "125 Church St",
            },
            recipient={
                "postal_code": "V6M2V9",
                "city": "Vancouver",
                "person_name": "Jane Doe",
                "company_name": "B corp.",
                "country_code": "CA",
                "phone_number": "604 000 0000",
                "state_code": "BC",
                "address_line1": "5840 Oak St",
            },
            parcels=[
                {
                    "weight": 1.0,
                    "weight_unit": "KG",
                    "package_preset": "canadapost_corrugated_small_box",
                }
            ],
            created_by=self.user,
            test_mode=False,
            tracking_number="123456789012",
            carrier=create_carrier_snapshot(self.carrier),
        )

        # Create test pickup (test_mode must match token's test_mode)
        self.pickup = models.Pickup.objects.create(
            address={
                "id": "adr_001122334455",
                "postal_code": "E1C4Z8",
                "city": "Moncton",
                "person_name": "John Poop",
                "company_name": "A corp.",
                "country_code": "CA",
                "phone_number": "514 000 0000",
                "state_code": "NB",
                "address_line1": "125 Church St",
            },
            carrier=create_carrier_snapshot(self.carrier),
            created_by=self.user,
            test_mode=False,
            pickup_date="2020-10-25",
            ready_time="13:00",
            closing_time="17:00",
            instruction="Should not be folded",
            package_location="At the main entrance hall",
            confirmation_number="00110215",
            pickup_charge={"name": "Pickup fees", "amount": 0.0, "currency": "CAD"},
        )
        self.pickup.shipments.set([self.shipment])

    def test_query_pickup(self):
        """Verify single pickup query."""
        response = self.query(
            """
            query get_pickup($id: String!) {
                pickup(id: $id) {
                    id
                    object_type
                    confirmation_number
                    pickup_date
                    ready_time
                    closing_time
                    carrier_name
                    carrier_id
                    test_mode
                }
            }
            """,
            operation_name="get_pickup",
            variables={"id": self.pickup.id},
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            lib.to_dict(response.data),
            {
                "data": {
                    "pickup": {
                        "id": self.pickup.id,
                        "object_type": "pickup",
                        "confirmation_number": "00110215",
                        "pickup_date": "2020-10-25",
                        "ready_time": "13:00",
                        "closing_time": "17:00",
                        "carrier_name": "canadapost",
                        "carrier_id": "canadapost",
                        "test_mode": False,
                    }
                }
            },
        )

    def test_query_pickup_with_address(self):
        """Verify pickup query includes address."""
        response = self.query(
            """
            query get_pickup($id: String!) {
                pickup(id: $id) {
                    id
                    address {
                        city
                        country_code
                        postal_code
                    }
                }
            }
            """,
            operation_name="get_pickup",
            variables={"id": self.pickup.id},
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(
            response.data["data"]["pickup"]["address"]["city"],
            "Moncton",
        )
        self.assertEqual(
            response.data["data"]["pickup"]["address"]["country_code"],
            "CA",
        )

    def test_query_pickup_with_tracking_numbers(self):
        """Verify pickup query includes tracking numbers from shipments."""
        response = self.query(
            """
            query get_pickup($id: String!) {
                pickup(id: $id) {
                    id
                    tracking_numbers
                }
            }
            """,
            operation_name="get_pickup",
            variables={"id": self.pickup.id},
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(
            response.data["data"]["pickup"]["tracking_numbers"],
            ["123456789012"],
        )

    def test_query_pickups_list(self):
        """Verify pickup list query with pagination."""
        response = self.query(
            """
            query get_pickups($filter: PickupFilter) {
                pickups(filter: $filter) {
                    page_info {
                        count
                        has_next_page
                    }
                    edges {
                        node {
                            id
                            confirmation_number
                            carrier_name
                        }
                    }
                }
            }
            """,
            operation_name="get_pickups",
            variables={"filter": {"first": 20, "offset": 0}},
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(response.data["data"]["pickups"]["page_info"]["count"], 1)
        self.assertEqual(
            response.data["data"]["pickups"]["edges"][0]["node"]["confirmation_number"],
            "00110215",
        )

    def test_query_pickups_filter_by_carrier(self):
        """Verify pickup filtering by carrier_name."""
        response = self.query(
            """
            query get_pickups($filter: PickupFilter) {
                pickups(filter: $filter) {
                    edges {
                        node {
                            id
                            carrier_name
                        }
                    }
                }
            }
            """,
            operation_name="get_pickups",
            variables={"filter": {"carrier_name": ["canadapost"]}},
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(len(response.data["data"]["pickups"]["edges"]), 1)

    def test_query_pickups_filter_by_carrier_no_match(self):
        """Verify pickup filtering with non-matching carrier returns empty."""
        response = self.query(
            """
            query get_pickups($filter: PickupFilter) {
                pickups(filter: $filter) {
                    edges {
                        node {
                            id
                            carrier_name
                        }
                    }
                }
            }
            """,
            operation_name="get_pickups",
            variables={"filter": {"carrier_name": ["ups"]}},
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(len(response.data["data"]["pickups"]["edges"]), 0)

    def test_query_pickups_filter_by_confirmation_number(self):
        """Verify pickup filtering by confirmation_number."""
        response = self.query(
            """
            query get_pickups($filter: PickupFilter) {
                pickups(filter: $filter) {
                    edges {
                        node {
                            id
                            confirmation_number
                        }
                    }
                }
            }
            """,
            operation_name="get_pickups",
            variables={"filter": {"confirmation_number": "00110215"}},
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(len(response.data["data"]["pickups"]["edges"]), 1)

    def test_query_pickups_filter_by_date_range(self):
        """Verify pickup filtering by date range."""
        response = self.query(
            """
            query get_pickups($filter: PickupFilter) {
                pickups(filter: $filter) {
                    edges {
                        node {
                            id
                            pickup_date
                        }
                    }
                }
            }
            """,
            operation_name="get_pickups",
            variables={
                "filter": {
                    "pickup_date_after": "2020-10-01",
                    "pickup_date_before": "2020-10-31",
                }
            },
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(len(response.data["data"]["pickups"]["edges"]), 1)

    def test_query_pickups_filter_by_date_range_no_match(self):
        """Verify pickup filtering with date range outside returns empty."""
        response = self.query(
            """
            query get_pickups($filter: PickupFilter) {
                pickups(filter: $filter) {
                    edges {
                        node {
                            id
                            pickup_date
                        }
                    }
                }
            }
            """,
            operation_name="get_pickups",
            variables={
                "filter": {
                    "pickup_date_after": "2021-01-01",
                    "pickup_date_before": "2021-12-31",
                }
            },
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(len(response.data["data"]["pickups"]["edges"]), 0)

    def test_query_pickup_not_found(self):
        """Verify querying non-existent pickup returns null."""
        response = self.query(
            """
            query get_pickup($id: String!) {
                pickup(id: $id) {
                    id
                }
            }
            """,
            operation_name="get_pickup",
            variables={"id": "pck_nonexistent"},
        )

        self.assertResponseNoErrors(response)
        self.assertIsNone(response.data["data"]["pickup"])
