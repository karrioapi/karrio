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

        self.assertEqual(lib.to_dict(request.serialize()[0]), RateRequest)

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
        "city": "MELBOURNE",
        "state_code": "VIC",
        "postal_code": "3000",
        "country_code": "AU",
    },
    "recipient": {
        "city": "Ballajura",
        "state_code": "WA",
        "postal_code": "6066",
        "country_code": "AU",
    },
    "parcels": [
        {
            "height": 10,
            "length": 10,
            "width": 10,
            "weight": 2.0,
            "weight_unit": "KG",
            "dimension_unit": "CM",
        },
    ],
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "tge",
            "carrier_name": "tge",
            "currency": "AUD",
            "service": "tge_freight_service",
            "extra_charges": [
                {"amount": 14.92, "currency": "AUD", "name": "BaseAmount"},
                {"amount": 12.42, "currency": "AUD", "name": "GSTAmount"},
                {"amount": 39.15, "currency": "AUD", "name": "TotalChargeAmount"},
                {"amount": 2.59, "currency": "AUD", "name": "TotalSurcharges"},
                {"amount": 9.22, "currency": "AUD", "name": "FreightCharge"},
                {"amount": 4.0, "currency": "AUD", "name": "TransitTime"},
            ],
            "meta": {"EnquiryID": "34270397", "service_name": "tge_freight_service"},
            "total_charge": 39.15,
            "transit_days": 4,
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
            "message": "The combination of MessageSender, SourceSystemCode, Shipment "
            "Number or SSCC ID was invalid.",
        }
    ],
]


RateRequest = {
    "TollMessage": {
        "Header": {
            "CreateTimestamp": ANY,
            "DocumentType": "RateEnquiry",
            "Environment": "prd",
            "MessageIdentifier": ANY,
            "MessageReceiver": "TOLL",
            "MessageSender": "GOSHIPR",
            "MessageVersion": "1.0",
            "SourceSystemCode": "XP41",
        },
        "RateEnquiry": {
            "Request": {
                "BillToParty": {"AccountCode": "80502494"},
                "BusinessID": "IPEC",
                "ConsigneeParty": {
                    "PhysicalAddress": {
                        "CountryCode": "AU",
                        "PostalCode": "6066",
                        "StateCode": "WA",
                        "Suburb": "Ballajura",
                    }
                },
                "ConsignorParty": {
                    "PhysicalAddress": {
                        "CountryCode": "AU",
                        "PostalCode": "3000",
                        "StateCode": "VIC",
                        "Suburb": "MELBOURNE",
                    }
                },
                "FreightMode": "Road",
                "ShipmentFinancials": {
                    "ExtraServicesAmount": {"Currency": "AUD", "Value": "10"}
                },
                "ShipmentFlags": {"ExtraServiceFlag": "true"},
                "ShipmentItems": {
                    "ShipmentItem": [
                        {
                            "Commodity": {
                                "CommodityCode": "Z",
                                "CommodityDescription": "ALL FREIGHT",
                            },
                            "Dimensions": {
                                "Height": "10",
                                "Length": "10",
                                "Volume": "0.1",
                                "Weight": "2.0",
                                "Width": "10",
                            },
                            "ShipmentItemTotals": {"ShipmentItemCount": "1"},
                        }
                    ]
                },
                "ShipmentService": {"ServiceCode": "X"},
                "SystemFields": {"PickupDateTime": ANY},
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
