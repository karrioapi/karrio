import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestDPDHLGermanyShippingOptionOverrides(unittest.TestCase):
    """Test that shipping options override connection_config values."""

    def setUp(self):
        self.maxDiff = None
        self.ShipmentWithOptionsRequest = models.ShipmentRequest(
            **ShipmentPayloadWithOptions
        )

    def test_create_shipment_request_with_option_overrides(self):
        """Shipping options should override connection_config in the request payload."""
        request = gateway.mapper.create_shipment_request(
            self.ShipmentWithOptionsRequest
        )
        serialized = request.serialize()

        # Profile should be overridden by shipping option
        self.assertEqual(serialized["profile"], "MY_CUSTOM_PROFILE")
        # Cost center should be set from shipping option
        self.assertEqual(
            serialized["shipments"][0]["costCenter"], "CC-12345"
        )

    def test_create_shipment_with_label_type_option(self):
        """Shipping option label_type should override connection_config label_type in the URL."""
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentWithOptionsRequest).from_(
                gateway
            )

            url = mock.call_args[1]["url"]
            # Option sets PDF_910_300_600, overriding connection config ZPL2_910_300_700_oz
            self.assertIn("docFormat=PDF", url)
            self.assertIn("printFormat=910-300-600", url)


class TestDPDHLGermanyShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.IntlShipmentRequest = models.ShipmentRequest(**IntlShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(
            **ShipmentCancelPayload
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequest)

    def test_create_intl_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.IntlShipmentRequest)

        self.assertEqual(request.serialize(), IntlShipmentRequest)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(request.serialize(), ShipmentCancelRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/v2/orders?combine=false&docFormat=ZPL2&includeDocs=include&printFormat=910-300-700-oz",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/v2/orders?shipment=340434310428091700&profile=STANDARD_GRUPPENPROFIL",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelShipmentResponse
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)

    def test_parse_validation_messages_response(self):
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.return_value = ValidationMessagesErrorResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedValidationMessagesErrorResponse
            )

    def test_parse_multiple_validation_messages_response(self):
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.return_value = MultipleValidationMessagesErrorResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response),
                ParsedMultipleValidationMessagesErrorResponse,
            )

    def test_parse_shipment_response_with_customs_doc(self):
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponseWithCustomsDoc
            parsed_response = (
                karrio.Shipment.create(self.IntlShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedShipmentResponseWithCustomsDoc
            )

    def test_parse_shipment_response_with_return_label(self):
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.return_value = ShipmentWeithReturnLabelResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response),
                ParsedShipmentWithReturnLabelResponse,
            )


if __name__ == "__main__":
    unittest.main()


ShipmentPayloadWithOptions = {
    "service": "dhl_parcel_de_paket",
    "reference": "Order No. 5678",
    "shipper": {
        "company_name": "My Online Shop GmbH",
        "address_line1": "Sträßchensweg",
        "street_number": "10",
        "postal_code": "53113",
        "city": "Bonn",
        "country_code": "DE",
        "email": "max@mustermann.de",
    },
    "recipient": {
        "company_name": "Maria Muster",
        "address_line1": "Kurt-Schumacher-Str. 20",
        "address_line2": "Apartment 107",
        "postal_code": "53113",
        "city": "Bonn",
        "country_code": "DE",
        "email": "maria@musterfrau.de",
        "phone_number": "+49 987654321",
    },
    "parcels": [
        {
            "weight": 0.5,
            "weight_unit": "KG",
        }
    ],
    "options": {
        "dhl_parcel_de_label_type": "PDF_910_300_600",
        "dhl_parcel_de_cost_center": "CC-12345",
        "dhl_parcel_de_profile": "MY_CUSTOM_PROFILE",
    },
}

