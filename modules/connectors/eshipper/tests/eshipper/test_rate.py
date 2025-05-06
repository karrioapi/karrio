import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio.sdk as karrio
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
                f"{gateway.settings.server_url}/api/v2/quote",
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


RatePayload = {
    "shipper": {
        "company_name": "Test Company- From",
        "address_line1": "9, Van Der Graaf Court",
        "city": "Brampton",
        "postal_code": "L4T3T1",
        "country_code": "CA",
        "state_code": "CA-ON",
    },
    "recipient": {
        "company_name": "Test Company - Destination",
        "address_line1": "9, Van Der Graaf Court",
        "city": "Brampton",
        "postal_code": "L4T3T1",
        "country_code": "CA",
        "state_code": "CA-ON",
    },
    "parcels": [
        {
            "length": 15,
            "width": 10,
            "height": 12,
            "weight": 10,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "description": "Package 1 Description",
        },
        {
            "length": 15,
            "width": 10,
            "height": 10,
            "weight": 5,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "description": "Package 2 Description",
        },
    ],
    "options": {
        "shipping_date": "2024-07-16T10:00",
    },
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "eshipper",
            "carrier_name": "eshipper",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 29.82, "currency": "CAD", "name": "baseCharge"},
                {"amount": 3.58, "currency": "CAD", "name": "fuelSurcharge"},
                {"amount": 37.75, "currency": "CAD", "name": "totalChargedAmount"},
                {"amount": 4.34, "currency": "CAD", "name": "HST"},
            ],
            "meta": {
                "eshipper_carrier_id": 2,
                "eshipper_carrier_name": "Purolator",
                "eshipper_service_id": 5000010,
                "eshipper_service_name": "Purolator Ground",
                "rate_provider": "purolator",
                "service_name": "eshipper_purolator_ground",
            },
            "service": "eshipper_purolator_ground",
            "total_charge": 37.75,
            "transit_days": 1,
        },
        {
            "carrier_id": "eshipper",
            "carrier_name": "eshipper",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 30.38, "currency": "CAD", "name": "baseCharge"},
                {"amount": 3.64, "currency": "CAD", "name": "fuelSurcharge"},
                {"amount": 38.44, "currency": "CAD", "name": "totalChargedAmount"},
                {"amount": 4.42, "currency": "CAD", "name": "HST"},
            ],
            "meta": {
                "eshipper_carrier_id": 2,
                "eshipper_carrier_name": "Purolator",
                "eshipper_service_id": 5000001,
                "eshipper_service_name": "Purolator Express",
                "rate_provider": "purolator",
                "service_name": "eshipper_purolator_express",
            },
            "service": "eshipper_purolator_express",
            "total_charge": 38.44,
            "transit_days": 1,
        },
        {
            "carrier_id": "eshipper",
            "carrier_name": "eshipper",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 44.63, "currency": "CAD", "name": "baseCharge"},
                {"amount": 51.7, "currency": "CAD", "name": "totalChargedAmount"},
                {"amount": 1.12, "currency": "CAD", "name": "Carbon Surcharge Fee"},
                {"amount": 5.95, "currency": "CAD", "name": "HST"},
            ],
            "meta": {
                "eshipper_carrier_id": 45,
                "eshipper_carrier_name": "Canpar",
                "eshipper_service_id": 5000128,
                "eshipper_service_name": "Select Parcel",
                "rate_provider": "canpar",
                "service_name": "eshipper_canpar_select_parcel",
            },
            "service": "eshipper_canpar_select_parcel",
            "total_charge": 51.7,
            "transit_days": 1,
        },
        {
            "carrier_id": "eshipper",
            "carrier_name": "eshipper",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 45.09, "currency": "CAD", "name": "baseCharge"},
                {"amount": 52.23, "currency": "CAD", "name": "totalChargedAmount"},
                {"amount": 1.13, "currency": "CAD", "name": "Carbon Surcharge Fee"},
                {"amount": 6.01, "currency": "CAD", "name": "HST"},
            ],
            "meta": {
                "eshipper_carrier_id": 6,
                "eshipper_carrier_name": "Canpar",
                "eshipper_service_id": 5000184,
                "eshipper_service_name": "Ground",
                "rate_provider": "canpar",
                "service_name": "eshipper_ups_ground",
            },
            "service": "eshipper_ups_ground",
            "total_charge": 52.23,
            "transit_days": 1,
        },
        {
            "carrier_id": "eshipper",
            "carrier_name": "eshipper",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 45.14, "currency": "CAD", "name": "baseCharge"},
                {"amount": 52.28, "currency": "CAD", "name": "totalChargedAmount"},
                {"amount": 1.13, "currency": "CAD", "name": "Carbon Surcharge Fee"},
                {"amount": 6.01, "currency": "CAD", "name": "HST"},
            ],
            "meta": {
                "eshipper_carrier_id": 45,
                "eshipper_carrier_name": "Canpar",
                "eshipper_service_id": 5000131,
                "eshipper_service_name": "Express Parcel",
                "rate_provider": "canpar",
                "service_name": "eshipper_canpar_express_parcel",
            },
            "service": "eshipper_canpar_express_parcel",
            "total_charge": 52.28,
            "transit_days": 1,
        },
        {
            "carrier_id": "eshipper",
            "carrier_name": "eshipper",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 46.97, "currency": "CAD", "name": "baseCharge"},
                {"amount": 5.64, "currency": "CAD", "name": "fuelSurcharge"},
                {"amount": 59.45, "currency": "CAD", "name": "totalChargedAmount"},
                {"amount": 6.84, "currency": "CAD", "name": "HST"},
            ],
            "meta": {
                "eshipper_carrier_id": 2,
                "eshipper_carrier_name": "Purolator",
                "eshipper_service_id": 5000003,
                "eshipper_service_name": "Purolator Express 1030",
                "rate_provider": "purolator",
                "service_name": "eshipper_purolator_express_1030",
            },
            "service": "eshipper_purolator_express_1030",
            "total_charge": 59.45,
            "transit_days": 1,
        },
        {
            "carrier_id": "eshipper",
            "carrier_name": "eshipper",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 72.31, "currency": "CAD", "name": "baseCharge"},
                {"amount": 8.68, "currency": "CAD", "name": "fuelSurcharge"},
                {"amount": 91.52, "currency": "CAD", "name": "totalChargedAmount"},
                {"amount": 10.53, "currency": "CAD", "name": "HST"},
            ],
            "meta": {
                "eshipper_carrier_id": 2,
                "eshipper_carrier_name": "Purolator",
                "eshipper_service_id": 5000002,
                "eshipper_service_name": "Purolator Express 9AM",
                "rate_provider": "purolator",
                "service_name": "eshipper_purolator_express_9am",
            },
            "service": "eshipper_purolator_express_9am",
            "total_charge": 91.52,
            "transit_days": 1,
        },
    ],
    [
        {
            "carrier_id": "eshipper",
            "carrier_name": "eshipper",
            "code": "warning",
            "details": {},
            "message": "PYK: More than 1 package is not supported by the carrier",
        },
        {
            "carrier_id": "eshipper",
            "carrier_name": "eshipper",
            "code": "warning",
            "details": {},
            "message": "Canada Post: More than 1 package is not supported by the carrier",
        },
        {
            "carrier_id": "eshipper",
            "carrier_name": "eshipper",
            "code": "warning",
            "details": {},
            "message": "Fleet Optics: More than 1 package is not supported by the carrier",
        },
        {
            "carrier_id": "eshipper",
            "carrier_name": "eshipper",
            "code": "warning",
            "details": {},
            "message": "Skip: Multiple shipments not supported.",
        },
        {
            "carrier_id": "eshipper",
            "carrier_name": "eshipper",
            "code": "warning",
            "details": {},
            "message": "SmartePost INTL: More than 1 package is not supported by the carrier",
        },
        {
            "carrier_id": "eshipper",
            "carrier_name": "eshipper",
            "code": "warning",
            "details": {},
            "message": "USPS: Destination country not serviced by the carrier.",
        },
        {
            "carrier_id": "eshipper",
            "carrier_name": "eshipper",
            "code": "warning",
            "details": {},
            "message": "FlashBird: No carrier settings for company [8000180], carrier [FlashBird]with id [8000010], origin country [CA], destination country [CA] and account number [null].",
        },
        {
            "carrier_id": "eshipper",
            "carrier_name": "eshipper",
            "code": "warning",
            "details": {},
            "message": "UPS: 250002: Invalid Authentication Information.. ",
        },
        {
            "carrier_id": "eshipper",
            "carrier_name": "eshipper",
            "code": "warning",
            "details": {},
            "message": "Federal Express: NOT.FOUND.ERROR: The resource you requested is no longer available. Please modify your request and try again.",
        },
    ],
]

