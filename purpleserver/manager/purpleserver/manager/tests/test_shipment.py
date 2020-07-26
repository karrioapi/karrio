import json
from unittest.mock import ANY
from django.urls import reverse
from rest_framework import status
from purpleserver.core.tests import APITestCase
import purpleserver.manager.models as models


class TestParcels(APITestCase):

    def test_create_shipment(self):
        url = reverse('purpleserver.manager:shipment-list')
        data = SHIPMENT_DATA

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response_data, SHIPMENT_RESPONSE)


class TestParcelDetails(APITestCase):
    def setUp(self) -> None:
        super().setUp()

        self.shipper: models.Address = models.Address.objects.create(**{
            "postal_code": "E1C4Z8",
            "city": "Moncton",
            "federal_tax_id": None,
            "state_tax_id": None,
            "person_name": "John Poop",
            "company_name": "A corp.",
            "country_code": "CA",
            "email": None,
            "phone_number": "514 000 0000",
            "state_code": "NB",
            "suburb": None,
            "residential": False,
            "address_line1": "125 Church St",
            "address_line2": None,
            "user": self.user
        })
        self.recipient: models.Address = models.Address.objects.create(**{
            "postal_code": "V6M2V9",
            "city": "Vancouver",
            "federal_tax_id": None,
            "state_tax_id": None,
            "person_name": "Jane Doe",
            "company_name": "B corp.",
            "country_code": "CA",
            "email": None,
            "phone_number": "514 000 9999",
            "state_code": "BC",
            "suburb": None,
            "residential": False,
            "address_line1": "5840 Oak St",
            "address_line2": None,
            "user": self.user
        })
        self.parcel: models.Parcel = models.Parcel.objects.create(**{
            "weight": 1,
            "width": 20,
            "height": 10,
            "length": 29,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "user": self.user
        })
        self.shipment: models.Shipment = models.Shipment.objects.create(
            shipper=self.shipper,
            recipient=self.recipient,
            parcel=self.parcel,
            user=self.user
        )

    def test_update_shipment(self):
        url = reverse('purpleserver.manager:shipment-details', kwargs=dict(pk=self.shipment.pk))
        data = SHIPMENT_UPDATE_DATA

        response = self.client.patch(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, SHIPMENT_UPDATE_RESPONSE)


SHIPMENT_DATA = {
    "recipient": {
        "addressLine1": "125 Church St",
        "personName": "John Poop",
        "companyName": "A corp.",
        "phoneNumber": "514 000 0000",
        "city": "Moncton",
        "countryCode": "CA",
        "postalCode": "E1C4Z8",
        "residential": False,
        "stateCode": "NB"
    },
    "shipper": {
        "addressLine1": "5840 Oak St",
        "personName": "Jane Doe",
        "companyName": "B corp.",
        "phoneNumber": "514 000 9999",
        "city": "Vancouver",
        "countryCode": "CA",
        "postalCode": "V6M2V9",
        "residential": False,
        "stateCode": "BC"
    },
    "parcel": {
        "weight": 1,
        "packagePreset": "canadapost_corrugated_small_box"
    },
    "payment": {
        "currency": "CAD",
        "paidBy": "sender"
    },
    "carrierIds": ["canadapost"]
}

SHIPMENT_RESPONSE = {
    "id": ANY,
    "status": "created",
    "carrierName": None,
    "carrierId": None,
    "label": None,
    "trackingNumber": None,
    "selectedRate": None,
    "selectedRateId": None,
    "rates": [],
    "trackingUrl": None,
    "shipper": {
        "id": ANY,
        "postalCode": "V6M2V9",
        "city": "Vancouver",
        "federalTaxId": None,
        "stateTaxId": None,
        "personName": "Jane Doe",
        "companyName": "B corp.",
        "countryCode": "CA",
        "email": None,
        "phoneNumber": "514 000 9999",
        "stateCode": "BC",
        "suburb": None,
        "residential": False,
        "addressLine1": "5840 Oak St",
        "addressLine2": None
    },
    "recipient": {
        "id": ANY,
        "postalCode": "E1C4Z8",
        "city": "Moncton",
        "federalTaxId": None,
        "stateTaxId": None,
        "personName": "John Poop",
        "companyName": "A corp.",
        "countryCode": "CA",
        "email": None,
        "phoneNumber": "514 000 0000",
        "stateCode": "NB",
        "suburb": None,
        "residential": False,
        "addressLine1": "125 Church St",
        "addressLine2": None
    },
    "parcel": {
        "id": ANY,
        "weight": 1.0,
        "width": None,
        "height": None,
        "length": None,
        "packagingType": None,
        "packagePreset": "canadapost_corrugated_small_box",
        "description": None,
        "content": None,
        "isDocument": False,
        "weightUnit": None,
        "dimensionUnit": None
    },
    "services": [],
    "options": {},
    "payment": {
        "id": ANY,
        "paidBy": "sender",
        "amount": None,
        "currency": "CAD",
        "accountNumber": None,
        "creditCard": None,
        "contact": None
    },
    "customs": None,
    "docImages": [],
    "reference": None,
    "carrierIds": [
        "canadapost"
    ]
}

SHIPMENT_UPDATE_DATA = {
    "shipper": {
        "personName": "John Doe",
    },
    "customs": {
        "terms_of_trade": "DDU"
    }
}

SHIPMENT_UPDATE_RESPONSE = {
    "id": ANY,
    "status": "created",
    "carrierName": None,
    "carrierId": None,
    "label": None,
    "trackingNumber": None,
    "selectedRate": None,
    "selectedRateId": None,
    "rates": [],
    "trackingUrl": None,
    "shipper": {
        "id": ANY,
        "postalCode": "E1C4Z8",
        "city": "Moncton",
        "federalTaxId": None,
        "stateTaxId": None,
        "personName": "John Doe",
        "companyName": "A corp.",
        "countryCode": "CA",
        "email": None,
        "phoneNumber": "514 000 0000",
        "stateCode": "NB",
        "suburb": None,
        "residential": False,
        "addressLine1": "125 Church St",
        "addressLine2": None
    },
    "recipient": {
        "id": ANY,
        "postalCode": "V6M2V9",
        "city": "Vancouver",
        "federalTaxId": None,
        "stateTaxId": None,
        "personName": "Jane Doe",
        "companyName": "B corp.",
        "countryCode": "CA",
        "email": None,
        "phoneNumber": "514 000 9999",
        "stateCode": "BC",
        "suburb": None,
        "residential": False,
        "addressLine1": "5840 Oak St",
        "addressLine2": None
    },
    "parcel": {
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
    },
    "services": [],
    "options": {},
    "payment": None,
    "customs": {
        "id": ANY,
        "noEei": None,
        "aes": None,
        "description": None,
        "termsOfTrade": "DDU",
        "commodities": None,
        "duty": None,
        "invoice": None,
        "commercialInvoice": None
    },
    "docImages": [],
    "reference": None,
    "carrierIds": []
}
