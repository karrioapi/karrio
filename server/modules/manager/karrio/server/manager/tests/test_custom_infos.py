import json
from unittest.mock import ANY
from django.urls import reverse
from rest_framework import status
from karrio.server.core.tests import APITestCase
from karrio.server.manager.models import Customs


class TestCustomsInfo(APITestCase):
    def test_create_customs(self):
        url = reverse("karrio.server.manager:customs-list")
        data = CUSTOMS_DATA

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response_data, CUSTOMS_RESPONSE)


class TestCustomsInfoDetails(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.customs: Customs = Customs.objects.create(**{"created_by": self.user})

    def test_update_customs(self):
        url = reverse(
            "karrio.server.manager:customs-details", kwargs=dict(pk=self.customs.pk)
        )
        data = CUSTOMS_UPDATE_DATA

        response = self.client.patch(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, CUSTOMS_UPDATE_RESPONSE)


CUSTOMS_DATA = {
    "incoterm": "DDU",
    "commodities": [
        {"description": "cn", "weight": 4.0, "weight_unit": "KG", "sku": "cc"},
    ],
}

CUSTOMS_RESPONSE = {
    "certify": None,
    "commercial_invoice": None,
    "commodities": [
        {
            "description": "cn",
            "id": ANY,
            "object_type": "commodity",
            "origin_country": None,
            "parent_id": None,
            "quantity": 1,
            "metadata": {},
            "sku": "cc",
            "hs_code": None,
            "value_amount": None,
            "value_currency": None,
            "weight": 4.0,
            "weight_unit": "KG",
        }
    ],
    "content_description": None,
    "content_type": None,
    "duty": None,
    "id": ANY,
    "object_type": "customs_info",
    "incoterm": "DDU",
    "invoice": None,
    "invoice_date": None,
    "options": {},
    "signer": None,
}

CUSTOMS_UPDATE_DATA = {"incoterm": "DDP"}

CUSTOMS_UPDATE_RESPONSE = {
    "certify": None,
    "commercial_invoice": None,
    "commodities": [],
    "content_description": None,
    "content_type": None,
    "duty": None,
    "id": ANY,
    "object_type": "customs_info",
    "incoterm": "DDP",
    "invoice": None,
    "invoice_date": None,
    "options": {},
    "signer": None,
}
