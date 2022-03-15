import json
from unittest.mock import ANY
from django.urls import reverse
from rest_framework import status
from karrio.server.core.tests import APITestCase
from karrio.server.manager.models import Address


class TestAddresses(APITestCase):
    def test_create_address(self):
        url = reverse("karrio.server.manager:address-list")
        data = ADDRESS_DATA

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response_data, ADDRESS_RESPONSE)


class TestAddressDetails(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.address: Address = Address.objects.create(
            **{
                "address_line1": "5205 rue riviera",
                "person_name": "Old town Daniel",
                "phone_number": "438 222 2222",
                "city": "Montreal",
                "country_code": "CA",
                "postal_code": "H8Z2Z3",
                "residential": True,
                "state_code": "QC",
                "suburb": "Hamilton",
                "validate_location": False,
                "validation": None,
                "created_by": self.user,
            }
        )

    def test_update_address(self):
        url = reverse(
            "karrio.server.manager:address-details", kwargs=dict(pk=self.address.pk)
        )
        data = ADDRESS_UPDATE_DATA

        response = self.client.patch(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, ADDRESS_UPDATE_RESPONSE)


ADDRESS_DATA = {
    "address_line1": "5205 rue riviera",
    "person_name": "Old town Daniel",
    "phone_number": "438 222 2222",
    "city": "Montreal",
    "country_code": "CA",
    "postal_code": "H8Z2Z3",
    "residential": True,
    "state_code": "QC",
}

ADDRESS_RESPONSE = {
    "id": ANY,
    "object_type": "address",
    "postal_code": "H8Z2Z3",
    "city": "Montreal",
    "federal_tax_id": None,
    "state_tax_id": None,
    "person_name": "Old town Daniel",
    "company_name": None,
    "country_code": "CA",
    "email": None,
    "phone_number": "+1 438-222-2222",
    "state_code": "QC",
    "suburb": None,
    "residential": True,
    "address_line1": "5205 rue riviera",
    "address_line2": None,
    "validate_location": False,
    "validation": None,
}

ADDRESS_UPDATE_DATA = {
    "person_name": "John Doe",
    "company_name": "Doe corp",
    "residential": False,
    "suburb": None,
}

ADDRESS_UPDATE_RESPONSE = {
    "id": ANY,
    "object_type": "address",
    "postal_code": "H8Z2Z3",
    "city": "Montreal",
    "federal_tax_id": None,
    "state_tax_id": None,
    "person_name": "John Doe",
    "company_name": "Doe corp",
    "country_code": "CA",
    "email": None,
    "phone_number": "438 222 2222",
    "state_code": "QC",
    "suburb": None,
    "residential": False,
    "address_line1": "5205 rue riviera",
    "address_line2": None,
    "validate_location": False,
    "validation": None,
}
