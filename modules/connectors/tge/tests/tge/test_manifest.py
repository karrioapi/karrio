import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestTGEManifest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ManifestRequest = models.ManifestRequest(**ManifestPayload)

    def test_create_manifest_request(self):
        request = gateway.mapper.create_manifest_request(self.ManifestRequest)

        self.assertEqual(request.serialize()[0], ManifestRequest)

    def test_create_manifest(self):
        with patch("karrio.mappers.tge.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Manifest.create(self.ManifestRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/printmanifest",
            )

    def test_parse_manifest_response(self):
        with patch("karrio.mappers.tge.proxy.lib.request") as mock:
            mock.return_value = ManifestResponse
            parsed_response = (
                karrio.Manifest.create(self.ManifestRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedManifestResponse)


if __name__ == "__main__":
    unittest.main()


ManifestPayload = {
    "shipment_identifiers": ["8880419999995"],
    "address": {
        "company_name": "TEST USER",
        "address_line1": "17 VULCAN RD",
        "address_line2": "Testing",
        "city": "CANNING VALE",
        "postal_code": "6155",
        "country_code": "AU",
        "state_code": "WA",
    },
    "options": {
        "shipments": [
            {
                "shipment_identifier": "8880419999995",
                "tracking_number": "8880419999995",
                "shipper": {
                    "company_name": "TEST USER",
                    "address_line1": "17 VULCAN RD",
                    "address_line2": "Testing",
                    "city": "CANNING VALE",
                    "postal_code": "6155",
                    "country_code": "AU",
                    "state_code": "WA",
                },
                "recipient": {
                    "address_line1": "17 VULCAN RD",
                    "city": "CANNING VALE",
                    "postal_code": "6155",
                    "country_code": "AU",
                    "person_name": "TEST USER",
                    "state_code": "WA",
                },
                "parcels": [
                    {
                        "height": 10.0,
                        "length": 20.0,
                        "weight": 100.0,
                        "width": 30.0,
                        "dimension_unit": "CM",
                        "weight_unit": "KG",
                        "description": "Item- Carton",
                    },
                ],
                "service": "tge_freight_service",
                "options": {
                    "shipment_date": "2024-02-08",
                    "instructions": "Shipment With DG",
                    "tge_despatch_date": "2024-02-08T09:44:11.518Z",
                    "tge_required_delivery_date": "2024-02-11T09:44:11.518Z",
                },
                "reference": "testing 123",
                "meta": {
                    "SSCCs": ["00099475103613941860"],
                    "ShipmentID": "8880419999995",
                    "shipment_count": 9999995,
                    "sscc_count": 361394186,
                },
            }
        ]
    },
}

ParsedManifestResponse = [
    {
        "carrier_id": "tge",
        "carrier_name": "tge",
        "doc": {"manifest": ANY},
        "meta": {},
    },
    [],
]


ManifestRequest = {
    "TollMessage": {
        "Header": {
            "CreateTimestamp": ANY,
            "DocumentType": "Manifest",
            "Environment": "PRD",
            "MessageIdentifier": ANY,
            "MessageSender": "GOSHIPR",
            "MessageVersion": "2.5",
            "SourceSystemCode": "YF73",
        },
        "Print": {
            "BusinessID": "IPEC",
            "ConsignorParty": {
                "Contact": {"Name": "TEST USER"},
                "PartyName": "TEST USER",
                "PhysicalAddress": {
                    "AddressLine1": "17 VULCAN RD",
                    "AddressLine2": "Testing",
                    "AddressType": "Business",
                    "CountryCode": "AU",
                    "PostalCode": "6155",
                    "StateCode": "WA",
                    "Suburb": "CANNING VALE",
                },
            },
            "CreateDateTime": ANY,
            "DatePeriodCollection": {
                "DatePeriod": [
                    {
                        "DateTime": "2024-02-08T09:44:11.518Z",
                        "DateType": "DespatchDate",
                    },
                    {
                        "DateTime": "2024-02-11T09:44:11.518Z",
                        "DateType": "RequiredDeliveryDate",
                    },
                ]
            },
            "ManifestID": {"Value": "8880419999995"},
            "PrintDocumentType": "Manifest",
            "PrintSettings": {
                "IsLabelThermal": "false",
                "IsZPLRawResponseRequired": "false",
                "PDF": {"IsPDFA4": "true", "PDFSettings": {"StartQuadrant": "1"}},
            },
            "ShipmentCollection": {
                "Shipment": [
                    {
                        "BillToParty": {"AccountCode": "80502494", "Payer": "S"},
                        "ConsigneeParty": {
                            "Contact": {"Name": "TEST USER"},
                            "PartyName": "TEST USER",
                            "PhysicalAddress": {
                                "AddressLine1": "17 VULCAN RD",
                                "AddressType": "Business",
                                "CountryCode": "AU",
                                "PostalCode": "6155",
                                "StateCode": "WA",
                                "Suburb": "CANNING VALE",
                            },
                        },
                        "CreateDateTime": ANY,
                        "DatePeriodCollection": {
                            "DatePeriod": [
                                {
                                    "DateTime": "2024-02-08T09:44:11.518Z",
                                    "DateType": "DespatchDate",
                                },
                                {
                                    "DateTime": "2024-02-11T09:44:11.518Z",
                                    "DateType": "RequiredDeliveryDate",
                                },
                            ]
                        },
                        "FreightMode": "Road",
                        "References": {
                            "Reference": [
                                {
                                    "ReferenceType": "ShipmentReference1",
                                    "ReferenceValue": "testing 123",
                                }
                            ]
                        },
                        "ShipmentID": "8880419999995",
                        "ShipmentItemCollection": {
                            "ShipmentItem": [
                                {
                                    "Commodity": {
                                        "CommodityCode": "BG",
                                        "CommodityDescription": "BAG",
                                    },
                                    "Description": "Item- Carton",
                                    "Dimensions": {
                                        "Height": 10.0,
                                        "HeightUOM": "m3",
                                        "Length": 20.0,
                                        "LengthUOM": "m3",
                                        "Volume": 6000.0,
                                        "VolumeUOM": "m3",
                                        "Weight": 100.0,
                                        "WeightUOM": "kg",
                                        "Width": 30.0,
                                        "WidthUOM": "m3",
                                    },
                                    "IDs": {
                                        "ID": [
                                            {
                                                "SchemeName": "SSCC",
                                                "Value": "00099475103613941860",
                                            }
                                        ]
                                    },
                                    "ShipmentItemTotals": {"ShipmentItemCount": 1},
                                    "ShipmentService": {"ServiceCode": "X"},
                                }
                            ]
                        },
                        "SpecialInstruction": "Shipment With DG",
                    }
                ]
            },
        },
    }
}

ManifestResponse = """{
    "TollMessage": {
        "Header": {
            "ApplicationID": null,
            "AsynchronousMessageFlag": null,
            "CreateTimestamp": "2024-03-16 14:00:18.0",
            "DocumentType": "ResponseMessage",
            "Environment": "PRD",
            "MessageIdentifier": "d734c5d2-28ce-11e1-b467-0ed5f894f718b",
            "MessageReceiver": null,
            "MessageSender": "GOSHIPR",
            "MessageVersion": "2.5",
            "References": null,
            "SourceSystemCode": "YF73"
        },
        "ResponseMessages": {
            "ResponseMessage": [
                {
                    "ResponseID": {
                        "Value": "200"
                    },
                    "ResponseMessage": "JVBERi0xLjQKJfbk/N8KMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovVmVyc2lvbiAvMS41Ci9QYWdlcyAyIDAgUgovTmFtZXMgMyAwIFIKPj4KZW5kb2JqCjQgMCBvYmoKPDwKL01vZERhdGUgKEQ6MjAyNDAzMTYxNDAwMThaKQovQ3JlYXRvciAoQklSVCBSZXBvcnQgRW5naW5lIG5lc3RlZDovYXBwLmphci8hQk9PVC1JTkYvbGliL29yZy5lY2xpcHNlLmJpcnQucnVudGltZV80LjguMC0yMDE4MDYyNi00LjguMC5qYXIhLy4pCi9DcmVhdGlvbkRhdGUgKEQ6MjAyNDAzMTYxNDAwMThaKQovUHJvZHVjZXIgKGlUZXh0IDIuMS43IGJ5IDFUM1hUKQo+PgplbmRvYmoKMiAwIG9iago8PAovVHlwZSAvUGFnZXMKL0tpZHMgWzUgMCBSIDYgMCBSXQovQ291bnQgMgo+PgplbmRvYmoKMyAwIG9iago8PAovRGVzdHMgNyAwIFIKPj4KZW5kb2JqCjUgMCBvYmoKPDwKL0dyb3VwIDggMCBSCi9Db250ZW50cyA5IDAgUgovVHlwZSAvUGFnZQovUmVzb3VyY2VzIDEwIDAgUgovUGFyZW50IDIgMCBSCi9NZWRpYUJveCBbMC4wIDAuMCA4NDEuODkgNTk1LjI4XQovQ3JvcEJveCBbMC4wIDAuMCA4NDEuODkgNTk1LjI4XQovUm90YXRlIDAKPj4KZW5kb2JqCjYgMCBvYmoKPDwKL0dyb3VwIDExIDAgUgovQ29udGVudHMgMTIgMCBSCi9UeXBlIC9QYWdlCi9SZXNvdXJjZXMgMTMgMCBSCi9QYXJlbnQgMiAwIFIKL01lZGlhQm94IFswLjAgMC4wIDg0MS44OSA1OTUuMjhdCi9Dcm9wQm94IFswLjAgMC4wIDg0MS44OSA1OTUuMjhdCi9Sb3RhdGUgMAo+PgplbmRvYmoKNyAwIG9iago8PAovTmFtZXMgWyhfX2Jvb2ttYXJrXzEpIFs1IDAgUiAvWFlaIG51bGwgNTgyLjggMF0KIChfX2Jvb2ttYXJrXzIpIFs1IDAgUiAvWFlaIG51bGwgNTI5LjE2IDBdCiAoX19ib29rbWFya18zKSBbNSAwIFIgL1hZWiBudWxsIDQw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OTQKL0NvbG9ycyAxCi9QcmVkaWN0b3IgMTUKL0JpdHNQZXJDb21wb25lbnQgOAo+PgplbmRvYmoKeHJlZgowIDMwCjAwMDAwMDAwMDAgNjU1MzUgZg0KMDAwMDAwMDAxNSAwMDAwMCBuDQowMDAwMDAwMzIxIDAwMDAwIG4NCjAwMDAwMDAzODQgMDAwMDAgbg0KMDAwMDAwMDA5MSAwMDAwMCBuDQowMDAwMDAwNDE4IDAwMDAwIG4NCjAwMDAwMDA1ODkgMDAwMDAgbg0KMDAwMDAwMDc2MiAwMDAwMCBuDQowMDAwMDAxMTMzIDAwMDAwIG4NCjAwMDAwMDExOTkgMDAwMDAgbg0KMDAwMDAwNDA1MCAwMDAwMCBuDQowMDAwMDA0MjA0IDAwMDAwIG4NCjAwMDAwMDQyNzEgMDAwMDAgbg0KMDAwMDAwNzEyMyAwMDAwMCBuDQowMDAwMDA3Mjc3IDAwMDAwIG4NCjAwMDAwMDczMTQgMDAwMDAgbg0KMDAwMDAwNzM1OCAwMDAwMCBuDQowMDAwMDA4MDk3IDAwMDAwIG4NCjAwMDAwMTY2NzYgMDAwMDAgbg0KMDAwMDAxNjg4OSAwMDAwMCBuDQowMDAwMDE2OTI2IDAwMDAwIG4NCjAwMDAwMTY5NzAgMDAwMDAgbg0KMDAwMDAxNzcwOSAwMDAwMCBuDQowMDAwMDI2Mjg4IDAwMDAwIG4NCjAwMDAwMjY1MDEgMDAwMDAgbg0KMDAwMDAyNjYwMSAwMDAwMCBuDQowMDAwMDI2NzAwIDAwMDAwIG4NCjAwMDAwMjY3NzkgMDAwMDAgbg0KMDAwMDAyNjg3OSAwMDAwMCBuDQowMDAwMDI2OTc4IDAwMDAwIG4NCnRyYWlsZXIKPDwKL1Jvb3QgMSAwIFIKL0luZm8gNCAwIFIKL0lEIFs8NkEwNjFFRDBGMUU5QTczOTVCMkY0QTk5RUY3NjY5RkE+IDw2QTA2MUVEMEYxRTlBNzM5NUIyRjRBOTlFRjc2NjlGQT5dCi9TaXplIDMwCj4+CnN0YXJ0eHJlZgoyNzA1NwolJUVPRgo="
                }
            ]
        }
    }
}
"""