ShipmentPayload = {
    "service": "dhl_parcel_de_paket",
    "reference": "Order No. 1234",
    "shipper": {
        "company_name": "My Online Shop GmbH",
        "address_line1": "Sträßchensweg",
        "street_number": "10",
        "postal_code": "53113",
        "city": "Bonn",
        "country_code": "DE",
        "email": "max@mustermann.de",
    },
    "recipient": {
        "company_name": "Maria Muster",
        "address_line1": "Kurt-Schumacher-Str. 20",
        "address_line2": "Apartment 107",
        "postal_code": "53113",
        "city": "Bonn",
        "country_code": "DE",
        "email": "maria@musterfrau.de",
        "phone_number": "+49 987654321",
    },
    "parcels": [
        {
            "weight": 0.5,
            "length": 20,
            "width": 15,
            "height": 10,
            "weight_unit": "KG",
            "dimension_unit": "CM",
        }
    ],
}

IntlShipmentPayload = {
    "service": "dhl_parcel_de_europaket",
    "reference": "Order No. 1234",
    "shipper": {
        "company_name": "My Online Shop GmbH",
        "address_line1": "Sträßchensweg 10",
        "address_line2": "2. Etage",
        "postal_code": "53113",
        "city": "Bonn",
        "country_code": "DE",
        "email": "max@mustermann.de",
        "phone_number": "+49 123456789",
    },
    "recipient": {
        "company_name": "Joe Black",
        "address_line1": "10 Downing Street",
        "postal_code": "SW1A 1AA",
        "city": "London",
        "country_code": "GB",
        "email": "joe@black.uk",
        "phone_number": "+44 123456789",
    },
    "parcels": [
        {
            "weight": 0.5,
            "length": 20,
            "width": 15,
            "height": 10,
            "weight_unit": "KG",
            "dimension_unit": "CM",
        }
    ],
    "options": {
        "deutshepost_endorsement": "RETURN",
    },
    "customs": {
        "content_type": "commercial_goods",
        "duty": {
            "currency": "EUR",
            "declared_value": 1,
        },
        "commodities": [
            {
                "description": "Red T-Shirt",
                "quantity": 1,
                "hs_code": "123456",
                "origin_country": "FR",
                "value_amount": 10,
                "weight": 0.4,
                "weight_unit": "KG",
            }
        ],
    },
}

ShipmentCancelPayload = {
    "shipment_identifier": "340434310428091700",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "dhl_parcel_de",
        "carrier_name": "dhl_parcel_de",
        "docs": {
            "extra_documents": [
                {
                    "base64": ANY,
                    "category": "return_label",
                    "format": "PDF",
                    "print_format": "A4",
                    "url": ANY,
                },
                {
                    "base64": ANY,
                    "category": "cod_document",
                    "format": "PDF",
                    "print_format": "A4",
                    "url": ANY,
                },
            ],
            "invoice": ANY,
            "label": ANY,
        },
        "label_type": "PDF",
        "return_shipment": {
            "tracking_number": "340434310428091700",
            "shipment_identifier": "340434310428091700",
            "tracking_url": "https://www.dhl.com/de-en/home/tracking/tracking-parcel.html?submit=1&tracking-id=340434310428091700",
            "meta": {"returnShipmentNo": "340434310428091700"},
        },
        "meta": {
            "billing_number": "33333333330102",
            "carrier_tracking_link": "https://www.dhl.com/de-en/home/tracking/tracking-parcel.html?submit=1&tracking-id=340434310428091700",
            "shipmentNo": "340434310428091700",
            "shipmentRefNo": "340434310428091700",
            "shipment_identifiers": ["340434310428091700"],
            "tracking_numbers": ["340434310428091700"],
        },
        "shipment_identifier": "340434310428091700",
        "tracking_number": "340434310428091700",
    },
    [],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "dhl_parcel_de",
        "carrier_name": "dhl_parcel_de",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "dhl_parcel_de",
            "carrier_name": "dhl_parcel_de",
            "code": "401",
            "details": {"title": "Unauthorized"},
            "message": "Unauthorized for given resource.",
        }
    ],
]


