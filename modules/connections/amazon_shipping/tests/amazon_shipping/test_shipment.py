import unittest
from unittest.mock import patch
from karrio.core.utils import DP
from karrio.core.models import ShipmentRequest, ShipmentCancelRequest
from karrio import Shipment
from .fixture import gateway


class TestAmazonShippingShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**SHIPMENT_PAYLOAD)
        self.ShipmentCancelRequest = ShipmentCancelRequest(**CANCEL_SHIPMENT_PAYLOAD)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequestJSON)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(request.serialize(), CancelShipmentRequestJSON)

    def test_create_shipment(self):
        with patch("karrio.mappers.amazon_shipping.proxy.lib.request") as mock:
            mock.return_value = "{}"
            Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipping/v1/purchaseShipment",
            )

    def test_create_cancel_shipment(self):
        with patch("karrio.mappers.amazon_shipping.proxy.lib.request") as mock:
            mock.return_value = "{}"
            Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipping/v1/shipments/{self.ShipmentCancelRequest.shipment_identifier}/cancel",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.amazon_shipping.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponseJSON
            response = Shipment.create(self.ShipmentRequest).from_(gateway)

            with patch(
                "karrio.providers.amazon_shipping.shipment.create.lib.image_to_pdf"
            ) as mock:
                mock.return_value = ""
                parsed_response = response.parse()

                self.assertListEqual(
                    DP.to_dict(parsed_response), ParsedShipmentResponse
                )

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.amazon_shipping.proxy.lib.request") as mock:
            mock.return_value = ""
            parsed_response = (
                Shipment.cancel(self.ShipmentCancelRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                DP.to_dict(parsed_response), ParsedCancelShipmentResponse
            )


if __name__ == "__main__":
    unittest.main()


SHIPMENT_PAYLOAD = {
    "service": "amazon_shipping_ups_next_day_air",
    "reference": "order #1111",
    "recipient": {
        "company_name": "AmazonShipping",
        "address_line1": "417 Montgomery Street",
        "address_line2": "5th Floor",
        "city": "San Francisco",
        "state_code": "CA",
        "postal_code": "94104",
        "phone_number": "415-528-7555",
    },
    "shipper": {
        "person_name": "George Costanza",
        "company_name": "Vandelay Industries",
        "address_line1": "1 E 161st St.",
        "city": "Bronx",
        "state_code": "NY",
        "postal_code": "10451",
    },
    "parcels": [{"length": 9.0, "width": 6.0, "height": 2.0, "weight": 10.0}],
}

CANCEL_SHIPMENT_PAYLOAD = {
    "shipment_identifier": "shipment_id",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "amazon_shipping",
        "carrier_name": "amazon_shipping",
        "docs": {},
        "label_type": "PDF",
        "meta": {"containerReferenceId": "CRI123456789"},
        "tracking_number": "1512748795322",
    },
    [],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "amazon_shipping",
        "carrier_name": "amazon_shipping",
        "operation": "cancel shipment",
        "success": True,
    },
    [],
]


ShipmentRequestJSON = {
    "clientReferenceId": "order #1111",
    "containers": [
        {
            "containerType": "PACKAGE",
            "dimensions": {"height": 2.0, "length": 9.0, "unit": "IN", "width": 6.0},
            "weight": {"unit": "LB", "value": 10.0},
        }
    ],
    "labelSpecification": {"labelFormat": "PNG", "labelStockSize": "4X6"},
    "serviceType": "amazon_shipping_ups_next_day_air",
    "shipFrom": {
        "addressLine1": "1 E 161st St.",
        "city": "Bronx",
        "name": "George Costanza",
        "stateOrRegion": "NY",
    },
    "shipTo": {
        "addressLine1": "417 Montgomery Street",
        "addressLine2": "5th Floor",
        "city": "San Francisco",
        "phoneNumber": "415-528-7555",
        "stateOrRegion": "CA",
    },
}

CancelShipmentRequestJSON = "shipment_id"

ShipmentResponseJSON = """{
  "shipmentId": "89108749065090",
  "serviceRate": {
    "billableWeight": {
      "value": 4,
      "unit": "kg"
    },
    "totalCharge": {
      "value": 3.5,
      "unit": "GBP"
    },
    "serviceType": "Amazon Shipping Standard",
    "promise": {
      "deliveryWindow": {
        "start": "2018-08-25T20:22:30.737Z",
        "end": "2018-08-26T20:22:30.737Z"
      },
      "receiveWindow": {
        "start": "2018-08-23T09:22:30.737Z",
        "end": "2018-08-23T11:22:30.737Z"
      }
    }
  },
  "labelResults": [
    {
      "containerReferenceId": "CRI123456789",
      "trackingId": "1512748795322",
      "label": {
        "labelStream": "iVBORw0KGgo...AAAARK5CYII=(Truncated)",
        "labelSpecification": {
          "labelFormat": "PNG",
          "labelStockSize": "4x6"
        }
      }
    }
  ]
}

"""
