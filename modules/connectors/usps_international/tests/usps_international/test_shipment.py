import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
from tests import logger

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestUSPSShipping(unittest.TestCase):
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
        logger.debug(request.serialize())
        self.assertEqual(request.serialize(), ShipmentCancelRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.usps_international.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/international-labels/v3/international-label",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.usps_international.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/international-labels/v3/international-label/794947717776",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.usps_international.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.usps_international.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )
            logger.debug(lib.to_dict(parsed_response))
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelShipmentResponse
            )


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "shipper": {
        "company_name": "ABC Corp.",
        "address_line1": "1098 N Fraser Street",
        "city": "Georgetown",
        "postal_code": "29440",
        "country_code": "US",
        "person_name": "Tall Tom",
        "phone_number": "8005554526",
        "state_code": "SC",
    },
    "recipient": {
        "company_name": "Coffee Five",
        "address_line1": "R. da Quitanda, 86 - quiosque 01",
        "city": "Centro",
        "postal_code": "29440",
        "country_code": "BR",
        "person_name": "John",
        "phone_number": "8005554526",
        "state_code": "RJ",
    },
    "parcels": [
        {
            "height": 50,
            "length": 50,
            "weight": 20,
            "width": 12,
            "dimension_unit": "CM",
            "weight_unit": "KG",
        }
    ],
    "service": "usps_global_express_guaranteed",
    "customs": {
        "content_type": "merchandise",
        "incoterm": "DDU",
        "invoice": "INV-040903",
        "commodities": [
            {
                "weight": 2,
                "weight_unit": "KG",
                "quantity": 1,
                "hs_code": "XXXXX0000123",
                "value_amount": 30,
                "value_currency": "USD",
                "origin_country": "US",
            }
        ],
        "duty": {
            "paid_by": "recipient",
            "currency": "USD",
            "declared_value": 60,
        },
        "certify": True,
        "signer": "Admin",
        "options": {
            "license_number": "LIC-24356879",
            "certificate_number": "CERT-97865342",
        },
    },
    "options": {"shipment_date": "2021-05-15", "insurance": 75.0},
    "reference": "#Order 11111",
}

ShipmentCancelPayload = {
    "shipment_identifier": "794947717776",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "usps_international",
        "carrier_name": "usps_international",
        "docs": {"label": ANY},
        "label_type": "PDF",
        "meta": {"SKU": "DUXR0XXXXC01450", "postage": 36.12},
        "shipment_identifier": "9236190361980900000015",
        "tracking_number": "9236190361980900000015",
    },
    [],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "usps_international",
        "carrier_name": "usps_international",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequest = [
    {
        "customsForm": {
            "certificateNumber": "CERT-9786534",
            "contents": [
                {
                    "itemDescription": "Item",
                    "HSTariffNumber": "XXXXX0000123",
                    "countryofOrigin": "US",
                    "itemQuantity": 1,
                    "itemTotalValue": 30,
                    "itemTotalWeight": 4.41,
                    "itemValue": 30,
                    "itemWeight": 4.41,
                    "weightUOM": "lb",
                }
            ],
            "customsContentType": "MERCHANDISE",
            "invoiceNumber": "INV-040903",
            "licenseNumber": "LIC-24356879",
        },
        "fromAddress": {
            "ZIPCode": "29440",
            "city": "Georgetown",
            "firm": "ABC Corp.",
            "firstName": "Tall",
            "lastName": "Tom",
            "ignoreBadAddress": True,
            "phone": "8005554526",
            "streetAddress": "1098 N Fraser Street",
            "state": "SC",
        },
        "imageInfo": {"imageType": "PDF", "labelType": "4X6LABEL"},
        "packageDescription": {
            "customerReference": [{"referenceNumber": "#Order 11111"}],
            "destinationEntryFacilityType": "NONE",
            "dimensionsUOM": "in",
            "extraServices": [930],
            "girth": 124.0,
            "height": 19.69,
            "length": 19.69,
            "mailClass": "GLOBAL_EXPRESS_GUARANTEED",
            "mailingDate": "2021-05-15",
            "processingCategory": "NON_MACHINABLE",
            "rateIndicator": "DR",
            "weight": 44.1,
            "weightUOM": "lb",
            "width": 4.72,
            "packageOptions": {"packageValue": 30.0},
        },
        "senderAddress": {
            "ZIPCode": "29440",
            "state": "SC",
            "city": "Georgetown",
            "firm": "ABC Corp.",
            "firstName": "Tall",
            "lastName": "Tom",
            "ignoreBadAddress": True,
            "phone": "8005554526",
            "streetAddress": "1098 N Fraser Street",
        },
        "toAddress": {
            "city": "Centro",
            "country": "BR",
            "countryISOAlpha2Code": "BR",
            "firm": "Coffee Five",
            "firstName": "John",
            "lastName": "John",
            "phone": "8005554526",
            "postalCode": "29440",
            "province": "RJ",
            "streetAddress": "R. da Quitanda, 86 - quiosque 01",
        },
    }
]

ShipmentCancelRequest = [{"trackingNumber": "794947717776"}]

