import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging as logger

import karrio.sdk as karrio
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
        logger.debug(request.serialize())
        self.assertEqual(request.serialize(), ShipmentRequest)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )
        logger.debug(request.serialize())
        self.assertEqual(request.serialize(), ShipmentCancelRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/labels/v3/label",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/labels/v3/label/794947717776",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
            logger.debug(lib.to_dict(parsed_response))
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
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

    def test_parse_return_shipment_response(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = ReturnShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest)
                .from_(gateway)
                .parse()
            )
            print(parsed_response)
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedReturnShipmentResponse
            )

    def test_parse_shipment_response_sample2(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponseSample2
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
            logger.debug(lib.to_dict(parsed_response))
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedShipmentResponseSample2
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
        "company_name": "Horizon",
        "address_line1": "1309 S Agnew Avenue",
        "address_line2": "Apt 303",
        "city": "Oklahoma City",
        "postal_code": "73108",
        "country_code": "US",
        "person_name": "Lina Smith",
        "phone_number": "+1 123 456 7890",
        "state_code": "OK",
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
    "service": "usps_library_mail_nonstandard_single_piece",
    "options": {
        "signature_required": True,
        "shipment_date": "2024-07-28",
    },
    "reference": "#Order 11111",
}

ShipmentCancelPayload = {
    "shipment_identifier": "794947717776",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "usps",
        "carrier_name": "usps",
        "docs": {"invoice": ANY, "label": ANY},
        "label_type": "PDF",
        "meta": {
            "SKU": "DUXR0XXXXC06130",
            "postage": 18.76,
            "routingInformation": "42073108",
        },
        "selected_rate": {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "service": "346",
            "total_charge": 18.76,
            "currency": "USD",
            "extra_charges": [
                {"amount": 18.76, "currency": "USD", "name": "Postage"},
            ],
            "meta": {
                "SKU": "DUXR0XXXXC06130",
                "zone": "06",
                "commitment": "3 Days",
            },
        },
        "shipment_identifier": "9234690361980900000142",
        "tracking_number": "9234690361980900000142",
    },
    [],
]

