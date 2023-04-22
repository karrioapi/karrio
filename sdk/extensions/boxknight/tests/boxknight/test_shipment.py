import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestBoxKnightShipping(unittest.TestCase):
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
        with patch("karrio.mappers.boxknight.proxy.lib.request") as mocks:
            mocks.side_effect = [ShipmentResponse, ""]
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            create, download = mocks.call_args_list
            self.assertEqual(
                create[1]["url"],
                f"{gateway.settings.server_url}/orders",
            )
            self.assertEqual(
                download[1]["url"],
                f"{gateway.settings.server_url}/labels/11a7838-s74hhd8004-343398583d-33895?format=pdf",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.boxknight.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/orders/11a7838-s74hhd8004-343398583d-33895",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.boxknight.proxy.lib.request") as mocks:
            mocks.side_effect = [ShipmentResponse, ""]
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.boxknight.proxy.lib.request") as mock:
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
    "service": "boxknight_sameday",
    "reference": "shopifyid1234",
    "shipper": {
        "postal_code": "H4R 2A4",
        "address_line1": "4455A Boul. Poirier",
        "address_line2": "unit204 - BoxKnight HQ",
        "city": "Montreal",
        "state_code": "QC",
        "country_code": "CA",
        "residential": False,
        "company_name": "Metro Fleury No 2",
    },
    "recipient": {
        "person_name": "Charles Carmichael",
        "phone_number": "+15145573849",
        "postal_code": "H4R 2A4",
        "email": "charles.carmichael@boxknight.com",
        "address_line1": "4455A Boul. Poirier",
        "address_line2": "unit204 - BoxKnight HQ",
        "city": "Montreal",
        "state_code": "QC",
        "country_code": "CA",
        "residential": False,
    },
    "parcels": [
        {
            "height": 15.0,
            "length": 20.0,
            "width": 15.0,
            "weight": 1.5,
            "dimension_unit": "IN",
            "weight_unit": "LB",
            "reference_number": "12345",
        }
    ],
    "options": {
        "signature_required": False,
        "boxknight_notes": "The entrance is through the green fence on the left. If no answer, leave behind the black bin.",
    },
}

ShipmentCancelPayload = {
    "shipment_identifier": "11a7838-s74hhd8004-343398583d-33895",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "boxknight",
        "carrier_name": "boxknight",
        "docs": {},
        "label_type": "pdf",
        "meta": {"service_name": "SAMEDAY"},
        "shipment_identifier": "11a7838-s74hhd8004-343398583d-33895",
        "tracking_number": "11a7838-s74hhd8004-343398583d-33895",
    },
    [],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "boxknight",
        "carrier_name": "boxknight",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequest = {
    "order": {
        "merchantDisplayName": "Metro Fleury No 2",
        "notes": "The entrance is through the green fence on the left. If no answer, leave behind the black bin.",
        "originAddress": {
            "city": "Montreal",
            "country": "Canada",
            "isBusinessAddress": True,
            "postalCode": "H4R 2A4",
            "province": "Quebec",
            "street": "4455A Boul. Poirier",
            "unit": "unit204 - BoxKnight HQ",
        },
        "packageCount": 1,
        "packages": [
            {
                "refNumber": "12345",
                "sizeOptions": {
                    "height": 15.0,
                    "length": 20.0,
                    "unit": "inch",
                    "width": 15.0,
                },
                "weightOptions": {"unit": "lb", "weight": 1.5},
            }
        ],
        "recipient": {
            "email": "charles.carmichael@boxknight.com",
            "name": "Charles Carmichael",
            "phone": "+15145573849",
        },
        "recipientAddress": {
            "city": "Montreal",
            "country": "Canada",
            "isBusinessAddress": True,
            "postalCode": "H4R 2A4",
            "province": "Quebec",
            "street": "4455A Boul. Poirier",
            "unit": "unit204 - BoxKnight HQ",
        },
        "refNumber": "shopifyid1234",
        "service": "SAMEDAY",
        "signatureRequired": False,
    },
    "label_type": "pdf",
}


ShipmentCancelRequest = {"order_id": "11a7838-s74hhd8004-343398583d-33895"}

ShipmentResponse = """{
  "id": "11a7838-s74hhd8004-343398583d-33895"
}
"""

ShipmentCancelResponse = """{
  "id": "93e11b39-0af8-40bb-742a-912375a09743",
  "createdAt": "2019-10-25T22:56:06.000Z",
  "createdBy": "93e66b39-0uf8-40bb-742a-911235a09743",
  "merchantId": "13e11b39-0uf8-40bb-742a-913125a09743",
  "orderStatus": "GEOCODED",
  "scanningRequired": true,
  "validAddress": true,
  "labelUrl": "https://label12345.s3.amazonaws.com/BoxKnight-ShippingLabel-1234567.zpl",
  "pdfLabelUrl": "https://label12345.s3.amazonaws.com/BoxKnight-ShippingLabel-1234567.pdf",
  "recipient": {
    "name": "Charles Carmichael",
    "phone": "+15145573849",
    "notes": "Do not text, call instead.",
    "email": "charles.carmichael@boxknight.com"
  },
  "recipientAddress": {
    "number": 1234,
    "street": "Boul. Poirier",
    "city": "Montreal",
    "province": "Quebec",
    "country": "Canada",
    "postalCode": "H4R 2A4",
    "sublocality": "Communauté-Urbaine-de-Montréal",
    "location": {
      "lat": 45.4755722,
      "lng": -73.61911979999999
    }
  },
  "originAddress": {
    "number": 1234,
    "street": "Boul. Poirier",
    "city": "Montreal",
    "province": "Quebec",
    "country": "Canada",
    "postalCode": "H4R 2A4",
    "sublocality": "Communauté-Urbaine-de-Montréal",
    "location": {
      "lat": 45.4755722,
      "lng": -73.61911979999999
    }
  },
  "packageCount": 3,
  "signatureRequired": true,
  "service": "SAMEDAY",
  "notes": "The entrance is through the green fence on the left. If no answer, leave behind the black bin.",
  "refNumber": "shopifyid1234",
  "completeAfter": 1578439750000,
  "completeBefore": 1578439950000,
  "merchantDisplayName": "Metro Fleury No 2"
}
"""
