import json
from unittest.mock import ANY
from django.urls import reverse
from rest_framework import status
from purpleserver.core.tests import APITestCase
from purpleserver.manager.models import Customs


class TestCustomsInfo(APITestCase):

    def test_create_customs(self):
        url = reverse('purpleserver.manager:customs-list')
        data = CUSTOMS_DATA

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response_data, CUSTOMS_RESPONSE)


class TestCustomsInfoDetails(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.customs: Customs = Customs.objects.create(**{
            "user": self.user
        })

    def test_update_customs(self):
        url = reverse('purpleserver.manager:customs-details', kwargs=dict(pk=self.customs.pk))
        data = CUSTOMS_UPDATE_DATA

        response = self.client.patch(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, CUSTOMS_UPDATE_RESPONSE)


CUSTOMS_DATA = {
    "terms_of_trade": "DDU"
}

CUSTOMS_RESPONSE = {
    "id": ANY,
    "noEei": None,
    "aes": None,
    "description": None,
    "termsOfTrade": "DDU",
    "commodities": [],
    "duty": None,
    "invoice": None,
    "commercialInvoice": None
}

CUSTOMS_UPDATE_DATA = {
    "terms_of_trade": "DDP"
}

CUSTOMS_UPDATE_RESPONSE = {
    "id": ANY,
    "noEei": None,
    "aes": None,
    "description": None,
    "termsOfTrade": "DDP",
    "commodities": [],
    "duty": None,
    "invoice": None,
    "commercialInvoice": None
}
