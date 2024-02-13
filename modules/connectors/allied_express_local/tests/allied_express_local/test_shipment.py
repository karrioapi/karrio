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
        with patch("karrio.mappers.allied_express_local.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/GetLabelfull",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.allied_express_local.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/cancelJob/123456789/12345",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.allied_express_local.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.allied_express_local.proxy.lib.request") as mock:
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
        with patch("karrio.mappers.allied_express_local.proxy.lib.request") as mock:
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
    "service": "allied_local_vip_service",
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
        "carrier_id": "allied_express_local",
        "carrier_name": "allied_express_local",
        "docs": {"label": ANY},
        "label_type": "PDF",
        "meta": {"postal_code": "6155"},
        "shipment_identifier": "AET1021116",
        "tracking_number": "AET1021116",
    },
    [],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "allied_express_local",
        "carrier_name": "allied_express_local",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "allied_express_local",
            "carrier_name": "allied_express_local",
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
    "readyDate": ANY,
    "instructions": "This is just an instruction",
    "itemCount": 2,
    "items": [
        {
            "dangerous": False,
            "height": 50.0,
            "itemCount": 1,
            "length": 50.0,
            "volume": 0.03,
            "weight": 20.0,
            "width": 12.0,
        },
        {
            "dangerous": True,
            "height": 50.0,
            "itemCount": 1,
            "length": 50.0,
            "volume": 0.03,
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
    "serviceLevel": "V",
    "volume": 0.06,
    "weight": 40.0,
}

ShipmentCancelRequest = {"shipmentno": "123456789", "postalcode": "12345"}

ShipmentResponse = """{
    "Tracking": "AET1021116",
    "price_detail": {
        "price": {
            "chargeQuantity": "0",
            "cubicFactor": "0",
            "discountClass": {
                "@xsi:nil": "1"
            },
            "discountRate": "0.0",
            "grossPrice": "0.0",
            "jobCode": {
                "@xsi:nil": "1"
            },
            "netPrice": "0.0",
            "rateCode": {
                "@xsi:nil": "1"
            },
            "reason": "No Hire time found"
        }
    },
    "soapenv:Body": {
        "ns1:getLabelResponse": {
            "@xmlns:ns1": "http://neptune.alliedexpress.com.au/ttws-ejb",
            "result": "CnN0YXJ0eHJlZgoxNDUwMQolJUVPRgo="
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
