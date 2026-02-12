import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


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
                f"{gateway.settings.server_url}/v2/orders?combine=true&docFormat=ZPL2&printFormat=910-300-700-oz",
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


if __name__ == "__main__":
    unittest.main()


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
