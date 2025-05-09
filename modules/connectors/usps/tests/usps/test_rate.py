import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging as logger

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestUSPSRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/prices/v3/total-rates/search",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {
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
    "options": {
        "usps_label_delivery_service": True,
        "usps_price_type": "COMMERCIAL",
        "shipment_date": "2024-07-28",
    },
    "services": ["usps_parcel_select"],
    "reference": "REF-001",
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 74.92,
                    "currency": "USD",
                    "name": "Priority Mail Machinable Dimensional Rectangular",
                },
                {"amount": 4.85, "currency": "USD", "name": "Certified Mail"},
                {
                    "amount": 12.75,
                    "currency": "USD",
                    "name": "Certified Mail Restricted Delivery",
                },
                {"amount": 4.1, "currency": "USD", "name": "Return Receipt"},
                {
                    "amount": 12.75,
                    "currency": "USD",
                    "name": "Certified Mail Adult Signature Required",
                },
                {
                    "amount": 2.62,
                    "currency": "USD",
                    "name": "Return Receipt Electronic",
                },
                {
                    "amount": 12.75,
                    "currency": "USD",
                    "name": "Certified Mail Adult Signature Restricted Delivery",
                },
                {"amount": 7.7, "currency": "USD", "name": "COD Restricted Delivery"},
                {
                    "amount": 0.99,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 6 months",
                },
                {
                    "amount": 1.2,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 1 year",
                },
                {
                    "amount": 1.5,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 3 years",
                },
                {
                    "amount": 2.0,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 5 years",
                },
                {
                    "amount": 3.0,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 7 years",
                },
                {
                    "amount": 4.2,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 10 years",
                },
                {
                    "amount": 3.75,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 3 years with signature",
                },
                {
                    "amount": 4.75,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 5 years with signature",
                },
                {
                    "amount": 5.75,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 7 years with signature",
                },
                {
                    "amount": 6.75,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 10 years with signature",
                },
                {"amount": 3.7, "currency": "USD", "name": "Signature Confirmation"},
                {"amount": 9.35, "currency": "USD", "name": "Adult Signature Required"},
                {
                    "amount": 9.65,
                    "currency": "USD",
                    "name": "Adult Signature Restricted Delivery",
                },
                {
                    "amount": 11.4,
                    "currency": "USD",
                    "name": "Signature Confirmation Restricted Delivery",
                },
                {"amount": 1.25, "currency": "USD", "name": "Label Delivery"},
                {
                    "amount": 0.6,
                    "currency": "USD",
                    "name": "Live Animal Transportation Fee",
                },
                {
                    "amount": 7.7,
                    "currency": "USD",
                    "name": "Insurance Restricted Delivery",
                },
                {"amount": 18.6, "currency": "USD", "name": "Registered Mail"},
                {
                    "amount": 26.3,
                    "currency": "USD",
                    "name": "Registered Mail Restricted Delivery",
                },
            ],
            "meta": {
                "service_name": "usps_priority_mail",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "DR",
                "usps_zone": "08",
            },
            "service": "usps_priority_mail",
            "total_charge": 104.92,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 74.92,
                    "currency": "USD",
                    "name": "Priority Mail Machinable Dimensional Rectangular",
                },
                {"amount": 4.85, "currency": "USD", "name": "Certified Mail"},
                {
                    "amount": 12.75,
                    "currency": "USD",
                    "name": "Certified Mail Restricted Delivery",
                },
                {"amount": 4.1, "currency": "USD", "name": "Return Receipt"},
                {
                    "amount": 12.75,
                    "currency": "USD",
                    "name": "Certified Mail Adult Signature Required",
                },
                {
                    "amount": 2.62,
                    "currency": "USD",
                    "name": "Return Receipt Electronic",
                },
                {
                    "amount": 12.75,
                    "currency": "USD",
                    "name": "Certified Mail Adult Signature Restricted Delivery",
                },
                {"amount": 7.7, "currency": "USD", "name": "COD Restricted Delivery"},
                {
                    "amount": 0.99,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 6 months",
                },
                {
                    "amount": 1.2,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 1 year",
                },
                {
                    "amount": 1.5,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 3 years",
                },
                {
                    "amount": 2.0,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 5 years",
                },
                {
                    "amount": 3.0,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 7 years",
                },
                {
                    "amount": 4.2,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 10 years",
                },
                {
                    "amount": 3.75,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 3 years with signature",
                },
                {
                    "amount": 4.75,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 5 years with signature",
                },
                {
                    "amount": 5.75,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 7 years with signature",
                },
                {
                    "amount": 6.75,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 10 years with signature",
                },
                {"amount": 3.7, "currency": "USD", "name": "Signature Confirmation"},
                {"amount": 9.35, "currency": "USD", "name": "Adult Signature Required"},
                {
                    "amount": 9.65,
                    "currency": "USD",
                    "name": "Adult Signature Restricted Delivery",
                },
                {
                    "amount": 11.4,
                    "currency": "USD",
                    "name": "Signature Confirmation Restricted Delivery",
                },
                {"amount": 1.25, "currency": "USD", "name": "Label Delivery"},
                {
                    "amount": 0.6,
                    "currency": "USD",
                    "name": "Live Animal Transportation Fee",
                },
                {
                    "amount": 7.7,
                    "currency": "USD",
                    "name": "Insurance Restricted Delivery",
                },
                {"amount": 18.6, "currency": "USD", "name": "Registered Mail"},
                {
                    "amount": 26.3,
                    "currency": "USD",
                    "name": "Registered Mail Restricted Delivery",
                },
            ],
            "meta": {
                "service_name": "usps_priority_mail",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "DN",
                "usps_zone": "08",
            },
            "service": "usps_priority_mail",
            "total_charge": 104.92,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 181.9,
                    "currency": "USD",
                    "name": "Priority Mail Express Machinable Dimensional Rectangular",
                },
                {"amount": 12.5, "currency": "USD", "name": "Sunday/Holiday Delivery"},
                {"amount": 4.85, "currency": "USD", "name": "Certified Mail"},
                {
                    "amount": 12.75,
                    "currency": "USD",
                    "name": "Certified Mail Restricted Delivery",
                },
                {"amount": 4.1, "currency": "USD", "name": "Return Receipt"},
                {
                    "amount": 12.75,
                    "currency": "USD",
                    "name": "Certified Mail Adult Signature Required",
                },
                {
                    "amount": 2.62,
                    "currency": "USD",
                    "name": "Return Receipt Electronic",
                },
                {
                    "amount": 12.75,
                    "currency": "USD",
                    "name": "Certified Mail Adult Signature Restricted Delivery",
                },
                {"amount": 7.7, "currency": "USD", "name": "COD Restricted Delivery"},
                {
                    "amount": 0.99,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 6 months",
                },
                {
                    "amount": 1.2,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 1 year",
                },
                {
                    "amount": 1.5,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 3 years",
                },
                {
                    "amount": 2.0,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 5 years",
                },
                {
                    "amount": 3.0,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 7 years",
                },
                {
                    "amount": 4.2,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 10 years",
                },
                {
                    "amount": 3.75,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 3 years with signature",
                },
                {
                    "amount": 4.75,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 5 years with signature",
                },
                {
                    "amount": 5.75,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 7 years with signature",
                },
                {
                    "amount": 6.75,
                    "currency": "USD",
                    "name": "Premium Data Retention and Retrieval Services 10 years with signature",
                },
                {"amount": 9.35, "currency": "USD", "name": "Adult Signature Required"},
                {
                    "amount": 9.65,
                    "currency": "USD",
                    "name": "Adult Signature Restricted Delivery",
                },
                {"amount": 1.25, "currency": "USD", "name": "Label Delivery"},
                {
                    "amount": 0.6,
                    "currency": "USD",
                    "name": "Live Animal Transportation Fee",
                },
                {
                    "amount": 7.7,
                    "currency": "USD",
                    "name": "Insurance Restricted Delivery",
                },
                {"amount": 18.6, "currency": "USD", "name": "Registered Mail"},
                {
                    "amount": 26.3,
                    "currency": "USD",
                    "name": "Registered Mail Restricted Delivery",
                },
            ],
            "meta": {
                "service_name": "usps_priority_mail_express",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "DR",
                "usps_zone": "08",
            },
            "service": "usps_priority_mail_express",
            "total_charge": 211.9,
        },
    ],
    [],
]

