import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestAlliedExpressShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(
            **ShipmentCancelPayload
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(lib.to_dict(request.serialize()), ShipmentRequest)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(request.serialize(), ShipmentCancelRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.allied_express.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/GetLabelfull",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.allied_express.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/cancelJob/123456789/12345",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.allied_express.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.allied_express.proxy.lib.request") as mock:
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
        with patch("karrio.mappers.allied_express.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "shipper": {
        "company_name": "TESTING COMPANY",
        "address_line1": "17 VULCAN RD",
        "address_line2": "test",
        "city": "CANNING VALE",
        "postal_code": "6155",
        "country_code": "AU",
        "person_name": "TEST USER",
        "state_code": "WA",
        "email": "test@gmail.com",
        "phone_number": "(07) 3114 1499",
    },
    "recipient": {
        "company_name": "TESTING COMPANY",
        "address_line1": "17 VULCAN RD",
        "address_line2": "test",
        "city": "CANNING VALE",
        "postal_code": "6155",
        "country_code": "AU",
        "person_name": "TEST USER",
        "state_code": "WA",
        "email": "test@gmail.com",
    },
    "parcels": [
        {
            "height": 50,
            "length": 50,
            "weight": 20,
            "width": 12,
            "dimension_unit": "CM",
            "weight_unit": "KG",
            "options": {"dangerous_good": False},
        },
        {
            "height": 50,
            "length": 50,
            "weight": 20,
            "width": 12,
            "dimension_unit": "CM",
            "weight_unit": "KG",
            "options": {"dangerous_good": True},
        },
    ],
    "service": "allied_road_service",
    "options": {
        "instructions": "This is just an instruction",
    },
    "reference": "REF-001",
}


ShipmentCancelPayload = {
    "shipment_identifier": "123456789",
    "options": {"postal_code": "12345"},
}

ParsedShipmentResponse = [
    {
        "carrier_id": "allied_express",
        "carrier_name": "allied_express",
        "docs": {"label": ANY},
        "label_type": "PDF",
        "meta": {"postal_code": "6155"},
        "shipment_identifier": "AOE946862J",
        "tracking_number": "AOE946862J",
    },
    [],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "allied_express",
        "carrier_name": "allied_express",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "allied_express",
            "carrier_name": "allied_express",
            "code": "500",
            "details": {},
            "message": '"account" is a required property\n'
            "\n"
            'Failed validating "required" in schema',
        }
    ],
]

ShipmentRequest = {
    "account": "ACCOUNT",
    "bookedBy": "TEST USER",
    "instructions": "This is just an instruction",
    "itemCount": 2,
    "items": [
        {
            "dangerous": False,
            "height": 50.0,
            "itemCount": 1,
            "length": 50.0,
            "volume": 0.1,
            "weight": 20.0,
            "width": 12.0,
        },
        {
            "dangerous": True,
            "height": 50.0,
            "itemCount": 1,
            "length": 50.0,
            "volume": 0.1,
            "weight": 20.0,
            "width": 12.0,
        },
    ],
    "jobStops_D": {
        "companyName": "TESTING COMPANY",
        "contact": "TEST USER",
        "emailAddress": "test@gmail.com",
        "geographicAddress": {
            "address1": "17 VULCAN RD",
            "address2": "test",
            "country": "AU",
            "postCode": "6155",
            "state": "WA",
            "suburb": "CANNING VALE",
        },
        "phoneNumber": "(00) 0000 0000",
    },
    "jobStops_P": {
        "companyName": "TESTING COMPANY",
        "contact": "TEST USER",
        "emailAddress": "test@gmail.com",
        "geographicAddress": {
            "address1": "17 VULCAN RD",
            "address2": "test",
            "country": "AU",
            "postCode": "6155",
            "state": "WA",
            "suburb": "CANNING VALE",
        },
        "phoneNumber": "(07) 3114 1499",
    },
    "referenceNumbers": ["REF-001"],
    "serviceLevel": "R",
    "volume": 0.1,
    "weight": 40.0,
}

ShipmentCancelRequest = {"shipmentno": "123456789", "postalcode": "12345"}

