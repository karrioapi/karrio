import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TesteShipperShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(
            **ShipmentCancelPayload
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequest)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(request.serialize(), ShipmentCancelRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.eshipper.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.eshipper.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.eshipper.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.eshipper.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelShipmentResponse
            )


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {}

ShipmentCancelPayload = {
    "shipment_identifier": "794947717776",
}

ParsedShipmentResponse = []

ParsedCancelShipmentResponse = []


ShipmentRequest = {
    "scheduledShipDate": "2024-05-13T03:10:50.150Z",
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
        "phone": "\\ddd \\ddd\\dddd",
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
        "phone": "\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\d\\ddd\\ddd.\\dddd",
        "instructions": "string",
        "residential": True,
        "tailgateRequired": True,
        "confirmDelivery": True,
        "notifyRecipient": True,
    },
    "packagingUnit": "string",
    "packages": {
        "type": "string",
        "quantity": 0,
        "weightUnit": "string",
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
        "totalWeight": 0,
    },
    "reference1": "string",
    "reference2": "string",
    "reference3": "string",
    "transactionId": "string",
    "billingReference": "string",
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
            "phone": "\\ddd \\ddd \\dddd",
        },
        "remarks": "string",
    },
    "thirdPartyBilling": {
        "carrier": 0,
        "country": 0,
        "billToAccountNumber": "string",
        "billToPostalCode": "string",
    },
    "commodityType": "string",
    "isSaturdayService": True,
    "holdForPickupRequired": True,
    "specialEquipment": True,
    "deliveryAppointment": True,
    "insideDelivery": True,
    "insidePickup": True,
    "saturdayPickupRequired": True,
    "stackable": True,
    "serviceId": 0,
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
}

ShipmentCancelRequest = {
    "order": {
        "trackingId": "string",
        "orderId": "string",
        "message": "string",
    },
}


ShipmentResponse = """{
  "order": {
    "trackingId": "string",
    "orderId": "string",
    "message": "string"
  },
  "carrier": {
    "carrierName": "string",
    "serviceName": "string",
    "carrierLogoPath": "string"
  },
  "reference": {
    "code": "string",
    "name": "string"
  },
  "reference2": {
    "code": "string",
    "name": "string"
  },
  "reference3": {
    "code": "string",
    "name": "string"
  },
  "transactionId": "string",
  "billingReference": "string",
  "packages": [
    {
      "trackingNumber": "string"
    }
  ],
  "trackingUrl": "string",
  "brandedTrackingUrl": "string",
  "trackingNumber": "string",
  "labelData": {
    "label": [
      {
        "type": "string",
        "data": "string"
      }
    ]
  },
  "customsInvoice": {
    "type": "string",
    "data": "string"
  },
  "pickup": {
    "confirmationNumber": "string"
  },
  "packingSlip": "string",
  "quote": {
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
    "currency": "string",
    "carrierLogo": "string",
    "id": "string"
  },
  "billing": {
    "invoices": [
      {
        "invoiceNumber": "string",
        "charges": [
          {
            "charge": "string",
            "amount": "string",
            "adjustmentReasons": "string"
          }
        ],
        "total": 0
      }
    ]
  },
  "returnShipment": "string",
  "message": "string"
}
"""

ShipmentCancelResponse = """{
  "order": [
    {
      "trackingId": "string",
      "orderId": "string",
      "message": "string"
    }
  ]
}
"""
