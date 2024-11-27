import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
from tests import logger

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestUSPSRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        logger.debug(request.serialize())
        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.usps_international.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/international-prices/v3/total-rates/search",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.usps_international.proxy.lib.request") as mock:
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
        "company_name": "Coffee Five",
        "address_line1": "R. da Quitanda, 86 - quiosque 01",
        "city": "Centro",
        "postal_code": "29440",
        "country_code": "BR",
        "person_name": "John",
        "phone_number": "8005554526",
        "state_code": "Rio de Janeiro",
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
        "shipment_date": "2024-07-28",
        "usps_price_type": "RETAIL",
        "usps_label_delivery_service": True,
        "usps_return_receipt": True,
    },
    "services": ["usps_parcel_select"],
    "reference": "REF-001",
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 74.92,
                    "currency": "USD",
                    "name": "Priority Mail Machinable Dimensional " "Rectangular",
                }
            ],
            "meta": {
                "service_name": "PRIORITY_MAIL",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "DR",
                "usps_zone": "08",
            },
            "service": "PRIORITY_MAIL",
            "total_charge": 104.92,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 74.92,
                    "currency": "USD",
                    "name": "Priority Mail Machinable Dimensional " "Rectangular",
                }
            ],
            "meta": {
                "service_name": "PRIORITY_MAIL",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "DN",
                "usps_zone": "08",
            },
            "service": "PRIORITY_MAIL",
            "total_charge": 104.92,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 181.9,
                    "currency": "USD",
                    "name": "Priority Mail Express Machinable Dimensional "
                    "Rectangular",
                }
            ],
            "meta": {
                "service_name": "PRIORITY_MAIL_EXPRESS",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "DR",
                "usps_zone": "08",
            },
            "service": "PRIORITY_MAIL_EXPRESS",
            "total_charge": 211.9,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 181.9,
                    "currency": "USD",
                    "name": "Priority Mail Express Machinable Dimensional "
                    "Rectangular",
                }
            ],
            "meta": {
                "service_name": "PRIORITY_MAIL_EXPRESS",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "DN",
                "usps_zone": "08",
            },
            "service": "PRIORITY_MAIL_EXPRESS",
            "total_charge": 211.9,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 42.62,
                    "currency": "USD",
                    "name": "USPS Ground Advantage Machinable Dimensional "
                    "Rectangular",
                }
            ],
            "meta": {
                "service_name": "USPS_GROUND_ADVANTAGE",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "DR",
                "usps_zone": "08",
            },
            "service": "USPS_GROUND_ADVANTAGE",
            "total_charge": 60.62,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 42.62,
                    "currency": "USD",
                    "name": "USPS Ground Advantage Machinable Dimensional "
                    "Rectangular",
                }
            ],
            "meta": {
                "service_name": "USPS_GROUND_ADVANTAGE",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "DN",
                "usps_zone": "08",
            },
            "service": "USPS_GROUND_ADVANTAGE",
            "total_charge": 60.62,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 5.21,
                    "currency": "USD",
                    "name": "Parcel Select Machinable DDU Single-piece",
                }
            ],
            "meta": {
                "service_name": "PARCEL_SELECT",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "SP",
                "usps_zone": "08",
            },
            "service": "PARCEL_SELECT",
            "total_charge": 23.21,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 5.21,
                    "currency": "USD",
                    "name": "Parcel Select Machinable DDU Single-piece",
                }
            ],
            "meta": {
                "service_name": "PARCEL_SELECT",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "DR",
                "usps_zone": "08",
            },
            "service": "PARCEL_SELECT",
            "total_charge": 23.21,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 5.21,
                    "currency": "USD",
                    "name": "Parcel Select Machinable DDU Single-piece",
                }
            ],
            "meta": {
                "service_name": "PARCEL_SELECT",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "DN",
                "usps_zone": "08",
            },
            "service": "PARCEL_SELECT",
            "total_charge": 23.21,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 5.21,
                    "currency": "USD",
                    "name": "Parcel Select Machinable DDU Single-piece",
                }
            ],
            "meta": {
                "service_name": "PARCEL_SELECT",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "SP",
                "usps_zone": "08",
            },
            "service": "PARCEL_SELECT",
            "total_charge": 23.21,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 5.21,
                    "currency": "USD",
                    "name": "Parcel Select Machinable DDU Single-piece",
                }
            ],
            "meta": {
                "service_name": "PARCEL_SELECT",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "DR",
                "usps_zone": "08",
            },
            "service": "PARCEL_SELECT",
            "total_charge": 23.21,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 5.21,
                    "currency": "USD",
                    "name": "Parcel Select Machinable DDU Single-piece",
                }
            ],
            "meta": {
                "service_name": "PARCEL_SELECT",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "DN",
                "usps_zone": "08",
            },
            "service": "PARCEL_SELECT",
            "total_charge": 23.21,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 5.21,
                    "currency": "USD",
                    "name": "Parcel Select Machinable DDU Single-piece",
                }
            ],
            "meta": {
                "service_name": "PARCEL_SELECT",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "DE",
                "usps_zone": "08",
            },
            "service": "PARCEL_SELECT",
            "total_charge": 23.21,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 5.21,
                    "currency": "USD",
                    "name": "Parcel Select Machinable DDU Single-piece",
                }
            ],
            "meta": {
                "service_name": "PARCEL_SELECT",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "SR",
                "usps_zone": "08",
            },
            "service": "PARCEL_SELECT",
            "total_charge": 23.21,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 5.21,
                    "currency": "USD",
                    "name": "Parcel Select Machinable DDU Single-piece",
                }
            ],
            "meta": {
                "service_name": "PARCEL_SELECT",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "SN",
                "usps_zone": "08",
            },
            "service": "PARCEL_SELECT",
            "total_charge": 23.21,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 5.21,
                    "currency": "USD",
                    "name": "Parcel Select Machinable DDU Single-piece",
                }
            ],
            "meta": {
                "service_name": "PARCEL_SELECT",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "SP",
                "usps_zone": "08",
            },
            "service": "PARCEL_SELECT",
            "total_charge": 23.21,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 5.21,
                    "currency": "USD",
                    "name": "Parcel Select Machinable DDU Single-piece",
                }
            ],
            "meta": {
                "service_name": "PARCEL_SELECT",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "DR",
                "usps_zone": "08",
            },
            "service": "PARCEL_SELECT",
            "total_charge": 23.21,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 5.21,
                    "currency": "USD",
                    "name": "Parcel Select Machinable DDU Single-piece",
                }
            ],
            "meta": {
                "service_name": "PARCEL_SELECT",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "DN",
                "usps_zone": "08",
            },
            "service": "PARCEL_SELECT",
            "total_charge": 23.21,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 4.15,
                    "currency": "USD",
                    "name": "Connect Local Machinable DDU Small Flat Rate " "Bag",
                }
            ],
            "meta": {
                "service_name": "USPS_CONNECT_LOCAL",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "LS",
                "usps_zone": "08",
            },
            "service": "USPS_CONNECT_LOCAL",
            "total_charge": 4.15,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 4.15,
                    "currency": "USD",
                    "name": "Connect Local Machinable DDU Small Flat Rate " "Bag",
                }
            ],
            "meta": {
                "service_name": "USPS_CONNECT_LOCAL",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "LL",
                "usps_zone": "08",
            },
            "service": "USPS_CONNECT_LOCAL",
            "total_charge": 4.15,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 4.15,
                    "currency": "USD",
                    "name": "Connect Local Machinable DDU Small Flat Rate " "Bag",
                }
            ],
            "meta": {
                "service_name": "USPS_CONNECT_LOCAL",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "LF",
                "usps_zone": "08",
            },
            "service": "USPS_CONNECT_LOCAL",
            "total_charge": 4.15,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 4.15,
                    "currency": "USD",
                    "name": "Connect Local Machinable DDU Small Flat Rate " "Bag",
                }
            ],
            "meta": {
                "service_name": "USPS_CONNECT_LOCAL",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "LC",
                "usps_zone": "08",
            },
            "service": "USPS_CONNECT_LOCAL",
            "total_charge": 4.15,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 2.22,
                    "currency": "USD",
                    "name": "Bound Printed Matter Machinable DNDC " "Presorted",
                }
            ],
            "meta": {
                "service_name": "BOUND_PRINTED_MATTER",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "PR",
                "usps_zone": "08",
            },
            "service": "BOUND_PRINTED_MATTER",
            "total_charge": 2.38,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 2.22,
                    "currency": "USD",
                    "name": "Bound Printed Matter Machinable DNDC " "Presorted",
                }
            ],
            "meta": {
                "service_name": "BOUND_PRINTED_MATTER",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "PR",
                "usps_zone": "08",
            },
            "service": "BOUND_PRINTED_MATTER",
            "total_charge": 2.38,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 2.22,
                    "currency": "USD",
                    "name": "Bound Printed Matter Machinable DNDC " "Presorted",
                }
            ],
            "meta": {
                "service_name": "BOUND_PRINTED_MATTER",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "PR",
                "usps_zone": "08",
            },
            "service": "BOUND_PRINTED_MATTER",
            "total_charge": 2.38,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 2.22,
                    "currency": "USD",
                    "name": "Bound Printed Matter Machinable DNDC " "Presorted",
                }
            ],
            "meta": {
                "service_name": "BOUND_PRINTED_MATTER",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "PR",
                "usps_zone": "08",
            },
            "service": "BOUND_PRINTED_MATTER",
            "total_charge": 2.38,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 2.22,
                    "currency": "USD",
                    "name": "Bound Printed Matter Machinable DNDC " "Presorted",
                }
            ],
            "meta": {
                "service_name": "BOUND_PRINTED_MATTER",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "IRREGULAR",
                "usps_rate_indicator": "PR",
                "usps_zone": "08",
            },
            "service": "BOUND_PRINTED_MATTER",
            "total_charge": 2.38,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 2.22,
                    "currency": "USD",
                    "name": "Bound Printed Matter Machinable DNDC " "Presorted",
                }
            ],
            "meta": {
                "service_name": "BOUND_PRINTED_MATTER",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "IRREGULAR",
                "usps_rate_indicator": "PR",
                "usps_zone": "08",
            },
            "service": "BOUND_PRINTED_MATTER",
            "total_charge": 2.38,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 2.22,
                    "currency": "USD",
                    "name": "Bound Printed Matter Machinable DNDC " "Presorted",
                }
            ],
            "meta": {
                "service_name": "BOUND_PRINTED_MATTER",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "IRREGULAR",
                "usps_rate_indicator": "PR",
                "usps_zone": "08",
            },
            "service": "BOUND_PRINTED_MATTER",
            "total_charge": 2.38,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 2.22,
                    "currency": "USD",
                    "name": "Bound Printed Matter Machinable DNDC " "Presorted",
                }
            ],
            "meta": {
                "service_name": "BOUND_PRINTED_MATTER",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "IRREGULAR",
                "usps_rate_indicator": "PR",
                "usps_zone": "08",
            },
            "service": "BOUND_PRINTED_MATTER",
            "total_charge": 2.38,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 5.6,
                    "currency": "USD",
                    "name": "Library Mail Machinable Basic",
                }
            ],
            "meta": {
                "service_name": "LIBRARY_MAIL",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "BA",
                "usps_zone": "08",
            },
            "service": "LIBRARY_MAIL",
            "total_charge": 5.6,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 5.6,
                    "currency": "USD",
                    "name": "Library Mail Machinable Basic",
                }
            ],
            "meta": {
                "service_name": "LIBRARY_MAIL",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "5D",
                "usps_zone": "08",
            },
            "service": "LIBRARY_MAIL",
            "total_charge": 5.6,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 5.6,
                    "currency": "USD",
                    "name": "Library Mail Machinable Basic",
                }
            ],
            "meta": {
                "service_name": "LIBRARY_MAIL",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "IRREGULAR",
                "usps_rate_indicator": "BA",
                "usps_zone": "08",
            },
            "service": "LIBRARY_MAIL",
            "total_charge": 5.6,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 5.6,
                    "currency": "USD",
                    "name": "Library Mail Machinable Basic",
                }
            ],
            "meta": {
                "service_name": "LIBRARY_MAIL",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "IRREGULAR",
                "usps_rate_indicator": "5D",
                "usps_zone": "08",
            },
            "service": "LIBRARY_MAIL",
            "total_charge": 5.6,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 5.9,
                    "currency": "USD",
                    "name": "Media Mail Machinable Basic",
                }
            ],
            "meta": {
                "service_name": "MEDIA_MAIL",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "BA",
                "usps_zone": "08",
            },
            "service": "MEDIA_MAIL",
            "total_charge": 5.9,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 5.9,
                    "currency": "USD",
                    "name": "Media Mail Machinable Basic",
                }
            ],
            "meta": {
                "service_name": "MEDIA_MAIL",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "5D",
                "usps_zone": "08",
            },
            "service": "MEDIA_MAIL",
            "total_charge": 5.9,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 5.9,
                    "currency": "USD",
                    "name": "Media Mail Machinable Basic",
                }
            ],
            "meta": {
                "service_name": "MEDIA_MAIL",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "IRREGULAR",
                "usps_rate_indicator": "BA",
                "usps_zone": "08",
            },
            "service": "MEDIA_MAIL",
            "total_charge": 5.9,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 5.9,
                    "currency": "USD",
                    "name": "Media Mail Machinable Basic",
                }
            ],
            "meta": {
                "service_name": "MEDIA_MAIL",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "IRREGULAR",
                "usps_rate_indicator": "5D",
                "usps_zone": "08",
            },
            "service": "MEDIA_MAIL",
            "total_charge": 5.9,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 7.56,
                    "currency": "USD",
                    "name": "Parcel Select Machinable DNDC Single-piece",
                }
            ],
            "meta": {
                "service_name": "USPS_CONNECT_REGIONAL",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "SP",
                "usps_zone": "08",
            },
            "service": "USPS_CONNECT_REGIONAL",
            "total_charge": 25.56,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 7.56,
                    "currency": "USD",
                    "name": "Parcel Select Machinable DNDC Single-piece",
                }
            ],
            "meta": {
                "service_name": "USPS_CONNECT_REGIONAL",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "DR",
                "usps_zone": "08",
            },
            "service": "USPS_CONNECT_REGIONAL",
            "total_charge": 25.56,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 7.56,
                    "currency": "USD",
                    "name": "Parcel Select Machinable DNDC Single-piece",
                }
            ],
            "meta": {
                "service_name": "USPS_CONNECT_REGIONAL",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "DN",
                "usps_zone": "08",
            },
            "service": "USPS_CONNECT_REGIONAL",
            "total_charge": 25.56,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 7.56,
                    "currency": "USD",
                    "name": "Parcel Select Machinable DNDC Single-piece",
                }
            ],
            "meta": {
                "service_name": "USPS_CONNECT_REGIONAL",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "DE",
                "usps_zone": "08",
            },
            "service": "USPS_CONNECT_REGIONAL",
            "total_charge": 25.56,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 7.56,
                    "currency": "USD",
                    "name": "Parcel Select Machinable DNDC Single-piece",
                }
            ],
            "meta": {
                "service_name": "USPS_CONNECT_REGIONAL",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "SR",
                "usps_zone": "08",
            },
            "service": "USPS_CONNECT_REGIONAL",
            "total_charge": 25.56,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 7.56,
                    "currency": "USD",
                    "name": "Parcel Select Machinable DNDC Single-piece",
                }
            ],
            "meta": {
                "service_name": "USPS_CONNECT_REGIONAL",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "SN",
                "usps_zone": "08",
            },
            "service": "USPS_CONNECT_REGIONAL",
            "total_charge": 25.56,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 7.56,
                    "currency": "USD",
                    "name": "Parcel Select Machinable DNDC Single-piece",
                }
            ],
            "meta": {
                "service_name": "USPS_CONNECT_REGIONAL",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "SP",
                "usps_zone": "08",
            },
            "service": "USPS_CONNECT_REGIONAL",
            "total_charge": 25.56,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 7.56,
                    "currency": "USD",
                    "name": "Parcel Select Machinable DNDC Single-piece",
                }
            ],
            "meta": {
                "service_name": "USPS_CONNECT_REGIONAL",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "DR",
                "usps_zone": "08",
            },
            "service": "USPS_CONNECT_REGIONAL",
            "total_charge": 25.56,
        },
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {
                    "amount": 7.56,
                    "currency": "USD",
                    "name": "Parcel Select Machinable DNDC Single-piece",
                }
            ],
            "meta": {
                "service_name": "USPS_CONNECT_REGIONAL",
                "usps_price_type": "COMMERCIAL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "DN",
                "usps_zone": "08",
            },
            "service": "USPS_CONNECT_REGIONAL",
            "total_charge": 25.56,
        },
    ],
    [],
]