ShipmentRequest = {
    "profile": "STANDARD_GRUPPENPROFIL",
    "shipments": [
        {
            "billingNumber": "33333333330102",
            "consignee": {
                "addressHouse": "20",
                "addressStreet": "Kurt-Schumacher-Str.",
                "city": "Bonn",
                "country": "DEU",
                "email": "maria@musterfrau.de",
                "name": "Maria Muster",
                "name1": "Maria Muster",
                "phone": "+49 987654321",
                "postalCode": "53113",
            },
            "details": {
                "dim": {"height": 10.0, "length": 20.0, "uom": "cm", "width": 15.0},
                "weight": {"uom": "kg", "value": 0.5},
            },
            "product": "V01PAK",
            "refNo": "Order No. 1234",
            "services": {"endorsement": "RETURN"},
            "shipDate": ANY,
            "shipper": {
                "addressHouse": "10",
                "addressStreet": "Sträßchensweg",
                "city": "Bonn",
                "country": "DEU",
                "email": "max@mustermann.de",
                "name1": "My Online Shop GmbH",
                "postalCode": "53113",
            },
        }
    ],
}

IntlShipmentRequest = {
    "profile": "STANDARD_GRUPPENPROFIL",
    "shipments": [
        {
            "billingNumber": "33333333335401",  # V54EPAK (Europaket) test billing number
            "consignee": {
                "addressHouse": "10",
                "addressStreet": "Downing Street",
                "city": "London",
                "country": "GBR",
                "email": "joe@black.uk",
                "name": "Joe Black",
                "name1": "Joe Black",
                "phone": "+44 123456789",
                "postalCode": "SW1A 1AA",
            },
            "customs": {
                "exportDescription": "Other",
                "exportType": "COMMERCIAL_GOODS",
                "items": [
                    {
                        "countryOfOrigin": "FRA",
                        "hsCode": "123456",
                        "itemDescription": "Red T-Shirt",
                        "itemValue": {"currency": "EUR", "value": 10},
                        "itemWeight": {"uom": "kg", "value": 0.4},
                        "packagedQuantity": 1,
                    }
                ],
                "officeOfOrigin": "DEU",
                "shippingConditions": "DDP",
            },
            "details": {
                "dim": {"height": 10.0, "length": 20.0, "uom": "cm", "width": 15.0},
                "weight": {"uom": "kg", "value": 0.5},
            },
            "product": "V54EPAK",
            "refNo": "Order No. 1234",
            "services": {"endorsement": "RETURN"},
            "shipDate": ANY,
            "shipper": {
                "addressHouse": "10",
                "addressStreet": "Sträßchensweg",
                "city": "Bonn",
                "country": "DEU",
                "email": "max@mustermann.de",
                "name1": "My Online Shop GmbH",
                "postalCode": "53113",
            },
        }
    ],
}

ShipmentCancelRequest = {
    "shipment": "340434310428091700",
    "profile": "STANDARD_GRUPPENPROFIL",
}

