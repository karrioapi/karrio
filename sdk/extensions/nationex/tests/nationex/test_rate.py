import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestNationexRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertDictEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.nationex.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/Customers/113300/rates",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.nationex.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {
    "shipper": {
        "postal_code": "J3Y5T7",
        "country_code": "CA",
    },
    "recipient": {
        "postal_code": "H2H2S2",
        "country_code": "CA",
    },
    "parcels": [
        {
            "weight": 12.2,
            "height": 6.5,
            "length": 12.0,
            "width": 8.0,
            "weight_unit": "LB",
            "dimension_unit": "IN",
        }
    ],
    "options": {
        "shipment_date": "2021-03-31",
        "insurance": 100.0,
        "nationex_frozen_protection": True,
        "nationex_dangerous_goods": True,
    },
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "nationex",
            "carrier_name": "nationex",
            "currency": "CAD",
            "estimated_delivery": "2021-05-05",
            "extra_charges": [
                {"amount": 47.22, "currency": "CAD", "name": "Base Charge"},
                {"amount": 2.51, "currency": "CAD", "name": "Fuel Surcharge"},
                {"amount": 4.0, "currency": "CAD", "name": "NCVCharge"},
                {"amount": 12.97, "currency": "CAD", "name": "ADDITIONNAL INSURANCE"},
                {
                    "amount": 5.12,
                    "currency": "CAD",
                    "name": "CASH OR CHEQUE ON DELIVERY",
                },
                {"amount": 11.37, "currency": "CAD", "name": "DANGEROUS GOODS"},
                {"amount": 16.35, "currency": "CAD", "name": "DELIVERY BEFORE 10H30"},
                {"amount": 7.58, "currency": "CAD", "name": "FREEZE PROTECTION"},
                {"amount": 2.4, "currency": "CAD", "name": "Oversized parcel - Lenght"},
                {"amount": 8.4, "currency": "CAD", "name": "BEYOND SURCHARGE"},
                {"amount": 4.32, "currency": "CAD", "name": "Class B"},
                {"amount": 6.32, "currency": "CAD", "name": "Class C"},
                {"amount": 12.13, "currency": "CAD", "name": "Class D"},
                {"amount": 20.76, "currency": "CAD", "name": "Class P"},
                {"amount": 0.29, "currency": "CAD", "name": "GST"},
                {"amount": 1.55, "currency": "CAD", "name": "PST"},
            ],
            "service": "nationex_delivery",
            "total_charge": 61.12,
            "transit_days": 2,
        }
    ],
    [],
]


RateRequest = {
    "CustomerId": 113300,
    "ExpeditionDate": "2021-03-31",
    "ShipmentType": "Delivery",
    "SourcePostalCode": "J3Y5T7",
    "DestinationPostalCode": "H2H2S2",
    "TotalWeight": 12.2,
    "TotalParcels": 1,
    "UnitsOfMeasurement": "LI",
    "Accessory": {
        "InsuranceAmount": 100.0,
        "FrozenProtection": True,
        "DangerousGoods": True,
        "SNR": True,
    },
    "Parcels": [
        {
            "NCV": False,
            "Weight": 12.2,
            "Dimensions": {
                "Height": 6.5,
                "Length": 12.0,
                "Width": 8.0,
                "Cubing": 0.36,
            },
        }
    ],
}

RateResponse = """{
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
"""
