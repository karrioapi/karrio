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
        "shipment_date": "2024-07-16",
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
            "billingReference": "string",
            "carrierName": "string",
            "carrier_tracking_link": "string",
            "orderId": "string",
            "service_name": "string",
            "trackingId": "string",
            "tracking_numbers": ["string"],
            "transactionId": "string",
        },
        "shipment_identifier": "string",
        "tracking_number": "string",
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
                "height": 12.0,
                "length": 15.0,
                "weight": 10.0,
                "weightUnit": "KG",
                "width": 10.0,
            },
            {
                "description": "Package 2 Description",
                "dimensionUnit": "CM",
                "height": 10.0,
                "length": 15.0,
                "weight": 5.0,
                "weightUnit": "KG",
                "width": 10.0,
            },
        ],
        "quantity": 2,
        "totalWeight": 15.0,
        "type": "Package",
        "weightUnit": "KG",
    },
    "packagingUnit": "Imperial",
    "scheduledShipDate": "2024-07-16 00:00",
    "serviceId": "5000184",
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

ShipmentCancelRequest = {
    "order": {"orderId": "1234567890", "trackingId": "794947717776"}
}


ShipmentResponse = """{
  "order": {
    "trackingId": "string",
    "orderId": "string",
    "message": "string"
  },
  "carrier": {
    "carrierName": "string",
    "serviceName": "string",
    "carrierLogoPath": "string"
  },
  "reference": {
    "code": "string",
    "name": "string"
  },
  "reference2": {
    "code": "string",
    "name": "string"
  },
  "reference3": {
    "code": "string",
    "name": "string"
  },
  "transactionId": "string",
  "billingReference": "string",
  "packages": [
    {
      "trackingNumber": "string"
    }
  ],
  "trackingUrl": "string",
  "brandedTrackingUrl": "string",
  "trackingNumber": "string",
  "labelData": {
    "label": [
      {
        "type": "PDF",
        "data": "JVBERi0xLjQKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMyAwIFIKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL1R5cGUgL091dGxpbmVzCi9Db3VudCAwCj4+CmVuZG9iagozIDAgb2JqCjw8Ci9UeXBlIC9QYWdlcwovQ291bnQgMwovS2lkcyBbMTggMCBSIDE5IDAgUiAyMCAwIFJdCj4+CmVuZG9iago0IDAgb2JqClsvUERGIC9UZXh0IC9JbWFnZUIgL0ltYWdlQyAvSW1hZ2VJXQplbmRvYmoKNSAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9IZWx2ZXRpY2EKL0VuY29kaW5nIC9NYWNSb21hbkVuY29kaW5nCj4+CmVuZG9iago2IDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL0hlbHZldGljYS1Cb2xkCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKNyAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9IZWx2ZXRpY2EtT2JsaXF1ZQovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjggMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvSGVsdmV0aWNhLUJvbGRPYmxpcXVlCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKOSAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9Db3VyaWVyCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKMTAgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvQ291cmllci1Cb2xkCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKMTEgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvQ291cmllci1PYmxpcXVlCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKMTIgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvQ291cmllci1Cb2xkT2JsaXF1ZQovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjEzIDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL1RpbWVzLVJvbWFuCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKMTQgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvVGltZXMtQm9sZAovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjE1IDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL1RpbWVzLUl0YWxpYwovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjE2IDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL1RpbWVzLUJvbGRJdGFsaWMKL0VuY29kaW5nIC9NYWNSb21hbkVuY29kaW5nCj4+CmVuZG9iagoxNyAwIG9iaiAKPDwKL0NyZWF0aW9uRGF0ZSAoRDoyMDAzKQovUHJvZHVjZXIgKEZlZEV4IFNlcnZpY2VzKQovVGl0bGUgKEZlZEV4IFNoaXBwaW5nIExhYmVsKQ0vQ3JlYXRvciAoRmVkRXggQ3VzdG9tZXIgQXV0b21hdGlvbikNL0F1dGhvciAoQ0xTIFZlcnNpb24gNTEyMDEzNSkKPj4KZW5kb2JqCjE4IDAgb2JqCjw8Ci9UeXBlIC9QYWdlDS9QYXJlbnQgMyAwIFIKL1Jlc291cmNlcyA8PCAvUHJvY1NldCA0IDAgUiAKIC9Gb250IDw8IC9GMSA1IDAgUiAKL0YyIDYgMCBSIAovRjMgNyAwIFIgCi9GNCA4IDAgUiAKL0Y1IDkgMCBSIAovRjYgMTAgMCBSIAovRjcgMTEgMCBSIAovRjggMTIgMCBSIAovRjkgMTMgMCBSIAovRjEwIDE0IDAgUiAKL0YxMSAxNSAwIFIgCi9GMTIgMTYgMCBSIAogPj4KL1hPYmplY3QgPDwgL0ZlZEV4RXhwcmVzcyAyMyAwIFIKL0V4cHJlc3NFIDI0IDAgUgovYmFyY29kZTAgMjUgMCBSCi9GZWRFeEV4cHJlc3MgMjYgMCBSCi9FeHByZXNzRSAyNyAwIFIKPj4KPj4KL01lZGlhQm94IFswIDAgMjg4IDQzMl0KL1RyaW1Cb3hbMCAwIDI4OCA0MzJdCi9Db250ZW50cyAyMSAwIFIKL1JvdGF0ZSAwPj4KZW5kb2JqCjE5IDAgb2JqCjw8Ci9UeXBlIC9QYWdlDS9QYXJlbnQgMyAwIFIKL1Jlc291cmNlcyA8PCAvUHJvY1NldCA0IDAgUiAKIC9Gb250IDw8IC9GMSA1IDAgUiAKL0YyIDYgMCBSIAovRjMgNyAwIFIgCi9GNCA4IDAgUiAKL0Y1IDkgMCBSIAovRjYgMTAgMCBSIAovRjcgMTEgMCBSIAovRjggMTIgMCBSIAovRjkgMTMgMCBSIAovRjEwIDE0IDAgUiAKL0YxMSAxNSAwIFIgCi9GMTIgMTYgMCBSIAogPj4KL1hPYmplY3QgPDwgL0ZlZEV4RXhwcmVzcyAyMyAwIFIKL0V4cHJlc3NFIDI0IDAgUgovYmFyY29kZTAgMjUgMCBSCi9GZWRFeEV4cHJlc3MgMjYgMCBSCi9FeHByZXNzRSAyNyAwIFIKPj4KPj4KL01lZGlhQm94IFswIDAgMjg4IDQzMl0KL1RyaW1Cb3hbMCAwIDI4OCA0MzJdCi9Db250ZW50cyAyMiAwIFIKL1JvdGF0ZSAwPj4KZW5kb2JqCjIwIDAgb2JqCjw8Ci9UeXBlIC9QYWdlDS9QYXJlbnQgMyAwIFIKL1Jlc291cmNlcyA8PCAvUHJvY1NldCA0IDAgUiAKIC9Gb250IDw8IC9GMSA1IDAgUiAKL0YyIDYgMCBSIAovRjMgNyAwIFIgCi9GNCA4IDAgUiAKL0Y1IDkgMCBSIAovRjYgMTAgMCBSIAovRjcgMTEgMCBSIAovRjggMTIgMCBSIAovRjkgMTMgMCBSIAovRjEwIDE0IDAgUiAKL0YxMSAxNSAwIFIgCi9GMTIgMTYgMCBSIAogPj4KL1hPYmplY3QgPDwgL0ZlZEV4RXhwcmVzcyAyMyAwIFIKL0V4cHJlc3NFIDI0IDAgUgovYmFyY29kZTAgMjUgMCBSCi9GZWRFeEV4cHJlc3MgMjYgMCBSCi9FeHByZXNzRSAyNyAwIFIKPj4KPj4KL01lZGlhQm94IFswIDAgMjg4IDQzMl0KL1RyaW1Cb3hbMCAwIDI4OCA0MzJdCi9Db250ZW50cyAyMiAwIFIKL1JvdGF0ZSAwPj4KZW5kb2JqCjIxIDAgb2JqCjw8IC9MZW5ndGggMjYwNwovRmlsdGVyIFsvQVNDSUk4NURlY29kZSAvRmxhdGVEZWNvZGVdIAo+PgpzdHJlYW0KR2F0PS45bGpPSigjPHJOcnJGcTMsYiJRSVxAQjxYWyVnJUNWQl86XjhCWFJQUmw1NyZTVS9eRlBMZTJpaFpMTV1STl9gZSs7XjQnbCtEKGYKTWk3SDVjalozczUiOk0qYGVsL3BFUjlUXSRwKj1XKCw9ZVcudWdJbGR0Y1ckYlM5TUJpOz89aSJUTDRPMyVcdEU9J21eS3M1P1RsXVNzPjQKXClQPT0uaVUxSCR0NFkkaDxcYCw/NWFSLm1kRHJPQ0E1SzIxKCNILTFkOiZZQkhPO1lrMjZxUClYWnRROVJYNnFddC46J3EvMUo7Slw3RFMKTTglZ0VBJSgxYzEpZGk9XVVeXllQcWFGWUFGRWo7aHU5amM/TCdoUUlCRWZiLCFJLzBrRnJIXi9KZEEzXVw9RUlPTVswRixpbS9cbyEwLD8KUlM1SyhwM1ZbaF4zUjNkbC5gKm1bQHRaJF5MVlcxUUFlaGAqREVuZ3EhTHAqLExQW289TSpgVWoqYyk8b1o6R2E0LSVVJSNLKTw4Nix0SXMKcnIpWlttZXMzQltESyNQcVgybUZGU1tcYGBUbGphPiQ6XkdyaiooIXA/YmRGVz1eJS0nIWRSTzokLFNVTi1pRXNqaV9GXiMpT0NLW1BDUEMKLCRQUWZnMmpASE51KWc+XCooOVlTNDJEXEEvbXR0NjhaXnNNcmpwKlBiX3BNMyJUX1gkLyJRJUM9KU8mNydrXWYrYUEpLT09OVtjcF4kW1AKQkA+SykyKVw1JWQ8ayY6IV9NSyJbU24wJiM4SHVyIW8jWlEpTWQtSUs9L2U3M2VGUVo0OkVpdDdXcl9RbFwxP0RlRTEzNEM6LipDYFYjO0wKXlJfISo4ITFWODZSKDxrIm0lSFYoNWcvO1QrUi83X3RwWmloSj9OJWVSR2t0TjkxXSRrM0AtXUUnSVVHbm4lXDlFcEVBa104LC5tQzpoKjIKYj02dTFBPyEzXyVORzAwQXBxO0dYVCxCUTJlbSZFcShMXF42TWNqQGYoMCdoMXF0Ry5mbC40YjJsalBQWzldcE9iRC5rZCQnbzhLZismQj0KNnQzPlJaR1c9bmxjOCs1XChbcTYvVWgnTmtaU2tfPlFQazU2Vy9oODduJjIxPyFaaWBnUllwRmhebjZHRjgzQE5EZyFURiU5SFVJUDNbYDQKbilkaklcOXMiJmxVUVolV1QtISlkY11IUFlmTUQ1bCZWI3RAcz5oXUM0aVE0a1YjIzRxZC10S3FyKTghXydIIz1GZSE2U2k1Zmtycmc5WFQKNEVBXTE4LWZzJHBfN2tRRUBHQTU5Jy1dXFNSOSQ8TGtrY2JqY1xkUyIqMFktPVdZVW4zL0NaTTBtY2xjSFRqX3VWRExxRmc9WkFkVXFyIjUKJTUrO1s2M1g3Y3FlU2AjTDUoWzlWUDE3LWNFWjhBTFNAbFAlLl5aXFVEJyJucypRYFo1K0BzPSxcOCw6LFg5Oi47PXQ2MVNbcVhTQ0MvWkMKUyJePCpwLixDTktJZUgyVkNqWD80ISFUSS0qL0NrMms5UE5tMDVQal5pNkVlOUVGSDgpc11mXCxgdWkoWWxkVWJXX05gTC4+LmxNIjMlPGwKLEZPOV0hVUROXExFWV91YFpSOVAxaDZxcWhlWitAcSVUKnVoaDdObyVASWpbLj4tMHFnWCdbPFt0XmZPSyktYFQ+LEdRLlluYD1vVnI7ODcKWERfQ1dTUVpVMWtPQmFVME1vVklCLVgxQClSMlNkQmduTChlcm8hZGpiQVpGWi5xOE1dc2JwO2xSRjNeRF9lN1gzPmonTFRONFM3UXFSaFAKUF9sMCEmdSI+czlzKihfWVdlSV83bE1fNWkoOWRYQipxVjFTIldnKWRjOlBJNmkwPWMtdC5OYSEiR1lxIkdDJ09YUFQ9PCQxIiZpLlZiR1MKMk1lW1JGQSZLXW9yU1luZTwkXlAkXExFU2k4ZG4vJEVkSU8lUTZJP0Q4SVJII1xZTmNjWVEoK0VSaC4lRk1Yb1Q9dWxoaTtvaz5XbzA/SGsKQDEnK0NRKzEtRDJgZSY1TjlaK3JpPF42KGs2ZFY6XHVfMFE/UDZTRzp1WE5LNnJTZVJAbC9wLjJzUHIkWSZkJ2M3OEBpXCVCOllbJVpPRm4KXzAram1IbnEmN1U+U2JpWis1XWA+YzZbN2lkSURxZGxzRSFbWSt1bVZcIVVXSGpbYUlVKDxQanJEQ0UoJEpGc3JMSyFOISh1KkohS2xxXEMKYk1cUkg3cyQ/OltxYGVmWSM+VXM7RzlrLFNpXW88WFZFPSpTVkQyPEdDP0R0WG4sOTU1IjUuJWA6OXFTK2ZJKVhFaGJnc2kmWlFncjhpb2wKZ3U4b0QpV2FeI2xdbWtKcFJHbjJSKEFdPjhtSjlVOVA5YzxrVy9GYj4rWkdaLyopRilPUlUjOE5rTUU1JEw8dDZpdXNtTi5IajpSTUpzbEUKO15nI1ZZVD1nRUYwOmVwJDxYTFVGRjQxY1VObEw7alRtMDg7XmUqblMwIzpvbFA4RixBTmMza1ZjTk9qX0tvZTFmVlNFLUxfMClcTl9uYTMKS0YhOFMtLU0yaSldPVc9aiVRQWhvYTpOQkFQb0NpTzEoPj0uXyY0c1VXN3VsQElzWV4/MGRgVGA6WEpKbltVVjEhRmcqcEMwLEFmNj1GdD4KJlBDU2pDY0hWQmYtcytQMD1fW05VTHVwZGUuPSpMXWc9SlxRdCgxPypPcUE5LyVBPXRYJTBXLllRZ1tsYjhFb1dZN000PyViNGIuOnVYTUgKQDtRaUNbdCJJNT8vSVtcV1NmZ01gKUMuZWAwY2U1PXJYb2dGajtEa1RrPUVEKyxxX1ddV1QxcWMzVkJzZXJTUCNLajFILy0qNlJySnQqcEQKXio5NlA1V1JKWzNKRFVFJUUyXmklIT1zYlBSXXJeMThoP09VTm1jPWZIUSpIaGU0Myw9QSghdU0+NjxeYiVVYkdRQTU+LGpLKExNZ2AxM0cKZTw6RE0+Q0QhS2RGKEQpblgrRitoVkcwMy5uLEJsTzZZdSM9ZChbaktkRGstciswP09eOUxxVDpCSDBQMTUrblw5WUBdYlxobmdXa0stXF0KZ0dWOlBEOlBTai8jJGtnYUktL2xHU2w/QjU8YVMrNGVbdVYlSWw5US1tXCYhX2w9UTZtSyJccUonWEBjX3RYaiI2K1luckhiKmNyU2VRVz0KUkFwRiFwJShbJUosIVVOSDI3OENUMEUySFJwLF9OcWBdIiYyZltxRCVLUz5aX29eZjU7SWgxV24mUF5TMkVFLzI2b09RZCVuJWFSJ18xQiMKMTlEaSVpUEc/OystQj9QVHAnQmdvKU1YLiwrcUtocjdiUkNyVll0Nys4IVc3Py9OM1hGZUhmMElMM25PZURSPTIxXkI1WjhMTSM5ZzdbbzEKaHU+TGNtSmxTS1M4QX4+CmVuZHN0cmVhbQplbmRvYmoKMjIgMCBvYmoKPDwgL0xlbmd0aCAzMDY0Ci9GaWx0ZXIgWy9BU0NJSTg1RGVjb2RlIC9GbGF0ZURlY29kZV0gCj4+CnN0cmVhbQpHYXQ9Lj1gWUxsKDROLzJzNT9yNVFeTGguZEQjKykhSU1vP2ZPTldURWJmIS1FJG82KUJGZzNEcFhlO3QoPDAhPzI2QTMqTD5eREBlKEtmMwozb1YiWFh1NjJoYGFmM1pQUjhSaVYkNzNTJF8rR0dnY09MUTVkWipxPGwtXWwoWSFIXUhbZUF1NWxSVVgtMDUqbCE8bilULitoNSheRVNnUApWKEpBSiJFUjVaPSQ/Pz9pYkVLcFJETkxhczg5cTUhLltaa0xrI0FsczRuWFdNMz1pZVBsLjVkPkptQmhdODdcbEBLbk5pMllVPyUuPjBvWApUaE4+bW1iOz8mI0lAXFA9a3AjST1lNVFJXF4oNk5IKnM3NFdxQUhAKmxGP1RgSUNUQEpiMmd0RSVpO2sjNEdxWnBpZiMnbztxWWgtSCZOTgooazNTOFplbSpyMEgwJDQ0dHVxRDBQLj5UNnQyYj0yWDFDQGBcOHAtSSIqc0wxdVtfMkJKSC9nXFtpOG9VOF9bJEM5RSs6SFddTUFTPUchRwpeZTZzRmY+a2c8SUAlXkBwLTJuaD9OR1c+aVdkQzVEVEsjMXMlYSNEMSQrKnNTbG05ZFZwQXFFPDFERGdnUTVKJVRfO2NeYVlaNTdbcjZoVwojK3RHIVA7cjkjSiJrOTJBW2FAZExRaVlibzorNEElaUIhYGcvcEJZTm5acGtOW0VxcTUmZzNvVzFWa1xuQFk1VUYmNm0+UkQvXFxeXWhIWAooKDVGQic/M1VBPT1fZWU+aTgzYTxVWyRBX1QyNF9aLFFZPyNmXWJPPkJpQz9tZko0aWhHRCtcI0FqOWBfX1YyVWNgJyhrRnU7SS9XRTRcJgolVmQiW2NIXWZVU3JVZmwwQGQ8LjsuTGJFPCxgN2UuZSklcCpFIk4pQk9SIWFPZTUjTVg3YzQtXWoiSE9SLGBQKEJkJlU5ajdQNF5DKmcqWQo0STZuIUhPNmE6M29tSUkhQCI+cllaOzkoRCk7WS1qYkc3MXFfZlBCRV0+IVhPM2NfaTdNZGJsYU1DbVM8XSknSFMvcj02SDkwMGcsRklURgo0KGRzPkhNMENeNnFGLD1xWy44KzJRZFpWYkcuOk9cWHJjcUNDO1NNI1ZYLk4tSl9kN0pEITpVKlNfV1k4ZnIsQSooSnVBT1M1bSM+PCItawpoJlNPZD07PERXTGsmO1JUKm82LzotdE9dZWQ6OlVMIV0hTDcpKXFGUSYjNThrXGNQdDxdYnBPNz9QcWhxIWs1WjFdRiprOD1WO1tGKklaNwomdEtRNitBQy5LMEYjXVpeIkprXCVsUSI/WUU6VDhLZColQk0qZV4/LUQmV11DRjIidWIhbjJwXmddRFdVTCYzaiU0Qjo4Y1FiNUhCOlUzbwo4OmQkVjY1NzNdQzg8WiVYYT1KXFVtL2xUUl1uVWk3UGFER1ZRUSg5LSY7Zz9LbENiN0EsRC1QVjhBQks9TiFdMT1KQTo7XTNmMj9PPTVXUAplND0vakxUVFFuKUEyTDohMSdSR2FfWFx0WGpnT0FSI0BFOzFgaTA2Tk11R1NFRltCTS5TTFBuLHIwSjQrNSIqTWEnLi4lOyVvODosUEdJcApMPipgRjlTQjtNOThgcTUvaUdSLFtvSm1HUixPTDw3IickJVcrMixsTWNqTSpOJHMzTEBtW1EpbyxXVF1CYmNVUTsjbHAnX3FSJkQmMicpOgpxKD4kUzEoZks3KGY6czRhSjFRSFtHYWFsOTo6YnNdYDlUOGsoTkQxYUpjT0g4PGIlVEJ1ODxqT2opLW0qJSxuVWQ0L1JyISVhNjsjRmFCOQo3UyMuSyxaVT40NmwrYFtPOWtjZGxTJnA+LTdtRCdkXjg6XyFFYmRTTVlKZ0QnVW1mXC02a28lPmFlLT5bSF9vOT1KQTolW2tXVGNOKyMrRQpcbTU8JWFKNC9tRTM6WS1uZUs5PSElYThRcUJncnJMTkFaOFEwXEslTkNXSG5MKXM6R2FEQFs/IkNQcWBUUzkhQFY4UnRFMGNRZyNURyJZMAo0dSFvQlBtZ2haW1JZJksnIidHWDAtbkg0OVhvc19YVS5ZTGB0NGpZYmFpaVBhczBhcEowamRVPG8jLCc5Qjs0YS8mZUc0PUdVT2E+UitZbgo0PVpRP0QqaERHQVQ1KnVpRyQuQUgkISkqVVRBRnAxUVJnSyElYThRW2NxZyw8KkU3Km1jUWcyVjhETEcsPz4yZmReNjloY2BRMFc6aF9XbAosPFNcJiwqMjxaVlpfSFlRJk5wMCFFYylQOVdLM05KPkppcjBSbkM5L0AxKWtYczgqRmRfbUgnPTpqRklLNihnZjBYNXBFX1BRTy49dURyYQovc1UvTktMQUghcW9WJ0hOQSo1ME0rajAxJSlFRi5tNnVvIjonIlRMJzVRLmY2RmFzaUUwI1I/IktmJnNBZ1YtJyElcTghajdjRmc6PiFkdApNTXRYXD5VZ0Q1XG0/b00jKCpfNmpcbC9HYU1fYm1gWVpMZzE5amxeMDgpdTBnKW8hYGJeVCEqJFh1ZSg+W20lU201JVhaLl8vUzJiMStBKwpsPUJpSl07PFhvNFAla0hcM3VtdDU2SmBMXzMpTionKF0kJVFbNmUrSHEqKmI3KE5VU1ohJjNhVikjI05TJDNHVmVVI2cwJCVBb2FmLj5BKAo2YiNPVCJEYCxzKHJFKylNMD5GREo0akk6bTVlWVVRY2MsWUZpIiwyUS0jWVQ6YEw7QTJgMHMjLTgoUypxTVxzPjtnODNSZVoiQnVJO1p0Wgo9YSdzViJEPiIyaTtiRSssOlZDP18jUSpROGMqbkIpWV1ANlgnMUldTStiNEhfQTFGRGNjKTtPPmZZaElKNG5CYG0xMWRmaSVcM08qWlA+awowcVM+Qmk4RDlgQ145Vk8uJHFwbEJuPFAsVUxbJT4iW20jM21VWCNjL0xER0ZwPHAxJ1teXEdVNCM+ZE1RL0VRJFYkKjBgcWQjRTdCY2wmOQorYCdAJklaY1MkXD1WaGFUQWZfL1prKCVUNWA9QU4hST0lcjo+PT1MQThqU2FPK1hlKUVQSiFRVm4yckhsV0pbVjUnck1gY21XaXIpZypzcApAP0xCX0AzOSkoV09xWU9VIlcpblpPNzAwbzAtRW1kVCFYJjw7QSpsRmx1QzliRGIuLm4/MVE0MFgiTlhsPzlGOlBoVURkLypELUJDMD50NQpHUiliJ1thZ2AjTygpJilOdFFyLDVPWVl0WS5USEFScWdKYipSXmkkUSw2dWNDL2lOS15LOztdIllBNSRiaWRPPVtUTGs8RU8hLS5oOyc7KwonWHQtXkhFbDpDTVleQiFWWXA6LT1iIzQ9U1gpVi5tJUtSW2dzUC5nSFoudWFwTiFVQkRgKE8xak91YDNZKEN0Tk1kZC49aVduN1dXazY1VwokYWA4KkJMMC1XMlZbNF1RU2w7OTpBI08wbi5AKk9qNkckbEdfImZRSVlnO0BbcUxvYycjJURWXmlmVSpbK0Q+M21VMEA7YjpQN11YMldAJQpYT0JmPiknbm9XYWI+KSdtJEciRzRkVilfIiZyWGNVcUE5PGA9ZzBUbWwwP08kWFlTTVE1K2thcFkwXmtlMCtMcj07PjE5WnMmZj1FMStDYwpiJDsuMVUmJ01LR2RrMWlUal1eRElKYEAhRWtaVWRFPDFaX0VvRHE9aTBMVkkjKDhHZl1vJWQ8VjZwMjgkY0BQO0QwbGw3XWVRYV4mOEFdJgpIY01ZODgpbUIhXDJmPCZgVDpfbEskMUxqP29IJDZfL0tnSC45cDFhJXRFPjRybUx1OW0lMi5cQV9eY0wwOixlMi5lKEUuaiFfI01bP2E4cApBZWlOa1xCc2VpcjpBPVlVVDQnRFBEK2JdWktfdG5GaydaWzU5YiwwOWwnJCVATEJHNztKXVE0ZW0/U1FiQWU+Ymw2YEc8bUxtJVtcLTIxOwpPTHFHbj9fMlVhT287aTZTPkQ4JCRDRSIwKGRXL1ZgaiFTQ29gJyJicVpDPzJbR2xSZyxMKl5kSFcwaGFxVlxOKX4+CmVuZHN0cmVhbQplbmRvYmoKMjMgMCBvYmoKPDwgL1R5cGUgL1hPYmplY3QKL1N1YnR5cGUgL0ltYWdlCi9XaWR0aCAxMTgKL0hlaWdodCA0OQovQ29sb3JTcGFjZSAvRGV2aWNlR3JheQovQml0c1BlckNvbXBvbmVudCA4Ci9MZW5ndGggNDYxCi9GaWx0ZXIgWy9BU0NJSTg1RGVjb2RlIC9GbGF0ZURlY29kZV0KPj5zdHJlYW0KR2IiL2VKSV1SPyNYblhrVDZBPlhLbkRiV0IiTVpFYWpQcGQ0XScoXkBSbHQia0IiUzAkZiU/PW09NEM7Oy4kTihqUmNZUiVzZCZsOSRPdF4KKSY3PUwoNy1lcXFlQC4oL1NDOTg0LWZMWGVMWjVxY1o1bEFFQjU1PjNAMD1rIjtSaDJoQmNRTDMmSj81b1tjSDBiU0ZOXjw7O0A0MVNZOW0KYyJaST1ZbCNjNClgXyJZbG1OMyUuQS5sTlNgVmUvWTwlPy43KCgpLy5kQls7ayFKWyUnJURKXEk/K2E3OjVvTmtZXHFFUz4zPEk1YlptKEkKJWQ8QEIpOERidDNwS0djbGJRazEnaVpWczdOTTBcbyZSKnFVPmdIdS1GckNraDxrSEZHKlwkTT1fc1YvLSRcSkY6ZS8/PmZYQStDQ21wRGUKZFNQNkdjdSxcWCdBTD1hNUpDWzQ2Ry5ocDI9VTRlXiRlb1xRI2IqbTdDOCQtSkEoY1o/WWAnQzs2SnBIZVBsXCRIRUMhdV4qUWErNmdFTWsKW2ZFVipiLiM+cHI+LVdTZiM+aCZXP3Vra1RzaFlgPS9YLjY2QSo7YmlzL2RnQFFYWHNyOG07fj4KZW5kc3RyZWFtCmVuZG9iagoyNCAwIG9iago8PCAvVHlwZSAvWE9iamVjdAovU3VidHlwZSAvSW1hZ2UKL1dpZHRoIDU0Ci9IZWlnaHQgNTQKL0NvbG9yU3BhY2UgL0RldmljZUdyYXkKL0JpdHNQZXJDb21wb25lbnQgOAovTGVuZ3RoIDc3Ci9GaWx0ZXIgWy9BU0NJSTg1RGVjb2RlIC9GbGF0ZURlY29kZV0KPj5zdHJlYW0KR2IiMEpkMFRkcSRqNG9GXlUsIkhUczlFSUU7MEFULF9FKkxaJW9AN0psNVY7SCdDcz1UcnFEYUguNEJmI2M0T1ZUOyhkI2Y8R0U5fj4KZW5kc3RyZWFtCmVuZG9iagoyNSAwIG9iago8PCAvVHlwZSAvWE9iamVjdAovU3VidHlwZSAvSW1hZ2UKL1dpZHRoIDI3NwovSGVpZ2h0IDczCi9Db2xvclNwYWNlIC9EZXZpY2VHcmF5Ci9CaXRzUGVyQ29tcG9uZW50IDgKL0xlbmd0aCAxMzk0Ci9GaWx0ZXIgWy9BU0NJSTg1RGVjb2RlIC9GbGF0ZURlY29kZV0KPj5zdHJlYW0KR2IiL2NnUSE0LSRxJ2pqNUwjcFpHdTY9I0g/JWghJFonRWs9WCZuTU9vK0xPY1gvbXImKVZsP0ttSitFbkU5ISNrSSNwOTYyYy02LE11dUEKb0ZaSG08JnBIZ1NgJEAobS03LVVRKDckSV1fSl5ZU0E3bScpQiY5LVo7Oz1aNT03Xj5KZEhedFRxcWYqXz1JLWQqb0BVWjpjT1soIWFJTGEKYjByalFXUDslUFhjP3M8cFRbTzFiI0trUEVgdUVCV1xKUl47dVxrPjRSVjlmNGdoIjYzSnU2ZUgtQit1QzE8IjdpVVdbU1cqOllYalpjIygKQjdfQFpCWmM1T1w8cEQ8Q0RrTmVMYTE3O0o+TV5qMmovMWUrJV9sLTctSStaV1U0NCkvWDFzMCZXMEsiUElwOWZWPyYpSUMqWkNiNWtrZ1MKL1JgMGlGNkNibS4/RyZQJiZMRnNVKkZsWlVgbSpBKDxaWi9pb1lEWmFdL2phJ1I5Jjk5SUhLVF8uVTA4LzZlZ1NBZkI8NF9dQT8jO1wsJi0KIkQiZkBrJTVDTzZGZDhyXW8ldU1hOCdFcXEmTS5hOFxgJFRpciMvdCwvO1NWMFAiOjkkX2VuNFBpaVhFUW4hY1BeLyxUZjlkaEJkJ0kuZUEKUW9QISkmMj42IUUqKlgrVTtcbWBKYWVhRyUiY3BdMidaNV9dTUtEVUc2WVpVKDxUbzJCbXMjdDlZbG5uWG83IzMkJDAhbSluLFJQYGApcm8KN09gNT5LYjcrdCYyJFRST0M0YjVQXFgpYCs/PStmLXJtc10yQj0/bzJXWnVgVmBHbjdrYG4sdFVJYjtzckJxRUw3NjJdIyFTYGMoRGtTX0gKWCYrc1lyVFw7PU1MRD1cZCp1S2ZWWXRmKkUjS0A8bFRbO24vbjNNLyw+LSFZQmpoKm41Vjg0U0VaJ2FlUC1Hb14pSCdwI1cvNHJuRTQraTEKK0lCRlA1Uys0PThGOSU3Tyo6ZipuM0otYTc2MmIzYiFOV0hWKWhGK21iLC1VLUU5U05oST4sVSo8LkdtcC0pMiQvLztJOm4+W2I3cUljKDYKcElAI05UZSlHY0s3YFliUFRmZERhbiNLbVBdV145KDZqbGNMQlFlVzdxTCMjPDNlNW8rPC0pNGNsNFR1XFwoYFNiJm8qRUAnYytqam1aUCoKNE5nRkdFXiQmOi4mXyVQRkBONWQ1dSFgR1Y2bylVS0c3OCsmW1A6TGIlMnRRNC9DbF9OTltXI3A/XkxqNCRtVlZTZCZOMCwzPUA4J0xRKHQKTGBuZWAvWXM4aiwlbSVQOl9xMnItbWRjPVhYNSY+OiNZO24+LipHcGZtVyc8OE9fRWtsPSkkTi9HRCtRSFhyWD5HLCVpYUtzRlBDNjVfLE0KQD8yXic5Mk1JVz8kZ2s1aEQ+YGtuOzFPLSViazVuXVteOj5QX0YsaWIzM3ErW249OCFibkBBbGViMltVU2NoT0VrXVdpV189KCQxOjM4KTsKIklWbHFLNDFOK1BsNjxBOmk4Uyg0PSc1cChjV2RCQmQtZSNgMVdoOzs6QXQzQ3Q+YURLQklQaWNdKzMyXTtnXTRXWEVDM2drPFBMMnFnLHMKJG5FSDJqP14haFMrUztVTGR0U2pAYV9fYjtsQGprRlxvPUs1PCgxUSRzP3BjJGZzLi5abUE9dD47X0UpRzVjNzkocyokJFZCITA2WyEoLGUKLVUzTFJKbCQwWFxKT1loQjYtdSsoV28oVCMsVD0qLVVkPiU8V3FTXmVqKyUrZWRqXksiVnNIMi5wSCZXYT5sdUxOMDRPWUo0TkJoZz9DcSwKLi9zS19UPElEX1AkQCc0fj4KZW5kc3RyZWFtCmVuZG9iagoyNiAwIG9iago8PCAvVHlwZSAvWE9iamVjdAovU3VidHlwZSAvSW1hZ2UKL1dpZHRoIDExOAovSGVpZ2h0IDQ5Ci9Db2xvclNwYWNlIC9EZXZpY2VHcmF5Ci9CaXRzUGVyQ29tcG9uZW50IDgKL0xlbmd0aCA0NjEKL0ZpbHRlciBbL0FTQ0lJODVEZWNvZGUgL0ZsYXRlRGVjb2RlXQo+PnN0cmVhbQpHYiIvZUpJXVI/I1huWGtUNkE+WEtuRGJXQiJNWkVhalBwZDRdJyheQFJsdCJrQiJTMCRmJT89bT00Qzs7LiROKGpSY1lSJXNkJmw5JE90XgopJjc9TCg3LWVxcWVALigvU0M5ODQtZkxYZUxaNXFjWjVsQUVCNTU+M0AwPWsiO1JoMmhCY1FMMyZKPzVvW2NIMGJTRk5ePDs7QDQxU1k5bQpjIlpJPVlsI2M0KWBfIllsbU4zJS5BLmxOU2BWZS9ZPCU/LjcoKCkvLmRCWztrIUpbJSclREpcST8rYTc6NW9Oa1lccUVTPjM8STViWm0oSQolZDxAQik4RGJ0M3BLR2NsYlFrMSdpWlZzN05NMFxvJlIqcVU+Z0h1LUZyQ2toPGtIRkcqXCRNPV9zVi8tJFxKRjplLz8+ZlhBK0NDbXBEZQpkU1A2R2N1LFxYJ0FMPWE1SkNbNDZHLmhwMj1VNGVeJGVvXFEjYiptN0M4JC1KQShjWj9ZYCdDOzZKcEhlUGxcJEhFQyF1XipRYSs2Z0VNawpbZkVWKmIuIz5wcj4tV1NmIz5oJlc/dWtrVHNoWWA9L1guNjZBKjtiaXMvZGdAUVhYc3I4bTt+PgplbmRzdHJlYW0KZW5kb2JqCjI3IDAgb2JqCjw8IC9UeXBlIC9YT2JqZWN0Ci9TdWJ0eXBlIC9JbWFnZQovV2lkdGggNTQKL0hlaWdodCA1NAovQ29sb3JTcGFjZSAvRGV2aWNlR3JheQovQml0c1BlckNvbXBvbmVudCA4Ci9MZW5ndGggNzcKL0ZpbHRlciBbL0FTQ0lJODVEZWNvZGUgL0ZsYXRlRGVjb2RlXQo+PnN0cmVhbQpHYiIwSmQwVGRxJGo0b0ZeVSwiSFRzOUVJRTswQVQsX0UqTFolb0A3Smw1VjtIJ0NzPVRycURhSC40QmYjYzRPVlQ7KGQjZjxHRTl+PgplbmRzdHJlYW0KZW5kb2JqCnhyZWYKMCAyOAowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAwMDAwMDkgMDAwMDAgbiAKMDAwMDAwMDA1OCAwMDAwMCBuIAowMDAwMDAwMTA0IDAwMDAwIG4gCjAwMDAwMDAxNzYgMDAwMDAgbiAKMDAwMDAwMDIyOCAwMDAwMCBuIAowMDAwMDAwMzI2IDAwMDAwIG4gCjAwMDAwMDA0MjkgMDAwMDAgbiAKMDAwMDAwMDUzNSAwMDAwMCBuIAowMDAwMDAwNjQ1IDAwMDAwIG4gCjAwMDAwMDA3NDEgMDAwMDAgbiAKMDAwMDAwMDg0MyAwMDAwMCBuIAowMDAwMDAwOTQ4IDAwMDAwIG4gCjAwMDAwMDEwNTcgMDAwMDAgbiAKMDAwMDAwMTE1OCAwMDAwMCBuIAowMDAwMDAxMjU4IDAwMDAwIG4gCjAwMDAwMDEzNjAgMDAwMDAgbiAKMDAwMDAwMTQ2NiAwMDAwMCBuIAowMDAwMDAxNjM2IDAwMDAwIG4gCjAwMDAwMDIwNTMgMDAwMDAgbiAKMDAwMDAwMjQ3MCAwMDAwMCBuIAowMDAwMDAyODg3IDAwMDAwIG4gCjAwMDAwMDU1ODYgMDAwMDAgbiAKMDAwMDAwODc0MiAwMDAwMCBuIAowMDAwMDA5Mzg5IDAwMDAwIG4gCjAwMDAwMDk2NTAgMDAwMDAgbiAKMDAwMDAxMTIzMSAwMDAwMCBuIAowMDAwMDExODc4IDAwMDAwIG4gCnRyYWlsZXIKPDwKL0luZm8gMTcgMCBSCi9TaXplIDI4Ci9Sb290IDEgMCBSCj4+CnN0YXJ0eHJlZgoxMjEzOQolJUVPRgo="
      }
    ]
  },
  "customsInvoice": {
    "type": "string",
    "data": "string"
  },
  "pickup": {
    "confirmationNumber": "string"
  },
  "packingSlip": "string",
  "quote": {
    "carrierName": "string",
    "serviceId": 0,
    "serviceName": "string",
    "deliveryCarrier": "string",
    "modeTransport": "AIR",
    "transitDays": "string",
    "baseCharge": 0,
    "fuelSurcharge": 0,
    "fuelSurchargePercentage": 0,
    "carbonNeutralFees": 0,
    "surcharges": [
      {
        "name": "string",
        "amount": 0
      }
    ],
    "totalCharge": 0,
    "processingFees": 0,
    "taxes": [
      {
        "name": "string",
        "amount": 0
      }
    ],
    "totalChargedAmount": 0,
    "currency": "string",
    "carrierLogo": "string",
    "id": "string"
  },
  "billing": {
    "invoices": [
      {
        "invoiceNumber": "string",
        "charges": [
          {
            "charge": "string",
            "amount": "string",
            "adjustmentReasons": "string"
          }
        ],
        "total": 0
      }
    ]
  },
  "returnShipment": "string",
  "message": "string"
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
