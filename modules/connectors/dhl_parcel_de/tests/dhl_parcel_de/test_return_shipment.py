import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestDPDHLGermanyReturnShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ReturnShipmentRequest = models.ShipmentRequest(**ReturnShipmentPayload)
        self.ReturnShipmentWithCustomsRequest = models.ShipmentRequest(
            **ReturnShipmentWithCustomsPayload
        )

    def test_create_return_shipment_request(self):
        request = gateway.mapper.create_return_shipment_request(
            self.ReturnShipmentRequest
        )

        self.assertEqual(request.serialize(), ReturnShipmentRequest)

    def test_create_return_shipment_with_customs_request(self):
        request = gateway.mapper.create_return_shipment_request(
            self.ReturnShipmentWithCustomsRequest
        )

        self.assertEqual(request.serialize(), ReturnShipmentWithCustomsRequest)

    def test_create_return_shipment(self):
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ReturnShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.returns_server_url}/orders?labelType=BOTH",
            )

    def test_parse_return_shipment_response(self):
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.return_value = ReturnShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ReturnShipmentRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedReturnShipmentResponse
            )

    def test_parse_return_shipment_error_response(self):
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.return_value = ReturnShipmentErrorResponse
            parsed_response = (
                karrio.Shipment.create(self.ReturnShipmentRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedReturnShipmentErrorResponse
            )


if __name__ == "__main__":
    unittest.main()


ReturnShipmentPayload = {
    "service": "dhl_parcel_de_paket",
    "is_return": True,
    "reference": "Return Order 5678",
    "shipper": {
        "person_name": "Max Mustermann",
        "address_line1": "Charles-de-Gaulle Str.",
        "street_number": "20",
        "postal_code": "53113",
        "city": "Bonn",
        "country_code": "DE",
        "email": "max@mustermann.de",
        "phone_number": "+49 123456789",
    },
    "recipient": {
        "company_name": "DHL Retoure",
        "address_line1": "Retourenweg 1",
        "postal_code": "12345",
        "city": "Berlin",
        "country_code": "DE",
    },
    "parcels": [
        {
            "weight": 1.0,
            "weight_unit": "KG",
        }
    ],
}

ReturnShipmentWithCustomsPayload = {
    "service": "dhl_parcel_de_paket",
    "is_return": True,
    "reference": "Return Order 9012",
    "shipper": {
        "person_name": "Max Mustermann",
        "address_line1": "Musterstr.",
        "street_number": "1",
        "postal_code": "3344",
        "city": "Bern",
        "country_code": "CH",
        "email": "max@mustermann.de",
        "phone_number": "+41 123456789",
    },
    "recipient": {
        "company_name": "DHL Retoure",
        "address_line1": "Retourenweg 1",
        "postal_code": "12345",
        "city": "Berlin",
        "country_code": "DE",
    },
    "parcels": [
        {
            "weight": 1.2,
            "weight_unit": "KG",
        }
    ],
    "customs": {
        "content_type": "return_of_goods",
        "commodities": [
            {
                "description": "Artikel-Beschreibung 1",
                "quantity": 1,
                "weight": 0.5,
                "weight_unit": "KG",
                "value_amount": 1000,
                "value_currency": "EUR",
                "origin_country": "FR",
                "hs_code": "88011900",
            },
            {
                "description": "Artikel-Beschreibung 2",
                "quantity": 1,
                "weight": 0.7,
                "weight_unit": "KG",
                "value_amount": 12.99,
                "value_currency": "EUR",
                "origin_country": "DE",
                "hs_code": "12345678",
            },
        ],
    },
    "options": {
        "dhl_parcel_de_return_receiver_id": "che",
    },
}

ReturnShipmentRequest = {
    "receiverId": "deu",
    "customerReference": "Return Order 5678",
    "shipper": {
        "name1": "Max Mustermann",
        "addressStreet": "Charles-de-Gaulle Str.",
        "addressHouse": "20",
        "postalCode": "53113",
        "city": "Bonn",
        "email": "max@mustermann.de",
        "phone": "+49 123456789",
    },
    "itemWeight": {
        "uom": "kg",
        "value": 1.0,
    },
}

ReturnShipmentWithCustomsRequest = {
    "receiverId": "che",
    "customerReference": "Return Order 9012",
    "shipper": {
        "name1": "Max Mustermann",
        "addressStreet": "Musterstr.",
        "addressHouse": "1",
        "postalCode": "3344",
        "city": "Bern",
        "email": "max@mustermann.de",
        "phone": "+41 123456789",
    },
    "itemWeight": {
        "uom": "kg",
        "value": 1.2,
    },
    "customsDetails": {
        "items": [
            {
                "itemDescription": "Artikel-Beschreibung 1",
                "packagedQuantity": 1,
                "countryOfOrigin": "FRA",
                "hsCode": "88011900",
                "itemWeight": {"uom": "kg", "value": 0.5},
                "itemValue": {"currency": "EUR", "value": 1000},
            },
            {
                "itemDescription": "Artikel-Beschreibung 2",
                "packagedQuantity": 1,
                "countryOfOrigin": "DEU",
                "hsCode": "12345678",
                "itemWeight": {"uom": "kg", "value": 0.7},
                "itemValue": {"currency": "EUR", "value": 12.99},
            },
        ],
    },
}

ReturnShipmentResponse = """{
  "sstatus": {
    "title": "Created",
    "status": 201,
    "detail": "Created"
  },
  "shipmentNo": "999991587211",
  "label": {
    "b64": "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABmgvaeTAAAA="
  },
  "qrLabel": {
    "b64": "QRLabelBase64Content="
  },
  "qrLink": "https://www.dhl.de/retoure/qr/999991587211",
  "routingCode": "40327653113+99000933090010"
}
"""

ReturnShipmentErrorResponse = """{
  "title": "Bad Request",
  "status": 400,
  "detail": "Bad Request - The request could not be understood by the server due to malformed syntax."
}
"""

ParsedReturnShipmentResponse = [
    {
        "carrier_id": "dhl_parcel_de",
        "carrier_name": "dhl_parcel_de",
        "docs": {
            "extra_documents": [
                {
                    "base64": "QRLabelBase64Content=",
                    "category": "qr_label",
                    "format": "PDF",
                },
            ],
            "label": "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABmgvaeTAAAA=",
        },
        "label_type": "PDF",
        "meta": {
            "carrier_tracking_link": "https://www.dhl.com/de-en/home/tracking/tracking-parcel.html?submit=1&tracking-id=999991587211",
            "shipmentNo": "999991587211",
            "qrLink": "https://www.dhl.de/retoure/qr/999991587211",
            "routingCode": "40327653113+99000933090010",
            "shipment_identifiers": ["999991587211"],
            "tracking_numbers": ["999991587211"],
        },
        "shipment_identifier": "999991587211",
        "tracking_number": "999991587211",
    },
    [],
]

ParsedReturnShipmentErrorResponse = [
    None,
    [
        {
            "carrier_id": "dhl_parcel_de",
            "carrier_name": "dhl_parcel_de",
            "code": "400",
            "details": {"title": "Bad Request"},
            "message": "Bad Request - The request could not be understood by the server due to malformed syntax.",
        }
    ],
]
