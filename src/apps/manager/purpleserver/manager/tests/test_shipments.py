import json
from unittest.mock import ANY, patch
from django.urls import reverse
from rest_framework import status
from purplship.core.models import RateDetails, ChargeDetails, ShipmentDetails, ConfirmationDetails
from purpleserver.core.tests import APITestCase
import purpleserver.manager.models as models


class TestShipmentFixture(APITestCase):
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
            "validate_location": False,
            "validation": None,
            "created_by": self.user
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
            "validate_location": False,
            "validation": None,
            "created_by": self.user
        })
        self.parcel: models.Parcel = models.Parcel.objects.create(**{
            "weight": 1.0,
            "weight_unit": "KG",
            "package_preset": "canadapost_corrugated_small_box",
            "created_by": self.user
        })
        self.payment: models.Payment = models.Payment.objects.create(**{
            "currency": "CAD",
            "paid_by": "sender",
            "created_by": self.user
        })
        self.shipment: models.Shipment = models.Shipment.objects.create(
            shipper=self.shipper,
            recipient=self.recipient,
            payment=self.payment,
            created_by=self.user,
            test_mode=True,
        )
        self.shipment.shipment_parcels.set([self.parcel])


class TestShipments(APITestCase):

    def test_create_shipment(self):
        url = reverse('purpleserver.manager:shipment-list')
        data = SHIPMENT_DATA

        with patch("purpleserver.core.gateway.identity") as mock:
            mock.return_value = RETURNED_RATES_VALUE
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response_data, SHIPMENT_RESPONSE)


class TestShipmentDetails(TestShipmentFixture):
    def test_add_shipment_option(self):
        url = reverse('purpleserver.manager:shipment-options', kwargs=dict(pk=self.shipment.pk))
        data = SHIPMENT_OPTIONS

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data.get('options'), SHIPMENT_OPTIONS)

    def test_shipment_rates(self):
        url = reverse('purpleserver.manager:shipment-rates', kwargs=dict(pk=self.shipment.pk))

        with patch("purpleserver.core.gateway.identity") as mock:
            mock.return_value = RETURNED_RATES_VALUE
            response = self.client.get(url)
            response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(dict(rates=response_data['rates']), SHIPMENT_RATES)


class TestShipmentPurchase(TestShipmentFixture):
    def setUp(self) -> None:
        super().setUp()
        carrier = models.Carrier.objects.get(carrier_id="canadapost")
        self.shipment.shipment_rates = [
            {
                "id": "rat_f5c1317021cb4b3c8a5d3b7369ed99e4",
                "carrier_ref": carrier.pk,
                "base_charge": 101.83,
                "carrier_id": "canadapost",
                "carrier_name": "canadapost",
                "currency": "CAD",
                "discount": -9.04,
                "duties_and_taxes": 13.92,
                "extra_charges": [
                    {
                        "amount": 2.7,
                        "currency": "CAD",
                        "name": "Fuel surcharge"
                    },
                    {
                        "amount": -11.74,
                        "currency": "CAD",
                        "name": "SMB Savings"
                    }
                ],
                "service": "canadapost_priority",
                "total_charge": 106.71,
                "transit_days": 2,
                "test_mode": True
            }
        ]
        self.shipment.save()

    def test_purchase_shipment(self):
        url = reverse('purpleserver.manager:shipment-purchase', kwargs=dict(pk=self.shipment.pk))
        data = SHIPMENT_PURCHASE_DATA

        with patch("purpleserver.core.gateway.identity") as mock:
            mock.return_value = CREATED_SHIPMENT_RESPONSE
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, PURCHASED_SHIPMENT)

    def test_cancel_shipment(self):
        url = reverse('purpleserver.manager:shipment-details', kwargs=dict(pk=self.shipment.pk))

        with patch("purpleserver.core.gateway.identity") as mock:
            response = self.client.delete(url)
            response_data = json.loads(response.content)

            mock.assert_not_called()
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, CANCEL_RESPONSE)

    def test_cancel_purchased_shipment(self):
        url = reverse('purpleserver.manager:shipment-details', kwargs=dict(pk=self.shipment.pk))
        self.shipment.status = "purchased"
        self.shipment.shipment_identifier = "123456789012"
        self.shipment.selected_rate_carrier = self.carrier
        self.shipment.save()

        with patch("purpleserver.core.gateway.identity") as mock:
            mock.return_value = RETURNED_CANCEL_VALUE
            response = self.client.delete(url)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, CANCEL_PURCHASED_RESPONSE)