ShipmentResponse = """--mZ-FhSKSA2PdeSHqaaGcJysq
Content-Type: application/json
Content-Disposition: form-data; name="labelMetadata"

{"labelAddress":{"streetAddress":"R. da Quitanda, 86 - quiosque 01","secondaryAddress":"","city":"GEORGETOWN","state":"SC","ZIPCode":"29440","firstName":"John","firm":"Coffee Five","ignoreBadAddress":true},"routingInformation":"42029440","trackingNumber":"9236190361980900000015","postage":36.12,"extraServices":[{"name":"Insurance <= $500","price":0.0,"SKU":"DXIX0XXXXCX0100"}],"zone":"01","commitment":{"name":"6 Days","scheduleDeliveryDate":"2024-12-07"},"weightUOM":"LB","weight":44.1,"dimensionalWeight":13.0,"fees":[],"bannerText":"USPS TRACKING # USPS Ship","retailDistributionCode":"01","serviceTypeCode":"361","constructCode":"C03","SKU":"DUXR0XXXXC01450"}
--mZ-FhSKSA2PdeSHqaaGcJysq
Content-Type: application/pdf
Content-Disposition: form-data; filename="labelImage.pdf"; name="labelImage"

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dWJ0eXBlIC9UeXBlMQogIC9CYXNlRm9udCAvSGVsdmV0aWNhCiAgL0VuY29kaW5nIC9XaW5BbnNpRW5jb2RpbmcKPj4KZW5kb2JqCjE4IDAgb2JqCjw8CiAgL1R5cGUgL0ZvbnQKICAvU3VidHlwZSAvVHlwZTEKICAvQmFzZUZvbnQgL0hlbHZldGljYS1PYmxpcXVlCiAgL0VuY29kaW5nIC9XaW5BbnNpRW5jb2RpbmcKPj4KZW5kb2JqCjE5IDAgb2JqCjw8CiAgL1R5cGUgL0ZvbnQKICAvU3VidHlwZSAvVHlwZTEKICAvQmFzZUZvbnQgL0hlbHZldGljYS1Cb2xkCiAgL0VuY29kaW5nIC9XaW5BbnNpRW5jb2RpbmcKPj4KZW5kb2JqCjE2IDAgb2JqCjw8IC9UeXBlIC9QYWdlcwovQ291bnQgMQovS2lkcyBbMTQgMCBSIF0gPj4KZW5kb2JqCjIwIDAgb2JqCjw8CiAgL1R5cGUgL0NhdGFsb2cKICAvUGFnZXMgMTYgMCBSCiAgL0xhbmcgKHgtdW5rbm93bikKPj4KZW5kb2JqCjE1IDAgb2JqCjw8CiAgL0ZvbnQgPDwKICAvRjEgMTcgMCBSCiAgL0YyIDE4IDAgUgogIC9GMyAxOSAwIFIKPj4KICAvUHJvY1NldCBbL1BERiAvSW1hZ2VCIC9JbWFnZUMgL1RleHRdCiAgL1hPYmplY3QgPDwgL0ltMSA1IDAgUiAvSW0yIDEwIDAgUiA+PgogIC9Db2xvclNwYWNlIDw8IC9JQ0MyIDQgMCBSIC9JQ0M3IDkgMCBSID4+Cj4+CmVuZG9iagp4cmVmCjAgMjEKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwMDE1IDAwMDAwIG4gCjAwMDAwMDAxMzEgMDAwMDAgbiAKMDAwMDAwMjY4OCAwMDAwMCBuIAowMDAwMDAyNzA4IDAwMDAwIG4gCjAwMDAwMDI3NDEgMDAwMDAgbiAKMDAwMDAwMzAxMyAwMDAwMCBuIAowMDAwMDAzMDMxIDAwMDAwIG4gCjAwMDAwMDU1ODggMDAwMDAgbiAKMDAwMDAwNTYwOCAwMDAwMCBuIAowMDAwMDA1NjQxIDAwMDAwIG4gCjAwMDAwMDU5NjcgMDAwMDAgbiAKMDAwMDAwNTk4NyAwMDAwMCBuIAowMDAwMDIyMjU0IDAwMDAwIG4gCjAwMDAwMjIyNzYgMDAwMDAgbiAKMDAwMDAyMjkzNiAwMDAwMCBuIAowMDAwMDIyODAxIDAwMDAwIG4gCjAwMDAwMjI0NzAgMDAwMDAgbiAKMDAwMDAyMjU3NiAwMDAwMCBuIAowMDAwMDIyNjkwIDAwMDAwIG4gCjAwMDAwMjI4NjEgMDAwMDAgbiAKdHJhaWxlcgo8PAogIC9Sb290IDIwIDAgUgogIC9JbmZvIDEgMCBSCiAgL0lEIFs8QUVEMzZEQTQ5MjdCRjg4Rjg4ODcxMTMwNzJDOEI0MDQ+IDxBRUQzNkRBNDkyN0JGODhGODg4NzExMzA3MkM4QjQwND5dCiAgL1NpemUgMjEKPj4Kc3RhcnR4cmVmCjIzMTM1CiUlRU9GCg==
--mZ-FhSKSA2PdeSHqaaGcJysq--
"""

ShipmentCancelResponse = """{
	"trackingNumber": "9234690361980900000142",
	"status": "CANCELED"
}
"""
