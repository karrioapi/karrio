import json
from unittest.mock import ANY
from django.urls import reverse
from rest_framework import status
from purpleserver.core.tests import APITestCase
from purpleserver.manager.models import Parcel


class TestParcels(APITestCase):

    def test_create_parcel(self):
        url = reverse('purpleserver.manager:parcel-list')
        data = PARCEL_DATA

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response_data, PARCEL_RESPONSE)


class TestParcelDetails(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.parcel: Parcel = Parcel.objects.create(**{
            "weight": 1,
            "width": 20,
            "height": 10,
            "length": 29,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "user": self.user
        })

    def test_update_parcel(self):
        url = reverse('purpleserver.manager:parcel-details', kwargs=dict(pk=self.parcel.pk))
        data = PARCEL_UPDATE_DATA

        response = self.client.patch(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, PARCEL_UPDATE_RESPONSE)


PARCEL_DATA = {
    "weight": 1,
    "width": 20,
    "height": 10,
    "length": 29,
    "weightUnit": "KG",
    "dimensionUnit": "CM"
}

PARCEL_RESPONSE = {
    "id": ANY,
    "weight": 1.0,
    "width": 20.0,
    "height": 10.0,
    "length": 29.0,
    "packagingType": None,
    "packagePreset": None,
    "description": None,
    "content": None,
    "isDocument": False,
    "weightUnit": "KG",
    "dimensionUnit": "CM"
}

PARCEL_UPDATE_DATA = {
    "length": 25.0,
    "weightUnit": None,
    "dimensionUnit": "IN"
}

PARCEL_UPDATE_RESPONSE = {
    "id": ANY,
    "weight": 1.0,
    "width": 20.0,
    "height": 10.0,
    "length": 25.0,
    "packagingType": None,
    "packagePreset": None,
    "description": None,
    "content": None,
    "isDocument": False,
    "weightUnit": None,
    "dimensionUnit": "IN"
}
