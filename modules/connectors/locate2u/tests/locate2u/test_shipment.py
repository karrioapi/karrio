import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestLocate2uShipping(unittest.TestCase):
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

    # def test_create_shipment(self):
    #     with patch("karrio.mappers.locate2u.proxy.lib.request") as mock:
    #         mock.return_value = "{}"
    #         karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

    #         self.assertEqual(
    #             mock.call_args[1]["url"],
    #             f"{gateway.settings.server_url}/api/v1/stops",
    #         )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.locate2u.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/v1/stops/164557",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.locate2u.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.locate2u.proxy.lib.request") as mock:
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
    "service": "locate2u_local_delivery",
    "shipper": {
        "company_name": "Shipper Name",
        "person_name": "Shipper Attn Name",
        "federal_tax_id": "123456",
        "phone_number": "1234567890",
        "address_line1": "Address Line",
        "city": "City",
        "state_code": "StateProvinceCode",
        "postal_code": "PostalCode",
    },
    "recipient": {
        "company_name": "Locate2u",
        "person_name": "Matthew Robinson",
        "phone_number": "0123456789",
        "address_line1": "Level 4, Suite 4.11, 55 Miller St",
        "city": "Pyrmont",
        "state_code": "2009",
        "postal_code": "NSW",
        "country_code": "AU",
        "email": "matt.robinson@email.com",
    },
    "parcels": [
        {
            "dimension_unit": "CM",
            "weight_unit": "KG",
            "length": 7,
            "width": 5,
            "height": 2,
            "weight": 10,
            "items": [
                {
                    "sku": "1234567890",
                    "description": "Item A - Barcode scanning item",
                    "quantity": 1,
                    "metadata": {"currentLocation": "Warehouse"},
                }
            ],
        }
    ],
    "options": {
        "notes": "Please call before you deliver",
        "shipment_date": "2023-09-08",
        "appointment_time": "12:00",
        "duration_minutes": 10,
        "longitude": 151.192487,
        "latitude": -33.8706672,
    },
}

ShipmentCancelPayload = {
    "shipment_identifier": "164557",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "locate2u",
        "carrier_name": "locate2u",
        "docs": {"label": "No label..."},
        "label_type": "PDF",
        "meta": {"durationMinutes": 10, "shipmentId": 0},
        "shipment_identifier": "164557",
        "tracking_number": "164557",
    },
    [],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "locate2u",
        "carrier_name": "locate2u",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequest = {
    "contact": {
        "name": "Matthew Robinson",
        "phone": "0123456789",
        "email": "matt.robinson@email.com",
    },
    "name": "Locate2u",
    "address": "Level 4, Suite 4.11, 55 Miller St, Pyrmont NSW 2009, Australia",
    "location": {"latitude": -33.8706672, "longitude": 151.192487},
    "appointmentTime": "12:00",
    "durationMinutes": 10,
    "notes": "Please call before you deliver",
    "tripDate": "2023-09-08T00:00:00.000000Z",
    "load": {
        "height": 2.0,
        "length": 7.0,
        "quantity": 1,
        "volume": 7e-05,
        "weight": 10.0,
        "width": 5.0,
    },
    "lines": [
        {
            "barcode": "1234567890",
            "description": "Item A - Barcode scanning item",
            "currentLocation": "Warehouse",
            "quantity": 1,
        }
    ],
}


ShipmentCancelRequest = {"stopId": "164557"}

ShipmentResponse = """{
  "assignedTo": {
    "id": "ee59-b174-4698-ac55-81d9d",
    "name": "John Doe"
  },
  "stopId": 164557,
  "status": "Pending",
  "brandId": null,
  "contact": {
    "name": "Matthew Robinson",
    "phone": "0123456789",
    "email": "matt.robinson@email.com"
  },
  "name": "Locate2u",
  "address": "Level 4, Suite 4.11, 55 Miller St, Pyrmont NSW 2009, Australia",
  "location": {
    "latitude": -33.8706672,
    "longitude": 151.192487
  },
  "tripDate": "2023-09-08",
  "appointmentTime": "13:07",
  "timeWindowStart": null,
  "timeWindowEnd": null,
  "durationMinutes": 10,
  "notes": "Please call before you deliver",
  "lastModifiedDate": "2023-09-08T13:07:24.904Z",
  "customFields": {
    "custom1": "value",
    "custom2": "value",
    "custom3": "value"
  },
  "type": null,
  "shipmentId": 0,
  "load": {
    "quantity": 0,
    "volume": 0,
    "weight": 0,
    "length": 0,
    "width": 0,
    "height": 0
  },
  "source": null,
  "sourceReference": null,
  "customerId": 0,
  "runNumber": 0,
  "teamRegionId": 0,
  "teamMemberInvoiceId": 0,
  "customerInvoiceId": 0,
  "arrivalDate": "2023-09-08T13:07:24+00:00",
  "lines": [
    {
      "lineId": 201,
      "itemId": 101,
      "serviceId": null,
      "productVariantId": null,
      "barcode": "1234567890",
      "description": "Item A - Barcode scanning item",
      "quantity": 1,
      "status": "Created",
      "itemStatus": "",
      "unitPriceExTax": 0,
      "priceCurrency": ""
    }
  ],
  "driverInstructions": null,
  "oneTimePin": "0011"
}
"""

ShipmentCancelResponse = """{}"""
