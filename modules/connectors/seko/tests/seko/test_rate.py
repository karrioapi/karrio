import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging as logger

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestSEKOLogisticsRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.seko.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/ratesqueryv1/availablerates",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.seko.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {
  "customs": {
    "options": {
      "ioss": "IM3720021461",
      "eori_number": "GB457532476000"
    },
    "incoterm": "DAP",
    "commodities": [
      {
        "sku": "1234567890",
        "title": "iPod Nano",
        "weight": 1,
        "quantity": 1,
        "weight_unit": "KG",
        "value_amount": 17.26,
        "origin_country": "CN",
        "value_currency": "EUR"
      }
    ],
    "content_type": "merchandise"
  },
  "options": {
    "currency": "EUR",
    "shipping_date": "2025-07-14T23:47",
    "declared_value": 17.26,
    "seko_reference_2": "TSGBDERMUTFR002728973"
  },
  "parcels": [
    {
      "items": [
        {
          "sku": "1234567890",
          "title": "iPod Nano",
          "weight": 1,
          "quantity": 1,
          "weight_unit": "KG",
          "value_amount": 17.26,
          "origin_country": "CN",
          "value_currency": "EUR"
        }
      ],
      "width": 30,
      "height": 16,
      "length": 40,
      "weight": 1.2,
      "weight_unit": "KG",
      "dimension_unit": "CM",
      "reference_number": "ZS034789256GB"
    }
  ],
  "shipper": {
    "city": "London",
    "email": "customer@teleship.com",
    "state_code": "Egham",
    "person_name": "Teleship C/O SEKO Logistics",
    "postal_code": "TW20 8EY",
    "residential": True,
    "company_name": "Jane",
    "country_code": "GB",
    "phone_number": "+447557544686",
    "address_line1": "Unit 11, Egham Business Park",
    "address_line2": "Ten Acre Lane"
  },
  "recipient": {
    "city": "Munchen",
    "email": "customer@teleship.com",
    "person_name": "Lepold",
    "postal_code": "80804",
    "residential": True,
    "company_name": "Lepold",
    "country_code": "DE",
    "phone_number": "+447557544686",
    "address_line1": "Leopoldstrasse 119"
  },
  "reference": "TSGBDERMUTFR002728973",
  "return_address": {
    "city": "London",
    "email": "customer@teleship.com",
    "state_code": "Egham",
    "person_name": "Teleship C/O SEKO Logistics",
    "postal_code": "TW20 8EY",
    "residential": True,
    "company_name": "Teleship Inc",
    "country_code": "GB",
    "phone_number": "+447557544686",
    "address_line1": "Unit 11, Egham Business Park",
    "address_line2": "Ten Acre Lane"
  }
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "seko",
            "carrier_name": "seko",
            "currency": "GBP",
            "meta": {
                "CarrierServiceType": "InternationalCourier",
                "DeliveryType": "AIR TRACKED",
                "IsFreightForward": False,
                "IsRuralDelivery": False,
                "IsSaturdayDelivery": False,
                "QuoteId": "e7fdf36c-8f6a-4d3f-8d96-c8b5893a0e7f",
                "Route": "OFFSHORE->AKL- SI",
                "seko_carrier": "Omni Parcel",
                "service_name": "AIR TRACKED",
            },
            "service": "AIR TRACKED",
            "total_charge": 5.82,
        }
    ],
    [
        {
            "carrier_id": "seko",
            "carrier_name": "seko",
            "code": "ValidationError",
            "details": {
                "Key": "CountryCode",
                "Property": "Destination.Address.CountryCode",
            },
            "message": "CountryCode is required",
        }
    ],
]


RateRequest = {
    "DeliveryReference": "ORDER123",
    "Destination": {
        "Address": {
            "CountryCode": "NZ",
            "PostCode": "8061",
            "StreetAddress": "DestinationStreetAddress",
            "Suburb": "Christchurch",
        },
        "ContactPerson": "DestinationName",
        "DeliveryInstructions": "Desinationdeliveryinstructions",
        "Email": "destinationemail@email.com",
        "PhoneNumber": "123456789",
        "RecipientTaxId": "123456",
    },
    "IsSaturdayDelivery": False,
    "IsSignatureRequired": True,
    "Origin": {
        "Address": {
            "BuildingName": "TESTING COMPANY",
            "City": "WA",
            "CountryCode": "AU",
            "PostCode": "6155",
            "StreetAddress": "17 VULCAN RD",
            "Suburb": "CANNING VALE",
        },
        "ContactPerson": "TEST USER",
        "Email": "test@gmail.com",
        "Name": "TESTING COMPANY",
        "PhoneNumber": "(07) 3114 1499",
    },
    "Packages": [
        {
            "Height": 1.0,
            "Kg": 0.1,
            "Length": 1.0,
            "Name": "SATCHEL",
            "Type": "Box",
            "Width": 10.0,
        }
    ],
}


RateResponse = """{
  "Available": [
    {
      "QuoteId": "e7fdf36c-8f6a-4d3f-8d96-c8b5893a0e7f",
      "CarrierId": 604,
      "CarrierName": "Omni Parcel",
      "DeliveryType": "AIR TRACKED",
      "Cost": 5.82,
      "ServiceStandard": "",
      "Comments": "",
      "Route": "OFFSHORE->AKL- SI",
      "IsRuralDelivery": false,
      "IsSaturdayDelivery": false,
      "IsFreightForward": false,
      "CarrierServiceType": "InternationalCourier"
    }
  ],
  "Rejected": [
    {
      "CarrierName": "CarrierName",
      "DeliveryType": "DeliveryType",
      "Reason": "Reason"
    }
  ],
  "ValidationErrors": {
    "Property": "Destination.Address.CountryCode",
    "Message": "CountryCode is required",
    "Key": "CountryCode",
    "Value": ""
  }
}
"""