ShipmentResponse = """{
    "Price": {
        "soapenv:Envelope": {
            "@xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
            "@xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
            "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "soapenv:Body": {
                "ns1:calculatePriceResponse": {
                    "@xmlns:ns1": "http://neptune.alliedexpress.com.au/ttws-ejb",
                    "result": {
                        "jobCharge": "14.18",
                        "surcharges": [
                            {
                                "chargeCode": "ON FWD PICKUP",
                                "description": "ON FORWARD PICKUP",
                                "netValue": "0.0",
                                "quantity": "1"
                            },
                            {
                                "chargeCode": "ON FWD DELIVERY",
                                "description": "ON FORWARD DELIVERY",
                                "netValue": "0.0",
                                "quantity": "1"
                            },
                            {
                                "chargeCode": "HD",
                                "description": "FREIGHT OVERSIZED HOME DELIVERY",
                                "netValue": "0.0",
                                "quantity": "1"
                            },
                            {
                                "chargeCode": "LSC",
                                "description": "LENGTH SURCHARGE",
                                "netValue": "0.0",
                                "quantity": "1"
                            },
                            {
                                "chargeCode": "MHF",
                                "description": "HANDLING FEE",
                                "netValue": "0.0",
                                "quantity": "1"
                            }
                        ],
                        "totalCharge": "40.66"
                    }
                }
            }
        }
    },
    "Tracking": "AOE946862J",
    "soapenv:Body": {
        "ns1:getLabelResponse": {
            "@xmlns:ns1": "http://neptune.alliedexpress.com.au/ttws-ejb",
            "result": "JVBERi0xLjQKJeLjz9MKNCAwIG9iago8PC9UeXBlL1hPYmplY3QvQ29sb3JTcGFjZS9EZXZpY2VSR0IvU3VidHlwZS9JbWFnZS9CaXRzUGVyQ29tcG9uZW50IDgvV2lkdGggNDE0L0xlbmd0aCA1Mzk1L0hlaWdodCA1MC9GaWx0ZXIvRENURGVjb2RlPj5zdHJlYW0K/9j/4AAQSkZJRgABAgAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAAyAZ4DASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwBP+bQ/8/8AP/R/zd5/n/nwo/5tD/z/AM/9H/N3n+f+fCgDgPCX/JIfiL/3DP8A0oau/wD+bvP8/wDPhXAeEv8AkkPxF/7hn/pQ1d//AM3ef5/58KAD4f8A/NHf+41/7NR8QP8AmsX/AHBf/ZaPh/8A80d/7jX/ALNR8QP+axf9wX/2WgDgPFv/ACSH4df9xP8A9KFrv/iB/wA1i/7gv/stcB4t/wCSQ/Dr/uJ/+lC13/xA/wCaxf8AcF/9loAPh/8A80d/7jX/ALNR8QP+axf9wX/2Wj4f/wDNHf8AuNf+zUfED/msX/cF/wDZaAD4f/8ANHf+41/7NR+zL/zNP/bp/wC1qPh//wA0d/7jX/s1H7Mv/M0/9un/ALWoAPh//wA0d/7jX/s1cB4t/wCSQ/Dr/uJ/+lC13/w//wCaO/8Aca/9mrgPFv8AySH4df8AcT/9KFoA9/8AFv8AyV74df8AcT/9J1rwDwl/ySH4i/8AcM/9KGr3/wAW/wDJXvh1/wBxP/0nWvAPCX/JIfiL/wBwz/0oagDv/iB/zWL/ALgv/stH7TX/ADK3/b3/AO0aPiB/zWL/ALgv/stH7TX/ADK3/b3/AO0aAD4gf81i/wC4L/7LR8P/APmjv/ca/wDZqPiB/wA1i/7gv/stHw//AOaO/wDca/8AZqAD9mX/AJmn/t0/9rVwHhL/AJJD8Rf+4Z/6UNXf/sy/8zT/ANun/tauA8Jf8kh+Iv8A3DP/AEoagDv/AIgf81i/7gv/ALLR8P8A/mjv/ca/9mo+IH/NYv8AuC/+y0fD/wD5o7/3Gv8A2agA+IH/ADWL/uC/+y0fD/8A5o7/ANxr/wBmo+IH/NYv+4L/AOy0fD//AJo7/wBxr/2agDgPFv8AySH4df8AcT/9KFrv/wBpr/mVv+3v/wBo1wHi3/kkPw6/7if/AKULXf8A7TX/ADK3/b3/AO0aAD4gf81i/wC4L/7LR8QP+axf9wX/ANlo+IH/ADWL/uC/+y0fED/msX/cF/8AZaAD/m0P/P8Az/0fED/msX/cF/8AZaP+bQ/8/wDP/R8QP+axf9wX/wBloAPh/wD80d/7jX/s1cB4t/5JD8Ov+4n/AOlC13/w/wD+aO/9xr/2auA8W/8AJIfh1/3E/wD0oWgDv/2mv+ZW/wC3v/2jR8QP+axf9wX/ANlo/aa/5lb/ALe//aNHxA/5rF/3Bf8A2WgD0Dxb/wAle+HX/cT/APSda8A8W/8AJIfh1/3E/wD0oWvf/Fv/ACV74df9xP8A9J1rwDxb/wAkh+HX/cT/APShaAO//wCbvP8AP/PhR8P/APmjv/ca/wDZqP8Am7z/AD/z4UfD/wD5o7/3Gv8A2agA/wCbvP8AP/PhXAeEv+SQ/EX/ALhn/pQ1d/8A83ef5/58K4Dwl/ySH4i/9wz/ANKGoA7/AOIH/NYv+4L/AOy0ftNf8yt/29/+0aPiB/zWL/uC/wDstH7TX/Mrf9vf/tGgA/5u8/z/AM+FcB4t/wCSQ/Dr/uJ/+lC13/8Azd5/n/nwrgPFv/JIfh1/3E//AEoWgD3/AMJf8le+Iv8A3DP/AEnavP8A4f8A/NHf+41/7NXoHhL/AJK98Rf+4Z/6TtXn/wAP/wDmjv8A3Gv/AGagDgPCX/JIfiL/ANwz/wBKGr3/AMW/8le+HX/cT/8ASda8A8Jf8kh+Iv8A3DP/AEoavf8Axb/yV74df9xP/wBJ1oA8A8Jf8kh+Iv8A3DP/AEoajxb/AMkh+HX/AHE//ShaPCX/ACSH4i/9wz/0oajxb/ySH4df9xP/ANKFoA7/AP5tD/z/AM/9H/N3n+f+fCj/AJtD/wA/8/8AR/zd5/n/AJ8KAOA8Jf8AJIfiL/3DP/Shq7//AJu8/wA/8+FcB4S/5JD8Rf8AuGf+lDV3/wDzd5/n/nwoAPh//wA0d/7jX/s1HxA/5rF/3Bf/AGWj4f8A/NHf+41/7NR8QP8AmsX/AHBf/ZaAOA8W/wDJIfh1/wBxP/0oWu/+IH/NYv8AuC/+y1wHi3/kkPw6/wC4n/6ULXf/ABA/5rF/3Bf/AGWgA+H/APzR3/uNf+zUfED/AJrF/wBwX/2Wj4f/APNHf+41/wCzUfED/msX/cF/9loAPh//AM0d/wC41/7NR+zL/wAzT/26f+1qPh//AM0d/wC41/7NR+zL/wAzT/26f+1qAD4f/wDNHf8AuNf+zVwHi3/kkPw6/wC4n/6ULXf/AA//AOaO/wDca/8AZq4Dxb/ySH4df9xP/wBKFoA9/wDFv/JXvh1/3E//AEnWvAPCX/JIfiL/ANwz/wBKGr3/AMW/8le+HX/cT/8ASda8A8Jf8kh+Iv8A3DP/AEoagDv/AIgf81i/7gv/ALLR+01/zK3/AG9/+0aPiB/zWL/uC/8AstH7TX/Mrf8Ab3/7RoAPiB/zWL/uC/8AstHw/wD+aO/9xr/2aj4gf81i/wC4L/7LR8P/APmjv/ca/wDZqAD9mX/maf8At0/9rVwHhL/kkPxF/wC4Z/6UNXf/ALMv/M0/9un/ALWrgPCX/JIfiL/3DP8A0oagDv8A4gf81i/7gv8A7LR8P/8Amjv/AHGv/ZqPiB/zWL/uC/8AstHw/wD+aO/9xr/2agA+IH/NYv8AuC/+y0fD/wD5o7/3Gv8A2aj4gf8ANYv+4L/7LR8P/wDmjv8A3Gv/AGagDgPFv/JIfh1/3E//AEoWu/8A2mv+ZW/7e/8A2jXAeLf+SQ/Dr/uJ/wDpQtd/+01/zK3/AG9/+0aAD4gf81i/7gv/ALLR8QP+axf9wX/2Wj4gf81i/wC4L/7LR8QP+axf9wX/ANloAP8Am0P/AD/z/wBHxA/5rF/3Bf8A2Wj/AJtD/wA/8/8AR8QP+axf9wX/ANloAPh//wA0d/7jX/s1cB4t/wCSQ/Dr/uJ/+lC13/w//wCaO/8Aca/9mrgPFv8AySH4df8AcT/9KFoA7/8Aaa/5lb/t7/8AaNHxA/5rF/3Bf/ZaP2mv+ZW/7e//AGjR8QP+axf9wX/2WgD0Dxb/AMle+HX/AHE//Sda8A8W/wDJIfh1/wBxP/0oWvf/ABb/AMle+HX/AHE//Sda8A8W/wDJIfh1/wBxP/0oWgDv/wDm7z/P/PhR8P8A/mjv/ca/9mo/5u8/z/z4UfD/AP5o7/3Gv/ZqAD/m7z/P/PhXAeEv+SQ/EX/uGf8ApQ1d/wD83ef5/wCfCuA8Jf8AJIfiL/3DP/ShqAO/+IH/ADWL/uC/+y0ftNf8yt/29/8AtGj4gf8ANYv+4L/7LR+01/zK3/b3/wC0aAD/AJu8/wA/8+FcB4t/5JD8Ov8AuJ/+lC13/wDzd5/n/nwrgPFv/JIfh1/3E/8A0oWgD3/wl/yV74i/9wz/ANJ2rz/4f/8ANHf+41/7NXoHhL/kr3xF/wC4Z/6TtXn/AMP/APmjv/ca/wDZqAOA8Jf8kh+Iv/cM/wDShq9/8W/8le+HX/cT/wDSda8A8Jf8kh+Iv/cM/wDShq9/8W/8le+HX/cT/wDSdaAPAPCX/JIfiL/3DP8A0oajxb/ySH4df9xP/wBKFo8Jf8kh+Iv/AHDP/ShqPFv/ACSH4df9xP8A9KFoA7//AJtD/wA/8/8AR/zd5/n/AJ8KP+bQ/wDP/P8A0f8AN3n+f+fCgDgPCX/JIfiL/wBwz/0oau//AObvP8/8+FcB4S/5JD8Rf+4Z/wClDV3/APzd5/n/AJ8KAD4f/wDNHf8AuNf+zUfED/msX/cF/wDZaPh//wA0d/7jX/s1HxA/5rF/3Bf/AGWgDgPFv/JIfh1/3E//AEoWu/8AiB/zWL/uC/8AstcB4t/5JD8Ov+4n/wClC13/AMQP+axf9wX/ANloAPh//wA0d/7jX/s1HxA/5rF/3Bf/AGWj4f8A/NHf+41/7NR8QP8AmsX/AHBf/ZaAD4f/APNHf+41/wCzUfsy/wDM0/8Abp/7Wo+H/wDzR3/uNf8As1H7Mv8AzNP/AG6f+1qAD4f/APNHf+41/wCzVwHi3/kkPw6/7if/AKULXf8Aw/8A+aO/9xr/ANmrgPFv/JIfh1/3E/8A0oWgD3/xb/yV74df9xP/ANJ1rwDwl/ySH4i/9wz/ANKGr3/xb/yV74df9xP/ANJ1rwDwl/ySH4i/9wz/ANKGoA7/AOIH/NYv+4L/AOy0ftNf8yt/29/+0aPiB/zWL/uC/wDstH7TX/Mrf9vf/tGgA+IH/NYv+4L/AOy0fD//AJo7/wBxr/2aj4gf81i/7gv/ALLR8P8A/mjv/ca/9moAP2Zf+Zp/7dP/AGtXAeEv+SQ/EX/uGf8ApQ1d/wDsy/8AM0/9un/tauA8Jf8AJIfiL/3DP/ShqAO/+IH/ADWL/uC/+y0fD/8A5o7/ANxr/wBmo+IH/NYv+4L/AOy0fD//AJo7/wBxr/2agA+IH/NYv+4L/wCy0fD/AP5o7/3Gv/ZqPiB/zWL/ALgv/stHw/8A+aO/9xr/ANmoA4Dxb/ySH4df9xP/ANKFrv8A9pr/AJlb/t7/APaNcB4t/wCSQ/Dr/uJ/+lC13/7TX/Mrf9vf/tGgA+IH/NYv+4L/AOy0fED/AJrF/wBwX/2Wj4gf81i/7gv/ALLR8QP+axf9wX/2WgA/5tD/AM/8/wDR8QP+axf9wX/2Wj/m0P8Az/z/ANHxA/5rF/3Bf/ZaAD4f/wDNHf8AuNf+zVwHi3/kkPw6/wC4n/6ULXf/AA//AOaO/wDca/8AZq4Dxb/ySH4df9xP/wBKFoA7/wDaa/5lb/t7/wDaNHxA/wCaxf8AcF/9lo/aa/5lb/t7/wDaNHxA/wCaxf8AcF/9loA9A8W/8le+HX/cT/8ASda8A8W/8kh+HX/cT/8ASha9/wDFv/JXvh1/3E//AEnWvAPFv/JIfh1/3E//AEoWgDv/APm7z/P/AD4UfD//AJo7/wBxr/2aj/m7z/P/AD4UfD//AJo7/wBxr/2agA/5u8/z/wA+FcB4S/5JD8Rf+4Z/6UNXf/8AN3n+f+fCuA8Jf8kh+Iv/AHDP/ShqAO/+IH/NYv8AuC/+y0ftNf8AMrf9vf8A7Ro+IH/NYv8AuC/+y0ftNf8AMrf9vf8A7RoAP+bvP8/8+FcB4t/5JD8Ov+4n/wClC13/APzd5/n/AJ8K4Dxb/wAkh+HX/cT/APShaAPf/CX/ACV74i/9wz/0navP/h//AM0d/wC41/7NXoHhL/kr3xF/7hn/AKTtXn/w/wD+aO/9xr/2agDgPCX/ACSH4i/9wz/0oavf/Fv/ACV74df9xP8A9J1rwDwl/wAkh+Iv/cM/9KGr3/xb/wAle+HX/cT/APSdaAPAPCX/ACSH4i/9wz/0oajxb/ySH4df9xP/ANKFo8Jf8kh+Iv8A3DP/AEoajxb/AMkh+HX/AHE//ShaAO//AObQ/wDP/P8A0f8AN3n+f+fCiigDgPCX/JIfiL/3DP8A0oau/wD+bvP8/wDPhRRQAfD/AP5o7/3Gv/ZqPiB/zWL/ALgv/stFFAHAeLf+SQ/Dr/uJ/wDpQtd/8QP+axf9wX/2WiigA+H/APzR3/uNf+zUfED/AJrF/wBwX/2WiigA+H//ADR3/uNf+zUfsy/8zT/26f8AtaiigA+H/wDzR3/uNf8As1cB4t/5JD8Ov+4n/wClC0UUAe/+Lf8Akr3w6/7if/pOteAeEv8AkkPxF/7hn/pQ1FFAHf8AxA/5rF/3Bf8A2Wj9pr/mVv8At7/9o0UUAHxA/wCaxf8AcF/9lo+H/wDzR3/uNf8As1FFAB+zL/zNP/bp/wC1q4Dwl/ySH4i/9wz/ANKGoooA7/4gf81i/wC4L/7LR8P/APmjv/ca/wDZqKKAD4gf81i/7gv/ALLR8P8A/mjv/ca/9moooA4Dxb/ySH4df9xP/wBKFrv/ANpr/mVv+3v/ANo0UUAHxA/5rF/3Bf8A2Wj4gf8ANYv+4L/7LRRQAf8ANof+f+f+j4gf81i/7gv/ALLRRQAfD/8A5o7/ANxr/wBmrgPFv/JIfh1/3E//AEoWiigDv/2mv+ZW/wC3v/2jR8QP+axf9wX/ANloooA9A8W/8le+HX/cT/8ASda8A8W/8kh+HX/cT/8AShaKKAO//wCbvP8AP/PhR8P/APmjv/ca/wDZqKKAD/m7z/P/AD4VwHhL/kkPxF/7hn/pQ1FFAHf/ABA/5rF/3Bf/AGWj9pr/AJlb/t7/APaNFFAB/wA3ef5/58K4Dxb/AMkh+HX/AHE//ShaKKAPf/CX/JXviL/3DP8A0navP/h//wA0d/7jX/s1FFAHAeEv+SQ/EX/uGf8ApQ1e/wDi3/kr3w6/7if/AKTrRRQB4B4S/wCSQ/EX/uGf+lDUeLf+SQ/Dr/uJ/wDpQtFFAH//2QplbmRzdHJlYW0KZW5kb2JqCjUgMCBvYmoKPDwvTGVuZ3RoIDEwMzAvRmlsdGVyL0ZsYXRlRGVjb2RlPj5zdHJlYW0KeJy9WFtzozYUfudXnEfvTIx1Q8DO9IHYJHW6wV5MknaaTofBxGHryy4m3e2/7xFgry81pJHbOJZkfKTvXKRzPpkAhS4FAsy2sE0WxhfjMjK4BMZdiKaGHxkfDQY36qmSI7CRjhZG74oCZRA9GZ130Scli5/xlc9w8LWcRso54bXx62/YTw2FsjAEFdjPsZemLXEoqAvMZKIcWJAY5QO7klEjpuRqcYWuVlB9giuqfm6U0yszanFSrpCgDup7UgGUjXqivpls1GrVW4JUehPVz+t+t03KZ0xa9bdqdNgnxkai6nfbxKhWVu3mtaffxvVlkHaCYQOzhCnkNh5ExaNSH+3pXOWrxXsVHQKzKkJ7K9XrK5NPY/A2kMifRMPgGvqj27EX/KIJh2jMbkDrr5ZFnBS6VlmkBefKGwzh9u7SC72f9E2ivAFqHOdJOofhQNsovofEjpC8ke8K6Uh20yWEaqJRm7XsjHHvDsbPq2Wqaxh1eEu43g7zFn2YyiWN+jx2iP34DjjFVEWF6+oeQiJafD2IC203c94WUSp6lPUYYVwTinHecipC/0pt0ou61zWNtiWWcZz8Ec/0fWi5LUAUVk/AdP1n47Zi/9tRF/jmTUZN0vzPLHmb97arUNsFaqEtTEKXMchT42k/47ilGtLZWm0pNbYFvBOOvIH2UZMIQhtsfUiz2bN2BeKCtOAIahLt0kNZE0S00jUDQ9UC8c/0YHc+cU23nL9zSGy4v/vQ9wIIB1Ck60JXTUrBcUybb3eOPOAVXhAoNe+9D/4ZsKRswHrwtMNqMROJWe1y58Djz9ka8P/Ty7qAeAnZcl3kL0mRrZbayY00WyapZenmGkyg/L+udNQRzSBnK3RYDWhDmg7iRfr78d8ZfNgIO8lmy7h4yY+wtcss2/XrMbAK3nnhGu2Msl33vhLtKwodXwIxlUrTKu+BohrOv1/RmtXEzUaJybanxjpkOn1/eO8PYBjA9Wg0wFQZDIbRcBSYMLm7vPH7EUQj6HthOPRDiPzwdgJesCM3MV9lGtlc+NWltKuafT2FY5toXBcrLD+RW8Z5tizSKVz+Bd58nuHI//Y5T9drGK/yIp7v6EEU1gatBnt9BRbNN6bzcDXhtAD9K65WkxCkZozYuDfRx1ZNYr6UH9Uk7phUlvRNMhM3RrKAXraYERis4OMhw6tEULdqdjQ1utvRsTKHF6ZGej3Kp2kOYfqk60QbJD9diyaf0ySL8XL7vQbpA7p4+k4BDot0AfS9RUzyjTJs1OgHfHP52KF4JVMChyTEBtz57ICCsNOL6BIEx2ouo2M/1C47jeXNS5LVy1Kbw4oWmNAPfvS9n8/wC5RoophHZBEuYJfPXcCDB6+mJn8DleFXJwplbmRzdHJlYW0KZW5kb2JqCjEgMCBvYmoKPDwvR3JvdXA8PC9UeXBlL0dyb3VwL0NTL0RldmljZVJHQi9TL1RyYW5zcGFyZW5jeT4+L1BhcmVudCA2IDAgUi9Db250ZW50cyA1IDAgUi9UeXBlL1BhZ2UvUmVzb3VyY2VzPDwvWE9iamVjdDw8L2ltZzAgNCAwIFI+Pi9Qcm9jU2V0IFsvUERGIC9UZXh0IC9JbWFnZUIgL0ltYWdlQyAvSW1hZ2VJXS9Db2xvclNwYWNlPDwvQ1MvRGV2aWNlUkdCPj4vRm9udDw8L0YxIDIgMCBSL0YyIDMgMCBSPj4+Pi9NZWRpYUJveFswIDAgMjc1IDQxOV0vUm90YXRlIDkwPj4KZW5kb2JqCjggMCBvYmoKPDwvVHlwZS9YT2JqZWN0L0NvbG9yU3BhY2UvRGV2aWNlUkdCL1N1YnR5cGUvSW1hZ2UvQml0c1BlckNvbXBvbmVudCA4L1dpZHRoIDQxNC9MZW5ndGggNTMzNy9IZWlnaHQgNTAvRmlsdGVyL0RDVERlY29kZT4+c3RyZWFtCv/Y/+AAEEpGSUYAAQIAAAEAAQAA/9sAQwAIBgYHBgUIBwcHCQkICgwUDQwLCwwZEhMPFB0aHx4dGhwcICQuJyAiLCMcHCg3KSwwMTQ0NB8nOT04MjwuMzQy/9sAQwEJCQkMCwwYDQ0YMiEcITIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIy/8AAEQgAMgGeAwEiAAIRAQMRAf/EAB8AAAEFAQEBAQEBAAAAAAAAAAABAgMEBQYHCAkKC//EALUQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6g4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2drh4uPk5ebn6Onq8fLz9PX29/j5+v/EAB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC//EALURAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OXm5+jp6vLz9PX29/j5+v/aAAwDAQACEQMRAD8AT/m0P/P/AD/0f83ef5/58KP+bQ/8/wDP/R/zd5/n/nwoA4Dwl/ySH4i/9wz/ANKGrv8A/m7z/P8Az4VwHhL/AJJD8Rf+4Z/6UNXf/wDN3n+f+fCgA+H/APzR3/uNf+zUfED/AJrF/wBwX/2Wj4f/APNHf+41/wCzUfED/msX/cF/9loA4Dxb/wAkh+HX/cT/APSha7/4gf8ANYv+4L/7LXAeLf8AkkPw6/7if/pQtd/8QP8AmsX/AHBf/ZaAD4f/APNHf+41/wCzUfED/msX/cF/9lo+H/8AzR3/ALjX/s1HxA/5rF/3Bf8A2WgA+H//ADR3/uNf+zUfsy/8zT/26f8Ataj4f/8ANHf+41/7NR+zL/zNP/bp/wC1qAD4f/8ANHf+41/7NXAeLf8AkkPw6/7if/pQtd/8P/8Amjv/AHGv/Zq4Dxb/AMkh+HX/AHE//ShaAPf/ABb/AMle+HX/AHE//Sda8A8Jf8kh+Iv/AHDP/Shq9/8AFv8AyV74df8AcT/9J1rwDwl/ySH4i/8AcM/9KGoA7/4gf81i/wC4L/7LR+01/wAyt/29/wDtGj4gf81i/wC4L/7LR+01/wAyt/29/wDtGgA+IH/NYv8AuC/+y0fD/wD5o7/3Gv8A2aj4gf8ANYv+4L/7LR8P/wDmjv8A3Gv/AGagA/Zl/wCZp/7dP/a1cB4S/wCSQ/EX/uGf+lDV3/7Mv/M0/wDbp/7WrgPCX/JIfiL/ANwz/wBKGoA7/wCIH/NYv+4L/wCy0fD/AP5o7/3Gv/ZqPiB/zWL/ALgv/stHw/8A+aO/9xr/ANmoAPiB/wA1i/7gv/stHw//AOaO/wDca/8AZqPiB/zWL/uC/wDstHw//wCaO/8Aca/9moA4Dxb/AMkh+HX/AHE//Sha7/8Aaa/5lb/t7/8AaNcB4t/5JD8Ov+4n/wClC13/AO01/wAyt/29/wDtGgA+IH/NYv8AuC/+y0fED/msX/cF/wDZaPiB/wA1i/7gv/stHxA/5rF/3Bf/AGWgA/5tD/z/AM/9HxA/5rF/3Bf/AGWj/m0P/P8Az/0fED/msX/cF/8AZaAD4f8A/NHf+41/7NXAeLf+SQ/Dr/uJ/wDpQtd/8P8A/mjv/ca/9mrgPFv/ACSH4df9xP8A9KFoA7/9pr/mVv8At7/9o0fED/msX/cF/wDZaP2mv+ZW/wC3v/2jR8QP+axf9wX/ANloA9A8W/8AJXvh1/3E/wD0nWvAPFv/ACSH4df9xP8A9KFr3/xb/wAle+HX/cT/APSda8A8W/8AJIfh1/3E/wD0oWgDv/8Am7z/AD/z4UfD/wD5o7/3Gv8A2aj/AJu8/wA/8+FHw/8A+aO/9xr/ANmoAP8Am7z/AD/z4VwHhL/kkPxF/wC4Z/6UNXf/APN3n+f+fCuA8Jf8kh+Iv/cM/wDShqAO/wDiB/zWL/uC/wDstH7TX/Mrf9vf/tGj4gf81i/7gv8A7LR+01/zK3/b3/7RoAP+bvP8/wDPhR8P/wDmjv8A3Gv/AGaj/m7z/P8Az4UfD/8A5o7/ANxr/wBmoAP2Zf8Amaf+3T/2tR8P/wDmjv8A3Gv/AGaj9mX/AJmn/t0/9rUfD/8A5o7/ANxr/wBmoA4Dwl/ySH4i/wDcM/8AShq9/wDFv/JXvh1/3E//AEnWvAPCX/JIfiL/ANwz/wBKGr3/AMW/8le+HX/cT/8ASdaAPAPCX/JIfiL/ANwz/wBKGo8W/wDJIfh1/wBxP/0oWjwl/wAkh+Iv/cM/9KGo8W/8kh+HX/cT/wDShaAO/wD+bQ/8/wDP/R/zd5/n/nwo/wCbQ/8AP/P/AEf83ef5/wCfCgDgPCX/ACSH4i/9wz/0oau//wCbvP8AP/PhXAeEv+SQ/EX/ALhn/pQ1d/8A83ef5/58KAD4f/8ANHf+41/7NR8QP+axf9wX/wBlo+H/APzR3/uNf+zUfED/AJrF/wBwX/2WgDgPFv8AySH4df8AcT/9KFrv/iB/zWL/ALgv/stcB4t/5JD8Ov8AuJ/+lC13/wAQP+axf9wX/wBloAPh/wD80d/7jX/s1HxA/wCaxf8AcF/9lo+H/wDzR3/uNf8As1HxA/5rF/3Bf/ZaAD4f/wDNHf8AuNf+zUfsy/8AM0/9un/taj4f/wDNHf8AuNf+zUfsy/8AM0/9un/tagA+H/8AzR3/ALjX/s1cB4t/5JD8Ov8AuJ/+lC13/wAP/wDmjv8A3Gv/AGauA8W/8kh+HX/cT/8AShaAPf8Axb/yV74df9xP/wBJ1rwDwl/ySH4i/wDcM/8AShq9/wDFv/JXvh1/3E//AEnWvAPCX/JIfiL/ANwz/wBKGoA7/wCIH/NYv+4L/wCy0ftNf8yt/wBvf/tGj4gf81i/7gv/ALLR+01/zK3/AG9/+0aAD4gf81i/7gv/ALLR8P8A/mjv/ca/9mo+IH/NYv8AuC/+y0fD/wD5o7/3Gv8A2agA/Zl/5mn/ALdP/a1cB4S/5JD8Rf8AuGf+lDV3/wCzL/zNP/bp/wC1q4Dwl/ySH4i/9wz/ANKGoA7/AOIH/NYv+4L/AOy0fD//AJo7/wBxr/2aj4gf81i/7gv/ALLR8P8A/mjv/ca/9moAPiB/zWL/ALgv/stHw/8A+aO/9xr/ANmo+IH/ADWL/uC/+y0fD/8A5o7/ANxr/wBmoA4Dxb/ySH4df9xP/wBKFrv/ANpr/mVv+3v/ANo1wHi3/kkPw6/7if8A6ULXf/tNf8yt/wBvf/tGgA+IH/NYv+4L/wCy0fED/msX/cF/9lo+IH/NYv8AuC/+y0fED/msX/cF/wDZaAD/AJtD/wA/8/8AR8QP+axf9wX/ANlo/wCbQ/8AP/P/AEfED/msX/cF/wDZaAD4f/8ANHf+41/7NXAeLf8AkkPw6/7if/pQtd/8P/8Amjv/AHGv/Zq4Dxb/AMkh+HX/AHE//ShaAO//AGmv+ZW/7e//AGjR8QP+axf9wX/2Wj9pr/mVv+3v/wBo0fED/msX/cF/9loA9A8W/wDJXvh1/wBxP/0nWvAPFv8AySH4df8AcT/9KFr3/wAW/wDJXvh1/wBxP/0nWvAPFv8AySH4df8AcT/9KFoA7/8A5u8/z/z4UfD/AP5o7/3Gv/ZqP+bvP8/8+FHw/wD+aO/9xr/2agA/5u8/z/z4VwHhL/kkPxF/7hn/AKUNXf8A/N3n+f8AnwrgPCX/ACSH4i/9wz/0oagDv/iB/wA1i/7gv/stH7TX/Mrf9vf/ALRo+IH/ADWL/uC/+y0ftNf8yt/29/8AtGgA/wCbvP8AP/PhR8P/APmjv/ca/wDZqP8Am7z/AD/z4UfD/wD5o7/3Gv8A2agA/Zl/5mn/ALdP/a1Hw/8A+aO/9xr/ANmo/Zl/5mn/ALdP/a1Hw/8A+aO/9xr/ANmoA4Dwl/ySH4i/9wz/ANKGr3/xb/yV74df9xP/ANJ1rwDwl/ySH4i/9wz/ANKGr3/xb/yV74df9xP/ANJ1oA8A8Jf8kh+Iv/cM/wDShqPFv/JIfh1/3E//AEoWjwl/ySH4i/8AcM/9KGo8W/8AJIfh1/3E/wD0oWgDv/8Am0P/AD/z/wBH/N3n+f8Anwo/5tD/AM/8/wDR/wA3ef5/58KAOA8Jf8kh+Iv/AHDP/Shq7/8A5u8/z/z4VwHhL/kkPxF/7hn/AKUNXf8A/N3n+f8AnwoAPh//AM0d/wC41/7NR8QP+axf9wX/ANlo+H//ADR3/uNf+zUfED/msX/cF/8AZaAOA8W/8kh+HX/cT/8ASha7/wCIH/NYv+4L/wCy1wHi3/kkPw6/7if/AKULXf8AxA/5rF/3Bf8A2WgA+H//ADR3/uNf+zUfED/msX/cF/8AZaPh/wD80d/7jX/s1HxA/wCaxf8AcF/9loAPh/8A80d/7jX/ALNR+zL/AMzT/wBun/taj4f/APNHf+41/wCzUfsy/wDM0/8Abp/7WoAPh/8A80d/7jX/ALNXAeLf+SQ/Dr/uJ/8ApQtd/wDD/wD5o7/3Gv8A2auA8W/8kh+HX/cT/wDShaAPf/Fv/JXvh1/3E/8A0nWvAPCX/JIfiL/3DP8A0oavf/Fv/JXvh1/3E/8A0nWvAPCX/JIfiL/3DP8A0oagDv8A4gf81i/7gv8A7LR+01/zK3/b3/7Ro+IH/NYv+4L/AOy0ftNf8yt/29/+0aAD4gf81i/7gv8A7LR8P/8Amjv/AHGv/ZqPiB/zWL/uC/8AstHw/wD+aO/9xr/2agA/Zl/5mn/t0/8Aa1cB4S/5JD8Rf+4Z/wClDV3/AOzL/wAzT/26f+1q4Dwl/wAkh+Iv/cM/9KGoA7/4gf8ANYv+4L/7LR8P/wDmjv8A3Gv/AGaj4gf81i/7gv8A7LR8P/8Amjv/AHGv/ZqAD4gf81i/7gv/ALLR8P8A/mjv/ca/9mo+IH/NYv8AuC/+y0fD/wD5o7/3Gv8A2agDgPFv/JIfh1/3E/8A0oWu/wD2mv8AmVv+3v8A9o1wHi3/AJJD8Ov+4n/6ULXf/tNf8yt/29/+0aAD4gf81i/7gv8A7LR8QP8AmsX/AHBf/ZaPiB/zWL/uC/8AstHxA/5rF/3Bf/ZaAD/m0P8Az/z/ANHxA/5rF/3Bf/ZaP+bQ/wDP/P8A0fED/msX/cF/9loAPh//AM0d/wC41/7NXAeLf+SQ/Dr/ALif/pQtd/8AD/8A5o7/ANxr/wBmrgPFv/JIfh1/3E//AEoWgDv/ANpr/mVv+3v/ANo0fED/AJrF/wBwX/2Wj9pr/mVv+3v/ANo0fED/AJrF/wBwX/2WgD0Dxb/yV74df9xP/wBJ1rwDxb/ySH4df9xP/wBKFr3/AMW/8le+HX/cT/8ASda8A8W/8kh+HX/cT/8AShaAO/8A+bvP8/8APhR8P/8Amjv/AHGv/ZqP+bvP8/8APhR8P/8Amjv/AHGv/ZqAD/m7z/P/AD4VwHhL/kkPxF/7hn/pQ1d//wA3ef5/58K4Dwl/ySH4i/8AcM/9KGoA7/4gf81i/wC4L/7LR+01/wAyt/29/wDtGj4gf81i/wC4L/7LR+01/wAyt/29/wDtGgA/5u8/z/z4UfD/AP5o7/3Gv/ZqP+bvP8/8+FHw/wD+aO/9xr/2agA/Zl/5mn/t0/8Aa1Hw/wD+aO/9xr/2aj9mX/maf+3T/wBrUfD/AP5o7/3Gv/ZqAOA8Jf8AJIfiL/3DP/Shq9/8W/8AJXvh1/3E/wD0nWvAPCX/ACSH4i/9wz/0oavf/Fv/ACV74df9xP8A9J1oA8A8Jf8AJIfiL/3DP/ShqPFv/JIfh1/3E/8A0oWjwl/ySH4i/wDcM/8AShqPFv8AySH4df8AcT/9KFoA7/8A5tD/AM/8/wDR/wA3ef5/58KKKAOA8Jf8kh+Iv/cM/wDShq7/AP5u8/z/AM+FFFAB8P8A/mjv/ca/9mo+IH/NYv8AuC/+y0UUAcB4t/5JD8Ov+4n/AOlC13/xA/5rF/3Bf/ZaKKAD4f8A/NHf+41/7NR8QP8AmsX/AHBf/ZaKKAD4f/8ANHf+41/7NR+zL/zNP/bp/wC1qKKAD4f/APNHf+41/wCzVwHi3/kkPw6/7if/AKULRRQB7/4t/wCSvfDr/uJ/+k614B4S/wCSQ/EX/uGf+lDUUUAd/wDED/msX/cF/wDZaP2mv+ZW/wC3v/2jRRQAfED/AJrF/wBwX/2Wj4f/APNHf+41/wCzUUUAH7Mv/M0/9un/ALWrgPCX/JIfiL/3DP8A0oaiigDv/iB/zWL/ALgv/stHw/8A+aO/9xr/ANmoooAPiB/zWL/uC/8AstHw/wD+aO/9xr/2aiigDgPFv/JIfh1/3E//AEoWu/8A2mv+ZW/7e/8A2jRRQAfED/msX/cF/wDZaPiB/wA1i/7gv/stFFAB/wA2h/5/5/6PiB/zWL/uC/8AstFFAB8P/wDmjv8A3Gv/AGauA8W/8kh+HX/cT/8AShaKKAO//aa/5lb/ALe//aNHxA/5rF/3Bf8A2WiigD0Dxb/yV74df9xP/wBJ1rwDxb/ySH4df9xP/wBKFoooA7//AJu8/wA/8+FHw/8A+aO/9xr/ANmoooAP+bvP8/8APhXAeEv+SQ/EX/uGf+lDUUUAd/8AED/msX/cF/8AZaP2mv8AmVv+3v8A9o0UUAH/ADd5/n/nwo+H/wDzR3/uNf8As1FFAB+zL/zNP/bp/wC1qPh//wA0d/7jX/s1FFAHAeEv+SQ/EX/uGf8ApQ1e/wDi3/kr3w6/7if/AKTrRRQB4B4S/wCSQ/EX/uGf+lDUeLf+SQ/Dr/uJ/wDpQtFFAH//2QplbmRzdHJlYW0KZW5kb2JqCjkgMCBvYmoKPDwvTGVuZ3RoIDEwMzAvRmlsdGVyL0ZsYXRlRGVjb2RlPj5zdHJlYW0KeJy9WFtzozYUfudXnEfvTIx1Q8DO9IHYJHW6wV5MknaaTofBxGHryy4m3e2/7xFgry81pJHbOJZkfKTvXKRzPpkAhS4FAsy2sE0WxhfjMjK4BMZdiKaGHxkfDQY36qmSI7CRjhZG74oCZRA9GZ130Scli5/xlc9w8LWcRso54bXx62/YTw2FsjAEFdjPsZemLXEoqAvMZKIcWJAY5QO7klEjpuRqcYWuVlB9giuqfm6U0yszanFSrpCgDup7UgGUjXqivpls1GrVW4JUehPVz+t+t03KZ0xa9bdqdNgnxkai6nfbxKhWVu3mtaffxvVlkHaCYQOzhCnkNh5ExaNSH+3pXOWrxXsVHQKzKkJ7K9XrK5NPY/A2kMifRMPgGvqj27EX/KIJh2jMbkDrr5ZFnBS6VlmkBefKGwzh9u7SC72f9E2ivAFqHOdJOofhQNsovofEjpC8ke8K6Uh20yWEaaJRm7XsjHHvDsbPq2Wqaxh1eEu43g7zFn2YyiWN+jx2iP34DjjFVEWF6+oeQiJafD2IC203c94WUSp6lPUYYVwTinHecipC/wo3Kb2oe13TaFtiGcfJH/FM34eW2wLEYPUEuoeP2bit2P921AW+eZNRkzT/M0ve5r3tKtR2gVpoC5PQZQzy1HjazzhuqYZ0tlZbSo1tAe+EI2+gfdQkgtAGWx/SbPasXYG4IC04gppEu/RQ1gQRrXTNwFC1QPwzPdidT1zTLefvJBob7u8+9L0AwgEU6brQVZNScBzT5tudIw94hRcESs1774N/BiwpG7AePO2wWsxEYla73Dnw+HO2Bvz/9LIuIF5CtlwX+UtSZKuldnIjzZZJalm6uQYTKP+vKx11RDPI2QodVgPakKaDeJH+fvx3Bh82wk6y2TIuXvIjbO0yy3b9egysgndeuEY7o2zXva9E+4pCx5dATKXStMp7oKiG8+9XtGY1cbNRYrLtqbEOmU7fH977AxgGcD0aDTBVBoNhNBwFJkzuLm/8fgTRCPpeGA79ECI/vJ2AF+zITcxXmUY2F351Ke2qZl9P4dgmGtfFCstP5JZxni2LdAqXf4E3n2c48r99ztP1GsarvIjnO3oQhbVBq8FeX4FF843pPFxNOC1A/4qr1SQEqRkjNu5N9LFVk5gv5Uc1iTsmlSV9k8zEjZEsoJctZhQGK/h4yPAqEdStmh1Nje52dKzM4YWpkV6P8mmaQ5g+6TrRBslP16LJ5zTJYrzcfq9B+oAunr5TgMMiXQB9bxGTfKMMGzX6Ad9cPnYoXsmUwCEJsQF3PjugIOz0IroEwbGay+jYD7XLTmN585Jk9bLU5rCiBSb0gx997+cz/AIlmijmEVmEC9jlcxfw4MGrqcnfyUVXLAplbmRzdHJlYW0KZW5kb2JqCjcgMCBvYmoKPDwvR3JvdXA8PC9UeXBlL0dyb3VwL0NTL0RldmljZVJHQi9TL1RyYW5zcGFyZW5jeT4+L1BhcmVudCA2IDAgUi9Db250ZW50cyA5IDAgUi9UeXBlL1BhZ2UvUmVzb3VyY2VzPDwvWE9iamVjdDw8L2ltZzEgOCAwIFI+Pi9Qcm9jU2V0IFsvUERGIC9UZXh0IC9JbWFnZUIgL0ltYWdlQyAvSW1hZ2VJXS9Db2xvclNwYWNlPDwvQ1MvRGV2aWNlUkdCPj4vRm9udDw8L0YxIDIgMCBSL0YyIDMgMCBSPj4+Pi9NZWRpYUJveFswIDAgMjc1IDQxOV0vUm90YXRlIDkwPj4KZW5kb2JqCjEwIDAgb2JqClsxIDAgUi9YWVogMCAyODcgMF0KZW5kb2JqCjExIDAgb2JqCls3IDAgUi9YWVogMCAyODcgMF0KZW5kb2JqCjIgMCBvYmoKPDwvQmFzZUZvbnQvSGVsdmV0aWNhL1R5cGUvRm9udC9FbmNvZGluZy9XaW5BbnNpRW5jb2RpbmcvU3VidHlwZS9UeXBlMT4+CmVuZG9iagozIDAgb2JqCjw8L0Jhc2VGb250L0hlbHZldGljYS1Cb2xkL1R5cGUvRm9udC9FbmNvZGluZy9XaW5BbnNpRW5jb2RpbmcvU3VidHlwZS9UeXBlMT4+CmVuZG9iago2IDAgb2JqCjw8L0lUWFQoMi4xLjcpL1R5cGUvUGFnZXMvQ291bnQgMi9LaWRzWzEgMCBSIDcgMCBSXT4+CmVuZG9iagoxMiAwIG9iago8PC9OYW1lc1soSlJfUEFHRV9BTkNIT1JfMF8xKSAxMCAwIFIoSlJfUEFHRV9BTkNIT1JfMF8yKSAxMSAwIFJdPj4KZW5kb2JqCjEzIDAgb2JqCjw8L0Rlc3RzIDEyIDAgUj4+CmVuZG9iagoxNCAwIG9iago8PC9OYW1lcyAxMyAwIFIvVHlwZS9DYXRhbG9nL1ZpZXdlclByZWZlcmVuY2VzPDwvUHJpbnRTY2FsaW5nL0FwcERlZmF1bHQ+Pi9QYWdlcyA2IDAgUj4+CmVuZG9iagoxNSAwIG9iago8PC9DcmVhdG9yKEphc3BlclJlcG9ydHMgXChwZWVsT2ZmTGFiZWxcKSkvUHJvZHVjZXIoaVRleHQgMi4xLjcgYnkgMVQzWFQpL01vZERhdGUoRDoyMDIzMTIxNDAwNDgwNSsxMScwMCcpL0NyZWF0aW9uRGF0ZShEOjIwMjMxMjE0MDA0ODA1KzExJzAwJyk+PgplbmRvYmoKeHJlZgowIDE2CjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwNjY2MSAwMDAwMCBuIAowMDAwMDEzODczIDAwMDAwIG4gCjAwMDAwMTM5NjEgMDAwMDAgbiAKMDAwMDAwMDAxNSAwMDAwMCBuIAowMDAwMDA1NTYzIDAwMDAwIG4gCjAwMDAwMTQwNTQgMDAwMDAgbiAKMDAwMDAxMzUyNSAwMDAwMCBuIAowMDAwMDA2OTM3IDAwMDAwIG4gCjAwMDAwMTI0MjcgMDAwMDAgbiAKMDAwMDAxMzgwMSAwMDAwMCBuIAowMDAwMDEzODM3IDAwMDAwIG4gCjAwMDAwMTQxMjMgMDAwMDAgbiAKMDAwMDAxNDIwNiAwMDAwMCBuIAowMDAwMDE0MjQwIDAwMDAwIG4gCjAwMDAwMTQzNDUgMDAwMDAgbiAKdHJhaWxlcgo8PC9Sb290IDE0IDAgUi9JRCBbPDQ0YmZlMGFkZTViMWQ1MjgyYzNiY2Y2NTQzM2I3M2MzPjwwYWRjYzhhMjY5YzEwMWVmMDlhNzc3OGYxN2RiMjIwMT5dL0luZm8gMTUgMCBSL1NpemUgMTY+PgpzdGFydHhyZWYKMTQ1MDgKJSVFT0YK"
        }
    }
}
"""