SHIPMENT_DATA = {
    "recipient": {
        "address_line1": "125 Church St",
        "person_name": "John Poop",
        "company_name": "A corp.",
        "phone_number": "514 000 0000",
        "city": "Moncton",
        "country_code": "CA",
        "postal_code": "E1C4Z8",
        "residential": False,
        "state_code": "NB"
    },
    "shipper": {
        "address_line1": "5840 Oak St",
        "person_name": "Jane Doe",
        "company_name": "B corp.",
        "phone_number": "514 000 9999",
        "city": "Vancouver",
        "country_code": "CA",
        "postal_code": "V6M2V9",
        "residential": False,
        "state_code": "BC"
    },
    "parcels": [{
        "weight": 1,
        "weight_unit": "KG",
        "package_preset": "canadapost_corrugated_small_box"
    }],
    "payment": {
        "currency": "CAD",
        "paid_by": "sender"
    },
    "carrier_ids": ["canadapost"]
}

SHIPMENT_RATES = {
    "rates": [
        {
            "id": ANY,
            "carrier_ref": ANY,
            "base_charge": 101.83,
            "carrier_id": "canadapost",
            "carrier_name": "canadapost",
            "currency": "CAD",
            "discount": -9.04,
            "duties_and_taxes": 13.92,
            "extra_charges": [
                {
                    "amount": 2.7,
                    "currency": "CAD",
                    "name": "Fuel surcharge"
                },
                {
                    "amount": -11.74,
                    "currency": "CAD",
                    "name": "SMB Savings"
                }
            ],
            "service": "canadapost_priority",
            "total_charge": 106.71,
            "transit_days": 2,
            "meta": None,
            "test_mode": True
        }
    ]
}

SHIPMENT_RESPONSE = {
    "id": ANY,
    "status": "created",
    "carrier_name": None,
    "carrier_id": None,
    "label": None,
    "label_type": "PDF",
    "meta": {},
    "tracking_number": None,
    "shipment_identifier": None,
    "selected_rate": None,
    "selected_rate_id": None,
    **SHIPMENT_RATES,
    "tracking_url": None,
    "shipper": {
        "id": ANY,
        "postal_code": "V6M2V9",
        "city": "Vancouver",
        "federal_tax_id": None,
        "state_tax_id": None,
        "person_name": "Jane Doe",
        "company_name": "B corp.",
        "country_code": "CA",
        "email": None,
        "phone_number": "+1 514-000-9999",
        "state_code": "BC",
        "suburb": None,
        "residential": False,
        "address_line1": "5840 Oak St",
        "address_line2": None,
        "validate_location": False,
        "validation": None
    },
    "recipient": {
        "id": ANY,
        "postal_code": "E1C4Z8",
        "city": "Moncton",
        "federal_tax_id": None,
        "state_tax_id": None,
        "person_name": "John Poop",
        "company_name": "A corp.",
        "country_code": "CA",
        "email": None,
        "phone_number": "+1 514-000-0000",
        "state_code": "NB",
        "suburb": None,
        "residential": False,
        "address_line1": "125 Church St",
        "address_line2": None,
        "validate_location": False,
        "validation": None
    },
    "parcels": [{
        "id": ANY,
        "weight": 1.0,
        "width": 42.0,
        "height": 32.0,
        "length": 32.0,
        "packaging_type": None,
        "package_preset": "canadapost_corrugated_small_box",
        "description": None,
        "content": None,
        "is_document": False,
        "weight_unit": "KG",
        "dimension_unit": "CM"
    }],
    "services": [],
    "options": {},
    "payment": {
        "id": ANY,
        "paid_by": "sender",
        "amount": None,
        "currency": "CAD",
        "account_number": None,
        "contact": None
    },
    "customs": None,
    "reference": None,
    "carrier_ids": [
        "canadapost"
    ],
    "service": None,
    "created_at": ANY,
    "test_mode": True,
    "messages": []
}