ShipmentResponse = """{
  "status": {
    "title": "ok",
    "statusCode": 200,
    "instance": "string",
    "detail": "The Webservice call ran successfully."
  },
  "items": [
    {
      "shipmentNo": "340434310428091700",
      "returnShipmentNo": "340434310428091700",
      "sstatus": {
        "title": "OK",
        "statusCode": 200,
        "instance": "string",
        "detail": "The Webservice call ran successfully."
      },
      "shipmentRefNo": "340434310428091700",
      "label": {
        "b64": "string",
        "zpl2": "string",
        "url": "https://api-dev.dhl.com/parcel/de/shipping/v1-feature-order-endpoint/labels?token=x5xzrHE7ctmqPqk33k%2BKkBwbvIfYP4elMQsBFM%2BJOdiT2bmoaXXzris%2Ftz9jBtdVFLY5cCENit0Jnd9aXuxoNEXhP9PQ8tAVdPeXD26RZ6JZqF5NCJlrihrAv1%2FAOzuDPqWJLRVaRq461BpT4bcbzChAAHVg%2FHUaQAkeIkaZ8NqfcxWEQzK1AYJWczpy6sv6",
        "fileFormat": "PDF",
        "printFormat": "A4"
      },
      "returnLabel": {
        "b64": "string",
        "zpl2": "string",
        "url": "https://api-dev.dhl.com/parcel/de/shipping/v1-feature-order-endpoint/labels?token=x5xzrHE7ctmqPqk33k%2BKkBwbvIfYP4elMQsBFM%2BJOdiT2bmoaXXzris%2Ftz9jBtdVFLY5cCENit0Jnd9aXuxoNEXhP9PQ8tAVdPeXD26RZ6JZqF5NCJlrihrAv1%2FAOzuDPqWJLRVaRq461BpT4bcbzChAAHVg%2FHUaQAkeIkaZ8NqfcxWEQzK1AYJWczpy6sv6",
        "fileFormat": "PDF",
        "printFormat": "A4"
      },
      "customsDoc": {
        "b64": "string",
        "zpl2": "string",
        "url": "https://api-dev.dhl.com/parcel/de/shipping/v1-feature-order-endpoint/labels?token=x5xzrHE7ctmqPqk33k%2BKkBwbvIfYP4elMQsBFM%2BJOdiT2bmoaXXzris%2Ftz9jBtdVFLY5cCENit0Jnd9aXuxoNEXhP9PQ8tAVdPeXD26RZ6JZqF5NCJlrihrAv1%2FAOzuDPqWJLRVaRq461BpT4bcbzChAAHVg%2FHUaQAkeIkaZ8NqfcxWEQzK1AYJWczpy6sv6",
        "fileFormat": "PDF",
        "printFormat": "A4"
      },
      "codLabel": {
        "b64": "string",
        "zpl2": "string",
        "url": "https://api-dev.dhl.com/parcel/de/shipping/v1-feature-order-endpoint/labels?token=x5xzrHE7ctmqPqk33k%2BKkBwbvIfYP4elMQsBFM%2BJOdiT2bmoaXXzris%2Ftz9jBtdVFLY5cCENit0Jnd9aXuxoNEXhP9PQ8tAVdPeXD26RZ6JZqF5NCJlrihrAv1%2FAOzuDPqWJLRVaRq461BpT4bcbzChAAHVg%2FHUaQAkeIkaZ8NqfcxWEQzK1AYJWczpy6sv6",
        "fileFormat": "PDF",
        "printFormat": "A4"
      },
      "validationMessages": [
        {
          "property": "string",
          "validationMessage": "string",
          "validationState": "string"
        }
      ]
    }
  ]
}
"""

ShipmentWeithReturnLabelResponse = """{
  "status": {
    "title": "OK",
    "status": 200,
    "detail": "1 von 1 Sendung erfolgreich gedruckt.",
    "statusCode": 200
  },
  "items": [
    {
      "shipmentNo": "0034043333301020022796580",
      "returnShipmentNo": "60701001756402",
      "sstatus": {
        "title": "OK",
        "status": 200,
        "statusCode": 200
      },
      "shipmentRefNo": "LM-DE-DE-10013",
      "routingCode": "40327680807+99000943042250",
      "returnRoutingCode": "40327610117+99000933000000",
      "label": {
        "b64": "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",
        "fileFormat": "PDF",
        "printFormat": "A4"
      },
      "returnLabel": {
        "b64": "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",
        "fileFormat": "PDF",
        "printFormat": "910-300-710"
      },
      "validationMessages": [
        {
          "property": "shipper",
          "validationMessage": "Die angegebene Hausnummer kann nicht gefunden werden.",
          "validationState": "Warning"
        },
        {
          "property": "consignee",
          "validationMessage": "Der Ort ist zu dieser PLZ nicht bekannt. Die Sendung ist trotzdem leitcodierbar und es wurde ein Versandschein erzeugt.",
          "validationState": "Warning"
        },
        {
          "property": "services.dhlRetoure.returnAddress",
          "validationMessage": "Die angegebene Hausnummer kann nicht gefunden werden.",
          "validationState": "Warning"
        }
      ]
    }
  ]
}"""

