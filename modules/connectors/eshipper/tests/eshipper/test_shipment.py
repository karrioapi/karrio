import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TesteShipperShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(
            **ShipmentCancelPayload
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequest)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(request.serialize(), ShipmentCancelRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.eshipper.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/v2/ship",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.eshipper.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/v2/ship/cancel",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.eshipper.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.eshipper.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelShipmentResponse
            )


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "service": "eshipper_canpar_ground",
    "shipper": {
        "company_name": "Test Company- From",
        "address_line1": "9, Van Der Graaf Court",
        "city": "Brampton",
        "postal_code": "L4T3T1",
        "country_code": "CA",
        "state_code": "CA-ON",
    },
    "recipient": {
        "company_name": "Test Company - Destination",
        "address_line1": "9, Van Der Graaf Court",
        "city": "Brampton",
        "postal_code": "L4T3T1",
        "country_code": "CA",
        "state_code": "CA-ON",
    },
    "parcels": [
        {
            "length": 15,
            "width": 10,
            "height": 12,
            "weight": 10,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "description": "Package 1 Description",
        },
        {
            "length": 15,
            "width": 10,
            "height": 10,
            "weight": 5,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "description": "Package 2 Description",
        },
    ],
    "options": {
        "shipping_date": "2024-07-16T10:30",
    },
}

ShipmentCancelPayload = {
    "shipment_identifier": "794947717776",
    "options": {"orderId": "1234567890"},
}

