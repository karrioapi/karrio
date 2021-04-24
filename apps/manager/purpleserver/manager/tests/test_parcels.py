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
            "created_by": self.user
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
    "weight_unit": "KG",
    "dimension_unit": "CM"
}

PARCEL_RESPONSE = {
    "id": ANY,
    "weight": 1.0,
    "width": 20.0,
    "height": 10.0,
    "length": 29.0,
    "packaging_type": None,
    "package_preset": None,
    "description": None,
    "content": None,
    "is_document": False,
    "weight_unit": "KG",
    "dimension_unit": "CM"
}

PARCEL_UPDATE_DATA = {
    "width": 5.0,
    "height": 4.5,
    "length": 10.0,
    "weight_unit": "LB",
    "dimension_unit": "IN"
}

PARCEL_UPDATE_RESPONSE = {
    "id": ANY,
    "weight": 1.0,
    "width": 5.0,
    "height": 4.5,
    "length": 10.0,
    "packaging_type": None,
    "package_preset": None,
    "description": None,
    "content": None,
    "is_document": False,
    "weight_unit": "LB",
    "dimension_unit": "IN"
}