RateRequest = [
    {
        "accountNumber": "Your Account Number",
        "accountType": "EPS",
        "destinationCountryCode": "BR",
        "extraServices": [955],
        "foreignPostalCode": "29440",
        "height": 19.69,
        "itemValue": 0.0,
        "length": 19.69,
        "mailClass": "ALL",
        "mailingDate": "2024-07-28",
        "originZIPCode": "29440",
        "priceType": "RETAIL",
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
    },
    {
      "totalBasePrice": 154.2,
      "rates": [
        {
          "description": "Priority Mail Express Machinable Dimensional Nonrectangular",
          "priceType": "COMMERCIAL",
          "price": 154.2,
          "weight": 2.21,
          "dimWeight": 17.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "PRIORITY_MAIL_EXPRESS",
          "zone": "08",
          "productName": "Priority Mail Express",
          "productDefinition": "1-2 day specific guaranteed delivery by 6:00pm local delivery time",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "DN",
          "destinationEntryFacilityType": "NONE",
          "SKU": "DEXR0XXXXC08170"
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
    },
    {
      "totalBasePrice": 60.62,
      "rates": [
        {
          "description": "USPS Ground Advantage Machinable Dimensional Rectangular",
          "priceType": "COMMERCIAL",
          "price": 42.62,
          "weight": 2.21,
          "dimWeight": 22.0,
          "fees": [
            {
              "name": "Nonstandard Volume > 2 cu ft",
              "SKU": "D813XUXXXXX0000",
              "price": 18.0
            }
          ],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "USPS_GROUND_ADVANTAGE",
          "zone": "08",
          "productName": "USPS Ground Advantage",
          "productDefinition": "2-5 day specific delivery, perfect for packages weighing 1 ounce up to 70 lbs",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "DR",
          "destinationEntryFacilityType": "NONE",
          "SKU": "DUXR0XXXXC08220"
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
          "SKU": "D2KUYOXPXC00000"
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
          "SKU": "D2KU1OXPXC00000"
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
          "SKU": "D2KU3OXPXC00000"
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
          "SKU": "D2KU5OXPXC00000"
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
          "SKU": "D2KU7OXPXC00000"
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
          "SKU": "D2KUZOXPXC00000"
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
          "SKU": "D2KU3OSPXC00000"
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
          "SKU": "D2KU5OSPXC00000"
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
          "SKU": "D2KU7OSPXC00000"
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
          "SKU": "D2KUZOSPXC00000"
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
          "SKU": "DXTU0EXXXCX0000"
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
          "SKU": "DXSU0EXPXCX0000"
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
          "SKU": "DXSU0EJPXCX0000"
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
      "totalBasePrice": 28.72,
      "rates": [
        {
          "description": "USPS Ground Advantage Machinable Dimensional Nonrectangular",
          "priceType": "COMMERCIAL",
          "price": 28.72,
          "weight": 2.21,
          "dimWeight": 17.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "USPS_GROUND_ADVANTAGE",
          "zone": "08",
          "productName": "USPS Ground Advantage",
          "productDefinition": "2-5 day specific delivery, perfect for packages weighing 1 ounce up to 70 lbs",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "DN",
          "destinationEntryFacilityType": "NONE",
          "SKU": "DUXR0XXXXC08170"
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
          "SKU": "D2KUYOXPXC00000"
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
          "SKU": "D2KU1OXPXC00000"
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
          "SKU": "D2KU3OXPXC00000"
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
          "SKU": "D2KU5OXPXC00000"
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
          "SKU": "D2KU7OXPXC00000"
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
          "SKU": "D2KUZOXPXC00000"
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
          "SKU": "D2KU3OSPXC00000"
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
          "SKU": "D2KU5OSPXC00000"
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
          "SKU": "D2KU7OSPXC00000"
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
          "SKU": "D2KUZOSPXC00000"
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
          "SKU": "DXTU0EXXXCX0000"
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
          "SKU": "DXSU0EXPXCX0000"
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
          "SKU": "DXSU0EJPXCX0000"
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
      "totalBasePrice": 23.21,
      "rates": [
        {
          "description": "Parcel Select Machinable DDU Single-piece",
          "priceType": "COMMERCIAL",
          "price": 5.21,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [
            {
              "name": "Nonstandard Volume > 2 cu ft",
              "SKU": "D813XVUXXXX0000",
              "price": 18.0
            }
          ],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "PARCEL_SELECT",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "SP",
          "destinationEntryFacilityType": "DESTINATION_DELIVERY_UNIT",
          "SKU": "DVXP0XXUXC00030"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
      "totalBasePrice": 23.21,
      "rates": [
        {
          "description": "Parcel Select Machinable DDU Dimensional Rectangular",
          "priceType": "COMMERCIAL",
          "price": 5.21,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [
            {
              "name": "Nonstandard Volume > 2 cu ft",
              "SKU": "D813XVUXXXX0000",
              "price": 18.0
            }
          ],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "PARCEL_SELECT",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "DR",
          "destinationEntryFacilityType": "DESTINATION_DELIVERY_UNIT",
          "SKU": "DVXR0XXUXC00030"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
      "totalBasePrice": 5.21,
      "rates": [
        {
          "description": "Parcel Select Machinable DDU Dimensional Nonrectangular",
          "priceType": "COMMERCIAL",
          "price": 5.21,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "PARCEL_SELECT",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "DN",
          "destinationEntryFacilityType": "DESTINATION_DELIVERY_UNIT",
          "SKU": "DVXR0XXUXC00030"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
      "totalBasePrice": 25.56,
      "rates": [
        {
          "description": "Parcel Select Machinable DNDC Single-piece",
          "priceType": "COMMERCIAL",
          "price": 7.56,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [
            {
              "name": "Nonstandard Volume > 2 cu ft",
              "SKU": "D813XVCXXXX0000",
              "price": 18.0
            }
          ],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "PARCEL_SELECT",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "SP",
          "destinationEntryFacilityType": "DESTINATION_NETWORK_DISTRIBUTION_CENTER",
          "SKU": "DVXP0XXCXC00030"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
      "totalBasePrice": 25.56,
      "rates": [
        {
          "description": "Parcel Select Machinable DNDC Dimensional Rectangular",
          "priceType": "COMMERCIAL",
          "price": 7.56,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [
            {
              "name": "Nonstandard Volume > 2 cu ft",
              "SKU": "D813XVCXXXX0000",
              "price": 18.0
            }
          ],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "PARCEL_SELECT",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "DR",
          "destinationEntryFacilityType": "DESTINATION_NETWORK_DISTRIBUTION_CENTER",
          "SKU": "DVXR0XXCXC00030"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
      "totalBasePrice": 7.56,
      "rates": [
        {
          "description": "Parcel Select Machinable DNDC Dimensional Nonrectangular",
          "priceType": "COMMERCIAL",
          "price": 7.56,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "PARCEL_SELECT",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "DN",
          "destinationEntryFacilityType": "DESTINATION_NETWORK_DISTRIBUTION_CENTER",
          "SKU": "DVXR0XXCXC00030"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
      "totalBasePrice": 23.7,
      "rates": [
        {
          "description": "Parcel Select Machinable DSCF SCF",
          "priceType": "COMMERCIAL",
          "price": 5.7,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [
            {
              "name": "Nonstandard Volume > 2 cu ft",
              "SKU": "D813XVFTXXX0000",
              "price": 18.0
            }
          ],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "PARCEL_SELECT",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "DE",
          "destinationEntryFacilityType": "DESTINATION_SECTIONAL_CENTER_FACILITY",
          "SKU": "DVXP0XXFXC00030"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
      "totalBasePrice": 23.7,
      "rates": [
        {
          "description": "Parcel Select Machinable DSCF SCF Dimensional Rectangular",
          "priceType": "COMMERCIAL",
          "price": 5.7,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [
            {
              "name": "Nonstandard Volume > 2 cu ft",
              "SKU": "D813XVFTXXX0000",
              "price": 18.0
            }
          ],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "PARCEL_SELECT",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "SR",
          "destinationEntryFacilityType": "DESTINATION_SECTIONAL_CENTER_FACILITY",
          "SKU": "DVXR0XXFXC00030"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
      "totalBasePrice": 5.7,
      "rates": [
        {
          "description": "Parcel Select Machinable DSCF SCF Dimensional Nonrectangular",
          "priceType": "COMMERCIAL",
          "price": 5.7,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "PARCEL_SELECT",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "SN",
          "destinationEntryFacilityType": "DESTINATION_SECTIONAL_CENTER_FACILITY",
          "SKU": "DVXR0XXFXC00030"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
      "totalBasePrice": 23.7,
      "rates": [
        {
          "description": "Parcel Select Machinable DHUB Single-piece",
          "priceType": "COMMERCIAL",
          "price": 5.7,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [
            {
              "name": "Nonstandard Volume > 2 cu ft",
              "SKU": "D813XVHXXXX0000",
              "price": 18.0
            }
          ],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "PARCEL_SELECT",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "SP",
          "destinationEntryFacilityType": "DESTINATION_SERVICE_HUB",
          "SKU": "DVXP0XXBXC00030"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
      "totalBasePrice": 23.7,
      "rates": [
        {
          "description": "Parcel Select Machinable DHUB Dimensional Rectangular",
          "priceType": "COMMERCIAL",
          "price": 5.7,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [
            {
              "name": "Nonstandard Volume > 2 cu ft",
              "SKU": "D813XVHXXXX0000",
              "price": 18.0
            }
          ],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "PARCEL_SELECT",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "DR",
          "destinationEntryFacilityType": "DESTINATION_SERVICE_HUB",
          "SKU": "DVXR0XXBXC00030"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
      "totalBasePrice": 5.7,
      "rates": [
        {
          "description": "Parcel Select Machinable DHUB Dimensional Nonrectangular",
          "priceType": "COMMERCIAL",
          "price": 5.7,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "PARCEL_SELECT",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "DN",
          "destinationEntryFacilityType": "DESTINATION_SERVICE_HUB",
          "SKU": "DVXR0XXBXC00030"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
      "totalBasePrice": 4.15,
      "rates": [
        {
          "description": "Connect Local Machinable DDU Small Flat Rate Bag",
          "priceType": "COMMERCIAL",
          "price": 4.15,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "USPS_CONNECT_LOCAL",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "LS",
          "destinationEntryFacilityType": "DESTINATION_DELIVERY_UNIT",
          "SKU": "DVOA0XXXXC00250"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
      "totalBasePrice": 4.95,
      "rates": [
        {
          "description": "Connect Local Machinable DDU Large Flat Rate Bag",
          "priceType": "COMMERCIAL",
          "price": 4.95,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "USPS_CONNECT_LOCAL",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "LL",
          "destinationEntryFacilityType": "DESTINATION_DELIVERY_UNIT",
          "SKU": "DVOA1XXXXC00250"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
      "totalBasePrice": 4.95,
      "rates": [
        {
          "description": "Connect Local Machinable DDU Flat Rate Box",
          "priceType": "COMMERCIAL",
          "price": 4.95,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "USPS_CONNECT_LOCAL",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "LF",
          "destinationEntryFacilityType": "DESTINATION_DELIVERY_UNIT",
          "SKU": "DVOB0XXXXC00250"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
      "totalBasePrice": 23.21,
      "rates": [
        {
          "description": "Connect Local Machinable DDU ",
          "priceType": "COMMERCIAL",
          "price": 5.21,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [
            {
              "name": "Nonstandard Volume > 2 cu ft",
              "SKU": "D813XVUXXXX0000",
              "price": 18.0
            }
          ],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "USPS_CONNECT_LOCAL",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "LC",
          "destinationEntryFacilityType": "DESTINATION_DELIVERY_UNIT",
          "SKU": "DVGXXXXUXC00030"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
      "totalBasePrice": 2.38,
      "rates": [
        {
          "description": "Bound Printed Matter Machinable DNDC Presorted",
          "priceType": "COMMERCIAL",
          "price": 2.08,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "BOUND_PRINTED_MATTER",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "PR",
          "destinationEntryFacilityType": "DESTINATION_NETWORK_DISTRIBUTION_CENTER",
          "SKU": "DBPP0XXCXC00150"
        },
        {
          "description": "Bound Printed Matter Machinable DNDC Presorted",
          "priceType": "COMMERCIAL",
          "price": 0.135,
          "weight": 2.21,
          "dimWeight": 0.0,
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "BOUND_PRINTED_MATTER",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "PR",
          "destinationEntryFacilityType": "DESTINATION_NETWORK_DISTRIBUTION_CENTER",
          "SKU": "DBPP0XXCXD00150"
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
          "SKU": "D2KBYOXXXC00000"
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
          "SKU": "D2KB1OXXXC00000"
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
          "SKU": "D2KB3OXXXC00000"
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
          "SKU": "D2KB5OXXXC00000"
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
          "SKU": "D2KB7OXXXC00000"
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
          "SKU": "D2KBZOXXXC00000"
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
          "SKU": "D2KB3OSXXC00000"
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
          "SKU": "D2KB5OSXXC00000"
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
          "SKU": "D2KB7OSXXC00000"
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
          "SKU": "D2KBZOSXXC00000"
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
          "SKU": "DXTB0EXXXCX0000"
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
          "SKU": "DXSB0EXXXCX0000"
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
          "SKU": "DXSB0EJXXCX0000"
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
      "totalBasePrice": 1.17,
      "rates": [
        {
          "description": "Bound Printed Matter Machinable DDU Presorted",
          "priceType": "COMMERCIAL",
          "price": 1.01,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "BOUND_PRINTED_MATTER",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "PR",
          "destinationEntryFacilityType": "DESTINATION_DELIVERY_UNIT",
          "SKU": "DBPP0XXUXC00150"
        },
        {
          "description": "Bound Printed Matter Machinable DDU Presorted",
          "priceType": "COMMERCIAL",
          "price": 0.072,
          "weight": 2.21,
          "dimWeight": 0.0,
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "BOUND_PRINTED_MATTER",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "PR",
          "destinationEntryFacilityType": "DESTINATION_DELIVERY_UNIT",
          "SKU": "DBPP0XXUXD00150"
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
          "SKU": "D2KBYOXXXC00000"
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
          "SKU": "D2KB1OXXXC00000"
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
          "SKU": "D2KB3OXXXC00000"
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
          "SKU": "D2KB5OXXXC00000"
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
          "SKU": "D2KB7OXXXC00000"
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
          "SKU": "D2KBZOXXXC00000"
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
          "SKU": "D2KB3OSXXC00000"
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
          "SKU": "D2KB5OSXXC00000"
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
          "SKU": "D2KB7OSXXC00000"
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
          "SKU": "D2KBZOSXXC00000"
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
          "SKU": "DXTB0EXXXCX0000"
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
          "SKU": "DXSB0EXXXCX0000"
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
          "SKU": "DXSB0EJXXCX0000"
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
      "totalBasePrice": 2.8,
      "rates": [
        {
          "description": "Bound Printed Matter Machinable Presorted",
          "priceType": "COMMERCIAL",
          "price": 2.2,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "BOUND_PRINTED_MATTER",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "PR",
          "destinationEntryFacilityType": "NONE",
          "SKU": "DBPP0XXNXC00150"
        },
        {
          "description": "Bound Printed Matter Machinable Presorted",
          "priceType": "COMMERCIAL",
          "price": 0.272,
          "weight": 2.21,
          "dimWeight": 0.0,
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "BOUND_PRINTED_MATTER",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "PR",
          "destinationEntryFacilityType": "NONE",
          "SKU": "DBPP0XXNXD00150"
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
          "SKU": "D2KBYOXXXC00000"
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
          "SKU": "D2KB1OXXXC00000"
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
          "SKU": "D2KB3OXXXC00000"
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
          "SKU": "D2KB5OXXXC00000"
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
          "SKU": "D2KB7OXXXC00000"
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
          "SKU": "D2KBZOXXXC00000"
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
          "SKU": "D2KB3OSXXC00000"
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
          "SKU": "D2KB5OSXXC00000"
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
          "SKU": "D2KB7OSXXC00000"
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
          "SKU": "D2KBZOSXXC00000"
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
          "SKU": "DXTB0EXXXCX0000"
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
          "SKU": "DXSB0EXXXCX0000"
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
          "SKU": "DXSB0EJXXCX0000"
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
      "totalBasePrice": 1.61,
      "rates": [
        {
          "description": "Bound Printed Matter Machinable DSCF Presorted",
          "priceType": "COMMERCIAL",
          "price": 1.45,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "BOUND_PRINTED_MATTER",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "PR",
          "destinationEntryFacilityType": "DESTINATION_SECTIONAL_CENTER_FACILITY",
          "SKU": "DBPP0XXFXC00150"
        },
        {
          "description": "Bound Printed Matter Machinable DSCF Presorted",
          "priceType": "COMMERCIAL",
          "price": 0.072,
          "weight": 2.21,
          "dimWeight": 0.0,
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "BOUND_PRINTED_MATTER",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "PR",
          "destinationEntryFacilityType": "DESTINATION_SECTIONAL_CENTER_FACILITY",
          "SKU": "DBPP0XXFXD00150"
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
          "SKU": "D2KBYOXXXC00000"
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
          "SKU": "D2KB1OXXXC00000"
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
          "SKU": "D2KB3OXXXC00000"
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
          "SKU": "D2KB5OXXXC00000"
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
          "SKU": "D2KB7OXXXC00000"
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
          "SKU": "D2KBZOXXXC00000"
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
          "SKU": "D2KB3OSXXC00000"
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
          "SKU": "D2KB5OSXXC00000"
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
          "SKU": "D2KB7OSXXC00000"
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
          "SKU": "D2KBZOSXXC00000"
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
          "SKU": "DXTB0EXXXCX0000"
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
          "SKU": "DXSB0EXXXCX0000"
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
          "SKU": "DXSB0EJXXCX0000"
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
      "totalBasePrice": 2.38,
      "rates": [
        {
          "description": "Bound Printed Matter Irregular DNDC Presorted",
          "priceType": "COMMERCIAL",
          "price": 2.08,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "BOUND_PRINTED_MATTER",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "IRREGULAR",
          "rateIndicator": "PR",
          "destinationEntryFacilityType": "DESTINATION_NETWORK_DISTRIBUTION_CENTER",
          "SKU": "DBPP0XXCXC00150"
        },
        {
          "description": "Bound Printed Matter Irregular DNDC Presorted",
          "priceType": "COMMERCIAL",
          "price": 0.135,
          "weight": 2.21,
          "dimWeight": 0.0,
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "BOUND_PRINTED_MATTER",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "IRREGULAR",
          "rateIndicator": "PR",
          "destinationEntryFacilityType": "DESTINATION_NETWORK_DISTRIBUTION_CENTER",
          "SKU": "DBPP0XXCXD00150"
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
          "SKU": "D2KBYOXXXC00000"
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
          "SKU": "D2KB1OXXXC00000"
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
          "SKU": "D2KB3OXXXC00000"
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
          "SKU": "D2KB5OXXXC00000"
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
          "SKU": "D2KB7OXXXC00000"
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
          "SKU": "D2KBZOXXXC00000"
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
          "SKU": "D2KB3OSXXC00000"
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
          "SKU": "D2KB5OSXXC00000"
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
          "SKU": "D2KB7OSXXC00000"
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
          "SKU": "D2KBZOSXXC00000"
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
          "SKU": "DXTB0EXXXCX0000"
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
          "SKU": "DXSB0EXXXCX0000"
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
          "SKU": "DXSB0EJXXCX0000"
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
      "totalBasePrice": 1.17,
      "rates": [
        {
          "description": "Bound Printed Matter Irregular DDU Presorted",
          "priceType": "COMMERCIAL",
          "price": 1.01,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "BOUND_PRINTED_MATTER",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "IRREGULAR",
          "rateIndicator": "PR",
          "destinationEntryFacilityType": "DESTINATION_DELIVERY_UNIT",
          "SKU": "DBPP0XXUXC00150"
        },
        {
          "description": "Bound Printed Matter Irregular DDU Presorted",
          "priceType": "COMMERCIAL",
          "price": 0.072,
          "weight": 2.21,
          "dimWeight": 0.0,
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "BOUND_PRINTED_MATTER",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "IRREGULAR",
          "rateIndicator": "PR",
          "destinationEntryFacilityType": "DESTINATION_DELIVERY_UNIT",
          "SKU": "DBPP0XXUXD00150"
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
          "SKU": "D2KBYOXXXC00000"
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
          "SKU": "D2KB1OXXXC00000"
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
          "SKU": "D2KB3OXXXC00000"
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
          "SKU": "D2KB5OXXXC00000"
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
          "SKU": "D2KB7OXXXC00000"
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
          "SKU": "D2KBZOXXXC00000"
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
          "SKU": "D2KB3OSXXC00000"
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
          "SKU": "D2KB5OSXXC00000"
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
          "SKU": "D2KB7OSXXC00000"
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
          "SKU": "D2KBZOSXXC00000"
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
          "SKU": "DXTB0EXXXCX0000"
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
          "SKU": "DXSB0EXXXCX0000"
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
          "SKU": "DXSB0EJXXCX0000"
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
      "totalBasePrice": 2.8,
      "rates": [
        {
          "description": "Bound Printed Matter Irregular Presorted",
          "priceType": "COMMERCIAL",
          "price": 2.2,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "BOUND_PRINTED_MATTER",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "IRREGULAR",
          "rateIndicator": "PR",
          "destinationEntryFacilityType": "NONE",
          "SKU": "DBPP0XXNXC00150"
        },
        {
          "description": "Bound Printed Matter Irregular Presorted",
          "priceType": "COMMERCIAL",
          "price": 0.272,
          "weight": 2.21,
          "dimWeight": 0.0,
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "BOUND_PRINTED_MATTER",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "IRREGULAR",
          "rateIndicator": "PR",
          "destinationEntryFacilityType": "NONE",
          "SKU": "DBPP0XXNXD00150"
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
          "SKU": "D2KBYOXXXC00000"
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
          "SKU": "D2KB1OXXXC00000"
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
          "SKU": "D2KB3OXXXC00000"
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
          "SKU": "D2KB5OXXXC00000"
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
          "SKU": "D2KB7OXXXC00000"
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
          "SKU": "D2KBZOXXXC00000"
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
          "SKU": "D2KB3OSXXC00000"
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
          "SKU": "D2KB5OSXXC00000"
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
          "SKU": "D2KB7OSXXC00000"
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
          "SKU": "D2KBZOSXXC00000"
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
          "SKU": "DXTB0EXXXCX0000"
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
          "SKU": "DXSB0EXXXCX0000"
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
          "SKU": "DXSB0EJXXCX0000"
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
      "totalBasePrice": 1.61,
      "rates": [
        {
          "description": "Bound Printed Matter Irregular DSCF Presorted",
          "priceType": "COMMERCIAL",
          "price": 1.45,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "BOUND_PRINTED_MATTER",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "IRREGULAR",
          "rateIndicator": "PR",
          "destinationEntryFacilityType": "DESTINATION_SECTIONAL_CENTER_FACILITY",
          "SKU": "DBPP0XXFXC00150"
        },
        {
          "description": "Bound Printed Matter Irregular DSCF Presorted",
          "priceType": "COMMERCIAL",
          "price": 0.072,
          "weight": 2.21,
          "dimWeight": 0.0,
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "BOUND_PRINTED_MATTER",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "IRREGULAR",
          "rateIndicator": "PR",
          "destinationEntryFacilityType": "DESTINATION_SECTIONAL_CENTER_FACILITY",
          "SKU": "DBPP0XXFXD00150"
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
          "SKU": "D2KBYOXXXC00000"
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
          "SKU": "D2KB1OXXXC00000"
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
          "SKU": "D2KB3OXXXC00000"
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
          "SKU": "D2KB5OXXXC00000"
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
          "SKU": "D2KB7OXXXC00000"
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
          "SKU": "D2KBZOXXXC00000"
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
          "SKU": "D2KB3OSXXC00000"
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
          "SKU": "D2KB5OSXXC00000"
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
          "SKU": "D2KB7OSXXC00000"
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
          "SKU": "D2KBZOSXXC00000"
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
          "SKU": "DXTB0EXXXCX0000"
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
          "SKU": "DXSB0EXXXCX0000"
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
          "SKU": "DXSB0EJXXCX0000"
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
      "totalBasePrice": 5.6,
      "rates": [
        {
          "description": "Library Mail Machinable Basic",
          "priceType": "COMMERCIAL",
          "price": 5.6,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "LIBRARY_MAIL",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "BA",
          "destinationEntryFacilityType": "NONE",
          "SKU": "DLXX0XXXBC00030"
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
          "SKU": "D2KLYOXXXC00000"
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
          "SKU": "D2KL1OXXXC00000"
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
          "SKU": "D2KL3OXXXC00000"
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
          "SKU": "D2KL5OXXXC00000"
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
          "SKU": "D2KL7OXXXC00000"
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
          "SKU": "D2KLZOXXXC00000"
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
          "SKU": "D2KL3OSXXC00000"
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
          "SKU": "D2KL5OSXXC00000"
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
          "SKU": "D2KL7OSXXC00000"
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
          "SKU": "D2KLZOSXXC00000"
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
          "SKU": "DXTL0EXXXCX0000"
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
          "SKU": "DXSL0EXXXCX0000"
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
          "SKU": "DXSL0EJXXCX0000"
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
      "totalBasePrice": 4.52,
      "rates": [
        {
          "description": "Library Mail Machinable 5-digit",
          "priceType": "COMMERCIAL",
          "price": 4.52,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "LIBRARY_MAIL",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "5D",
          "destinationEntryFacilityType": "NONE",
          "SKU": "DLXX0XXX5C00030"
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
          "SKU": "D2KLYOXXXC00000"
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
          "SKU": "D2KL1OXXXC00000"
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
          "SKU": "D2KL3OXXXC00000"
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
          "SKU": "D2KL5OXXXC00000"
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
          "SKU": "D2KL7OXXXC00000"
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
          "SKU": "D2KLZOXXXC00000"
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
          "SKU": "D2KL3OSXXC00000"
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
          "SKU": "D2KL5OSXXC00000"
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
          "SKU": "D2KL7OSXXC00000"
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
          "SKU": "D2KLZOSXXC00000"
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
          "SKU": "DXTL0EXXXCX0000"
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
          "SKU": "DXSL0EXXXCX0000"
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
          "SKU": "DXSL0EJXXCX0000"
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
      "totalBasePrice": 5.6,
      "rates": [
        {
          "description": "Library Mail Irregular Basic",
          "priceType": "COMMERCIAL",
          "price": 5.6,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "LIBRARY_MAIL",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "IRREGULAR",
          "rateIndicator": "BA",
          "destinationEntryFacilityType": "NONE",
          "SKU": "DLXX0XXXBC00030"
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
          "SKU": "D2KLYOXXXC00000"
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
          "SKU": "D2KL1OXXXC00000"
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
          "SKU": "D2KL3OXXXC00000"
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
          "SKU": "D2KL5OXXXC00000"
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
          "SKU": "D2KL7OXXXC00000"
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
          "SKU": "D2KLZOXXXC00000"
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
          "SKU": "D2KL3OSXXC00000"
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
          "SKU": "D2KL5OSXXC00000"
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
          "SKU": "D2KL7OSXXC00000"
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
          "SKU": "D2KLZOSXXC00000"
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
          "SKU": "DXTL0EXXXCX0000"
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
          "SKU": "DXSL0EXXXCX0000"
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
          "SKU": "DXSL0EJXXCX0000"
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
      "totalBasePrice": 4.52,
      "rates": [
        {
          "description": "Library Mail Irregular 5-digit",
          "priceType": "COMMERCIAL",
          "price": 4.52,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "LIBRARY_MAIL",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "IRREGULAR",
          "rateIndicator": "5D",
          "destinationEntryFacilityType": "NONE",
          "SKU": "DLXX0XXX5C00030"
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
          "SKU": "D2KLYOXXXC00000"
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
          "SKU": "D2KL1OXXXC00000"
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
          "SKU": "D2KL3OXXXC00000"
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
          "SKU": "D2KL5OXXXC00000"
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
          "SKU": "D2KL7OXXXC00000"
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
          "SKU": "D2KLZOXXXC00000"
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
          "SKU": "D2KL3OSXXC00000"
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
          "SKU": "D2KL5OSXXC00000"
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
          "SKU": "D2KL7OSXXC00000"
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
          "SKU": "D2KLZOSXXC00000"
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
          "SKU": "DXTL0EXXXCX0000"
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
          "SKU": "DXSL0EXXXCX0000"
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
          "SKU": "DXSL0EJXXCX0000"
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
      "totalBasePrice": 5.9,
      "rates": [
        {
          "description": "Media Mail Machinable Basic",
          "priceType": "COMMERCIAL",
          "price": 5.9,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "MEDIA_MAIL",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "BA",
          "destinationEntryFacilityType": "NONE",
          "SKU": "DMXX0XXXBC00030"
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
          "SKU": "D2KMYOXXXC00000"
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
          "SKU": "D2KM1OXXXC00000"
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
          "SKU": "D2KM3OXXXC00000"
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
          "SKU": "D2KM5OXXXC00000"
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
          "SKU": "D2KM7OXXXC00000"
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
          "SKU": "D2KMZOXXXC00000"
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
          "SKU": "D2KM3OSXXC00000"
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
          "SKU": "D2KM5OSXXC00000"
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
          "SKU": "D2KM7OSXXC00000"
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
          "SKU": "D2KMZOSXXC00000"
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
          "SKU": "DXTM0EXXXCX0000"
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
          "SKU": "DXSM0EXXXCX0000"
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
          "SKU": "DXSM0EJXXCX0000"
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
      "totalBasePrice": 4.76,
      "rates": [
        {
          "description": "Media Mail Machinable 5-digit",
          "priceType": "COMMERCIAL",
          "price": 4.76,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "MEDIA_MAIL",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "5D",
          "destinationEntryFacilityType": "NONE",
          "SKU": "DMXX0XXX5C00030"
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
          "SKU": "D2KMYOXXXC00000"
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
          "SKU": "D2KM1OXXXC00000"
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
          "SKU": "D2KM3OXXXC00000"
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
          "SKU": "D2KM5OXXXC00000"
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
          "SKU": "D2KM7OXXXC00000"
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
          "SKU": "D2KMZOXXXC00000"
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
          "SKU": "D2KM3OSXXC00000"
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
          "SKU": "D2KM5OSXXC00000"
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
          "SKU": "D2KM7OSXXC00000"
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
          "SKU": "D2KMZOSXXC00000"
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
          "SKU": "DXTM0EXXXCX0000"
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
          "SKU": "DXSM0EXXXCX0000"
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
          "SKU": "DXSM0EJXXCX0000"
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
      "totalBasePrice": 5.9,
      "rates": [
        {
          "description": "Media Mail Irregular Basic",
          "priceType": "COMMERCIAL",
          "price": 5.9,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "MEDIA_MAIL",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "IRREGULAR",
          "rateIndicator": "BA",
          "destinationEntryFacilityType": "NONE",
          "SKU": "DMXX0XXXBC00030"
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
          "SKU": "D2KMYOXXXC00000"
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
          "SKU": "D2KM1OXXXC00000"
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
          "SKU": "D2KM3OXXXC00000"
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
          "SKU": "D2KM5OXXXC00000"
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
          "SKU": "D2KM7OXXXC00000"
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
          "SKU": "D2KMZOXXXC00000"
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
          "SKU": "D2KM3OSXXC00000"
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
          "SKU": "D2KM5OSXXC00000"
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
          "SKU": "D2KM7OSXXC00000"
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
          "SKU": "D2KMZOSXXC00000"
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
          "SKU": "DXTM0EXXXCX0000"
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
          "SKU": "DXSM0EXXXCX0000"
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
          "SKU": "DXSM0EJXXCX0000"
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
      "totalBasePrice": 4.76,
      "rates": [
        {
          "description": "Media Mail Irregular 5-digit",
          "priceType": "COMMERCIAL",
          "price": 4.76,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "MEDIA_MAIL",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "IRREGULAR",
          "rateIndicator": "5D",
          "destinationEntryFacilityType": "NONE",
          "SKU": "DMXX0XXX5C00030"
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
          "SKU": "D2KMYOXXXC00000"
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
          "SKU": "D2KM1OXXXC00000"
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
          "SKU": "D2KM3OXXXC00000"
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
          "SKU": "D2KM5OXXXC00000"
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
          "SKU": "D2KM7OXXXC00000"
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
          "SKU": "D2KMZOXXXC00000"
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
          "SKU": "D2KM3OSXXC00000"
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
          "SKU": "D2KM5OSXXC00000"
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
          "SKU": "D2KM7OSXXC00000"
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
          "SKU": "D2KMZOSXXC00000"
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
          "SKU": "DXTM0EXXXCX0000"
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
          "SKU": "DXSM0EXXXCX0000"
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
          "SKU": "DXSM0EJXXCX0000"
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
      "totalBasePrice": 25.56,
      "rates": [
        {
          "description": "Parcel Select Machinable DNDC Single-piece",
          "priceType": "COMMERCIAL",
          "price": 7.56,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [
            {
              "name": "Nonstandard Volume > 2 cu ft",
              "SKU": "D813XVCXXXX0000",
              "price": 18.0
            }
          ],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "USPS_CONNECT_REGIONAL",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "SP",
          "destinationEntryFacilityType": "DESTINATION_NETWORK_DISTRIBUTION_CENTER",
          "SKU": "DVXP0XXCXC00030"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
      "totalBasePrice": 25.56,
      "rates": [
        {
          "description": "Parcel Select Machinable DNDC Dimensional Rectangular",
          "priceType": "COMMERCIAL",
          "price": 7.56,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [
            {
              "name": "Nonstandard Volume > 2 cu ft",
              "SKU": "D813XVCXXXX0000",
              "price": 18.0
            }
          ],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "USPS_CONNECT_REGIONAL",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "DR",
          "destinationEntryFacilityType": "DESTINATION_NETWORK_DISTRIBUTION_CENTER",
          "SKU": "DVXR0XXCXC00030"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
      "totalBasePrice": 7.56,
      "rates": [
        {
          "description": "Parcel Select Machinable DNDC Dimensional Nonrectangular",
          "priceType": "COMMERCIAL",
          "price": 7.56,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "USPS_CONNECT_REGIONAL",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "DN",
          "destinationEntryFacilityType": "DESTINATION_NETWORK_DISTRIBUTION_CENTER",
          "SKU": "DVXR0XXCXC00030"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
      "totalBasePrice": 23.7,
      "rates": [
        {
          "description": "Parcel Select Machinable DSCF SCF",
          "priceType": "COMMERCIAL",
          "price": 5.7,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [
            {
              "name": "Nonstandard Volume > 2 cu ft",
              "SKU": "D813XVFTXXX0000",
              "price": 18.0
            }
          ],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "USPS_CONNECT_REGIONAL",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "DE",
          "destinationEntryFacilityType": "DESTINATION_SECTIONAL_CENTER_FACILITY",
          "SKU": "DVXP0XXFXC00030"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
      "totalBasePrice": 23.7,
      "rates": [
        {
          "description": "Parcel Select Machinable DSCF SCF Dimensional Rectangular",
          "priceType": "COMMERCIAL",
          "price": 5.7,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [
            {
              "name": "Nonstandard Volume > 2 cu ft",
              "SKU": "D813XVFTXXX0000",
              "price": 18.0
            }
          ],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "USPS_CONNECT_REGIONAL",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "SR",
          "destinationEntryFacilityType": "DESTINATION_SECTIONAL_CENTER_FACILITY",
          "SKU": "DVXR0XXFXC00030"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
      "totalBasePrice": 5.7,
      "rates": [
        {
          "description": "Parcel Select Machinable DSCF SCF Dimensional Nonrectangular",
          "priceType": "COMMERCIAL",
          "price": 5.7,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "USPS_CONNECT_REGIONAL",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "SN",
          "destinationEntryFacilityType": "DESTINATION_SECTIONAL_CENTER_FACILITY",
          "SKU": "DVXR0XXFXC00030"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
      "totalBasePrice": 23.7,
      "rates": [
        {
          "description": "Parcel Select Machinable DHUB Single-piece",
          "priceType": "COMMERCIAL",
          "price": 5.7,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [
            {
              "name": "Nonstandard Volume > 2 cu ft",
              "SKU": "D813XVHXXXX0000",
              "price": 18.0
            }
          ],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "USPS_CONNECT_REGIONAL",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "SP",
          "destinationEntryFacilityType": "DESTINATION_SERVICE_HUB",
          "SKU": "DVXP0XXBXC00030"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
      "totalBasePrice": 23.7,
      "rates": [
        {
          "description": "Parcel Select Machinable DHUB Dimensional Rectangular",
          "priceType": "COMMERCIAL",
          "price": 5.7,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [
            {
              "name": "Nonstandard Volume > 2 cu ft",
              "SKU": "D813XVHXXXX0000",
              "price": 18.0
            }
          ],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "USPS_CONNECT_REGIONAL",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "DR",
          "destinationEntryFacilityType": "DESTINATION_SERVICE_HUB",
          "SKU": "DVXR0XXBXC00030"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
      "totalBasePrice": 5.7,
      "rates": [
        {
          "description": "Parcel Select Machinable DHUB Dimensional Nonrectangular",
          "priceType": "COMMERCIAL",
          "price": 5.7,
          "weight": 2.21,
          "dimWeight": 0.0,
          "fees": [],
          "startDate": "2024-10-06",
          "endDate": "",
          "mailClass": "USPS_CONNECT_REGIONAL",
          "zone": "08",
          "productName": "",
          "productDefinition": "",
          "processingCategory": "MACHINABLE",
          "rateIndicator": "DN",
          "destinationEntryFacilityType": "DESTINATION_SERVICE_HUB",
          "SKU": "DVXR0XXBXC00030"
        }
      ],
      "extraServices": [
        {
          "extraService": "991",
          "name": "Sunday/Holiday Delivery",
          "priceType": "COMMERCIAL",
          "price": 1.95,
          "warnings": [
            {
              "warningCode": "001",
              "warningDescription": "Contract rate not found for request. Published rate returned."
            }
          ],
          "SKU": "DXZ6XXXXXCX0000"
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
          "SKU": "D2KVYOXXXC00000"
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
          "SKU": "D2KV1OXXXC00000"
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
          "SKU": "D2KV3OXXXC00000"
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
          "SKU": "D2KV5OXXXC00000"
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
          "SKU": "D2KV7OXXXC00000"
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
          "SKU": "D2KVZOXXXC00000"
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
          "SKU": "D2KV3OSXXC00000"
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
          "SKU": "D2KV5OSXXC00000"
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
          "SKU": "D2KV7OSXXC00000"
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
          "SKU": "D2KVZOSXXC00000"
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
          "SKU": "DXTV0EXXXCX0000"
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
          "SKU": "DXSV0EXXXCX0000"
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
          "SKU": "DXSV0EJXXCX0000"
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