ParsedShipmentResponse = [
    {
        "carrier_id": "eshipper",
        "carrier_name": "eshipper",
        "docs": {"label": ANY},
        "label_type": "PDF",
        "meta": {
            "carrier_tracking_link": "https://www.purolator.com/en/shipping/tracker?pin=329041222335",
            "rate_provider": "purolator",
            "orderId": "8000000010948",
            "eshipper_carrier_name": "Purolator",
            "service_name": "eshipper_purolator_ground_1030",
            "tracking_numbers": ["329041222335"],
        },
        "shipment_identifier": "8000000010948",
        "tracking_number": "329041222335",
    },
    [],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "eshipper",
        "carrier_name": "eshipper",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequest = {
    "packages": {
        "packages": [
            {
                "description": "Package 1 Description",
                "dimensionUnit": "CM",
                "height": 12,
                "length": 15,
                "weight": 10,
                "weightUnit": "KG",
                "width": 10,
            },
            {
                "description": "Package 2 Description",
                "dimensionUnit": "CM",
                "height": 10,
                "length": 15,
                "weight": 5,
                "weightUnit": "KG",
                "width": 10,
            },
        ],
        "type": "Package",
    },
    "packagingUnit": "Metric",
    "scheduledShipDate": "2024-07-16 10:30",
    "serviceId": 4500,
    "from": {
        "address1": "9, Van Der Graaf Court",
        "attention": "Test Company- From",
        "city": "Brampton",
        "company": "Test Company- From",
        "country": "CA",
        "province": "CA-ON",
        "zip": "L4T3T1",
    },
    "to": {
        "address1": "9, Van Der Graaf Court",
        "attention": "Test Company - Destination",
        "city": "Brampton",
        "company": "Test Company - Destination",
        "country": "CA",
        "province": "CA-ON",
        "zip": "L4T3T1",
    },
}

ShipmentCancelRequest = {"order": {"orderId": "1234567890"}}


ShipmentResponse = """{
  "carrier": {
    "carrierName": "Purolator",
    "serviceName": "Purolator Ground 1030"
  },
  "customsInvoice": null,
  "labelData": {
    "label": [
      {
        "data": "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Ci9UeXBlL0ZvbnQKL1N1YnR5cGUvVHJ1ZVR5cGUKL0Jhc2VGb250L0FyaWFsLEJvbGQKL0VuY29kaW5nL1dpbkFuc2lFbmNvZGluZwovRm9udERlc2NyaXB0b3IgOSAwIFIKL0ZpcnN0Q2hhciAwCi9MYXN0Q2hhciAyNTUKL1dpZHRoc1s3NTAgNzUwIDc1MCA3NTAgNzUwIDc1MCA3NTAgNzUwIDc1MCA3NTAgNzUwIDc1MCA3NTAgNzUwIDc1MCA3NTAgNzUwIDc1MCA3NTAgNzUwIDc1MCA3NTAgNzUwIDc1MCA3NTAgNzUwIDc1MCA3NTAgNzUwIDc1MCA3NTAgNzUwIDI3NyAzMzMgNDc0IDU1NiA1NTYgODg5IDcyMiAyMzcgMzMzIDMzMyAzODkgNTgzIDI3NyAzMzMgMjc3IDI3NyA1NTYgNTU2IDU1NiA1NTYgNTU2IDU1NiA1NTYgNTU2IDU1NiA1NTYgMzMzIDMzMyA1ODMgNTgzIDU4MyA2MTAgOTc1IDcyMiA3MjIgNzIyIDcyMiA2NjYgNjEwIDc3NyA3MjIgMjc3IDU1NiA3MjIgNjEwIDgzMyA3MjIgNzc3IDY2NiA3NzcgNzIyIDY2NiA2MTAgNzIyIDY2NiA5NDMgNjY2IDY2NiA2MTAgMzMzIDI3NyAzMzMgNTgzIDU1NiAzMzMgNTU2IDYxMCA1NTYgNjEwIDU1NiAzMzMgNjEwIDYxMCAyNzcgMjc3IDU1NiAyNzcgODg5IDYxMCA2MTAgNjEwIDYxMCAzODkgNTU2IDMzMyA2MTAgNTU2IDc3NyA1NTYgNTU2IDUwMCAzODkgMjc5IDM4OSA1ODMgNzUwIDU1NiA3NTAgMjc3IDU1NiA1MDAgMTAwMCA1NTYgNTU2IDMzMyAxMDAwIDY2NiAzMzMgMTAwMCA3NTAgNjEwIDc1MCA3NTAgMjc3IDI3NyA1MDAgNTAwIDM1MCA1NTYgMTAwMCAzMzMgMTAwMCA1NTYgMzMzIDk0MyA3NTAgNTAwIDY2NiAyNzcgMzMzIDU1NiA1NTYgNTU2IDU1NiAyNzkgNTU2IDMzMyA3MzYgMzcwIDU1NiA1ODMgMzMzIDczNiA1NTIgMzk5IDU0OCAzMzMgMzMzIDMzMyA1NzYgNTU2IDMzMyAzMzMgMzMzIDM2NSA1NTYgODMzIDgzMyA4MzMgNjEwIDcyMiA3MjIgNzIyIDcyMiA3MjIgNzIyIDEwMDAgNzIyIDY2NiA2NjYgNjY2IDY2NiAyNzcgMjc3IDI3NyAyNzcgNzIyIDcyMiA3NzcgNzc3IDc3NyA3NzcgNzc3IDU4MyA3NzcgNzIyIDcyMiA3MjIgNzIyIDY2NiA2NjYgNjEwIDU1NiA1NTYgNTU2IDU1NiA1NTYgNTU2IDg4OSA1NTYgNTU2IDU1NiA1NTYgNTU2IDI3NyAyNzcgMjc3IDI3NyA2MTAgNjEwIDYxMCA2MTAgNjEwIDYxMCA2MTAgNTQ4IDYxMCA2MTAgNjEwIDYxMCA2MTAgNTU2IDYxMCA1NTZdCj4+CmVuZG9iagoxMSAwIG9iago8PAovVHlwZS9Gb250RGVzY3JpcHRvcgovQXNjZW50IDkwNQovQ2FwSGVpZ2h0IDcxNgovRGVzY2VudCAtMjEyCi9GbGFncyAzMgovRm9udEJCb3hbLTY2NSAtMzI1IDIwMDAgMTAwNl0KL0l0YWxpY0FuZ2xlIDAKL1N0ZW1WIDAKL1hIZWlnaHQgNTE5Ci9Gb250TmFtZS9BcmlhbAo+PgplbmRvYmoKMTIgMCBvYmoKPDwKL1R5cGUvRm9udAovU3VidHlwZS9UcnVlVHlwZQovQmFzZUZvbnQvQXJpYWwKL0VuY29kaW5nL1dpbkFuc2lFbmNvZGluZwovRm9udERlc2NyaXB0b3IgMTEgMCBSCi9GaXJzdENoYXIgMAovTGFzdENoYXIgMjU1Ci9XaWR0aHNbNzUwIDc1MCA3NTAgNzUwIDc1MCA3NTAgNzUwIDc1MCA3NTAgNzUwIDc1MCA3NTAgNzUwIDc1MCA3NTAgNzUwIDc1MCA3NTAgNzUwIDc1MCA3NTAgNzUwIDc1MCA3NTAgNzUwIDc1MCA3NTAgNzUwIDc1MCA3NTAgNzUwIDc1MCAyNzcgMjc3IDM1NCA1NTYgNTU2IDg4OSA2NjYgMTkwIDMzMyAzMzMgMzg5IDU4MyAyNzcgMzMzIDI3NyAyNzcgNTU2IDU1NiA1NTYgNTU2IDU1NiA1NTYgNTU2IDU1NiA1NTYgNTU2IDI3NyAyNzcgNTgzIDU4MyA1ODMgNTU2IDEwMTUgNjY2IDY2NiA3MjIgNzIyIDY2NiA2MTAgNzc3IDcyMiAyNzcgNTAwIDY2NiA1NTYgODMzIDcyMiA3NzcgNjY2IDc3NyA3MjIgNjY2IDYxMCA3MjIgNjY2IDk0MyA2NjYgNjY2IDYxMCAyNzcgMjc3IDI3NyA0NjkgNTU2IDMzMyA1NTYgNTU2IDUwMCA1NTYgNTU2IDI3NyA1NTYgNTU2IDIyMiAyMjIgNTAwIDIyMiA4MzMgNTU2IDU1NiA1NTYgNTU2IDMzMyA1MDAgMjc3IDU1NiA1MDAgNzIyIDUwMCA1MDAgNTAwIDMzMyAyNTkgMzMzIDU4MyA3NTAgNTU2IDc1MCAyMjIgNTU2IDMzMyAxMDAwIDU1NiA1NTYgMzMzIDEwMDAgNjY2IDMzMyAxMDAwIDc1MCA2MTAgNzUwIDc1MCAyMjIgMjIyIDMzMyAzMzMgMzUwIDU1NiAxMDAwIDMzMyAxMDAwIDUwMCAzMzMgOTQzIDc1MCA1MDAgNjY2IDI3NyAzMzMgNTU2IDU1NiA1NTYgNTU2IDI1OSA1NTYgMzMzIDczNiAzNzAgNTU2IDU4MyAzMzMgNzM2IDU1MiAzOTkgNTQ4IDMzMyAzMzMgMzMzIDU3NiA1MzcgMzMzIDMzMyAzMzMgMzY1IDU1NiA4MzMgODMzIDgzMyA2MTAgNjY2IDY2NiA2NjYgNjY2IDY2NiA2NjYgMTAwMCA3MjIgNjY2IDY2NiA2NjYgNjY2IDI3NyAyNzcgMjc3IDI3NyA3MjIgNzIyIDc3NyA3NzcgNzc3IDc3NyA3NzcgNTgzIDc3NyA3MjIgNzIyIDcyMiA3MjIgNjY2IDY2NiA2MTAgNTU2IDU1NiA1NTYgNTU2IDU1NiA1NTYgODg5IDUwMCA1NTYgNTU2IDU1NiA1NTYgMjc3IDI3NyAyNzcgMjc3IDU1NiA1NTYgNTU2IDU1NiA1NTYgNTU2IDU1NiA1NDggNjEwIDU1NiA1NTYgNTU2IDU1NiA1MDAgNTU2IDUwMF0KPj4KZW5kb2JqCjEzIDAgb2JqCjw8Ci9UeXBlL1hPYmplY3QKL1N1YnR5cGUvSW1hZ2UKL0xlbmd0aCAxNzkzCi9GaWx0ZXIvRmxhdGVEZWNvZGUKL1dpZHRoIDg5OQovSGVpZ2h0IDMyNQovQml0c1BlckNvbXBvbmVudCAxCi9Db2xvclNwYWNlL0RldmljZUdyYXkKL0ludGVycG9sYXRlIHRydWUKPj4Kc3Ry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",
        "type": "pdf"
      }
    ]
  },
  "order": { "id": "8000000010948", "message": "" },
  "packages": [{ "trackingNumber": "329041222335" }],
  "packingSlip": null,
  "pickup": null,
  "quote": {
    "baseCharge": 120.68,
    "carrierName": "Purolator",
    "currency": "CAD",
    "fuelSurcharge": 14.48,
    "fuelSurchargePercentage": 12,
    "modeTransport": "AIR",
    "serviceId": 5000013,
    "serviceName": "Purolator Ground 1030",
    "surcharges": null,
    "taxes": null,
    "totalCharge": 141.92,
    "totalChargedAmount": 141.92,
    "transitDays": "5"
  },
  "reference": { "code": null, "name": null },
  "reference2": null,
  "reference3": null,
  "trackingNumber": "329041222335",
  "trackingUrl": "https://www.purolator.com/en/shipping/tracker?pin=329041222335"
}
"""

ShipmentCancelResponse = """{
  "order": [
    {
      "trackingId": "string",
      "orderId": "string",
      "message": "string"
    }
  ]
}
"""
