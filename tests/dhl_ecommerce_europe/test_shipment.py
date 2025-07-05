import unittest
from unittest.mock import patch, ANY
from .fixture import gateway, ShipmentPayload

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestDHLEcommerceEuropeShipping(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(
            shipment_identifier="00340434292135100186"
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        # Check if the request structure is correct
        self.assertIn("plannedShippingDateAndTime", request.serialize())
        self.assertEqual(request.serialize()["productCode"], "V01PAK")

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        # Check if the cancel request has the tracking number
        self.assertIn("shipmentTrackingNumber", request.serialize())

    def test_create_shipment(self):
        with patch("karrio.mappers.dhl_ecommerce_europe.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            # Check if the correct URL is being called
            self.assertIn("api", mock.call_args[1]["url"])

    def test_cancel_shipment(self):
        with patch("karrio.mappers.dhl_ecommerce_europe.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            # Check if the correct URL is being called
            self.assertIn("api", mock.call_args[1]["url"])

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.dhl_ecommerce_europe.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            # Check if the response structure is correct
            parsed_data = lib.to_dict(parsed_response)
            self.assertEqual(len(parsed_data), 2)  # [shipment_details, messages]
            self.assertEqual(len(parsed_data[1]), 0)  # No error messages
            
            shipment_details = parsed_data[0]
            self.assertEqual(shipment_details['carrier_id'], 'dhl_ecommerce_europe')
            self.assertEqual(shipment_details['tracking_number'], '00340434292135100186')
            self.assertIn('docs', shipment_details)
            if shipment_details['docs']:
                self.assertIn('label', shipment_details['docs'])

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.dhl_ecommerce_europe.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedCancelResponse)


if __name__ == "__main__":
    unittest.main()

ParsedShipmentResponse = [
    {
        "carrier_id": "dhl_ecommerce_europe",
        "carrier_name": "dhl_ecommerce_europe",
        "label": "JVBERi0xLjQKJeLjz9MKNyAwIG9iago8PAovVHlwZSAvUGFnZQovUGFyZW50IDEgMCBSCi9NZWRpYUJveCBbIDAgMCA2MTIgNzkyIF0KL0Ny",
        "meta": {
            "charges": [
                {
                    "currencyType": "BILLC",
                    "price": 25.5,
                    "priceCurrency": "EUR",
                    "priceType": "TOTAL",
                    "serviceCodeMutuallyExclusive": False,
                }
            ],
            "documents": [
                {
                    "content": "JVBERi0xLjQKJeLjz9MKNyAwIG9iago8PAovVHlwZSAvUGFnZQovUGFyZW50IDEgMCBSCi9NZWRpYUJveCBbIDAgMCA2MTIgNzkyIF0KL0Ny",
                    "imageFormat": "PDF",
                    "typeCode": "waybill-doc",
                }
            ],
            "shipment_details": [
                {
                    "localProductCode": "V01PAK",
                    "productCode": "V01PAK",
                    "serviceHandlingFeatureCodes": [],
                    "shipmentTrackingNumber": "00340434292135100186",
                }
            ],
        },
        "shipment_identifier": "00340434292135100186",
        "tracking_number": "00340434292135100186",
    },
    [],
]

ParsedCancelResponse = [
    {
        "carrier_id": "dhl_ecommerce_europe",
        "carrier_name": "dhl_ecommerce_europe",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]

ShipmentResponse = """{
  "shipmentTrackingNumber": "00340434292135100186",
  "shipmentDetails": [
    {
      "shipmentTrackingNumber": "00340434292135100186",
      "productCode": "V01PAK",
      "localProductCode": "V01PAK",
      "serviceHandlingFeatureCodes": []
    }
  ],
  "documents": [
    {
      "imageFormat": "PDF",
      "content": "JVBERi0xLjQKJeLjz9MKNyAwIG9iago8PAovVHlwZSAvUGFnZQovUGFyZW50IDEgMCBSCi9NZWRpYUJveCBbIDAgMCA2MTIgNzkyIF0KL0Ny",
      "typeCode": "waybill-doc"
    }
  ],
  "onDemandDelivery": {
    "deliveryOption": "servicepoint",
    "location": "DE",
    "specialInstructions": [],
    "gateCode": "",
    "whereIsTheKey": "",
    "neighborName": "",
    "neighborHouseNumber": "",
    "authorizerName": "",
    "servicePointId": "8003-0900",
    "requestedDeliveryDate": "2025-01-22"
  },
  "shipmentCharges": [
    {
      "currencyType": "BILLC",
      "priceCurrency": "EUR",
      "price": 25.50,
      "priceType": "TOTAL",
      "serviceCodeMutuallyExclusive": false
    }
  ]
}"""

ShipmentCancelResponse = """{
  "success": true
}""" 