RateRequest = [
    {
        "accountNumber": "Your Account Number",
        "accountType": "EPS",
        "destinationZIPCode": "73108",
        "extraServices": [415],
        "height": 19.69,
        "length": 19.69,
        "mailClasses": ["PARCEL_SELECT"],
        "mailingDate": "2024-07-28",
        "originZIPCode": "29440",
        "priceType": "COMMERCIAL",
        "weight": 44.1,
        "width": 4.72,
    }
]


RateResponse = """{
  "rateOptions": [
    {
      "totalBasePrice": 104.92,
      "rates": [
        {
          "description": "Priority Mail Machinable Dimensional Rectangular",
          "priceType": "COMMERCIAL",
          "price": 74.92,
          "weight": 2.21,
          "dimWeight": 22.0,
          "fees": [
            {
              "name": "Nonstandard Volume > 2 cu ft",
              "SKU": "D813XXNXXXX0000",
              "price": 30.0
            }
          ],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "PRIORITY_MAIL",
          "zone": "08",
          "productName": "Priority Mail",
          "productDefinition": "1-3 day specific delivery to all U.S. states and territories",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "DR",
          "destinationEntryFacilityType": "NONE",
          "SKU": "DPXR0XXXXC08220"
        }
      ],
      "extraServices": [
        {
          "extraService": "910",
          "name": "Certified Mail",
          "priceType": "COMMERCIAL",
          "price": 4.85,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXEX0XXXXCX0000"
        },
        {
          "extraService": "911",
          "name": "Certified Mail Restricted Delivery",
          "priceType": "COMMERCIAL",
          "price": 12.75,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXEX0XJXXCX0000"
        },
        {
          "extraService": "955",
          "name": "Return Receipt",
          "priceType": "COMMERCIAL",
          "price": 4.1,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXRX0XXXXCX0000"
        },
        {
          "extraService": "912",
          "name": "Certified Mail Adult Signature Required",
          "priceType": "COMMERCIAL",
          "price": 12.75,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXEX0XAXXCX0000"
        },
        {
          "extraService": "957",
          "name": "Return Receipt Electronic",
          "priceType": "COMMERCIAL",
          "price": 2.62,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXRX0EXXXCX0000"
        },
        {
          "extraService": "913",
          "name": "Certified Mail Adult Signature Restricted Delivery",
          "priceType": "COMMERCIAL",
          "price": 12.75,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXEX0XBXXCX0000"
        },
        {
          "extraService": "917",
          "name": "COD Restricted Delivery",
          "priceType": "COMMERCIAL",
          "price": 7.7,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXCX0XJXXCX0000"
        },
        {
          "extraService": "480",
          "name": "Premium Data Retention and Retrieval Services 6 months",
          "priceType": "COMMERCIAL",
          "price": 0.99,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KPYOXXXC00000"
        },
        {
          "extraService": "481",
          "name": "Premium Data Retention and Retrieval Services 1 year",
          "priceType": "COMMERCIAL",
          "price": 1.2,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KP1OXXXC00000"
        },
        {
          "extraService": "482",
          "name": "Premium Data Retention and Retrieval Services 3 years",
          "priceType": "COMMERCIAL",
          "price": 1.5,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KP3OXXXC00000"
        },
        {
          "extraService": "483",
          "name": "Premium Data Retention and Retrieval Services 5 years",
          "priceType": "COMMERCIAL",
          "price": 2.0,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KP5OXXXC00000"
        },
        {
          "extraService": "484",
          "name": "Premium Data Retention and Retrieval Services 7 years",
          "priceType": "COMMERCIAL",
          "price": 3.0,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KP7OXXXC00000"
        },
        {
          "extraService": "485",
          "name": "Premium Data Retention and Retrieval Services 10 years",
          "priceType": "COMMERCIAL",
          "price": 4.2,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KPZOXXXC00000"
        },
        {
          "extraService": "486",
          "name": "Premium Data Retention and Retrieval Services 3 years with signature",
          "priceType": "COMMERCIAL",
          "price": 3.75,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KP3OSXXC00000"
        },
        {
          "extraService": "960",
          "name": "Return Receipt For Merchandise",
          "priceType": "COMMERCIAL",
          "price": 0.0,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXRX0MXXXCX0000"
        },
        {
          "extraService": "487",
          "name": "Premium Data Retention and Retrieval Services 5 years with signature",
          "priceType": "COMMERCIAL",
          "price": 4.75,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KP5OSXXC00000"
        },
        {
          "extraService": "488",
          "name": "Premium Data Retention and Retrieval Services 7 years with signature",
          "priceType": "COMMERCIAL",
          "price": 5.75,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KP7OSXXC00000"
        },
        {
          "extraService": "489",
          "name": "Premium Data Retention and Retrieval Services 10 years with signature",
          "priceType": "COMMERCIAL",
          "price": 6.75,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KPZOSXXC00000"
        },
        {
          "extraService": "920",
          "name": "USPS Tracking",
          "priceType": "COMMERCIAL",
          "price": 0.0,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXTP0EXXXCX0000"
        },
        {
          "extraService": "921",
          "name": "Signature Confirmation",
          "priceType": "COMMERCIAL",
          "price": 3.7,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXSP0EXXXCX0000"
        },
        {
          "extraService": "922",
          "name": "Adult Signature Required",
          "priceType": "COMMERCIAL",
          "price": 9.35,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXAX0XXXXCX0000"
        },
        {
          "extraService": "923",
          "name": "Adult Signature Restricted Delivery",
          "priceType": "COMMERCIAL",
          "price": 9.65,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXBX0XXXXCX0000"
        },
        {
          "extraService": "924",
          "name": "Signature Confirmation Restricted Delivery",
          "priceType": "COMMERCIAL",
          "price": 11.4,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXSP0EJXXCX0000"
        },
        {
          "extraService": "415",
          "name": "Label Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.25,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXQX0XXXXCX0000"
        },
        {
          "extraService": "856",
          "name": "Live Animal Transportation Fee",
          "priceType": "COMMERCIAL",
          "price": 0.6,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DX5X0XXXXCX0000"
        },
        {
          "extraService": "934",
          "name": "Insurance Restricted Delivery",
          "priceType": "COMMERCIAL",
          "price": 7.7,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXIX0XJXXCX0000"
        },
        {
          "extraService": "940",
          "name": "Registered Mail",
          "priceType": "COMMERCIAL",
          "price": 18.6,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXGX0XXXXCX0000"
        },
        {
          "extraService": "941",
          "name": "Registered Mail Restricted Delivery",
          "priceType": "COMMERCIAL",
          "price": 26.3,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXGX0XJXXCX0000"
        }
      ]
    },
    {
      "totalBasePrice": 59.77,
      "rates": [
        {
          "description": "Priority Mail Machinable Dimensional Nonrectangular",
          "priceType": "COMMERCIAL",
          "price": 59.77,
          "weight": 2.21,
          "dimWeight": 17.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "PRIORITY_MAIL",
          "zone": "08",
          "productName": "Priority Mail",
          "productDefinition": "1-3 day specific delivery to all U.S. states and territories",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "DN",
          "destinationEntryFacilityType": "NONE",
          "SKU": "DPXR0XXXXC08170"
        }
      ],
      "extraServices": [
        {
          "extraService": "910",
          "name": "Certified Mail",
          "priceType": "COMMERCIAL",
          "price": 4.85,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXEX0XXXXCX0000"
        },
        {
          "extraService": "911",
          "name": "Certified Mail Restricted Delivery",
          "priceType": "COMMERCIAL",
          "price": 12.75,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXEX0XJXXCX0000"
        },
        {
          "extraService": "955",
          "name": "Return Receipt",
          "priceType": "COMMERCIAL",
          "price": 4.1,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXRX0XXXXCX0000"
        },
        {
          "extraService": "912",
          "name": "Certified Mail Adult Signature Required",
          "priceType": "COMMERCIAL",
          "price": 12.75,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXEX0XAXXCX0000"
        },
        {
          "extraService": "957",
          "name": "Return Receipt Electronic",
          "priceType": "COMMERCIAL",
          "price": 2.62,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXRX0EXXXCX0000"
        },
        {
          "extraService": "913",
          "name": "Certified Mail Adult Signature Restricted Delivery",
          "priceType": "COMMERCIAL",
          "price": 12.75,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXEX0XBXXCX0000"
        },
        {
          "extraService": "917",
          "name": "COD Restricted Delivery",
          "priceType": "COMMERCIAL",
          "price": 7.7,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXCX0XJXXCX0000"
        },
        {
          "extraService": "480",
          "name": "Premium Data Retention and Retrieval Services 6 months",
          "priceType": "COMMERCIAL",
          "price": 0.99,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KPYOXXXC00000"
        },
        {
          "extraService": "481",
          "name": "Premium Data Retention and Retrieval Services 1 year",
          "priceType": "COMMERCIAL",
          "price": 1.2,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KP1OXXXC00000"
        },
        {
          "extraService": "482",
          "name": "Premium Data Retention and Retrieval Services 3 years",
          "priceType": "COMMERCIAL",
          "price": 1.5,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KP3OXXXC00000"
        },
        {
          "extraService": "483",
          "name": "Premium Data Retention and Retrieval Services 5 years",
          "priceType": "COMMERCIAL",
          "price": 2.0,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KP5OXXXC00000"
        },
        {
          "extraService": "484",
          "name": "Premium Data Retention and Retrieval Services 7 years",
          "priceType": "COMMERCIAL",
          "price": 3.0,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KP7OXXXC00000"
        },
        {
          "extraService": "485",
          "name": "Premium Data Retention and Retrieval Services 10 years",
          "priceType": "COMMERCIAL",
          "price": 4.2,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KPZOXXXC00000"
        },
        {
          "extraService": "486",
          "name": "Premium Data Retention and Retrieval Services 3 years with signature",
          "priceType": "COMMERCIAL",
          "price": 3.75,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KP3OSXXC00000"
        },
        {
          "extraService": "960",
          "name": "Return Receipt For Merchandise",
          "priceType": "COMMERCIAL",
          "price": 0.0,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXRX0MXXXCX0000"
        },
        {
          "extraService": "487",
          "name": "Premium Data Retention and Retrieval Services 5 years with signature",
          "priceType": "COMMERCIAL",
          "price": 4.75,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KP5OSXXC00000"
        },
        {
          "extraService": "488",
          "name": "Premium Data Retention and Retrieval Services 7 years with signature",
          "priceType": "COMMERCIAL",
          "price": 5.75,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KP7OSXXC00000"
        },
        {
          "extraService": "489",
          "name": "Premium Data Retention and Retrieval Services 10 years with signature",
          "priceType": "COMMERCIAL",
          "price": 6.75,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KPZOSXXC00000"
        },
        {
          "extraService": "920",
          "name": "USPS Tracking",
          "priceType": "COMMERCIAL",
          "price": 0.0,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXTP0EXXXCX0000"
        },
        {
          "extraService": "921",
          "name": "Signature Confirmation",
          "priceType": "COMMERCIAL",
          "price": 3.7,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXSP0EXXXCX0000"
        },
        {
          "extraService": "922",
          "name": "Adult Signature Required",
          "priceType": "COMMERCIAL",
          "price": 9.35,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXAX0XXXXCX0000"
        },
        {
          "extraService": "923",
          "name": "Adult Signature Restricted Delivery",
          "priceType": "COMMERCIAL",
          "price": 9.65,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXBX0XXXXCX0000"
        },
        {
          "extraService": "924",
          "name": "Signature Confirmation Restricted Delivery",
          "priceType": "COMMERCIAL",
          "price": 11.4,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXSP0EJXXCX0000"
        },
        {
          "extraService": "415",
          "name": "Label Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.25,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXQX0XXXXCX0000"
        },
        {
          "extraService": "856",
          "name": "Live Animal Transportation Fee",
          "priceType": "COMMERCIAL",
          "price": 0.6,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DX5X0XXXXCX0000"
        },
        {
          "extraService": "934",
          "name": "Insurance Restricted Delivery",
          "priceType": "COMMERCIAL",
          "price": 7.7,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXIX0XJXXCX0000"
        },
        {
          "extraService": "940",
          "name": "Registered Mail",
          "priceType": "COMMERCIAL",
          "price": 18.6,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXGX0XXXXCX0000"
        },
        {
          "extraService": "941",
          "name": "Registered Mail Restricted Delivery",
          "priceType": "COMMERCIAL",
          "price": 26.3,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXGX0XJXXCX0000"
        }
      ]
    },
    {
      "totalBasePrice": 211.9,
      "rates": [
        {
          "description": "Priority Mail Express Machinable Dimensional Rectangular",
          "priceType": "COMMERCIAL",
          "price": 181.9,
          "weight": 2.21,
          "dimWeight": 22.0,
          "fees": [
            {
              "name": "Nonstandard Volume > 2 cu ft",
              "SKU": "D813XXNXXXX0000",
              "price": 30.0
            }
          ],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "PRIORITY_MAIL_EXPRESS",
          "zone": "08",
          "productName": "Priority Mail Express",
          "productDefinition": "1-2 day specific guaranteed delivery by 6:00pm local delivery time",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "DR",
          "destinationEntryFacilityType": "NONE",
          "SKU": "DEXR0XXXXC08220"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 12.5,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZE0XXXXCX0000"
        },
        {
          "extraService": "910",
          "name": "Certified Mail",
          "priceType": "COMMERCIAL",
          "price": 4.85,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXEX0XXXXCX0000"
        },
        {
          "extraService": "911",
          "name": "Certified Mail Restricted Delivery",
          "priceType": "COMMERCIAL",
          "price": 12.75,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXEX0XJXXCX0000"
        },
        {
          "extraService": "955",
          "name": "Return Receipt",
          "priceType": "COMMERCIAL",
          "price": 4.1,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXRX0XXXXCX0000"
        },
        {
          "extraService": "912",
          "name": "Certified Mail Adult Signature Required",
          "priceType": "COMMERCIAL",
          "price": 12.75,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXEX0XAXXCX0000"
        },
        {
          "extraService": "957",
          "name": "Return Receipt Electronic",
          "priceType": "COMMERCIAL",
          "price": 2.62,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXRX0EXXXCX0000"
        },
        {
          "extraService": "913",
          "name": "Certified Mail Adult Signature Restricted Delivery",
          "priceType": "COMMERCIAL",
          "price": 12.75,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXEX0XBXXCX0000"
        },
        {
          "extraService": "917",
          "name": "COD Restricted Delivery",
          "priceType": "COMMERCIAL",
          "price": 7.7,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXCX0XJXXCX0000"
        },
        {
          "extraService": "480",
          "name": "Premium Data Retention and Retrieval Services 6 months",
          "priceType": "COMMERCIAL",
          "price": 0.99,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KEYOXXXC00000"
        },
        {
          "extraService": "481",
          "name": "Premium Data Retention and Retrieval Services 1 year",
          "priceType": "COMMERCIAL",
          "price": 1.2,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KE1OXXXC00000"
        },
        {
          "extraService": "482",
          "name": "Premium Data Retention and Retrieval Services 3 years",
          "priceType": "COMMERCIAL",
          "price": 1.5,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KE3OXXXC00000"
        },
        {
          "extraService": "483",
          "name": "Premium Data Retention and Retrieval Services 5 years",
          "priceType": "COMMERCIAL",
          "price": 2.0,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KE5OXXXC00000"
        },
        {
          "extraService": "484",
          "name": "Premium Data Retention and Retrieval Services 7 years",
          "priceType": "COMMERCIAL",
          "price": 3.0,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KE7OXXXC00000"
        },
        {
          "extraService": "485",
          "name": "Premium Data Retention and Retrieval Services 10 years",
          "priceType": "COMMERCIAL",
          "price": 4.2,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KEZOXXXC00000"
        },
        {
          "extraService": "486",
          "name": "Premium Data Retention and Retrieval Services 3 years with signature",
          "priceType": "COMMERCIAL",
          "price": 3.75,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KE3OSXXC00000"
        },
        {
          "extraService": "960",
          "name": "Return Receipt For Merchandise",
          "priceType": "COMMERCIAL",
          "price": 0.0,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXRX0MXXXCX0000"
        },
        {
          "extraService": "487",
          "name": "Premium Data Retention and Retrieval Services 5 years with signature",
          "priceType": "COMMERCIAL",
          "price": 4.75,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KE5OSXXC00000"
        },
        {
          "extraService": "488",
          "name": "Premium Data Retention and Retrieval Services 7 years with signature",
          "priceType": "COMMERCIAL",
          "price": 5.75,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KE7OSXXC00000"
        },
        {
          "extraService": "489",
          "name": "Premium Data Retention and Retrieval Services 10 years with signature",
          "priceType": "COMMERCIAL",
          "price": 6.75,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "D2KEZOSXXC00000"
        },
        {
          "extraService": "920",
          "name": "USPS Tracking",
          "priceType": "COMMERCIAL",
          "price": 0.0,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXTE0EXXXCX0000"
        },
        {
          "extraService": "922",
          "name": "Adult Signature Required",
          "priceType": "COMMERCIAL",
          "price": 9.35,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXAX0XXXXCX0000"
        },
        {
          "extraService": "923",
          "name": "Adult Signature Restricted Delivery",
          "priceType": "COMMERCIAL",
          "price": 9.65,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXBX0XXXXCX0000"
        },
        {
          "extraService": "415",
          "name": "Label Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.25,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXQX0XXXXCX0000"
        },
        {
          "extraService": "856",
          "name": "Live Animal Transportation Fee",
          "priceType": "COMMERCIAL",
          "price": 0.6,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DX5X0XXXXCX0000"
        },
        {
          "extraService": "934",
          "name": "Insurance Restricted Delivery",
          "priceType": "COMMERCIAL",
          "price": 7.7,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXIX0XJXXCX0000"
        },
        {
          "extraService": "940",
          "name": "Registered Mail",
          "priceType": "COMMERCIAL",
          "price": 18.6,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXGX0XXXXCX0000"
        },
        {
          "extraService": "941",
          "name": "Registered Mail Restricted Delivery",
          "priceType": "COMMERCIAL",
          "price": 26.3,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXGX0XJXXCX0000"
        }
      ]
    }
  ]
}
"""
