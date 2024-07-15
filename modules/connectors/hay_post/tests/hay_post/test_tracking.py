import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestHayPostTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest.get("tracking_numbers"))

    def test_get_tracking(self):
        with patch("karrio.mappers.hay_post.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/Api/Order/Tracking/{TrackingNumber}",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.hay_post.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)


if __name__ == "__main__":
    unittest.main()

TrackingNumber = "PAS105759416AM"

TrackingPayload = {
    "tracking_numbers": [TrackingNumber],
}

TrackingRequest = {
    "tracking_numbers": [TrackingNumber]
}

TrackingResponse = """{
    "order": {
        "id": 15022783,
        "customerId": 999999999,
        "trackingId": "PAS105759416AM",
        "amount": 1810,
        "weight": 100,
        "stateId": 1,
        "comment": "Test",
        "service": {
            "id": 4,
            "name": "Parcel"
        },
        "category": {
            "id": 1,
            "name": "Simple"
        },
        "transactionId": null,
        "bundle": null,
        "shipment": null,
        "createDate": "2024-06-10T08:59:21",
        "isVerified": false,
        "recaddress": null,
        "locationId": null,
        "codAmount": null,
        "paymentMethodId": 0,
        "isInternational": false,
        "partner": null
    },
    "info": null,
    "orderDestinationAddress": {
        "country": {
            "id": 11,
            "name": "Armenia"
        },
        "provinceState": {
            "id": 27,
            "name": "ԵՐԵՎԱՆ"
        },
        "cityVillage": {
            "id": 0,
            "name": "Երևան"
        },
        "street": {
            "id": 0,
            "name": "Սարյան"
        },
        "building": {
            "id": 0,
            "name": "22"
        },
        "apartment": {
            "id": 0,
            "name": "2"
        },
        "postalCode": "0002",
        "address": null,
        "isHomeDelivery": false,
        "isDeliveryPaid": false,
        "deliveryDate": "0001-01-01T00:00:00",
        "receiverInfo": {
            "companyName": "string",
            "firstName": "Գրտեստ",
            "lastName": "Գրտեստ",
            "phoneNumber": "37477885882",
            "email": "string",
            "nickname": null
        },
        "factreceiverInfo": null
    },
    "returnAddress": {
        "country": {
            "id": 11,
            "name": null
        },
        "provinceState": {
            "id": 29,
            "name": "ԿՈՏԱՅՔ"
        },
        "cityVillage": {
            "id": 0,
            "name": "ԿՈՏԱՅՔ"
        },
        "street": {
            "id": 0,
            "name": "ԿՈՏԱՅՔ"
        },
        "building": {
            "id": 0,
            "name": "ԿՈՏԱՅՔ"
        },
        "apartment": {
            "id": 0,
            "name": null
        },
        "postalCode": null,
        "address": null,
        "isHomeDelivery": false,
        "isDeliveryPaid": false,
        "deliveryDate": "0001-01-01T00:00:00",
        "receiverInfo": {
            "companyName": null,
            "firstName": "testCustomer",
            "lastName": "testCustomer",
            "phoneNumber": null,
            "email": null,
            "nickname": null
        },
        "factreceiverInfo": null
    },
    "customer": {
        "customerId": 999999999,
        "firstName": "testCustomer",
        "lastName": "testCustomer",
        "phone": null,
        "legalType": {
            "id": 3,
            "name": "Legal"
        },
        "documents": [],
        "companyName": null
    },
    "orderStateHistories": [
        {
            "id": 59700773,
            "orderId": 15022783,
            "stateId": 1,
            "createDate": "2024-06-10T08:59:20.5298",
            "userId": 999999999,
            "isActive": true
        }
    ],
    "additionalServices": [
        {
            "id": 2,
            "name": "Notification Ordered",
            "fee": 380,
            "key": "add_s_notification_ordered",
            "relationIndexId": 12,
            "isActive": true
        }
    ],
    "rejectedOrders": []
}
"""

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "hay_post",
            "carrier_name": "hay_post",
            "delivered": False,
            "events": [
                {
                    "date": "2024-06-10",
                    "description": "Test",
                    "time": "2024-06-10"
                }
            ],
            "info": {
                "customer_name": "testCustomer testCustomer",
                "note": "Test",
                "order_date": "2024-06-10",
                "order_id": "15022783",
                "package_weight": "100",
                "shipment_destination_country": "Armenia",
                "shipment_destination_postal_code": "Armenia",
                "shipment_pickup_date": "2024-06-10",
                "shipment_service": "Parcel"
            },
            "status": "in_transit",
            "tracking_number": "PAS105759416AM"
        }
    ],
    []
]