ShipmentCancelResponse = """{
  "status": {
    "title": "ok",
    "statusCode": 200,
    "instance": "string",
    "detail": "The Webservice call ran successfully."
  },
  "items": [
    {
      "shipmentNo": 340434310428091700,
      "sstatus": {
        "title": "OK",
        "status": 200
      },
      "label": {
        "url": "https://api-dev.dhl.com/parcel/de/shipping/v1-feature-order-endpoint/labels?token=x5xzrHE7ctmqPqk33k%2BKkBwbvIfYP4elMQsBFM%2BJOdiT2bmoaXXzris%2Ftz9jBtdVFLY5cCENit0Jnd9aXuxoNEXhP9PQ8tAVdPeXD26RZ6JZqF5NCJlrihrAv1%2FAOzuDPqWJLRVaRq461BpT4bcbzChAAHVg%2FHUaQAkeIkaZ8NqfcxWEQzK1AYJWczpy6sv6",
        "format": "PDF"
      }
    }
  ]
}
"""

ErrorResponse = """{
  "title": "Unauthorized",
  "statusCode": 401,
  "detail": "Unauthorized for given resource."
}
"""

ValidationMessagesErrorResponse = """{
  "status": {
    "title": "Error",
    "statusCode": 400,
    "instance": "string",
    "detail": "Validation failed."
  },
  "items": [
    {
      "shipmentNo": "340434310428091700",
      "validationMessages": [
        {
          "property": "shipper.addressStreet",
          "validationMessage": "Street name is required",
          "validationState": "Error"
        }
      ]
    }
  ]
}
"""

ParsedValidationMessagesErrorResponse = [
    None,
    [
        {
            "carrier_id": "dhl_parcel_de",
            "carrier_name": "dhl_parcel_de",
            "code": "400",
            "details": {"instance": "string", "title": "Error"},
            "message": "Validation failed.",
        },
        {
            "carrier_id": "dhl_parcel_de",
            "carrier_name": "dhl_parcel_de",
            "code": "Error",
            "details": {
                "property": "shipper.addressStreet",
                "shipmentNo": "340434310428091700",
                "validationState": "Error",
            },
            "message": "shipper.addressStreet: Street name is required",
        },
    ],
]

MultipleValidationMessagesErrorResponse = """{
  "status": {
    "title": "ok",
    "statusCode": 200,
    "instance": "string",
    "detail": "The Webservice call ran successfully."
  },
  "items": [
    {
      "shipmentNo": "340434310428091701",
      "validationMessages": [
        {
          "property": "consignee.postalCode",
          "validationMessage": "Postal code format is invalid",
          "validationState": "Error"
        },
        {
          "property": "consignee.city",
          "validationMessage": "City name is required",
          "validationState": "Error"
        },
        {
          "property": "details.weight",
          "validationMessage": "Weight exceeds maximum limit",
          "validationState": "Warning"
        }
      ]
    }
  ]
}
"""

ParsedMultipleValidationMessagesErrorResponse = [
    None,
    [
        {
            "carrier_id": "dhl_parcel_de",
            "carrier_name": "dhl_parcel_de",
            "code": "Error",
            "details": {
                "property": "consignee.postalCode",
                "shipmentNo": "340434310428091701",
                "validationState": "Error",
            },
            "message": "consignee.postalCode: Postal code format is invalid",
        },
        {
            "carrier_id": "dhl_parcel_de",
            "carrier_name": "dhl_parcel_de",
            "code": "Error",
            "details": {
                "property": "consignee.city",
                "shipmentNo": "340434310428091701",
                "validationState": "Error",
            },
            "message": "consignee.city: City name is required",
        },
        {
            "carrier_id": "dhl_parcel_de",
            "carrier_name": "dhl_parcel_de",
            "code": "Warning",
            "details": {
                "property": "details.weight",
                "shipmentNo": "340434310428091701",
                "validationState": "Warning",
            },
            "message": "details.weight: Weight exceeds maximum limit",
        },
    ],
]

