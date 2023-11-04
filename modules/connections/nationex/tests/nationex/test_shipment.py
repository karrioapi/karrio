import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestNationexShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(
            **ShipmentCancelPayload
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertDictEqual(request.serialize(), ShipmentRequest)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(request.serialize(), ShipmentCancelRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.nationex.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/Shipments",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.nationex.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/Shipments/501883938",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.nationex.proxy.lib.request") as mock:
            mock.side_effect = [ShipmentResponse, ""]
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.nationex.proxy.lib.request") as mock:
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


ShipmentPayload = {
    "service": "nationex_delivery",
    "shipper": {
        "postal_code": "J3Y5T7",
        "person_name": "Sonia",
        "country_code": "CA",
        "city": "Montreal",
        "state_code": "QC",
        "address_line1": "Apple street",
        "address_line2": "3rd floor",
        "street_number": "880",
        "email": "example@gmail.com",
        "phone_number": "555123456",
    },
    "recipient": {
        "postal_code": "H2H2S2",
        "person_name": "John",
        "country_code": "CA",
        "city": "Montreal",
        "state_code": "QC",
        "address_line1": "Apple street",
        "address_line2": "3rd floor",
        "street_number": "433",
        "email": "example@gmail.com",
    },
    "parcels": [
        {
            "weight": 5.5,
            "height": 6.5,
            "length": 12.0,
            "width": 8.0,
            "weight_unit": "LB",
            "dimension_unit": "IN",
        }
    ],
    "options": {
        "shipment_date": "2021-03-30",
        "insurance": 100.0,
        "nationex_frozen_protection": True,
        "nationex_dangerous_goods": True,
        "nationex_snr": True,
        "shipment_note": "If no answer leave under the stairs",
    },
    "reference": "CX4335",
}

ShipmentCancelPayload = {
    "shipment_identifier": "501883938",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "nationex",
        "carrier_name": "nationex",
        "docs": {},
        "label_type": "PDF",
        "meta": {"tracking_numbers": [50188393801, 50188393802]},
        "shipment_identifier": "501883938",
        "tracking_number": "501883938",
    },
    [],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "nationex",
        "carrier_name": "nationex",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequest = {
    "label": {"format": "4x6", "orientation": "portrait", "type": "PDF"},
    "shipment": {
        "Accessory": {
            "DangerousGoods": True,
            "FrozenProtection": True,
            "InsuranceAmount": 100.0,
            "SNR": True,
        },
        "BillingAccount": 165556,
        "CustomerId": 113300,
        "Destination": {
            "Address1": "Apple street",
            "Address2": "3rd floor",
            "Contact": "John",
            "Email": "example@gmail.com",
            "NoCivic": "433",
            "PostalCode": "H2H2S2",
            "ProvinceState": "QC",
            "StreetName": "Apple street",
        },
        "ExpeditionDate": "2021-03-30",
        "Note": "If no answer leave under the stairs",
        "Parcels": [
            {
                "Dimensions": {
                    "Cubing": 0.36,
                    "Height": 6.5,
                    "Length": 12.0,
                    "Width": 8.0,
                },
                "NCV": False,
                "Weight": 5.5,
            }
        ],
        "ReferenceNumber": "CX4335",
        "Sender": {
            "Address1": "Apple street",
            "Address2": "3rd floor",
            "Contact": "Sonia",
            "Email": "example@gmail.com",
            "NoCivic": "880",
            "Phone": "555123456",
            "PostalCode": "J3Y5T7",
            "ProvinceState": "QC",
            "StreetName": "Apple street",
        },
        "ShipmentType": "Delivery",
        "TotalParcels": 1,
        "TotalWeight": 5.5,
        "UnitsOfMeasurement": "LI",
    },
}

ShipmentCancelRequest = {"shipment_id": "501883938"}

ShipmentResponse = """{
  "ShipmentId": 501883938,
  "ConsolId": 501883122,
  "BillingAccount": 165556,
  "ParcelIds": [
    50188393801,
    50188393802
  ],
  "Barcodes": [
    501883938010,
    501883938027
  ],
  "RatesDetail": {
    "BasePrice": 47.22,
    "SurchargeCharges": [
      {
        "Id": "99",
        "Charge": 2.404,
        "BeyondId": 0,
        "NameFr": "Colis hors-norme - Longueur",
        "NameEn": "Oversized parcel - Lenght"
      },
      {
        "Id": "519",
        "Charge": 8.404,
        "BeyondId": 102,
        "NameFr": "SURCHARGE RÉGION ÉLOIGNÉE",
        "NameEn": "BEYOND SURCHARGE"
      },
      {
        "Id": "0",
        "Charge": 4.323,
        "BeyondId": 0,
        "NameFr": "Classe B",
        "NameEn": "Class B"
      },
      {
        "Id": "0",
        "Charge": 6.323,
        "BeyondId": 0,
        "NameFr": "Classe C",
        "NameEn": "Class C"
      },
      {
        "Id": "0",
        "Charge": 12.13,
        "BeyondId": 0,
        "NameFr": "Classe D",
        "NameEn": "Class D"
      },
      {
        "Id": "0",
        "Charge": 20.76,
        "BeyondId": 0,
        "NameFr": "Classe P",
        "NameEn": "Class P"
      }
    ],
    "TaxCharges": [
      {
        "Id": "GST",
        "Charge": 0.287,
        "Rate": 0.05,
        "NameFr": "TPS",
        "NameEn": "GST"
      },
      {
        "Id": "PST",
        "Charge": 1.548,
        "Rate": 0.1,
        "NameFr": "TVQ",
        "NameEn": "PST"
      },
      {
        "Id": "HST",
        "Charge": 0,
        "Rate": 0,
        "NameFr": "TVH",
        "NameEn": "HST"
      }
    ],
    "AccessoryCharges": [
      {
        "Id": "1",
        "Charge": 12.97,
        "NameFr": "ASSURANCE SUPPL├ëMENTAIRE",
        "NameEn": "ADDITIONNAL INSURANCE"
      },
      {
        "Id": "2",
        "Charge": 5.125,
        "NameFr": "PAYABLE SUR LIVRAISON",
        "NameEn": "CASH OR CHEQUE ON DELIVERY"
      },
      {
        "Id": "3",
        "Charge": 11.366,
        "NameFr": "MATI├êRE DANGEREUSES",
        "NameEn": "DANGEROUS GOODS"
      },
      {
        "Id": "4",
        "Charge": 16.351,
        "NameFr": "LIVRAISON AVANT 10H30",
        "NameEn": "DELIVERY BEFORE 10H30"
      },
      {
        "Id": "5",
        "Charge": 7.577,
        "NameFr": "PROTECTION CONTRE LE GEL",
        "NameEn": "FREEZE PROTECTION"
      }
    ],
    "NCVCharge": 4,
    "FuelRate": 0.1425,
    "FuelCharge": 2.51,
    "SubTotal": 55.89,
    "Total": 61.12,
    "TotalBillableWeight": 0,
    "BillingZone": "NL",
    "DelayTransitDays": 2,
    "EstimatedDeliveryDate": "2021-05-05"
  }
}
"""

ShipmentCancelResponse = """{}
"""
