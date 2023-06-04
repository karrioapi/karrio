import unittest
import logging
from unittest.mock import patch, ANY
from karrio.core.utils import DP
from karrio.core.models import ShipmentRequest, ShipmentCancelRequest
from .fixture import gateway
import karrio


class TestUPSShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**package_shipment_data)
        self.ShipmentCancelRequest = ShipmentCancelRequest(
            **shipment_cancel_request_data
        )

    def test_create_package_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        self.assertEqual(request.serialize(), ShipmentRequestJSON)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(
            request.serialize(),
            {"shipmentidentificationnumber": "1ZWA82900191640782"},
        )

    def test_create_package_shipment_with_package_preset_request(self):
        request = gateway.mapper.create_shipment_request(
            ShipmentRequest(**package_shipment_with_package_preset_data)
        )
        self.assertEqual(request.serialize(), ShipmentRequestWithPresetJSON)

    @patch("karrio.mappers.ups.proxy.lib.request", return_value="{}")
    def test_create_shipment(self, http_mock):
        karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, f"{gateway.settings.server_url}/api/shipments/v2205/ship")

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponseJSON
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
            self.assertListEqual(DP.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponseJSON
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(
                DP.to_dict(parsed_response), ParsedShipmentCancelResponse
            )


if __name__ == "__main__":
    unittest.main()


shipment_cancel_request_data = {"shipment_identifier": "1ZWA82900191640782"}

package_shipment_data = {
    "shipper": {
        "company_name": "Shipper Name",
        "person_name": "Shipper Attn Name",
        "federal_tax_id": "123456",
        "phone_number": "1234567890",
        "address_line1": "Address Line",
        "city": "City",
        "state_code": "StateProvinceCode",
        "postal_code": "PostalCode",
        "country_code": "CountryCode",
    },
    "recipient": {
        "company_name": "Ship To Name",
        "person_name": "Ship To Attn Name",
        "phone_number": "1234567890",
        "address_line1": "Address Line",
        "city": "City",
        "state_code": "StateProvinceCode",
        "postal_code": "PostalCode",
        "country_code": "CountryCode",
    },
    "parcels": [
        {
            "dimension_unit": "IN",
            "weight_unit": "LB",
            "packaging_type": "ups_customer_supplied_package",
            "description": "Description",
            "length": 7,
            "width": 5,
            "height": 2,
            "weight": 10,
        }
    ],
    "service": "ups_express_ca",
    "options": {"email_notification_to": "test@mail.com"},
    "payment": {"paid_by": "sender"},
    "reference": "Your Customer Context",
}

package_shipment_with_package_preset_data = {
    "shipper": {
        "company_name": "Shipper Name",
        "person_name": "Shipper Attn Name",
        "federal_tax_id": "123456",
        "phone_number": "1234567890",
        "address_line1": "Address Line",
        "city": "City",
        "state_code": "StateProvinceCode",
        "postal_code": "PostalCode",
        "country_code": "CountryCode",
    },
    "recipient": {
        "company_name": "Ship To Name",
        "person_name": "Ship To Attn Name",
        "phone_number": "1234567890",
        "address_line1": "Address Line",
        "city": "City",
        "state_code": "StateProvinceCode",
        "postal_code": "PostalCode",
        "country_code": "CountryCode",
    },
    "parcels": [
        {
            "packaging_type": "ups_customer_supplied_package",
            "description": "Description",
            "package_preset": "ups_medium_express_box",
        }
    ],
    "service": "ups_express_ca",
    "payment": {"paid_by": "sender"},
    "options": {"email_notification_to": "test@mail.com"},
    "reference": "Your Customer Context",
    "label_type": "ZPL",
}


NegotiatedParsedShipmentResponse = [
    {
        "carrier_name": "ups",
        "carrier_id": "ups",
        "tracking_number": "1ZWA82900191640782",
        "shipment_identifier": "1ZWA82900191640782",
        "label_type": "PDF",
        "docs": {"label": ANY},
        "meta": {
            "carrier_tracking_link": "https://www.ups.com/track?loc=en_US&requester=QUIC&tracknum=1ZWA82900191640782/trackdetails"
        },
    },
    [],
]

ParsedShipmentResponse = [
    {
        "carrier_name": "ups",
        "carrier_id": "ups",
        "tracking_number": "1ZXXXXXXXXXXXXXXXX",
        "shipment_identifier": "1ZXXXXXXXXXXXXXXXX",
        "label_type": "PDF",
        "docs": {"label": ANY},
        "meta": {
            "carrier_tracking_link": "https://www.ups.com/track?loc=en_US&requester=QUIC&tracknum=1ZXXXXXXXXXXXXXXXX/trackdetails",
            "tracking_numbers": ["1ZXXXXXXXXXXXXXXXX"],
        },
    },
    [],
]

ParsedShipmentCancelResponse = [
    {
        "carrier_id": "ups",
        "carrier_name": "ups",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequestJSON = {
    "ShipmentRequest": {
        "LabelSpecification": {
            "LabelImageFormat": {"Code": "PNG", "Description": "lable format"},
            "LabelStockSize": {"Height": "6", "Width": "4"},
        },
        "Request": {
            "RequestOption": "validate",
            "SubVersion": "v2205",
            "TransactionReference": {"CustomerContext": "Your Customer Context"},
        },
        "Shipment": {
            "Description": "Description",
            "InvoiceLineTotal": {"CurrencyCode": "USD", "MonetaryValue": "1.0"},
            "NumOfPiecesInShipment": "0",
            "Package": [
                {
                    "Dimensions": {
                        "Height": "2.0",
                        "Length": "7.0",
                        "UnitOfMeasurement": {"Code": "IN", "Description": "Dimension"},
                        "Width": "5.0",
                    },
                    "PackageWeight": {
                        "UnitOfMeasurement": {"Code": "LBS", "Description": "Weight"},
                        "Weight": "10.0",
                    },
                    "Packaging": {"Code": "02", "Description": "Packaging Type"},
                }
            ],
            "PaymentInformation": {
                "ShipmentCharge": [
                    {
                        "BillShipper": {"AccountNumber": "Your Account Number"},
                        "Type": "01",
                    },
                    {
                        "BillShipper": {"AccountNumber": "Your Account Number"},
                        "Type": "02",
                    },
                ]
            },
            "RatingMethodRequestedIndicator": "Y",
            "ReferenceNumber": {
                "Code": "CountryCode",
                "Value": "Your Customer Context",
            },
            "Service": {"Code": "01", "Description": "ups_next_day_air"},
            "ShipFrom": {
                "Address": {
                    "AddressLine": "Address Line",
                    "City": "City",
                    "CountryCode": "CountryCode",
                    "PostalCode": "PostalCode",
                    "StateProvinceCode": "StateProvinceCode",
                },
                "AttentionName": "Shipper Attn Name",
                "CompanyDisplayableName": "Shipper Name",
                "Name": "Shipper Name",
                "Phone": {"Number": "1234567890"},
                "TaxIdentificationNumber": "123456",
            },
            "ShipTo": {
                "Address": {
                    "AddressLine": "Address Line",
                    "City": "City",
                    "CountryCode": "CountryCode",
                    "PostalCode": "PostalCode",
                    "StateProvinceCode": "StateProvinceCode",
                },
                "AttentionName": "Ship To Attn Name",
                "CompanyDisplayableName": "Ship To Name",
                "Name": "Ship To Name",
                "Phone": {"Number": "1234567890"},
            },
            "ShipmentRatingOptions": {"NegotiatedRatesIndicator": "Y"},
            "ShipmentServiceOptions": {
                "Notification": [
                    {
                        "EMail": {"EMailAddress": "test@mail.com"},
                        "NotificationCode": "8",
                    }
                ]
            },
            "Shipper": {
                "Address": {
                    "AddressLine": "Address Line",
                    "City": "City",
                    "CountryCode": "CountryCode",
                    "PostalCode": "PostalCode",
                    "StateProvinceCode": "StateProvinceCode",
                },
                "AttentionName": "Shipper Attn Name",
                "CompanyDisplayableName": "Shipper Name",
                "Name": "Shipper Name",
                "Phone": {"Number": "1234567890"},
                "ShipperNumber": "Your Account Number",
                "TaxIdentificationNumber": "123456",
            },
            "TaxInformationIndicator": "Y",
        },
    }
}

ShipmentRequestWithPresetJSON = {
    "ShipmentRequest": {
        "LabelSpecification": {
            "LabelImageFormat": {"Code": "ZPL", "Description": "lable format"},
            "LabelStockSize": {"Height": "6", "Width": "4"},
        },
        "Request": {
            "RequestOption": "validate",
            "SubVersion": "v2205",
            "TransactionReference": {"CustomerContext": "Your Customer Context"},
        },
        "Shipment": {
            "Description": "Description",
            "InvoiceLineTotal": {"CurrencyCode": "USD", "MonetaryValue": "1.0"},
            "NumOfPiecesInShipment": "0",
            "Package": [
                {
                    "Dimensions": {
                        "Height": "11.0",
                        "Length": "3.0",
                        "UnitOfMeasurement": {"Code": "IN", "Description": "Dimension"},
                        "Width": "16.0",
                    },
                    "PackageWeight": {
                        "UnitOfMeasurement": {"Code": "LBS", "Description": "Weight"},
                        "Weight": "30.0",
                    },
                    "Packaging": {"Code": "02", "Description": "Packaging Type"},
                }
            ],
            "PaymentInformation": {
                "ShipmentCharge": [
                    {
                        "BillShipper": {"AccountNumber": "Your Account Number"},
                        "Type": "01",
                    },
                    {
                        "BillShipper": {"AccountNumber": "Your Account Number"},
                        "Type": "02",
                    },
                ]
            },
            "RatingMethodRequestedIndicator": "Y",
            "ReferenceNumber": {
                "Code": "CountryCode",
                "Value": "Your Customer Context",
            },
            "Service": {"Code": "01", "Description": "ups_next_day_air"},
            "ShipFrom": {
                "Address": {
                    "AddressLine": "Address Line",
                    "City": "City",
                    "CountryCode": "CountryCode",
                    "PostalCode": "PostalCode",
                    "StateProvinceCode": "StateProvinceCode",
                },
                "AttentionName": "Shipper Attn Name",
                "CompanyDisplayableName": "Shipper Name",
                "Name": "Shipper Name",
                "Phone": {"Number": "1234567890"},
                "TaxIdentificationNumber": "123456",
            },
            "ShipTo": {
                "Address": {
                    "AddressLine": "Address Line",
                    "City": "City",
                    "CountryCode": "CountryCode",
                    "PostalCode": "PostalCode",
                    "StateProvinceCode": "StateProvinceCode",
                },
                "AttentionName": "Ship To Attn Name",
                "CompanyDisplayableName": "Ship To Name",
                "Name": "Ship To Name",
                "Phone": {"Number": "1234567890"},
            },
            "ShipmentRatingOptions": {"NegotiatedRatesIndicator": "Y"},
            "ShipmentServiceOptions": {
                "Notification": [
                    {
                        "EMail": {"EMailAddress": "test@mail.com"},
                        "NotificationCode": "8",
                    }
                ]
            },
            "Shipper": {
                "Address": {
                    "AddressLine": "Address Line",
                    "City": "City",
                    "CountryCode": "CountryCode",
                    "PostalCode": "PostalCode",
                    "StateProvinceCode": "StateProvinceCode",
                },
                "AttentionName": "Shipper Attn Name",
                "CompanyDisplayableName": "Shipper Name",
                "Name": "Shipper Name",
                "Phone": {"Number": "1234567890"},
                "ShipperNumber": "Your Account Number",
                "TaxIdentificationNumber": "123456",
            },
            "TaxInformationIndicator": "Y",
        },
    }
}

ShipmentResponseJSON = """{
	"ShipmentResponse": {
		"Response": {
			"ResponseStatus": {
				"Code": "1",
				"Description": "Success"
			},
			"Alert": [
				{
					"Code": "121524",
					"Description": "The payer of Duty and Tax charges is not required for UPS Letter, Documents of No Commercial Value or Qualified Domestic Shipments."
				},
				{
					"Code": "120900",
					"Description": "User Id and Shipper Number combination is not qualified to receive negotiated rates"
				}
			],
			"TransactionReference": {
				"CustomerContext": "testing",
				"TransactionIdentifier": "iewssoat2643k31L9059jT"
			}
		},
		"ShipmentResults": {
			"Disclaimer": {
				"Code": "01",
				"Description": "Taxes are included in the shipping cost and apply to the transportation charges but additional duties/taxes may apply and are not reflected in the total amount due."
			},
			"ShipmentCharges": {
				"BaseServiceCharge": {
					"CurrencyCode": "CAD",
					"MonetaryValue": "114.05"
				},
				"TransportationCharges": {
					"CurrencyCode": "CAD",
					"MonetaryValue": "135.15"
				},
				"ItemizedCharges": [
					{
						"Code": "178",
						"CurrencyCode": "CAD",
						"MonetaryValue": "0.00"
					},
					{
						"Code": "375",
						"CurrencyCode": "CAD",
						"MonetaryValue": "21.10"
					}
				],
				"ServiceOptionsCharges": {
					"CurrencyCode": "CAD",
					"MonetaryValue": "0.00"
				},
				"TaxCharges": {
					"Type": "HST",
					"MonetaryValue": "20.27"
				},
				"TotalCharges": {
					"CurrencyCode": "CAD",
					"MonetaryValue": "135.15"
				},
				"TotalChargesWithTaxes": {
					"CurrencyCode": "CAD",
					"MonetaryValue": "155.42"
				}
			},
			"RatingMethod": "01",
			"BillableWeightCalculationMethod": "02",
			"BillingWeight": {
				"UnitOfMeasurement": {
					"Code": "LBS",
					"Description": "Pounds"
				},
				"Weight": "10.0"
			},
			"ShipmentIdentificationNumber": "1ZXXXXXXXXXXXXXXXX",
			"PackageResults": {
				"TrackingNumber": "1ZXXXXXXXXXXXXXXXX",
				"ServiceOptionsCharges": {
					"CurrencyCode": "CAD",
					"MonetaryValue": "0.00"
				},
				"ShippingLabel": {
					"ImageFormat": {
						"Code": "PNG",
						"Description": "PNG"
					},
					"GraphicImage": "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",
					"HTMLImage": "PCFET0NUWVBFIEhUTUwgUFVCTElDICItLy9JRVRGLy9EVEQgSFRNTCAzLjIvL0VOIj4KPGh0bWw+PGhlYWQ+PHRpdGxlPgpWaWV3L1ByaW50IExhYmVsPC90aXRsZT48bWV0YSBjaGFyc2V0PSJVVEYtOCI+PC9oZWFkPjxzdHlsZT4KICAgIC5zbWFsbF90ZXh0IHtmb250LXNpemU6IDgwJTt9CiAgICAubGFyZ2VfdGV4dCB7Zm9udC1zaXplOiAxMTUlO30KPC9zdHlsZT4KPGJvZHkgYmdjb2xvcj0iI0ZGRkZGRiI+CjxkaXYgY2xhc3M9Imluc3RydWN0aW9ucy1kaXYiPgo8dGFibGUgY2xhc3M9Imluc3RydWN0aW9ucy10YWJsZSIgbmFtZWJvcmRlcj0iMCIgY2VsbHBhZGRpbmc9IjAiIGNlbGxzcGFjaW5nPSIwIiB3aWR0aD0iNjAwIj48dHI+Cjx0ZCBoZWlnaHQ9IjQxMCIgYWxpZ249ImxlZnQiIHZhbGlnbj0idG9wIj4KPEIgY2xhc3M9ImxhcmdlX3RleHQiPlZpZXcvUHJpbnQgTGFiZWw8L0I+CiZuYnNwOzxicj4KJm5ic3A7PGJyPgo8b2wgY2xhc3M9InNtYWxsX3RleHQiPiA8bGk+PGI+UHJpbnQgdGhlIGxhYmVsOjwvYj4gJm5ic3A7ClNlbGVjdCBQcmludCBmcm9tIHRoZSBGaWxlIG1lbnUgaW4gdGhpcyBicm93c2VyIHdpbmRvdyB0byBwcmludCB0aGUgbGFiZWwgYmVsb3cuPGJyPjxicj48bGk+PGI+CkZvbGQgdGhlIHByaW50ZWQgbGFiZWwgYXQgdGhlIGRvdHRlZCBsaW5lLjwvYj4gJm5ic3A7ClBsYWNlIHRoZSBsYWJlbCBpbiBhIFVQUyBTaGlwcGluZyBQb3VjaC4gSWYgeW91IGRvIG5vdCBoYXZlIGEgcG91Y2gsIGFmZml4IHRoZSBmb2xkZWQgbGFiZWwgdXNpbmcgY2xlYXIgcGxhc3RpYyBzaGlwcGluZyB0YXBlIG92ZXIgdGhlIGVudGlyZSBsYWJlbC48YnI+PGJyPjxsaT48Yj5HRVRUSU5HIFlPVVIgU0hJUE1FTlQgVE8gVVBTPGJyPgpDdXN0b21lcnMgd2l0aG91dCBhIERhaWx5IFBpY2t1cDwvYj48dWw+PGxpPkdyb3VuZCwgMyBEYXkgU2VsZWN0LCBhbmQgU3RhbmRhcmQgdG8gQ2FuYWRhIHNoaXBtZW50cyBtdXN0IGJlIGRyb3BwZWQgb2ZmIGF0IGFuIGF1dGhvcml6ZWQgVVBTIGxvY2F0aW9uLCBvciBoYW5kZWQgdG8gYSBVUFMgZHJpdmVyLiBQaWNrdXAgc2VydmljZSBpcyBub3QgYXZhaWxhYmxlIGZvciB0aGVzZSBzZXJ2aWNlcy4gVG8gZmluZCB0aGUgbmVhcmVzdCBkcm9wLW9mZiBsb2NhdGlvbiwgc2VsZWN0IHRoZSBEcm9wLW9mZiBpY29uIGZyb20gdGhlIFVQUyB0b29sIGJhci48bGk+CkFpciBzaGlwbWVudHMgKGluY2x1ZGluZyBXb3JsZHdpZGUgRXhwcmVzcyBhbmQgRXhwZWRpdGVkKSBjYW4gYmUgcGlja2VkIHVwIG9yIGRyb3BwZWQgb2ZmLiBUbyBzY2hlZHVsZSBhIHBpY2t1cCwgb3IgdG8gZmluZCBhIGRyb3Atb2ZmIGxvY2F0aW9uLCBzZWxlY3QgdGhlIFBpY2t1cCBvciBEcm9wLW9mZiBpY29uIGZyb20gdGhlIFVQUyB0b29sIGJhci4gPC91bD48YnI+CjxiPkN1c3RvbWVycyB3aXRoIGEgRGFpbHkgUGlja3VwPC9iPjx1bD48bGk+CllvdXIgZHJpdmVyIHdpbGwgcGlja3VwIHlvdXIgc2hpcG1lbnQocykgYXMgdXN1YWwuIDwvdWw+PGJyPgo8L29sPjwvdGQ+PC90cj48L3RhYmxlPjx0YWJsZSBib3JkZXI9IjAiIGNlbGxwYWRkaW5nPSIwIiBjZWxsc3BhY2luZz0iMCIgd2lkdGg9IjYwMCI+Cjx0cj4KPHRkIGNsYXNzPSJzbWFsbF90ZXh0IiBhbGlnbj0ibGVmdCIgdmFsaWduPSJ0b3AiPgombmJzcDsmbmJzcDsmbmJzcDsKPGEgbmFtZT0iZm9sZEhlcmUiPkZPTEQgSEVSRTwvYT48L3RkPgo8L3RyPgo8dHI+Cjx0ZCBhbGlnbj0ibGVmdCIgdmFsaWduPSJ0b3AiPjxocj4KPC90ZD4KPC90cj4KPC90YWJsZT4KCjx0YWJsZT4KPHRyPgo8dGQgaGVpZ2h0PSIxMCI+Jm5ic3A7CjwvdGQ+CjwvdHI+CjwvdGFibGU+Cgo8L2Rpdj4KPHRhYmxlIGJvcmRlcj0iMCIgY2VsbHBhZGRpbmc9IjAiIGNlbGxzcGFjaW5nPSIwIiB3aWR0aD0iNjUwIiA+PHRyPgo8dGQgYWxpZ249ImxlZnQiIHZhbGlnbj0idG9wIj4KPElNRyBTUkM9Ii4vbGFiZWwxWjAwMlI0ODE0MjkyMjE0MzMucG5nIiBoZWlnaHQ9IjM5MiIgd2lkdGg9IjY1MSI+CjwvdGQ+CjwvdHI+PC90YWJsZT4KPC9ib2R5Pgo8L2h0bWw+Cg=="
				}
			}
		}
	}
}
"""

ShipmentCancelResponseJSON = """{
    "VoidShipmentResponse": {
        "Response": {
            "ResponseStatus": {"Code": "1", "Description": "Success"},
            "TransactionReference": {
                "CustomerContext": "string",
                "TransactionIdentifier": "string"
            }
        },
        "SummaryResult": {"Status": {"Code": "1", "Description": "Success"}},
        "PackageLevelResult": [
            {
                "TrackingNumber": "string",
                "Status": {"Code": "1", "Description": "Success"}
            }
        ]
    }
}
"""
