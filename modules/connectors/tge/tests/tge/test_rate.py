import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestAlliedExpressRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(lib.to_dict(request.serialize()), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.tge.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/calculatePrice",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.tge.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.tge.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {
    "shipper": {
        "company_name": "TESTING COMPANY",
        "address_line1": "17 VULCAN RD",
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
    "services": ["allied_road_service"],
    "options": {
        "instructions": "This is just an instruction",
    },
    "reference": "REF-001",
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "tge",
            "carrier_name": "tge",
            "currency": "AUD",
            "extra_charges": [
                {"amount": 14.18, "currency": "AUD", "name": "Job charge"}
            ],
            "meta": {"service_name": "allied_road_service"},
            "service": "allied_road_service",
            "total_charge": 40.66,
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "tge",
            "carrier_name": "tge",
            "code": "400",
            "details": {},
            "message": "Validation failed: java.lang.Exception: Exception thrown in "
            "SuburbDAO.getSuburb :java.lang.Exception: No valid JNDI name "
            "found for state UM",
        }
    ],
]


RateRequest = {
    "TollMessage": {
        "Header": {
            "MessageVersion": "1.0",
            "MessageIdentifier": "a255d5b1-e395-450f-b61f-f20baa673818",
            "CreateTimestamp": "2024-02-24T15:03:28.787+11:00",
            "DocumentType": "RateEnquiry",
            "Environment": "PRD",
            "SourceSystemCode": "XP41",
            "MessageSender": "GOSHIPR",
            "MessageReceiver": "TOLL",
        },
        "RateEnquiry": {
            "Request": {
                "BusinessID": "IPEC",
                "SystemFields": {"PickupDateTime": "2024-03-12T13:26:02.000+00:00"},
                "ShipmentService": {"ServiceCode": "X", "ShipmentProductCode": ""},
                "ShipmentFlags": {"ExtraServiceFlag": "true"},
                "ShipmentFinancials": {
                    "ExtraServicesAmount": {"Currency": "AUD", "Value": 5000.00}
                },
                "FreightMode": "Road",
                "BillToParty": {"AccountCode": "80502494"},
                "ConsignorParty": {
                    "PhysicalAddress": {
                        "Suburb": "MELBOURNE",
                        "StateCode": "VIC",
                        "PostalCode": "3000",
                        "CountryCode": "AU",
                    }
                },
                "ConsigneeParty": {
                    "PhysicalAddress": {
                        "Suburb": "Ballajura",
                        "StateCode": "WA",
                        "PostalCode": "6066",
                        "CountryCode": "AU",
                    }
                },
                "ShipmentItems": {
                    "ShipmentItem": [
                        {
                            "Commodity": {
                                "CommodityCode": "Z",
                                "CommodityDescription": "ALL FREIGHT",
                            },
                            "ShipmentItemTotals": {"ShipmentItemCount": 1},
                            "Dimensions": {
                                "Width": 10,
                                "Length": 10,
                                "Height": 10,
                                "Volume": 0.001,
                                "Weight": 2.0,
                            },
                        }
                    ]
                },
            }
        },
    }
}

RateResponse = """{
    "TollMessage": {
        "Header": {
            "MessageVersion": "1.0",
            "MessageIdentifier": "a255d5b1-e395-450f-b61f-f20baa673818",
            "CreateTimestamp": "2024-03-09T21:30:20.022+11:00",
            "DocumentType": "RateEnquiry",
            "Environment": "prd",
            "SourceSystemCode": "XP41",
            "MessageSender": "TOLL",
            "MessageReceiver": "GOSHIPR",
            "ResponseStatus": null,
            "References": {
                "Reference": [
                    {
                        "ReferenceType": "MapSpecVersion",
                        "ReferenceValue": "ToM-RateEnq-to-ToM-RateEnq.2"
                    }
                ]
            }
        },
        "RateEnquiry": {
            "Response": {
                "BaseAmount": {
                    "Currency": "AUD",
                    "Value": "14.92"
                },
                "GSTAmount": {
                    "Currency": "AUD",
                    "Value": "12.42"
                },
                "TotalChargeAmount": {
                    "Currency": "AUD",
                    "Value": "39.15"
                },
                "TotalSurcharges": {
                    "Currency": "AUD",
                    "Value": "2.59"
                },
                "FreightCharge": {
                    "Currency": "AUD",
                    "Value": "9.22"
                },
                "TollExtraServiceCharge": {
                    "Currency": "AUD",
                    "Value": "0.0"
                },
                "TotalFees": {
                    "Currency": "AUD",
                    "Value": null
                },
                "EnquiryID": "34270397",
                "TransitTime": {
                    "UOM": "Day(s)",
                    "Value": "4"
                }
            }
        }
    }
}
"""

ErrorResponse = """{
    "TollMessage": {
        "ErrorMessages": {
            "ErrorMessage": [
                {
                    "ErrorMessage": "The combination of MessageSender, SourceSystemCode, Shipment Number or SSCC ID was invalid.",
                    "ErrorNumber": {
                        "Value": "PRINT00400"
                    }
                }
            ]
        },
        "Header": {
            "ApplicationID": null,
            "AsynchronousMessageFlag": null,
            "CreateTimestamp": "2024-02-07T08:20:11.518Z",
            "DocumentType": "ErrorMessage",
            "Environment": "PRD",
            "MessageIdentifier": "d734c5d2-28ce-11e1-b467-0ed5f894f718b",
            "MessageReceiver": null,
            "MessageSender": "GOSHIPR",
            "MessageVersion": "2.5",
            "References": null,
            "SourceSystemCode": "XP41"
        }
    }
}
"""
