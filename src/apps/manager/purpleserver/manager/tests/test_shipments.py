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
            "weight": 1.0,
            "package_preset": "canadapost_corrugated_small_box",
            "user": self.user
        })
        self.payment: models.Payment = models.Payment.objects.create(**{
            "currency": "CAD",
            "paid_by": "sender",
            "user": self.user
        })
        self.shipment: models.Shipment = models.Shipment.objects.create(
            shipper=self.shipper,
            recipient=self.recipient,
            payment=self.payment,
            user=self.user,
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
        self.assertDictEqual(dict(rates=response_data['shipment']['rates']), SHIPMENT_RATES)


class TestShipmentPurchase(TestShipmentFixture):
    def setUp(self) -> None:
        super().setUp()
        self.shipment.shipment_rates = [
            {
                "id": "rat_f5c1317021cb4b3c8a5d3b7369ed99e4",
                "carrier_ref": models.Carrier.objects.get(carrier_id="canadapost").pk,
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
        self.shipment.save()

        with patch("purpleserver.core.gateway.identity") as mock:
            mock.return_value = RETURNED_CANCEL_VALUE
            response = self.client.delete(url)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, CANCEL_PURCHASED_RESPONSE)


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
    "parcels": [{
        "weight": 1,
        "packagePreset": "canadapost_corrugated_small_box"
    }],
    "payment": {
        "currency": "CAD",
        "paidBy": "sender"
    },
    "carrierIds": ["canadapost"]
}

SHIPMENT_RATES = {
    "rates": [
        {
            "id": ANY,
            "carrierRef": ANY,
            "baseCharge": 101.83,
            "carrierId": "canadapost",
            "carrierName": "canadapost",
            "currency": "CAD",
            "discount": -9.04,
            "dutiesAndTaxes": 13.92,
            "extraCharges": [
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
            "totalCharge": 106.71,
            "transitDays": 2,
            "meta": None,
            "testMode": True
        }
    ]
}

SHIPMENT_RESPONSE = {
    "id": ANY,
    "status": "created",
    "carrierName": None,
    "carrierId": None,
    "label": None,
    "meta": {},
    "trackingNumber": None,
    "selectedRate": None,
    "selectedRateId": None,
    **SHIPMENT_RATES,
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
    "parcels": [{
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
    }],
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
    ],
    "service": None,
    "createdAt": ANY,
    "shipmentIdentifier": ANY,
    "testMode": True
}


SHIPMENT_OPTIONS = {
    "insurance": {
        "amount": 54
    },
    "currency": "CAD"
}


RETURNED_RATES_VALUE = [(
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
)]


SHIPMENT_PURCHASE_DATA = {
    "selectedRateId": "rat_f5c1317021cb4b3c8a5d3b7369ed99e4"
}

SELECTED_RATE = {
    "id": ANY,
    "carrierRef": ANY,
    "baseCharge": 101.83,
    "carrierId": "canadapost",
    "carrierName": "canadapost",
    "currency": "CAD",
    "discount": -9.04,
    "dutiesAndTaxes": 13.92,
    "extraCharges": [
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
    "totalCharge": 106.71,
    "transitDays": 2,
    "meta": None,
    "testMode": True
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
    "messages": [],
    "shipment": {
        "id": ANY,
        "status": "purchased",
        "carrierName": "canadapost",
        "carrierId": "canadapost",
        "label": ANY,
        "meta": {},
        "trackingNumber": "123456789012",
        "shipmentIdentifier": "123456789012",
        "selectedRate": SELECTED_RATE,
        "selectedRateId": ANY,
        "service": "canadapost_priority",
        "rates": [SELECTED_RATE],
        "trackingUrl": "/v1/tracking_status/canadapost/123456789012?test",
        "shipper": {
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
        "parcels": [{
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
        }],
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
        "carrierIds": [],
        "createdAt": ANY,
        "testMode": True
    }
}

CANCEL_RESPONSE = {
  "messages": [],
  "confirmation": {
    "carrierName": "None Selected",
    "carrierId": "None Selected",
    "operation": "Cancel Shipment",
    "success": True
  }
}

CANCEL_PURCHASED_RESPONSE = {
  "messages": [],
  "confirmation": {
    "carrierName": "canadapost",
    "carrierId": "canadapost",
    "operation": "Cancel Shipment",
    "success": True
  }
}