ShipmentCancelResponse = """{
    "soapenv:Envelope": {
        "@xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
        "@xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
        "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "soapenv:Body": {
            "ns1:cancelDispatchJobResponse": {
                "@xmlns:ns1": "http://neptune.alliedexpress.com.au/ttws-ejb",
                "result": "0"
            }
        }
    }
}
"""

ErrorResponse = """"account" is a required property

Failed validating "required" in schema: {
    "$id": "https: //example.com/object1627830556.json",
    "$schema": "http: //json-schema.org/draft-07/schema#",
    "additionalProperties": False,
    "definitions": {},
    "properties": {
        "account": {
            "$id": "#root/account",
            "description": "Please add account in ""request",
            "minLength": 1,
            "type": "string"
        },
        "bookedBy": {
            "$id": "#root/bookedBy",
            "description": "Please add bookedBy in ""request",
            "minLength": 1,
            "type": "string"
        },
        "instructions": {
            "$id": "#root/instructions",
            "description": "Please add ""instructions in ""request",
            "type": "string"
        },
        "itemCount": {
            "$id": "#root/itemCount",
            "description": "Please add itemCount in ""request",
            "minimum": 1,
            "type": "number"
        },
        "items": {
            "$id": "#root/items",
            "default": [],
            "items": {
                "$id": "#root/items/items",
                "additionalProperties": False,
                "properties": {
                    "dangerous": {
                        "$id": "#root/items/items/dangerous",
                        "description": "Please ""add ""dangerous ""in ""request",
                        "type": "boolean"
                    },
                    "height": {
                        "$id": "#root/items/items/height",
                        "description": "Please ""add ""height ""in ""request",
                        "minimum": 0.0001,
                        "type": "number"
                    },
                    "itemCount": {
                        "$id": "#root/items/items/itemCount",
                        "description": "Please ""add ""itemCount ""in ""request",
                        "minimum": 1,
                        "type": "number"
                    },
                    "length": {
                        "$id": "#root/items/items/height",
                        "description": "Please ""add ""length ""in ""request",
                        "minimum": 0.0001,
                        "type": "number"
                    },
                    "volume": {
                        "$id": "#root/items/items/volume",
                        "description": "Please ""add ""volume ""in ""request",
                        "minimum": 0.0001,
                        "type": "number"
                    },
                    "weight": {
                        "$id": "#root/items/items/weight",
                        "description": "Please ""add ""weight ""in ""request",
                        "minimum": 0.0001,
                        "type": "number"
                    },
                    "width": {
                        "$id": "#root/items/items/width",
                        "description": "Please ""add ""width ""in ""request",
                        "minimum": 0.0001,
                        "type": "number"
                    }
                },
                "required": [
                    "itemCount",
                    "volume",
                    "weight"
                ],
                "title": "Items",
                "type": "object"
            },
            "title": "items",
            "type": "array"
        },
        "jobStops_D": {
            "$id": "#root/jobStops_D",
            "additionalProperties": False,
            "properties": {
                "companyName": {
                    "$id": "#root/jobStops_D/companyName",
                    "description": "Please ""add ""companyName ""in ""request",
                    "minLength": 2,
                    "type": "string"
                },
                "contact": {
                    "$id": "#root/jobStops_D/contact",
                    "description": "Please ""add ""contact ""in ""request",
                    "minLength": 2,
                    "type": "string"
                },
                "emailAddress": {
                    "$id": "#root/jobStops_D/emailAddress",
                    "description": "Please ""add ""emailAddress ""in ""request",
                    "minLength": 2,
                    "type": "string"
                },
                "geographicAddress": {
                    "$id": "#root/jobStops_D/geographicAddress",
                    "additionalProperties": False,
                    "properties": {
                        "address1": {
                            "$id": "#root/jobStops_D/geographicAddress/address1",
                            "description": "Please ""add ""address1 ""in ""request",
                            "minLength": 2,
                            "type": "string"
                        },
                        "address2": {
                            "$id": "#root/jobStops_D/geographicAddress/address2",
                            "description": "Please ""add ""address2 ""in ""request",
                            "type": "string"
                        },
                        "country": {
                            "$id": "#root/jobStops_D/geographicAddress/country",
                            "description": "Please ""add ""country ""in ""request",
                            "minLength": 2,
                            "type": "string"
                        },
                        "postCode": {
                            "$id": "#root/jobStops_D/geographicAddress/postCode",
                            "description": "Please ""add ""postCode ""in ""request",
                            "minLength": 2,
                            "type": "string"
                        },
                        "state": {
                            "$id": "#root/jobStops_D/geographicAddress/state",
                            "description": "Please ""add ""state ""in ""request",
                            "minLength": 2,
                            "type": "string"
                        },
                        "suburb": {
                            "$id": "#root/jobStops_D/geographicAddress/suburb",
                            "description": "Please ""add ""suburb ""in ""request",
                            "minLength": 2,
                            "type": "string"
                        }
                    },
                    "required": [
                        "address1",
                        "country",
                        "postCode",
                        "state",
                        "suburb"
                    ],
                    "title": "geographicAddress",
                    "type": "object"
                },
                "phoneNumber": {
                    "$id": "#root/jobStops_D/phoneNumber",
                    "description": "Please ""phoneNumber ""by ""in ""request",
                    "minLength": 2,
                    "type": "string"
                }
            },
            "required": [
                "contact",
                "geographicAddress"
            ],
            "title": "jobStops_D",
            "type": "object"
        },
        "jobStops_P": {
            "$id": "#root/jobStops_P",
            "additionalProperties": False,
            "properties": {
                "companyName": {
                    "$id": "#root/jobStops_P/companyName",
                    "description": "Please ""add ""companyName ""in ""request",
                    "minLength": 2,
                    "type": "string"
                },
                "contact": {
                    "$id": "#root/jobStops_P/contact",
                    "description": "Please ""add ""contact ""in ""request",
                    "minLength": 2,
                    "type": "string"
                },
                "emailAddress": {
                    "$id": "#root/jobStops_P/emailAddress",
                    "description": "Please ""add ""emailAddress ""in ""request",
                    "minLength": 2,
                    "type": "string"
                },
                "geographicAddress": {
                    "$id": "#root/jobStops_P/geographicAddress",
                    "additionalProperties": False,
                    "properties": {
                        "address1": {
                            "$id": "#root/jobStops_P/geographicAddress/address1",
                            "description": "Please ""add ""address1 ""in ""request",
                            "minLength": 2,
                            "type": "string"
                        },
                        "address2": {
                            "$id": "#root/jobStops_P/geographicAddress/address2",
                            "description": "Please ""add ""address2 ""in ""request",
                            "type": "string"
                        },
                        "country": {
                            "$id": "#root/jobStops_P/geographicAddress/country",
                            "description": "Please ""add ""country ""in ""request",
                            "minLength": 2,
                            "type": "string"
                        },
                        "postCode": {
                            "$id": "#root/jobStops_P/geographicAddress/postCode",
                            "description": "Please ""add ""postCode ""in ""request",
                            "minLength": 2,
                            "type": "string"
                        },
                        "state": {
                            "$id": "#root/jobStops_P/geographicAddress/state",
                            "description": "Please ""add ""state ""in ""request",
                            "minLength": 2,
                            "type": "string"
                        },
                        "suburb": {
                            "$id": "#root/jobStops_P/geographicAddress/suburb",
                            "description": "Please ""add ""suburb ""in ""request",
                            "minLength": 2,
                            "type": "string"
                        }
                    },
                    "required": [
                        "address1",
                        "country",
                        "postCode",
                        "state",
                        "suburb"
                    ],
                    "title": "geographicAddress",
                    "type": "object"
                },
                "phoneNumber": {
                    "$id": "#root/jobStops_P/phoneNumber",
                    "description": "Please ""phoneNumber ""by ""in ""request",
                    "minLength": 2,
                    "type": "string"
                }
            },
            "required": [
                "contact",
                "geographicAddress",
                "phoneNumber",
                "companyName",
                "emailAddress"
            ],
            "title": "jobStops_P",
            "type": "object"
        },
        "referenceNumbers": {
            "$id": "#root/referenceNumbers",
            "default": [],
            "title": "referenceNumbers",
            "type": "array"
        },
        "serviceLevel": {
            "$id": "#root/serviceLevel",
            "description": "Please add ""serviceLevel in ""request",
            "minLength": 1,
            "type": "string"
        },
        "volume": {
            "$id": "#root/volume",
            "description": "Please add volume in ""request",
            "minimum": 0.0001,
            "type": "number"
        },
        "weight": {
            "$id": "#root/weight",
            "description": "Please add weight in ""request",
            "minimum": 0.0001,
            "type": "number"
        }
    },
    "required": [
        "bookedBy",
        "itemCount",
        "account",
        "serviceLevel",
        "volume",
        "weight",
        "items",
        "jobStops_D"
    ],
    "title": "Root",
    "type": "object"
}

On instance: {
    "bookedBy": "TEST USER",
    "instructions": "This is just an instruction",
    "itemCount": 2,
    "items": [
        {
            "dangerous": False,
            "height": 50,
            "itemCount": 1,
            "length": 50,
            "volume": 0.036,
            "weight": 20,
            "width": 12
        },
        {
            "dangerous": True,
            "height": 50,
            "itemCount": 1,
            "length": 50,
            "volume": 0.036,
            "weight": 20,
            "width": 12
        }
    ],
    "jobStops_D": {
        "companyName": "TESTING COMPANY",
        "contact": "TEST USER",
        "emailAddress": "test@gmail.com",
        "geographicAddress": {
            "address1": "17 VULCAN RD",
            "address2": "test",
            "country": "AU",
            "postCode": "6155",
            "state": "WA",
            "suburb": "CANNING VALE"
        },
        "phoneNumber": "(07) 3114 1499"
    },
    "jobStops_P": {
        "companyName": "TESTING COMPANY",
        "contact": "TEST USER",
        "emailAddress": "test@gmail.com",
        "geographicAddress": {
            "address1": "17 VULCAN RD",
            "address2": "test",
            "country": "AU",
            "postCode": "6155",
            "state": "WA",
            "suburb": "CANNING VALE"
        },
        "phoneNumber": "(07) 3114 1499"
    },
    "referenceNumbers": [
        "REF-001",
        "REF-001"
    ],
    "serviceLevel": "R",
    "volume": 0.072,
    "weight": 41
}
"""
