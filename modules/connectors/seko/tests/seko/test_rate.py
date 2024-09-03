import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
from tests import logger

import karrio
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
                f"{gateway.settings.server_url}",
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
        "company_name": "CGI",
        "address_line1": "23 jardin private",
        "city": "Ottawa",
        "postal_code": "k1k 4t3",
        "country_code": "CA",
        "person_name": "Jain",
        "state_code": "ON",
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
    "options": {},
    "reference": "REF-001",
}

ParsedRateResponse = []


RateRequest = {
    "DeliveryReference": "ORDER123",
    "Destination": {
        "Id": 0,
        "Name": "DestinationName",
        "Address": {
            "BuildingName": "",
            "StreetAddress": "DestinationStreetAddress",
            "Suburb": "Avonside",
            "City": "Christchurch",
            "PostCode": "8061",
            "CountryCode": "NZ",
        },
        "ContactPerson": "DestinationContact",
        "PhoneNumber": "123456789",
        "Email": "destinationemail@email.com",
        "DeliveryInstructions": "Desinationdeliveryinstructions",
        "RecipientTaxId": "123456",
    },
    "IsSaturdayDelivery": False,
    "IsSignatureRequired": True,
    "Packages": [
        {
            "Height": 1,
            "Length": 1,
            "Id": 0,
            "Width": 10,
            "Kg": 0.1,
            "Name": "SATCHEL",
            "PackageCode": "DLE",
            "Type": "Box",
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