RateRequest = {
    "from": {
        "attention": "Test Company- From",
        "company": "Test Company- From",
        "address1": "9, Van Der Graaf Court",
        "city": "Brampton",
        "province": "CA-ON",
        "country": "CA",
        "zip": "L4T3T1",
    },
    "to": {
        "attention": "Test Company - Destination",
        "company": "Test Company - Destination",
        "address1": "9, Van Der Graaf Court",
        "city": "Brampton",
        "province": "CA-ON",
        "zip": "L4T3T1",
        "country": "CA",
    },
    "scheduledShipDate": "2024-07-16 10:00",
    "packagingUnit": "Metric",
    "packages": {
        "type": "Package",
        "packages": [
            {
                "length": 15,
                "width": 10,
                "height": 12,
                "weight": 10,
                "description": "Package 1 Description",
                "dimensionUnit": "CM",
                "weightUnit": "KG",
            },
            {
                "length": 15,
                "width": 10,
                "height": 10,
                "weight": 5,
                "description": "Package 2 Description",
                "dimensionUnit": "CM",
                "weightUnit": "KG",
            },
        ],
    },
}

RateResponse = """{
  "uuid": "1c18cf1d-565e-4d54-8499-de05cc79e981",
  "quotes": [
    {
      "carrierName": "Purolator",
      "serviceId": 5000010,
      "serviceName": "Purolator Ground",
      "modeTransport": "GROUND",
      "transitDays": "1",
      "baseCharge": 29.82,
      "fuelSurcharge": 3.58,
      "fuelSurchargePercentage": 12.02,
      "surcharges": null,
      "totalCharge": 37.75,
      "taxes": [
        {
          "name": "HST",
          "amount": 4.34
        }
      ],
      "totalChargedAmount": 37.75,
      "currency": "CAD"
    },
    {
      "carrierName": "Purolator",
      "serviceId": 5000001,
      "serviceName": "Purolator Express",
      "modeTransport": "AIR",
      "transitDays": "1",
      "baseCharge": 30.38,
      "fuelSurcharge": 3.64,
      "fuelSurchargePercentage": 11.98,
      "surcharges": null,
      "totalCharge": 38.44,
      "taxes": [
        {
          "name": "HST",
          "amount": 4.42
        }
      ],
      "totalChargedAmount": 38.44,
      "currency": "CAD"
    },
    {
      "carrierName": "Canpar",
      "serviceId": 5000128,
      "serviceName": "Select Parcel",
      "modeTransport": "GROUND",
      "transitDays": "1",
      "baseCharge": 44.63,
      "fuelSurcharge": 0.0,
      "fuelSurchargePercentage": 0.0,
      "surcharges": [
        {
          "name": "Carbon Surcharge Fee",
          "amount": 1.12
        }
      ],
      "totalCharge": 51.7,
      "taxes": [
        {
          "name": "HST",
          "amount": 5.95
        }
      ],
      "totalChargedAmount": 51.7,
      "currency": "CAD"
    },
    {
      "carrierName": "Canpar",
      "serviceId": 5000184,
      "serviceName": "Ground",
      "modeTransport": "GROUND",
      "transitDays": "1",
      "baseCharge": 45.09,
      "fuelSurcharge": 0.0,
      "fuelSurchargePercentage": 0.0,
      "surcharges": [
        {
          "name": "Carbon Surcharge Fee",
          "amount": 1.13
        }
      ],
      "totalCharge": 52.23,
      "taxes": [
        {
          "name": "HST",
          "amount": 6.01
        }
      ],
      "totalChargedAmount": 52.23,
      "currency": "CAD"
    },
    {
      "carrierName": "Canpar",
      "serviceId": 5000131,
      "serviceName": "Express Parcel",
      "modeTransport": "GROUND",
      "transitDays": "1",
      "baseCharge": 45.14,
      "fuelSurcharge": 0.0,
      "fuelSurchargePercentage": 0.0,
      "surcharges": [
        {
          "name": "Carbon Surcharge Fee",
          "amount": 1.13
        }
      ],
      "totalCharge": 52.28,
      "taxes": [
        {
          "name": "HST",
          "amount": 6.01
        }
      ],
      "totalChargedAmount": 52.28,
      "currency": "CAD"
    },
    {
      "carrierName": "Purolator",
      "serviceId": 5000003,
      "serviceName": "Purolator Express 1030",
      "modeTransport": "AIR",
      "transitDays": "1",
      "baseCharge": 46.97,
      "fuelSurcharge": 5.64,
      "fuelSurchargePercentage": 12.01,
      "surcharges": null,
      "totalCharge": 59.45,
      "taxes": [
        {
          "name": "HST",
          "amount": 6.84
        }
      ],
      "totalChargedAmount": 59.45,
      "currency": "CAD"
    },
    {
      "carrierName": "Purolator",
      "serviceId": 5000002,
      "serviceName": "Purolator Express 9AM",
      "modeTransport": "AIR",
      "transitDays": "1",
      "baseCharge": 72.31,
      "fuelSurcharge": 8.68,
      "fuelSurchargePercentage": 12.0,
      "surcharges": null,
      "totalCharge": 91.52,
      "taxes": [
        {
          "name": "HST",
          "amount": 10.53
        }
      ],
      "totalChargedAmount": 91.52,
      "currency": "CAD"
    }
  ],
  "warnings": [
    "PYK: More than 1 package is not supported by the carrier",
    "Canada Post: More than 1 package is not supported by the carrier",
    "Fleet Optics: More than 1 package is not supported by the carrier",
    "Skip: Multiple shipments not supported.",
    "SmartePost INTL: More than 1 package is not supported by the carrier",
    "USPS: Destination country not serviced by the carrier.",
    "FlashBird: No carrier settings for company [8000180], carrier [FlashBird]with id [8000010], origin country [CA], destination country [CA] and account number [null].",
    "UPS: 250002: Invalid Authentication Information.. ",
    "Federal Express: NOT.FOUND.ERROR: The resource you requested is no longer available. Please modify your request and try again."
  ]
}
"""