SHIPMENT_OPTIONS = {
    "insurance": {
        "amount": 54
    },
    "currency": "CAD"
}


RETURNED_RATES_VALUE = (
    [
        RateDetails(
            carrier_id="canadapost",
            carrier_name="canadapost",
            currency="CAD",
            transit_days=2,
            service="canadapost_priority",
            discount=-9.04,
            base_charge=101.83,
            total_charge=106.71,
            duties_and_taxes=13.92,
            extra_charges=[
                ChargeDetails(
                    amount=2.7,
                    currency="CAD",
                    name="Fuel surcharge"
                ),
                ChargeDetails(
                    amount=-11.74,
                    currency="CAD",
                    name="SMB Savings"
                )
            ]
        )
    ],
    [],
)


SHIPMENT_PURCHASE_DATA = {
    "selected_rate_id": "rat_f5c1317021cb4b3c8a5d3b7369ed99e4"
}

SELECTED_RATE = {
    "id": ANY,
    "carrier_ref": ANY,
    "base_charge": 101.83,
    "carrier_id": "canadapost",
    "carrier_name": "canadapost",
    "currency": "CAD",
    "discount": -9.04,
    "duties_and_taxes": 13.92,
    "extra_charges": [
        {
            "amount": 2.7,
            "currency": "CAD",
            "name": "Fuel surcharge"
        },
        {
            "amount": -11.74,
            "currency": "CAD",
            "name": "SMB Savings"
        }
    ],
    "service": "canadapost_priority",
    "total_charge": 106.71,
    "transit_days": 2,
    "meta": None,
    "test_mode": True
}

CREATED_SHIPMENT_RESPONSE = (
    ShipmentDetails(
        carrier_id="canadapost",
        carrier_name="canadapost",
        label="==apodifjoefr",
        tracking_number="123456789012",
        shipment_identifier="123456789012"
    ),
    []
)

RETURNED_CANCEL_VALUE = (
    ConfirmationDetails(
        carrier_name="canadapost",
        carrier_id="canadapost",
        success=True,
        operation="Cancel Shipment"
    ),
    [],
)

PURCHASED_SHIPMENT = {
    "id": ANY,
    "status": "purchased",
    "carrier_name": "canadapost",
    "carrier_id": "canadapost",
    "label": ANY,
    "label_type": "PDF",
    "meta": {},
    "tracking_number": "123456789012",
    "shipment_identifier": "123456789012",
    "selected_rate": SELECTED_RATE,
    "selected_rate_id": ANY,
    "service": "canadapost_priority",
    "rates": [SELECTED_RATE],
    "tracking_url": "/v1/trackers/canadapost/123456789012?test",
    "shipper": {
        "id": ANY,
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
        "validate_location": False,
        "validation": None
    },
    "recipient": {
        "id": ANY,
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
        "validate_location": False,
        "validation": None
    },
    "parcels": [{
        "id": ANY,
        "weight": 1.0,
        "width": None,
        "height": None,
        "length": None,
        "packaging_type": None,
        "package_preset": "canadapost_corrugated_small_box",
        "description": None,
        "content": None,
        "is_document": False,
        "weight_unit": "KG",
        "dimension_unit": None
    }],
    "services": [],
    "options": {},
    "payment": {
        "id": ANY,
        "paid_by": "sender",
        "amount": None,
        "currency": "CAD",
        "account_number": None,
        "contact": None
    },
    "customs": None,
    "reference": None,
    "carrier_ids": [],
    "created_at": ANY,
    "test_mode": True,
    "messages": []
}

CANCEL_RESPONSE = {
  "messages": [],
  "confirmation": {
    "carrier_name": "None Selected",
    "carrier_id": "None Selected",
    "operation": "Cancel Shipment",
    "success": True
  }
}

CANCEL_PURCHASED_RESPONSE = {
  "messages": [],
  "confirmation": {
    "carrier_name": "canadapost",
    "carrier_id": "canadapost",
    "operation": "Cancel Shipment",
    "success": True
  }
}
