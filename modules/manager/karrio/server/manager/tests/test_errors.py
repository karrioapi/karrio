import json
from django.urls import reverse
from rest_framework import status
from karrio.server.core.tests import APITestCase


class TestNotFoundErrors(APITestCase):
    def test_address_not_found_returns_resource_name(self):
        url = reverse(
            "karrio.server.manager:address-details",
            kwargs=dict(pk="nonexistent_id"),
        )
        response = self.client.get(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(
            response_data,
            {"errors": [{"code": "not_found", "message": "Address not found", "level": "warning"}]},
        )

    def test_parcel_not_found_returns_resource_name(self):
        url = reverse(
            "karrio.server.manager:parcel-details",
            kwargs=dict(pk="nonexistent_id"),
        )
        response = self.client.get(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(
            response_data,
            {"errors": [{"code": "not_found", "message": "Parcel not found", "level": "warning"}]},
        )

    def test_shipment_not_found_returns_resource_name(self):
        url = reverse(
            "karrio.server.manager:shipment-details",
            kwargs=dict(pk="nonexistent_id"),
        )
        response = self.client.get(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(
            response_data,
            {"errors": [{"code": "not_found", "message": "Shipment not found", "level": "warning"}]},
        )

    def test_customs_not_found_returns_resource_name(self):
        url = reverse(
            "karrio.server.manager:customs-details",
            kwargs=dict(pk="nonexistent_id"),
        )
        response = self.client.get(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(
            response_data,
            {"errors": [{"code": "not_found", "message": "Customs not found", "level": "warning"}]},
        )


class TestValidationErrors(APITestCase):
    def test_shipment_validation_error_format(self):
        url = reverse("karrio.server.manager:shipment-list")
        data = {
            "shipper": {},
            "recipient": {},
            "parcels": [],
        }
        response = self.client.post(url, data, format="json")
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response_data)
        self.assertTrue(len(response_data["errors"]) > 0)
        # Validation errors should have level="error"
        for error in response_data["errors"]:
            self.assertEqual(error.get("level"), "error")

    def test_address_validation_error_format(self):
        url = reverse("karrio.server.manager:address-list")
        data = {"country_code": "INVALID"}
        response = self.client.post(url, data, format="json")
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response_data)
        self.assertTrue(len(response_data["errors"]) > 0)
        # Validation errors should have level="error"
        for error in response_data["errors"]:
            self.assertEqual(error.get("level"), "error")