ParsedShipmentResponseSample2 = [
    {
        "carrier_id": "usps",
        "carrier_name": "usps",
        "docs": {
            "invoice": ANY,
            "label": ANY,
        },
        "label_type": "PDF",
        "meta": {
            "SKU": "DUXR0XXXXC08220",
            "postage": 42.62,
            "routingInformation": "42032827",
        },
        "selected_rate": {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "service": "346",
            "total_charge": 42.62,
            "currency": "USD",
            "extra_charges": [
                {"amount": 42.62, "currency": "USD", "name": "Postage"},
                {"amount": 18.0, "currency": "USD", "name": "Nonstandard Volume > 2 cu ft"},
            ],
            "meta": {
                "SKU": "DUXR0XXXXC08220",
                "zone": "08",
                "commitment": "5 Days",
            },
        },
        "shipment_identifier": "9234690361980900000265",
        "tracking_number": "9234690361980900000265",
    },
    [],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "usps",
        "carrier_name": "usps",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequest = [
    {
        "fromAddress": {
            "ZIPCode": "29440",
            "city": "Georgetown",
            "state": "SC",
            "firm": "ABC Corp.",
            "firstName": "Tall",
            "lastName": "Tom",
            "ignoreBadAddress": True,
            "phone": "8005554526",
            "streetAddress": "1098 N Fraser Street",
        },
        "imageInfo": {
            "imageType": "PDF",
            "labelType": "4X6LABEL",
            "receiptOption": "NONE",
        },
        "packageDescription": {
            "customerReference": [
                {"printReferenceNumber": True, "referenceNumber": "#Order 11111"}
            ],
            "destinationEntryFacilityType": "NONE",
            "dimensionsUOM": "in",
            "girth": 124.0,
            "height": 19.69,
            "inductionZIPCode": "29440",
            "length": 19.69,
            "mailClass": "LIBRARY_MAIL",
            "mailingDate": "2024-07-28",
            "processingCategory": "NON_MACHINABLE",
            "rateIndicator": "DR",
            "weight": 44.1,
            "weightUOM": "lb",
            "width": 4.72,
        },
        "senderAddress": {
            "ZIPCode": "29440",
            "city": "Georgetown",
            "firm": "ABC Corp.",
            "state": "SC",
            "firstName": "Tall",
            "lastName": "Tom",
            "ignoreBadAddress": True,
            "phone": "8005554526",
            "streetAddress": "1098 N Fraser Street",
        },
        "toAddress": {
            "ZIPCode": "73108",
            "city": "Oklahoma City",
            "firm": "Horizon",
            "firstName": "Lina",
            "lastName": "Smith",
            "ignoreBadAddress": True,
            "phone": "1234567890",
            "secondaryAddress": "Apt 303",
            "state": "OK",
            "streetAddress": "1309 S Agnew Avenue",
        },
    }
]

ShipmentCancelRequest = [{"trackingNumber": "794947717776"}]

ShipmentResponse = """--r6-fpGYWbdZmd9w5-850fEfX
Content-Type: application/json
Content-Disposition: form-data; name="labelMetadata"

{"labelAddress":{"streetAddress":"1309 S Agnew Avenue","secondaryAddress":"Apt 303","city":"Oklahoma City","state":"OK","ZIPCode":"73108","firstName":"Lina Smith","firm":"Horizon","ignoreBadAddress":true},"routingInformation":"42073108","trackingNumber":"9234690361980900000142","postage":18.76,"extraServices":[{"name":"USPS Tracking","price":0.0,"SKU":"DXTU0EXXXCX0000"}],"zone":"06","commitment":{"name":"3 Days","scheduleDeliveryDate":"2024-11-22"},"weightUOM":"LB","weight":4.1,"dimensionalWeight":13.0,"fees":[],"bannerText":"USPS TRACKING # USPS Ship","retailDistributionCode":"01","serviceTypeCode":"346","constructCode":"C03","SKU":"DUXR0XXXXC06130"}
--r6-fpGYWbdZmd9w5-850fEfX
Content-Type: application/pdf
Content-Disposition: form-data; filename="labelImage.pdf"; name="labelImage"

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YmoKMTMgMCBvYmoKNjU0NAplbmRvYmoKMTQgMCBvYmoKPDwKICAvUmVzb3VyY2VzIDE1IDAgUgogIC9UeXBlIC9QYWdlCiAgL01lZGlhQm94IFswIDAgMjg4IDQzMl0KICAvQ3JvcEJveCBbMCAwIDI4OCA0MzJdCiAgL0JsZWVkQm94IFswIDAgMjg4IDQzMl0KICAvVHJpbUJveCBbMCAwIDI4OCA0MzJdCiAgL1BhcmVudCAxNiAwIFIKICAvQ29udGVudHMgMTIgMCBSCj4+CmVuZG9iagoxNyAwIG9iago8PAogIC9UeXBlIC9Gb250CiAgL1N1YnR5cGUgL1R5cGUxCiAgL0Jhc2VGb250IC9IZWx2ZXRpY2EKICAvRW5jb2RpbmcgL1dpbkFuc2lFbmNvZGluZwo+PgplbmRvYmoKMTggMCBvYmoKPDwKICAvVHlwZSAvRm9udAogIC9TdWJ0eXBlIC9UeXBlMQogIC9CYXNlRm9udCAvSGVsdmV0aWNhLU9ibGlxdWUKICAvRW5jb2RpbmcgL1dpbkFuc2lFbmNvZGluZwo+PgplbmRvYmoKMTkgMCBvYmoKPDwKICAvVHlwZSAvRm9udAogIC9TdWJ0eXBlIC9UeXBlMQogIC9CYXNlRm9udCAvSGVsdmV0aWNhLUJvbGQKICAvRW5jb2RpbmcgL1dpbkFuc2lFbmNvZGluZwo+PgplbmRvYmoKMTYgMCBvYmoKPDwgL1R5cGUgL1BhZ2VzCi9Db3VudCAxCi9LaWRzIFsxNCAwIFIgXSA+PgplbmRvYmoKMjAgMCBvYmoKPDwKICAvVHlwZSAvQ2F0YWxvZwogIC9QYWdlcyAxNiAwIFIKICAvTGFuZyAoeC11bmtub3duKQo+PgplbmRvYmoKMTUgMCBvYmoKPDwKICAvRm9udCA8PAogIC9GMSAxNyAwIFIKICAvRjIgMTggMCBSCiAgL0YzIDE5IDAgUgo+PgogIC9Qcm9jU2V0IFsvUERGIC9JbWFnZUIgL0ltYWdlQyAvVGV4dF0KICAvWE9iamVjdCA8PCAvSW0xIDUgMCBSIC9JbTIgMTAgMCBSID4+CiAgL0NvbG9yU3BhY2UgPDwgL0lDQzIgNCAwIFIgL0lDQzcgOSAwIFIgPj4KPj4KZW5kb2JqCnhyZWYKMCAyMQowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAwMDAwMTUgMDAwMDAgbiAKMDAwMDAwMDEzMSAwMDAwMCBuIAowMDAwMDAyNjg4IDAwMDAwIG4gCjAwMDAwMDI3MDggMDAwMDAgbiAKMDAwMDAwMjc0MSAwMDAwMCBuIAowMDAwMDAzMDEzIDAwMDAwIG4gCjAwMDAwMDMwMzEgMDAwMDAgbiAKMDAwMDAwNTU4OCAwMDAwMCBuIAowMDAwMDA1NjA4IDAwMDAwIG4gCjAwMDAwMDU2NDEgMDAwMDAgbiAKMDAwMDAwNTk2MyAwMDAwMCBuIAowMDAwMDA1OTgzIDAwMDAwIG4gCjAwMDAwMTI2MDMgMDAwMDAgbiAKMDAwMDAxMjYyNCAwMDAwMCBuIAowMDAwMDEzMjg0IDAwMDAwIG4gCjAwMDAwMTMxNDkgMDAwMDAgbiAKMDAwMDAxMjgxOCAwMDAwMCBuIAowMDAwMDEyOTI0IDAwMDAwIG4gCjAwMDAwMTMwMzggMDAwMDAgbiAKMDAwMDAxMzIwOSAwMDAwMCBuIAp0cmFpbGVyCjw8CiAgL1Jvb3QgMjAgMCBSCiAgL0luZm8gMSAwIFIKICAvSUQgWzw1OENCNTg0MkM5ODc5MDYxQkE0ODI5MDFGMkE0QTZDQz4gPDU4Q0I1ODQyQzk4NzkwNjFCQTQ4MjkwMUYyQTRBNkNDPl0KICAvU2l6ZSAyMQo+PgpzdGFydHhyZWYKMTM0ODMKJSVFT0YK
--r6-fpGYWbdZmd9w5-850fEfX
Content-Type: application/pdf
Content-Disposition: form-data; filename="receiptImage.pdf"; name="receiptImage"

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IDAgb2JqCjw8IC9UeXBlIC9QYWdlcwovQ291bnQgMQovS2lkcyBbNCAwIFIgXSA+PgplbmRvYmoKOSAwIG9iago8PAogIC9UeXBlIC9DYXRhbG9nCiAgL1BhZ2VzIDYgMCBSCiAgL0xhbmcgKHgtdW5rbm93bikKPj4KZW5kb2JqCjUgMCBvYmoKPDwgL0ZvbnQgPDwgL0YyIDcgMCBSIC9GMyA4IDAgUiA+PiAvUHJvY1NldCBbL1BERiAvSW1hZ2VCIC9JbWFnZUMgL1RleHRdID4+CmVuZG9iagp4cmVmCjAgMTAKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwMDE1IDAwMDAwIG4gCjAwMDAwMDAxMzEgMDAwMDAgbiAKMDAwMDAwODU2NiAwMDAwMCBuIAowMDAwMDA4NTg2IDAwMDAwIG4gCjAwMDAwMDkxMzAgMDAwMDAgbiAKMDAwMDAwODk5OSAwMDAwMCBuIAowMDAwMDA4Nzc2IDAwMDAwIG4gCjAwMDAwMDg4ODkgMDAwMDAgbiAKMDAwMDAwOTA1NyAwMDAwMCBuIAp0cmFpbGVyCjw8CiAgL1Jvb3QgOSAwIFIKICAvSW5mbyAxIDAgUgogIC9JRCBbPDA2QjhFNDU1NjNERDBGRDE1NUY3QUQyRDlEQkRCRjVBPiA8MDZCOEU0NTU2M0REMEZEMTU1RjdBRDJEOURCREJGNUE+XQogIC9TaXplIDEwCj4+CnN0YXJ0eHJlZgo5MjIxCiUlRU9GCg==
--r6-fpGYWbdZmd9w5-850fEfX--
"""

ShipmentResponseSample2 = '--FNfrpx9bbvOkzqOIlaOc8mp+\r\nContent-Type: application/json\r\nContent-Disposition: form-data; name="labelMetadata"\r\n\r\n{"labelAddress":{"streetAddress":"Jeff Fuqua Blvd 1","secondaryAddress":"","city":"Orlando","state":"FL","ZIPCode":"32827","firstName":"Martin","lastName":"Martin","ignoreBadAddress":true},"routingInformation":"42032827","trackingNumber":"9234690361980900000265","postage":42.62,"extraServices":[{"name":"USPS Tracking","price":0.0,"SKU":"DXTU0EXXXCX0000"}],"zone":"08","commitment":{"name":"5 Days","scheduleDeliveryDate":"2024-12-02"},"weightUOM":"LB","weight":2.21,"dimensionalWeight":22.0,"fees":[{"name":"Nonstandard Volume > 2 cu ft","price":18.0,"SKU":"D813XUXXXXX0000"}],"bannerText":"USPS TRACKING # USPS Ship","retailDistributionCode":"02","serviceTypeCode":"346","constructCode":"C03","SKU":"DUXR0XXXXC08220"}\r\n--FNfrpx9bbvOkzqOIlaOc8mp+\r\nContent-Type: application/pdf\r\nContent-Disposition: form-data; filename="labelImage.pdf"; name="labelImage"\r\n\r\n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WzAgMCAyODggNDMyXQogIC9CbGVlZEJveCBbMCAwIDI4OCA0MzJdCiAgL1RyaW1Cb3ggWzAgMCAyODggNDMyXQogIC9QYXJlbnQgMTYgMCBSCiAgL0NvbnRlbnRzIDEyIDAgUgo+PgplbmRvYmoKMTcgMCBvYmoKPDwKICAvVHlwZSAvRm9udAogIC9TdWJ0eXBlIC9UeXBlMQogIC9CYXNlRm9udCAvSGVsdmV0aWNhCiAgL0VuY29kaW5nIC9XaW5BbnNpRW5jb2RpbmcKPj4KZW5kb2JqCjE4IDAgb2JqCjw8CiAgL1R5cGUgL0ZvbnQKICAvU3VidHlwZSAvVHlwZTEKICAvQmFzZUZvbnQgL0hlbHZldGljYS1PYmxpcXVlCiAgL0VuY29kaW5nIC9XaW5BbnNpRW5jb2RpbmcKPj4KZW5kb2JqCjE5IDAgb2JqCjw8CiAgL1R5cGUgL0ZvbnQKICAvU3VidHlwZSAvVHlwZTEKICAvQmFzZUZvbnQgL0hlbHZldGljYS1Cb2xkCiAgL0VuY29kaW5nIC9XaW5BbnNpRW5jb2RpbmcKPj4KZW5kb2JqCjE2IDAgb2JqCjw8IC9UeXBlIC9QYWdlcwovQ291bnQgMQovS2lkcyBbMTQgMCBSIF0gPj4KZW5kb2JqCjIwIDAgb2JqCjw8CiAgL1R5cGUgL0NhdGFsb2cKICAvUGFnZXMgMTYgMCBSCiAgL0xhbmcgKHgtdW5rbm93bikKPj4KZW5kb2JqCjE1IDAgb2JqCjw8CiAgL0ZvbnQgPDwKICAvRjEgMTcgMCBSCiAgL0YyIDE4IDAgUgogIC9GMyAxOSAwIFIKPj4KICAvUHJvY1NldCBbL1BERiAvSW1hZ2VCIC9JbWFnZUMgL1RleHRdCiAgL1hPYmplY3QgPDwgL0ltMSA1IDAgUiAvSW0yIDEwIDAgUiA+PgogIC9Db2xvclNwYWNlIDw8IC9JQ0MyIDQgMCBSIC9JQ0M3IDkgMCBSID4+Cj4+CmVuZG9iagp4cmVmCjAgMjEKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwMDE1IDAwMDAwIG4gCjAwMDAwMDAxMzEgMDAwMDAgbiAKMDAwMDAwMjY4OCAwMDAwMCBuIAowMDAwMDAyNzA4IDAwMDAwIG4gCjAwMDAwMDI3NDEgMDAwMDAgbiAKMDAwMDAwMzAxMyAwMDAwMCBuIAowMDAwMDAzMDMxIDAwMDAwIG4gCjAwMDAwMDU1ODggMDAwMDAgbiAKMDAwMDAwNTYwOCAwMDAwMCBuIAowMDAwMDA1NjQxIDAwMDAwIG4gCjAwMDAwMDU5NjcgMDAwMDAgbiAKMDAwMDAwNTk4NyAwMDAwMCBuIAowMDAwMDEyNDk2IDAwMDAwIG4gCjAwMDAwMTI1MTcgMDAwMDAgbiAKMDAwMDAxMzE3NyAwMDAwMCBuIAowMDAwMDEzMDQyIDAwMDAwIG4gCjAwMDAwMTI3MTEgMDAwMDAgbiAKMDAwMDAxMjgxNyAwMDAwMCBuIAowMDAwMDEyOTMxIDAwMDAwIG4gCjAwMDAwMTMxMDIgMDAwMDAgbiAKdHJhaWxlcgo8PAogIC9Sb290IDIwIDAgUgogIC9JbmZvIDEgMCBSCiAgL0lEIFs8QTkyRjc5MTI3QjVDODc0MDBGMkM0MzNFODRCRjMxOEU+IDxBOTJGNzkxMjdCNUM4NzQwMEYyQzQzM0U4NEJGMzE4RT5dCiAgL1NpemUgMjEKPj4Kc3RhcnR4cmVmCjEzMzc2CiUlRU9GCg==\r\n--FNfrpx9bbvOkzqOIlaOc8mp+\r\nContent-Type: application/pdf\r\nContent-Disposition: form-data; filename="receiptImage.pdf"; name="receiptImage"\r\n\r\n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ZG9iago5IDAgb2JqCjw8CiAgL1R5cGUgL0NhdGFsb2cKICAvUGFnZXMgNiAwIFIKICAvTGFuZyAoeC11bmtub3duKQo+PgplbmRvYmoKNSAwIG9iago8PCAvRm9udCA8PCAvRjIgNyAwIFIgL0YzIDggMCBSID4+IC9Qcm9jU2V0IFsvUERGIC9JbWFnZUIgL0ltYWdlQyAvVGV4dF0gPj4KZW5kb2JqCnhyZWYKMCAxMAowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAwMDAwMTUgMDAwMDAgbiAKMDAwMDAwMDEzMSAwMDAwMCBuIAowMDAwMDA4NTE0IDAwMDAwIG4gCjAwMDAwMDg1MzQgMDAwMDAgbiAKMDAwMDAwOTA3OCAwMDAwMCBuIAowMDAwMDA4OTQ3IDAwMDAwIG4gCjAwMDAwMDg3MjQgMDAwMDAgbiAKMDAwMDAwODgzNyAwMDAwMCBuIAowMDAwMDA5MDA1IDAwMDAwIG4gCnRyYWlsZXIKPDwKICAvUm9vdCA5IDAgUgogIC9JbmZvIDEgMCBSCiAgL0lEIFs8QzcyRDI0OTBFNUQ2MzU4N0Q0RUU0RjRGMjA5Q0M2QkQ+IDxDNzJEMjQ5MEU1RDYzNTg3RDRFRTRGNEYyMDlDQzZCRD5dCiAgL1NpemUgMTAKPj4Kc3RhcnR4cmVmCjkxNjkKJSVFT0YK\r\n--FNfrpx9bbvOkzqOIlaOc8mp+--'

ParsedReturnShipmentResponse = [
    {
        "carrier_id": "usps",
        "carrier_name": "usps",
        "docs": {
            "invoice": ANY,
            "label": ANY,
            "extra_documents": [
                {
                    "category": "return_label",
                    "format": "PDF",
                    "base64": ANY,
                }
            ],
        },
        "label_type": "PDF",
        "meta": {
            "SKU": "DUXR0XXXXC06130",
            "postage": 18.76,
            "routingInformation": "42073108",
            "labelBrokerID": "LB00001",
        },
        "selected_rate": {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "service": "346",
            "total_charge": 18.76,
            "currency": "USD",
            "extra_charges": [
                {"amount": 18.76, "currency": "USD", "name": "Postage"},
            ],
            "meta": {
                "SKU": "DUXR0XXXXC06130",
                "zone": "06",
                "commitment": "3 Days",
            },
        },
        "return_shipment": {
            "tracking_number": "9234690361980900000999",
            "shipment_identifier": "9234690361980900000999",
            "tracking_url": "https://tools.usps.com/go/TrackConfirmAction?tLabels=9234690361980900000999",
            "meta": {"returnLabelBrokerID": "RLB00001"},
        },
        "shipment_identifier": "9234690361980900000142",
        "tracking_number": "9234690361980900000142",
    },
    [],
]

ReturnShipmentResponse = """--r6-fpGYWbdZmd9w5-850fEfX
Content-Type: application/json
Content-Disposition: form-data; name="labelMetadata"

{"labelAddress":{"streetAddress":"1309 S Agnew Avenue","secondaryAddress":"Apt 303","city":"Oklahoma City","state":"OK","ZIPCode":"73108","firstName":"Lina Smith","firm":"Horizon","ignoreBadAddress":true},"routingInformation":"42073108","trackingNumber":"9234690361980900000142","postage":18.76,"extraServices":[{"name":"USPS Tracking","price":0.0,"SKU":"DXTU0EXXXCX0000"}],"zone":"06","commitment":{"name":"3 Days","scheduleDeliveryDate":"2024-11-22"},"weightUOM":"LB","weight":4.1,"dimensionalWeight":13.0,"fees":[],"bannerText":"USPS TRACKING # USPS Ship","retailDistributionCode":"01","serviceTypeCode":"346","constructCode":"C03","SKU":"DUXR0XXXXC06130","labelBrokerID":"LB00001"}
--r6-fpGYWbdZmd9w5-850fEfX
Content-Type: application/pdf
Content-Disposition: form-data; filename="labelImage.pdf"; name="labelImage"

JVBERi0xLjQKMSAwIG9iago8PC9UeXBlL0NhdGFsb2c+PgplbmRvYmoKJSVFT0YK
--r6-fpGYWbdZmd9w5-850fEfX
Content-Type: application/pdf
Content-Disposition: form-data; filename="receiptImage.pdf"; name="receiptImage"

JVBERi0xLjQKMiAwIG9iago8PC9UeXBlL1JlY2VpcHQ+PgplbmRvYmoKJSVFT0YK
--r6-fpGYWbdZmd9w5-850fEfX
Content-Type: application/json
Content-Disposition: form-data; name="returnLabelMetadata"

{"trackingNumber":"9234690361980900000999","labelBrokerID":"RLB00001","SKU":"DUXR0XXXXC06130"}
--r6-fpGYWbdZmd9w5-850fEfX
Content-Type: application/pdf
Content-Disposition: form-data; filename="returnLabelImage.pdf"; name="returnLabelImage"

JVBERi0xLjQKMyAwIG9iago8PC9UeXBlL1JldHVybj4+CmVuZG9iagoKJSVFT0YK
--r6-fpGYWbdZmd9w5-850fEfX--
"""

ShipmentCancelResponse = """{
	"trackingNumber": "9234690361980900000142",
	"status": "CANCELED"
}
"""
