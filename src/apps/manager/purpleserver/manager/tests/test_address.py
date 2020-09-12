import json
from unittest.mock import ANY
from django.urls import reverse
from rest_framework import status
from purpleserver.core.tests import APITestCase
from purpleserver.manager.models import Address


class TestAddresses(APITestCase):

    def test_create_address(self):
        url = reverse('purpleserver.manager:address-list')
        data = ADDRESS_DATA

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response_data, ADDRESS_RESPONSE)


class TestAddressDetails(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.address: Address = Address.objects.create(**{
            "address_line1": "5205 rue riviera",
            "person_name": "Old town Daniel",
            "phone_number": "438 222 2222",
            "city": "Montreal",
            "country_code": "CA",
            "postal_code": "H8Z2Z3",
            "residential": True,
            "state_code": "QC",
            "suburb": "Hamilton",
            "user": self.user
        })

    def test_update_address(self):
        url = reverse('purpleserver.manager:address-details', kwargs=dict(pk=self.address.pk))
        data = ADDRESS_UPDATE_DATA

        response = self.client.patch(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, ADDRESS_UPDATE_RESPONSE)


ADDRESS_DATA = {
    "addressLine1": "5205 rue riviera",
    "personName": "Old town Daniel",
    "phoneNumber": "438 222 2222",
    "city": "Montreal",
    "countryCode": "CA",
    "postalCode": "H8Z2Z3",
    "residential": True,
    "stateCode": "QC"
}

ADDRESS_RESPONSE = {
    "id": ANY,
    "postalCode": "H8Z2Z3",
    "city": "Montreal",
    "federalTaxId": None,
    "stateTaxId": None,
    "personName": "Old town Daniel",
    "companyName": None,
    "countryCode": "CA",
    "email": None,
    "phoneNumber": "438 222 2222",
    "stateCode": "QC",
    "suburb": None,
    "residential": True,
    "addressLine1": "5205 rue riviera",
    "addressLine2": None
}

ADDRESS_UPDATE_DATA = {
    "personName": "John Doe",
    "companyName": "Doe corp",
    "residential": False,
    "suburb": None
}

ADDRESS_UPDATE_RESPONSE = {
    "id": ANY,
    "postalCode": "H8Z2Z3",
    "city": "Montreal",
    "federalTaxId": None,
    "stateTaxId": None,
    "personName": "John Doe",
    "companyName": "Doe corp",
    "countryCode": "CA",
    "email": None,
    "phoneNumber": "438 222 2222",
    "stateCode": "QC",
    "suburb": None,
    "residential": False,
    "addressLine1": "5205 rue riviera",
    "addressLine2": None
}