ShipmentResponseWithCustomsDoc = """{
    "status": {
        "title": "OK",
        "status": 200,
        "detail": "1 of 1 shipment successfully printed.",
        "statusCode": 200
    },
    "items": [
        {
            "shipmentNo": "CD530123554DE",
            "sstatus": {
                "title": "OK",
                "status": 200,
                "statusCode": 200
            },
            "shipmentRefNo": "Order No. 1234",
            "routingCode": "403826SW1A1AA+67000000",
            "label": {
                "b64": "JVBERi0xLjUK",
                "fileFormat": "PDF",
                "printFormat": "910-300-710"
            },
            "customsDoc": {
                "b64": "JVBERi0xLjUKCustomsDoc",
                "fileFormat": "PDF",
                "printFormat": "A4-PT"
            },
            "validationMessages": []
        }
    ]
}"""

ParsedShipmentResponseWithCustomsDoc = [
    {
        "carrier_id": "dhl_parcel_de",
        "carrier_name": "dhl_parcel_de",
        "docs": {"invoice": "JVBERi0xLjUKCustomsDoc", "label": "JVBERi0xLjUK"},
        "label_type": "PDF",
        "meta": {
            "billing_number": "33333333335401",  # V54EPAK (Europaket) test billing number
            "carrier_tracking_link": "https://www.dhl.com/de-en/home/tracking/tracking-parcel.html?submit=1&tracking-id=CD530123554DE",
            "shipmentNo": "CD530123554DE",
            "shipmentRefNo": "Order No. 1234",
            "shipment_identifiers": ["CD530123554DE"],
            "tracking_numbers": ["CD530123554DE"],
        },
        "shipment_identifier": "CD530123554DE",
        "tracking_number": "CD530123554DE",
    },
    [],
]

ParsedShipmentWithReturnLabelResponse = [
    {
        "carrier_id": "dhl_parcel_de",
        "carrier_name": "dhl_parcel_de",
        "docs": {
            "extra_documents": [
                {
                    "base64": ANY,
                    "category": "return_label",
                    "format": "PDF",
                    "print_format": "910-300-710",
                },
            ],
            "label": ANY,
        },
        "label_type": "PDF",
        "return_shipment": {
            "tracking_number": "60701001756402",
            "shipment_identifier": "60701001756402",
            "tracking_url": "https://www.dhl.com/de-en/home/tracking/tracking-parcel.html?submit=1&tracking-id=60701001756402",
            "meta": {"returnShipmentNo": "60701001756402"},
        },
        "meta": {
            "billing_number": "33333333330102",
            "carrier_tracking_link": "https://www.dhl.com/de-en/home/tracking/tracking-parcel.html?submit=1&tracking-id=0034043333301020022796580",
            "shipmentNo": "0034043333301020022796580",
            "shipmentRefNo": "LM-DE-DE-10013",
            "shipment_identifiers": ["0034043333301020022796580"],
            "tracking_numbers": ["0034043333301020022796580"],
        },
        "shipment_identifier": "0034043333301020022796580",
        "tracking_number": "0034043333301020022796580",
    },
    [
        {
            "carrier_id": "dhl_parcel_de",
            "carrier_name": "dhl_parcel_de",
            "code": "Warning",
            "details": {
                "property": "shipper",
                "shipmentNo": "0034043333301020022796580",
                "validationState": "Warning",
            },
            "message": "shipper: Die angegebene Hausnummer kann nicht gefunden werden.",
        },
        {
            "carrier_id": "dhl_parcel_de",
            "carrier_name": "dhl_parcel_de",
            "code": "Warning",
            "details": {
                "property": "consignee",
                "shipmentNo": "0034043333301020022796580",
                "validationState": "Warning",
            },
            "message": "consignee: Der Ort ist zu dieser PLZ nicht bekannt. Die Sendung ist trotzdem leitcodierbar und es wurde ein Versandschein erzeugt.",
        },
        {
            "carrier_id": "dhl_parcel_de",
            "carrier_name": "dhl_parcel_de",
            "code": "Warning",
            "details": {
                "property": "services.dhlRetoure.returnAddress",
                "shipmentNo": "0034043333301020022796580",
                "validationState": "Warning",
            },
            "message": "services.dhlRetoure.returnAddress: Die angegebene Hausnummer kann nicht gefunden werden.",
        },
    ],
]
