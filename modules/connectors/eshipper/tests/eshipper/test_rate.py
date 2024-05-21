import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TesteShipperRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.eshipper.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.eshipper.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {}

ParsedRateResponse = []


RateRequest = {
    "scheduledShipDate": "2024-05-13T03:06:32.688Z",
    "from": {
        "attention": "string",
        "company": "string",
        "address1": "string",
        "address2": "string",
        "city": "string",
        "province": "string",
        "country": "string",
        "zip": "string",
        "email": "string",
        "phone": "8000000000",
        "instructions": "string",
        "residential": True,
        "tailgateRequired": True,
        "confirmDelivery": True,
        "notifyRecipient": True,
    },
    "to": {
        "attention": "string",
        "company": "string",
        "address1": "string",
        "address2": "string",
        "city": "string",
        "province": "string",
        "country": "string",
        "zip": "string",
        "email": "string",
        "phone": "8000000000",
        "instructions": "string",
        "residential": True,
        "tailgateRequired": True,
        "confirmDelivery": True,
        "notifyRecipient": True,
    },
    "packagingUnit": "string",
    "packages": {
        "type": "string",
        "packages": [
            {
                "height": 0,
                "length": 0,
                "width": 0,
                "dimensionUnit": "string",
                "weight": 0,
                "weightUnit": "string",
                "type": "string",
                "freightClass": "string",
                "nmfcCode": "string",
                "insuranceAmount": 0,
                "codAmount": 0,
                "description": "string",
                "harmonizedCode": "string",
                "skuCode": "string",
            }
        ],
    },
    "reference1": "string",
    "reference2": "string",
    "reference3": "string",
    "transactionId": "string",
    "signatureRequired": "string",
    "insuranceType": "string",
    "dangerousGoodsType": "string",
    "pickup": {
        "contactName": "string",
        "phoneNumber": "string",
        "pickupDate": "2024-05-13",
        "pickupTime": {"hour": 0, "minute": 0, "second": 0, "nano": 0},
        "closingTime": {"hour": 0, "minute": 0, "second": 0, "nano": 0},
        "palletPickupTime": {"hour": 0, "minute": 0, "second": 0, "nano": 0},
        "palletClosingTime": {"hour": 0, "minute": 0, "second": 0, "nano": 0},
        "palletDeliveryClosingTime": {"hour": 0, "minute": 0, "second": 0, "nano": 0},
        "location": "Receiving",
        "instructions": "string",
    },
    "customsInformation": {
        "contact": {
            "contactCompany": "string",
            "contactName": "string",
            "phone": "string",
            "brokerName": "string",
            "brokerTaxId": "string",
            "recipientTaxId": "string",
        },
        "items": {
            "item": [
                {
                    "hsnCode": "string",
                    "description": "string",
                    "originCountry": "string",
                    "quantity": 99999,
                    "unitPrice": 10000000,
                    "skuCode": "string",
                }
            ],
            "currency": "string",
        },
        "dutiesTaxes": {
            "dutiable": True,
            "billTo": "string",
            "accountNumber": "string",
            "sedNumber": "string",
        },
        "billingAddress": {
            "company": "string",
            "attention": "string",
            "address1": "string",
            "address2": "string",
            "city": "string",
            "province": "string",
            "country": "string",
            "zip": "string",
            "email": "string",
            "phone": "8000000000",
        },
        "remarks": "string",
    },
    "customsInBondFreight": True,
    "cod": {
        "codAddress": {
            "company": "string",
            "name": "string",
            "addressLine1": "string",
            "city": "string",
            "province": "string",
            "country": "string",
            "zip": "string",
        },
        "paymentType": "string",
    },
    "isSaturdayService": True,
    "holdForPickupRequired": True,
    "specialEquipment": True,
    "insideDelivery": True,
    "deliveryAppointment": True,
    "insidePickup": True,
    "saturdayPickupRequired": True,
    "stackable": True,
    "serviceId": 0,
    "thirdPartyBilling": {
        "carrier": 0,
        "country": 0,
        "billToAccountNumber": "string",
        "billToPostalCode": "string",
    },
    "commodityType": "string",
}

RateResponse = """{
  "uuid": "string",
  "quotes": [
    {
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
      "currency": "string"
    }
  ],
  "warnings": [
    "string"
  ],
  "errors": [
    "string"
  ]
}
"""
