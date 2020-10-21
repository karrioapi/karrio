import json
from unittest.mock import patch, ANY
from django.urls import reverse
from rest_framework import status
from purplship.core.models import ShipmentDetails
from purpleserver.core.tests import APITestCase


class TestShipping(APITestCase):

    def test_shipping_request(self):
        url = reverse('purpleserver.proxy:shipping-request')
        data = SHIPPING_DATA

        with patch("purpleserver.core.gateway.identity") as mock:
            mock.return_value = RETURNED_VALUE
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertDictEqual(response_data, SHIPPING_RESPONSE)


SHIPPING_DATA = {
    "selectedRateId": "prx_a9b96e5a82f644b0921bfed3190b4d6c",
    "options": {},
    "recipient": {
        "addressLine1": "125 Church St",
        "personName": "John Doe",
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
        "phoneNumber": "514 000 0000",
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
    "rates": [
        {
            "baseCharge": 101.83,
            "carrierId": "canadapost",
            "carrierName": "canadapost",
            "currency": "CAD",
            "discount": -9.04,
            "dutiesAndTaxes": 13.92,
            "estimatedDelivery": "2020-06-22",
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
            "id": "prx_a9b96e5a82f644b0921bfed3190b4d6c",
            "service": "canadapost_priority",
            "totalCharge": 106.71,
            "testMode": True
        },
        {
            "baseCharge": 27.36,
            "carrierId": "canadapost",
            "carrierName": "canadapost",
            "currency": "CAD",
            "discount": -3.06,
            "dutiesAndTaxes": 3.65,
            "estimatedDelivery": "2020-07-02",
            "extraCharges": [
                {
                    "amount": 0.71,
                    "currency": "CAD",
                    "name": "Fuel surcharge"
                },
                {
                    "amount": -3.77,
                    "currency": "CAD",
                    "name": "SMB Savings"
                }
            ],
            "id": "prx_9290e4a2c8e34c8d8c73ab990b029f3d",
            "service": "canadapost_regular_parcel",
            "totalCharge": 27.95,
            "testMode": True
        }
    ],
    "payment": {
        "currency": "CAD",
        "paidBy": "sender"
    }
}

RETURNED_VALUE = (
    ShipmentDetails(
        carrier_name="canadapost",
        carrier_id="canadapost",
        label="==apodifjoefr",
        tracking_number="123456789012",
        shipment_identifier="123456789012"
    ),
    [],
)

SHIPPING_RESPONSE = {
    'messages': [],
    'shipment': {
        'id': ANY,
        'status': 'purchased',
        'carrierName': 'canadapost',
        'carrierId': 'canadapost',
        'label': '==apodifjoefr',
        'trackingNumber': '123456789012',
        'shipmentIdentifier': '123456789012',
        'selectedRate': {
            'id': 'prx_a9b96e5a82f644b0921bfed3190b4d6c',
            'carrierName': 'canadapost',
            'carrierId': 'canadapost',
            'currency': 'CAD',
            'service': 'canadapost_priority',
            'discount': -9.04,
            'baseCharge': 101.83,
            'totalCharge': 106.71,
            'dutiesAndTaxes': 13.92,
            'transitDays': None,
            'extraCharges': [
                {
                    'name': 'Fuel surcharge',
                    'amount': 2.7,
                    'currency': 'CAD'
                },
                {
                    'name': 'SMB Savings',
                    'amount': -11.74,
                    'currency': 'CAD'
                }
            ],
            'meta': None,
            'carrierRef': None,
            'testMode': True
        },
        'selectedRateId': 'prx_a9b96e5a82f644b0921bfed3190b4d6c',
        'rates': [
            {
                'id': 'prx_a9b96e5a82f644b0921bfed3190b4d6c',
                'carrierName': 'canadapost',
                'carrierId': 'canadapost',
                'currency': 'CAD',
                'service': 'canadapost_priority',
                'discount': -9.04,
                'baseCharge': 101.83,
                'totalCharge': 106.71,
                'dutiesAndTaxes': 13.92,
                'transitDays': None,
                'extraCharges': [
                    {
                        'name': 'Fuel surcharge',
                        'amount': 2.7,
                        'currency': 'CAD'
                    },
                    {
                        'name': 'SMB Savings',
                        'amount': -11.74,
                        'currency': 'CAD'
                    }
                ],
                'meta': None,
                'carrierRef': None,
                'testMode': True
            },
            {
                'id': 'prx_9290e4a2c8e34c8d8c73ab990b029f3d',
                'carrierName': 'canadapost',
                'carrierId': 'canadapost',
                'currency': 'CAD',
                'service': 'canadapost_regular_parcel',
                'discount': -3.06,
                'baseCharge': 27.36,
                'totalCharge': 27.95,
                'dutiesAndTaxes': 3.65,
                'transitDays': None,
                'extraCharges': [
                    {
                        'name': 'Fuel surcharge',
                        'amount': 0.71,
                        'currency': 'CAD'
                    },
                    {
                        'name': 'SMB Savings',
                        'amount': -3.77,
                        'currency': 'CAD'
                    }
                ],
                'meta': None,
                'carrierRef': None,
                'testMode': True
            }
        ],
        'trackingUrl': '/v1/proxy/tracking/canadapost/123456789012?test',
        'service': 'canadapost_priority',
        'shipper': {
            'id': None,
            'postalCode': 'V6M2V9',
            'city': 'Vancouver',
            'federalTaxId': None,
            'stateTaxId': None,
            'personName': 'Jane Doe',
            'companyName': 'B corp.',
            'countryCode': 'CA',
            'email': None,
            'phoneNumber': '514 000 0000',
            'stateCode': 'BC',
            'suburb': None,
            'residential': False,
            'addressLine1': '5840 Oak St',
            'addressLine2': ''
        },
        'recipient': {
            'id': None,
            'postalCode': 'E1C4Z8',
            'city': 'Moncton',
            'federalTaxId': None,
            'stateTaxId': None,
            'personName': 'John Doe',
            'companyName': 'A corp.',
            'countryCode': 'CA',
            'email': None,
            'phoneNumber': '514 000 0000',
            'stateCode': 'NB',
            'suburb': None,
            'residential': False,
            'addressLine1': '125 Church St',
            'addressLine2': ''
        },
        'parcels': [
            {
                'id': None,
                'weight': 1.0,
                'width': None,
                'height': None,
                'length': None,
                'packagingType': None,
                'packagePreset': 'canadapost_corrugated_small_box',
                'description': None,
                'content': None,
                'isDocument': False,
                'weightUnit': None,
                'dimensionUnit': None
            }
        ],
        'services': [],
        'options': {},
        'payment': {
            'id': None,
            'paidBy': 'sender',
            'amount': None,
            'currency': 'CAD',
            'accountNumber': None,
            'creditCard': None,
            'contact': None
        },
        'customs': None,
        'docImages': [],
        'reference': '',
        'carrierIds': [],
        'meta': None,
        'createdAt': ANY,
        'testMode': True
    }
}