import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging as logger

import karrio.lib as lib
import karrio.sdk as karrio
import karrio.core.models as models


class TestUSPSRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)
        self.MachinableRateRequest = models.RateRequest(**MachinableRatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipments/v3/options/search",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)

    def test_parse_machinable_rate_response(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.MachinableRateRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                lib.to_dict(parsed_response), MachinableParsedRateResponse
            )


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

MachinableRatePayload = {
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
        "shipment_date": "2024-07-28",
        "usps_machinable_piece": True,
    },
}


ParsedRateResponse = [
    [
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 42.74, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS LIBRARY MAIL NONSTANDARD SINGLE PIECE",
                "usps_dimensional_weight": 0,
                "usps_extra_services": [920],
                "usps_guaranteed_delivery": False,
                "usps_mail_class": "LIBRARY_MAIL",
                "usps_price_type": "RETAIL",
                "usps_processing_category": "NONSTANDARD",
                "usps_rate_indicator": "SP",
                "usps_rate_sku": "DLXX0XXXUR00550",
                "usps_zone": "08",
            },
            "service": "usps_library_mail_nonstandard_single_piece",
            "total_charge": 42.74,
            "transit_days": 7,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 32.25, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS PRIORITY MAIL EXPRESS PADDED FLAT RATE ENVELOPE",
                "usps_dimensional_weight": 0,
                "usps_extra_services": [920],
                "usps_guaranteed_delivery": True,
                "usps_mail_class": "PRIORITY_MAIL_EXPRESS",
                "usps_price_type": "RETAIL",
                "usps_processing_category": "FLATS",
                "usps_rate_indicator": "FP",
                "usps_rate_sku": "DEFE2XXXXR00700",
                "usps_zone": "08",
            },
            "service": "usps_priority_mail_express_padded_flat_rate_envelope",
            "total_charge": 32.25,
            "transit_days": 2,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 32.25, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS PRIORITY MAIL EXPRESS PADDED FLAT RATE ENVELOPE",
                "usps_dimensional_weight": 0,
                "usps_extra_services": [920],
                "usps_guaranteed_delivery": True,
                "usps_mail_class": "PRIORITY_MAIL_EXPRESS",
                "usps_price_type": "RETAIL",
                "usps_processing_category": "NONSTANDARD",
                "usps_rate_indicator": "FP",
                "usps_rate_sku": "DEFE2XXXXR00700",
                "usps_zone": "08",
            },
            "service": "usps_priority_mail_express_padded_flat_rate_envelope",
            "total_charge": 32.25,
            "transit_days": 2,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 457.3, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS PRIORITY MAIL EXPRESS",
                "usps_dimensional_weight": 0,
                "usps_extra_services": [920],
                "usps_guaranteed_delivery": True,
                "usps_mail_class": "PRIORITY_MAIL_EXPRESS",
                "usps_price_type": "RETAIL",
                "usps_processing_category": "NONSTANDARD",
                "usps_rate_indicator": "PA",
                "usps_rate_sku": "DEXX0XXXXR08550",
                "usps_zone": "08",
            },
            "service": "usps_priority_mail_express",
            "total_charge": 457.3,
            "transit_days": 2,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 10.85, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS PRIORITY MAIL PADDED FLAT RATE ENVELOPE",
                "usps_dimensional_weight": 0,
                "usps_extra_services": [920],
                "usps_guaranteed_delivery": False,
                "usps_mail_class": "PRIORITY_MAIL",
                "usps_price_type": "RETAIL",
                "usps_processing_category": "FLATS",
                "usps_rate_indicator": "FP",
                "usps_rate_sku": "DPFE2XXXXR00700",
                "usps_zone": "08",
            },
            "service": "usps_priority_mail_padded_flat_rate_envelope",
            "total_charge": 10.85,
            "transit_days": 2,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 10.85, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS PRIORITY MAIL PADDED FLAT RATE ENVELOPE",
                "usps_dimensional_weight": 0,
                "usps_extra_services": [920],
                "usps_guaranteed_delivery": False,
                "usps_mail_class": "PRIORITY_MAIL",
                "usps_price_type": "RETAIL",
                "usps_processing_category": "NONSTANDARD",
                "usps_rate_indicator": "FP",
                "usps_rate_sku": "DPFE2XXXXR00700",
                "usps_zone": "08",
            },
            "service": "usps_priority_mail_padded_flat_rate_envelope",
            "total_charge": 10.85,
            "transit_days": 2,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 19.15, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS PRIORITY MAIL MEDIUM FLAT RATE BOX",
                "usps_dimensional_weight": 0,
                "usps_extra_services": [920],
                "usps_guaranteed_delivery": False,
                "usps_mail_class": "PRIORITY_MAIL",
                "usps_price_type": "RETAIL",
                "usps_processing_category": "NONSTANDARD",
                "usps_rate_indicator": "FB",
                "usps_rate_sku": "DPFB1XXXXR00700",
                "usps_zone": "08",
            },
            "service": "usps_priority_mail_medium_flat_rate_box",
            "total_charge": 19.15,
            "transit_days": 2,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 26.3, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS PRIORITY MAIL LARGE FLAT RATE BOX",
                "usps_dimensional_weight": 0,
                "usps_extra_services": [920],
                "usps_guaranteed_delivery": False,
                "usps_mail_class": "PRIORITY_MAIL",
                "usps_price_type": "RETAIL",
                "usps_processing_category": "NONSTANDARD",
                "usps_rate_indicator": "PL",
                "usps_rate_sku": "DPFB0XXXXR00700",
                "usps_zone": "08",
            },
            "service": "usps_priority_mail_large_flat_rate_box",
            "total_charge": 26.3,
            "transit_days": 2,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 25.05, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS PRIORITY MAIL LARGE FLAT RATE APO FPO DPO",
                "usps_dimensional_weight": 0,
                "usps_extra_services": [920],
                "usps_guaranteed_delivery": False,
                "usps_mail_class": "PRIORITY_MAIL",
                "usps_price_type": "RETAIL",
                "usps_processing_category": "NONSTANDARD",
                "usps_rate_indicator": "PM",
                "usps_rate_sku": "DPFB3XXXXR00700",
                "usps_zone": "08",
            },
            "service": "usps_priority_mail_large_flat_rate_apo_fpo_dpo",
            "total_charge": 25.05,
            "transit_days": 2,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 184.0, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS PRIORITY MAIL",
                "usps_dimensional_weight": 0,
                "usps_extra_services": [920],
                "usps_guaranteed_delivery": False,
                "usps_mail_class": "PRIORITY_MAIL",
                "usps_price_type": "RETAIL",
                "usps_processing_category": "NONSTANDARD",
                "usps_rate_indicator": "SP",
                "usps_rate_sku": "DPXX0XXXXR08550",
                "usps_zone": "08",
            },
            "service": "usps_priority_mail",
            "total_charge": 184.0,
            "transit_days": 2,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 151.85, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS GROUND ADVANTAGE",
                "usps_dimensional_weight": 0,
                "usps_extra_services": [920],
                "usps_guaranteed_delivery": False,
                "usps_mail_class": "USPS_GROUND_ADVANTAGE",
                "usps_price_type": "RETAIL",
                "usps_processing_category": "NONSTANDARD",
                "usps_rate_indicator": "SP",
                "usps_rate_sku": "DUXP0XXXXR08550",
                "usps_zone": "08",
            },
            "service": "usps_ground_advantage",
            "total_charge": 151.85,
            "transit_days": 4,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 45.13, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS MEDIA MAIL NONSTANDARD SINGLE PIECE",
                "usps_dimensional_weight": 0,
                "usps_extra_services": [920],
                "usps_guaranteed_delivery": False,
                "usps_mail_class": "MEDIA_MAIL",
                "usps_price_type": "RETAIL",
                "usps_processing_category": "NONSTANDARD",
                "usps_rate_indicator": "SP",
                "usps_rate_sku": "DMXX0XXXUR00550",
                "usps_zone": "08",
            },
            "service": "usps_media_mail_nonstandard_single_piece",
            "total_charge": 45.13,
            "transit_days": 7,
        },
    ],
    [],
]

MachinableParsedRateResponse = [
    [
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 42.74, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS LIBRARY MAIL NONSTANDARD SINGLE PIECE",
                "usps_dimensional_weight": 0,
                "usps_extra_services": [920],
                "usps_guaranteed_delivery": False,
                "usps_mail_class": "LIBRARY_MAIL",
                "usps_price_type": "RETAIL",
                "usps_processing_category": "NONSTANDARD",
                "usps_rate_indicator": "SP",
                "usps_rate_sku": "DLXX0XXXUR00550",
                "usps_zone": "08",
            },
            "service": "usps_library_mail_nonstandard_single_piece",
            "total_charge": 42.74,
            "transit_days": 7,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 32.25, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS PRIORITY MAIL EXPRESS PADDED FLAT RATE ENVELOPE",
                "usps_dimensional_weight": 0,
                "usps_extra_services": [920],
                "usps_guaranteed_delivery": True,
                "usps_mail_class": "PRIORITY_MAIL_EXPRESS",
                "usps_price_type": "RETAIL",
                "usps_processing_category": "FLATS",
                "usps_rate_indicator": "FP",
                "usps_rate_sku": "DEFE2XXXXR00700",
                "usps_zone": "08",
            },
            "service": "usps_priority_mail_express_padded_flat_rate_envelope",
            "total_charge": 32.25,
            "transit_days": 2,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 32.25, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS PRIORITY MAIL EXPRESS PADDED FLAT RATE ENVELOPE",
                "usps_dimensional_weight": 0,
                "usps_extra_services": [920],
                "usps_guaranteed_delivery": True,
                "usps_mail_class": "PRIORITY_MAIL_EXPRESS",
                "usps_price_type": "RETAIL",
                "usps_processing_category": "NONSTANDARD",
                "usps_rate_indicator": "FP",
                "usps_rate_sku": "DEFE2XXXXR00700",
                "usps_zone": "08",
            },
            "service": "usps_priority_mail_express_padded_flat_rate_envelope",
            "total_charge": 32.25,
            "transit_days": 2,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 457.3, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS PRIORITY MAIL EXPRESS",
                "usps_dimensional_weight": 0,
                "usps_extra_services": [920],
                "usps_guaranteed_delivery": True,
                "usps_mail_class": "PRIORITY_MAIL_EXPRESS",
                "usps_price_type": "RETAIL",
                "usps_processing_category": "NONSTANDARD",
                "usps_rate_indicator": "PA",
                "usps_rate_sku": "DEXX0XXXXR08550",
                "usps_zone": "08",
            },
            "service": "usps_priority_mail_express",
            "total_charge": 457.3,
            "transit_days": 2,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 10.85, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS PRIORITY MAIL PADDED FLAT RATE ENVELOPE",
                "usps_dimensional_weight": 0,
                "usps_extra_services": [920],
                "usps_guaranteed_delivery": False,
                "usps_mail_class": "PRIORITY_MAIL",
                "usps_price_type": "RETAIL",
                "usps_processing_category": "FLATS",
                "usps_rate_indicator": "FP",
                "usps_rate_sku": "DPFE2XXXXR00700",
                "usps_zone": "08",
            },
            "service": "usps_priority_mail_padded_flat_rate_envelope",
            "total_charge": 10.85,
            "transit_days": 2,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 10.85, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS PRIORITY MAIL PADDED FLAT RATE ENVELOPE",
                "usps_dimensional_weight": 0,
                "usps_extra_services": [920],
                "usps_guaranteed_delivery": False,
                "usps_mail_class": "PRIORITY_MAIL",
                "usps_price_type": "RETAIL",
                "usps_processing_category": "NONSTANDARD",
                "usps_rate_indicator": "FP",
                "usps_rate_sku": "DPFE2XXXXR00700",
                "usps_zone": "08",
            },
            "service": "usps_priority_mail_padded_flat_rate_envelope",
            "total_charge": 10.85,
            "transit_days": 2,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 19.15, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS PRIORITY MAIL MEDIUM FLAT RATE BOX",
                "usps_dimensional_weight": 0,
                "usps_extra_services": [920],
                "usps_guaranteed_delivery": False,
                "usps_mail_class": "PRIORITY_MAIL",
                "usps_price_type": "RETAIL",
                "usps_processing_category": "NONSTANDARD",
                "usps_rate_indicator": "FB",
                "usps_rate_sku": "DPFB1XXXXR00700",
                "usps_zone": "08",
            },
            "service": "usps_priority_mail_medium_flat_rate_box",
            "total_charge": 19.15,
            "transit_days": 2,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 26.3, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS PRIORITY MAIL LARGE FLAT RATE BOX",
                "usps_dimensional_weight": 0,
                "usps_extra_services": [920],
                "usps_guaranteed_delivery": False,
                "usps_mail_class": "PRIORITY_MAIL",
                "usps_price_type": "RETAIL",
                "usps_processing_category": "NONSTANDARD",
                "usps_rate_indicator": "PL",
                "usps_rate_sku": "DPFB0XXXXR00700",
                "usps_zone": "08",
            },
            "service": "usps_priority_mail_large_flat_rate_box",
            "total_charge": 26.3,
            "transit_days": 2,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 25.05, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS PRIORITY MAIL LARGE FLAT RATE APO FPO DPO",
                "usps_dimensional_weight": 0,
                "usps_extra_services": [920],
                "usps_guaranteed_delivery": False,
                "usps_mail_class": "PRIORITY_MAIL",
                "usps_price_type": "RETAIL",
                "usps_processing_category": "NONSTANDARD",
                "usps_rate_indicator": "PM",
                "usps_rate_sku": "DPFB3XXXXR00700",
                "usps_zone": "08",
            },
            "service": "usps_priority_mail_large_flat_rate_apo_fpo_dpo",
            "total_charge": 25.05,
            "transit_days": 2,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 184.0, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS PRIORITY MAIL",
                "usps_dimensional_weight": 0,
                "usps_extra_services": [920],
                "usps_guaranteed_delivery": False,
                "usps_mail_class": "PRIORITY_MAIL",
                "usps_price_type": "RETAIL",
                "usps_processing_category": "NONSTANDARD",
                "usps_rate_indicator": "SP",
                "usps_rate_sku": "DPXX0XXXXR08550",
                "usps_zone": "08",
            },
            "service": "usps_priority_mail",
            "total_charge": 184.0,
            "transit_days": 2,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 151.85, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS GROUND ADVANTAGE",
                "usps_dimensional_weight": 0,
                "usps_extra_services": [920],
                "usps_guaranteed_delivery": False,
                "usps_mail_class": "USPS_GROUND_ADVANTAGE",
                "usps_price_type": "RETAIL",
                "usps_processing_category": "NONSTANDARD",
                "usps_rate_indicator": "SP",
                "usps_rate_sku": "DUXP0XXXXR08550",
                "usps_zone": "08",
            },
            "service": "usps_ground_advantage",
            "total_charge": 151.85,
            "transit_days": 4,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 45.13, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS MEDIA MAIL NONSTANDARD SINGLE PIECE",
                "usps_dimensional_weight": 0,
                "usps_extra_services": [920],
                "usps_guaranteed_delivery": False,
                "usps_mail_class": "MEDIA_MAIL",
                "usps_price_type": "RETAIL",
                "usps_processing_category": "NONSTANDARD",
                "usps_rate_indicator": "SP",
                "usps_rate_sku": "DMXX0XXXUR00550",
                "usps_zone": "08",
            },
            "service": "usps_media_mail_nonstandard_single_piece",
            "total_charge": 45.13,
            "transit_days": 7,
        },
    ],
    [],
]

RateRequest = [
    {
        "destinationEntryFacilityType": "NONE",
        "destinationZIPCode": "73108",
        "originZIPCode": "29440",
        "packageDescription": {
            "extraServices": [415],
            "height": 19.69,
            "length": 19.69,
            "mailClass": "PARCEL_SELECT",
            "mailingDate": "2024-07-28",
            "weight": 44.1,
            "width": 4.72,
        },
        "pricingOptions": [
            {
                "paymentAccount": {
                    "accountNumber": "Your Account Number",
                    "accountType": "EPS",
                },
                "priceType": "COMMERCIAL",
            }
        ],
    }
]

RateResponse = """{
	"originZIPCode": "60601",
	"destinationZIPCode": "94105",
	"pricingOptions": [
		{
			"shippingOptions": [
				{
					"mailClass": "LIBRARY_MAIL",
					"rateOptions": [
						{
							"commitment": {
								"name": "7 Days",
								"scheduleDeliveryDate": "2025-06-06",
								"guaranteedDelivery": false
							},
							"totalPrice": 42.74,
							"totalBasePrice": 42.74,
							"rates": [
								{
									"description": "Library Mail Nonstandard Single-piece",
									"startDate": "2025-01-19",
									"endDate": "",
									"price": 42.74,
									"zone": "08",
									"weight": 55,
									"dimensionalWeight": 0,
									"dimWeight": 0,
									"fees": [],
									"priceType": "RETAIL",
									"mailClass": "LIBRARY_MAIL",
									"productName": "",
									"productDefinition": "",
									"processingCategory": "NONSTANDARD",
									"rateIndicator": "SP",
									"destinationEntryFacilityType": "NONE",
									"SKU": "DLXX0XXXUR00550"
								}
							],
							"extraServices": [
								{
									"name": "USPS Tracking",
									"price": 0,
									"extraService": "920",
									"priceType": "RETAIL",
									"warnings": [],
									"SKU": "DXTL0EXXXRX0000"
								}
							]
						}
					]
				},
				{
					"mailClass": "PRIORITY_MAIL_EXPRESS",
					"rateOptions": [
						{
							"commitment": {
								"name": "2 Days",
								"scheduleDeliveryDate": "2025-05-31",
								"guaranteedDelivery": true
							},
							"totalPrice": 32.25,
							"totalBasePrice": 32.25,
							"rates": [
								{
									"description": "Priority Mail Express Padded Flat Rate Envelope",
									"startDate": "2025-01-19",
									"endDate": "",
									"price": 32.25,
									"zone": "08",
									"weight": 55,
									"dimensionalWeight": 0,
									"dimWeight": 0,
									"fees": [],
									"priceType": "RETAIL",
									"mailClass": "PRIORITY_MAIL_EXPRESS",
									"productName": "Priority Mail Express Padded Flat Rate Envelope",
									"productDefinition": "1-2 day specific guaranteed delivery by 6:00pm local delivery time",
									"processingCategory": "FLATS",
									"rateIndicator": "FP",
									"destinationEntryFacilityType": "NONE",
									"SKU": "DEFE2XXXXR00700"
								}
							],
							"extraServices": [
								{
									"name": "USPS Tracking",
									"price": 0,
									"extraService": "920",
									"priceType": "RETAIL",
									"warnings": [],
									"SKU": "DXTE0EXXXRX0000"
								}
							]
						},
						{
							"commitment": {
								"name": "2 Days",
								"scheduleDeliveryDate": "2025-05-31",
								"guaranteedDelivery": true
							},
							"totalPrice": 32.25,
							"totalBasePrice": 32.25,
							"rates": [
								{
									"description": "Priority Mail Express Nonstandard Padded Flat Rate Envelope",
									"startDate": "2025-01-19",
									"endDate": "",
									"price": 32.25,
									"zone": "08",
									"weight": 55,
									"dimensionalWeight": 0,
									"dimWeight": 0,
									"fees": [],
									"priceType": "RETAIL",
									"mailClass": "PRIORITY_MAIL_EXPRESS",
									"productName": "Priority Mail Express Padded Flat Rate Envelope",
									"productDefinition": "1-2 day specific guaranteed delivery by 6:00pm local delivery time",
									"processingCategory": "NONSTANDARD",
									"rateIndicator": "FP",
									"destinationEntryFacilityType": "NONE",
									"SKU": "DEFE2XXXXR00700"
								}
							],
							"extraServices": [
								{
									"name": "USPS Tracking",
									"price": 0,
									"extraService": "920",
									"priceType": "RETAIL",
									"warnings": [],
									"SKU": "DXTE0EXXXRX0000"
								}
							]
						},
						{
							"commitment": {
								"name": "2 Days",
								"scheduleDeliveryDate": "2025-05-31",
								"guaranteedDelivery": true
							},
							"totalPrice": 457.3,
							"totalBasePrice": 457.3,
							"rates": [
								{
									"description": "Priority Mail Express Nonstandard Single-piece",
									"startDate": "2025-01-19",
									"endDate": "",
									"price": 457.3,
									"zone": "08",
									"weight": 55,
									"dimensionalWeight": 0,
									"dimWeight": 0,
									"fees": [],
									"priceType": "RETAIL",
									"mailClass": "PRIORITY_MAIL_EXPRESS",
									"productName": "Priority Mail Express",
									"productDefinition": "1-2 day specific guaranteed delivery by 6:00pm local delivery time",
									"processingCategory": "NONSTANDARD",
									"rateIndicator": "PA",
									"destinationEntryFacilityType": "NONE",
									"SKU": "DEXX0XXXXR08550"
								}
							],
							"extraServices": [
								{
									"name": "USPS Tracking",
									"price": 0,
									"extraService": "920",
									"priceType": "RETAIL",
									"warnings": [],
									"SKU": "DXTE0EXXXRX0000"
								}
							]
						}
					]
				},
				{
					"mailClass": "PRIORITY_MAIL",
					"rateOptions": [
						{
							"commitment": {
								"name": "2 Days",
								"scheduleDeliveryDate": "2025-06-02",
								"guaranteedDelivery": false
							},
							"totalPrice": 10.85,
							"totalBasePrice": 10.85,
							"rates": [
								{
									"description": "Priority Mail Padded Flat Rate Envelope",
									"startDate": "2025-01-19",
									"endDate": "",
									"price": 10.85,
									"zone": "08",
									"weight": 55,
									"dimensionalWeight": 0,
									"dimWeight": 0,
									"fees": [],
									"priceType": "RETAIL",
									"mailClass": "PRIORITY_MAIL",
									"productName": "Priority Mail Padded Flat Rate Envelope",
									"productDefinition": "1-3 day specific delivery to all U.S. states and territories",
									"processingCategory": "FLATS",
									"rateIndicator": "FP",
									"destinationEntryFacilityType": "NONE",
									"SKU": "DPFE2XXXXR00700"
								}
							],
							"extraServices": [
								{
									"name": "USPS Tracking",
									"price": 0,
									"extraService": "920",
									"priceType": "RETAIL",
									"warnings": [],
									"SKU": "DXTP0EXXXRX0000"
								}
							]
						},
						{
							"commitment": {
								"name": "2 Days",
								"scheduleDeliveryDate": "2025-06-02",
								"guaranteedDelivery": false
							},
							"totalPrice": 10.85,
							"totalBasePrice": 10.85,
							"rates": [
								{
									"description": "Priority Mail Nonstandard Padded Flat Rate Envelope",
									"startDate": "2025-01-19",
									"endDate": "",
									"price": 10.85,
									"zone": "08",
									"weight": 55,
									"dimensionalWeight": 0,
									"dimWeight": 0,
									"fees": [],
									"priceType": "RETAIL",
									"mailClass": "PRIORITY_MAIL",
									"productName": "Priority Mail Padded Flat Rate Envelope",
									"productDefinition": "1-3 day specific delivery to all U.S. states and territories",
									"processingCategory": "NONSTANDARD",
									"rateIndicator": "FP",
									"destinationEntryFacilityType": "NONE",
									"SKU": "DPFE2XXXXR00700"
								}
							],
							"extraServices": [
								{
									"name": "USPS Tracking",
									"price": 0,
									"extraService": "920",
									"priceType": "RETAIL",
									"warnings": [],
									"SKU": "DXTP0EXXXRX0000"
								}
							]
						},
						{
							"commitment": {
								"name": "2 Days",
								"scheduleDeliveryDate": "2025-06-02",
								"guaranteedDelivery": false
							},
							"totalPrice": 19.15,
							"totalBasePrice": 19.15,
							"rates": [
								{
									"description": "Priority Mail Nonstandard Medium Flat Rate Box",
									"startDate": "2025-01-19",
									"endDate": "",
									"price": 19.15,
									"zone": "08",
									"weight": 55,
									"dimensionalWeight": 0,
									"dimWeight": 0,
									"fees": [],
									"priceType": "RETAIL",
									"mailClass": "PRIORITY_MAIL",
									"productName": "Priority Mail Medium Flat Rate Box",
									"productDefinition": "1-3 day specific delivery to all U.S. states and territories",
									"processingCategory": "NONSTANDARD",
									"rateIndicator": "FB",
									"destinationEntryFacilityType": "NONE",
									"SKU": "DPFB1XXXXR00700"
								}
							],
							"extraServices": [
								{
									"name": "USPS Tracking",
									"price": 0,
									"extraService": "920",
									"priceType": "RETAIL",
									"warnings": [],
									"SKU": "DXTP0EXXXRX0000"
								}
							]
						},
						{
							"commitment": {
								"name": "2 Days",
								"scheduleDeliveryDate": "2025-06-02",
								"guaranteedDelivery": false
							},
							"totalPrice": 26.3,
							"totalBasePrice": 26.3,
							"rates": [
								{
									"description": "Priority Mail Nonstandard Large Flat Rate Box",
									"startDate": "2025-01-19",
									"endDate": "",
									"price": 26.3,
									"zone": "08",
									"weight": 55,
									"dimensionalWeight": 0,
									"dimWeight": 0,
									"fees": [],
									"priceType": "RETAIL",
									"mailClass": "PRIORITY_MAIL",
									"productName": "Priority Mail Large Flat Rate Box",
									"productDefinition": "1-3 day specific delivery to all U.S. states and territories",
									"processingCategory": "NONSTANDARD",
									"rateIndicator": "PL",
									"destinationEntryFacilityType": "NONE",
									"SKU": "DPFB0XXXXR00700"
								}
							],
							"extraServices": [
								{
									"name": "USPS Tracking",
									"price": 0,
									"extraService": "920",
									"priceType": "RETAIL",
									"warnings": [],
									"SKU": "DXTP0EXXXRX0000"
								}
							]
						},
						{
							"commitment": {
								"name": "2 Days",
								"scheduleDeliveryDate": "2025-06-02",
								"guaranteedDelivery": false
							},
							"totalPrice": 25.05,
							"totalBasePrice": 25.05,
							"rates": [
								{
									"description": "Priority Mail Nonstandard Large Flat Rate Box APO/FPO/DPO",
									"startDate": "2025-01-19",
									"endDate": "",
									"price": 25.05,
									"zone": "08",
									"weight": 55,
									"dimensionalWeight": 0,
									"dimWeight": 0,
									"fees": [],
									"priceType": "RETAIL",
									"mailClass": "PRIORITY_MAIL",
									"productName": "Priority Mail Large Flat Rate APO/FPO/DPO",
									"productDefinition": "1-3 day specific delivery to all U.S. states and territories",
									"processingCategory": "NONSTANDARD",
									"rateIndicator": "PM",
									"destinationEntryFacilityType": "NONE",
									"SKU": "DPFB3XXXXR00700"
								}
							],
							"extraServices": [
								{
									"name": "USPS Tracking",
									"price": 0,
									"extraService": "920",
									"priceType": "RETAIL",
									"warnings": [],
									"SKU": "DXTP0EXXXRX0000"
								}
							]
						},
						{
							"commitment": {
								"name": "2 Days",
								"scheduleDeliveryDate": "2025-06-02",
								"guaranteedDelivery": false
							},
							"totalPrice": 184,
							"totalBasePrice": 184,
							"rates": [
								{
									"description": "Priority Mail Nonstandard Single-piece",
									"startDate": "2025-01-19",
									"endDate": "",
									"price": 184,
									"zone": "08",
									"weight": 55,
									"dimensionalWeight": 0,
									"dimWeight": 0,
									"fees": [],
									"priceType": "RETAIL",
									"mailClass": "PRIORITY_MAIL",
									"productName": "Priority Mail",
									"productDefinition": "1-3 day specific delivery to all U.S. states and territories",
									"processingCategory": "NONSTANDARD",
									"rateIndicator": "SP",
									"destinationEntryFacilityType": "NONE",
									"SKU": "DPXX0XXXXR08550"
								}
							],
							"extraServices": [
								{
									"name": "USPS Tracking",
									"price": 0,
									"extraService": "920",
									"priceType": "RETAIL",
									"warnings": [],
									"SKU": "DXTP0EXXXRX0000"
								}
							]
						}
					]
				},
				{
					"mailClass": "USPS_GROUND_ADVANTAGE",
					"rateOptions": [
						{
							"commitment": {
								"name": "4 Days",
								"scheduleDeliveryDate": "2025-06-03",
								"guaranteedDelivery": false
							},
							"totalPrice": 151.85,
							"totalBasePrice": 151.85,
							"rates": [
								{
									"description": "USPS Ground Advantage Nonstandard Single-piece",
									"startDate": "2025-01-19",
									"endDate": "",
									"price": 151.85,
									"zone": "08",
									"weight": 55,
									"dimensionalWeight": 0,
									"dimWeight": 0,
									"fees": [],
									"priceType": "RETAIL",
									"mailClass": "USPS_GROUND_ADVANTAGE",
									"productName": "USPS Ground Advantage",
									"productDefinition": "2-5 day specific delivery, perfect for packages weighing 1 ounce up to 70 lbs",
									"processingCategory": "NONSTANDARD",
									"rateIndicator": "SP",
									"destinationEntryFacilityType": "NONE",
									"SKU": "DUXP0XXXXR08550"
								}
							],
							"extraServices": [
								{
									"name": "USPS Tracking",
									"price": 0,
									"extraService": "920",
									"priceType": "RETAIL",
									"warnings": [],
									"SKU": "DXTU0EXXXRX0000"
								}
							]
						}
					]
				},
				{
					"mailClass": "MEDIA_MAIL",
					"rateOptions": [
						{
							"commitment": {
								"name": "7 Days",
								"scheduleDeliveryDate": "2025-06-06",
								"guaranteedDelivery": false
							},
							"totalPrice": 45.13,
							"totalBasePrice": 45.13,
							"rates": [
								{
									"description": "Media Mail Nonstandard Single-piece",
									"startDate": "2025-01-19",
									"endDate": "",
									"price": 45.13,
									"zone": "08",
									"weight": 55,
									"dimensionalWeight": 0,
									"dimWeight": 0,
									"fees": [],
									"priceType": "RETAIL",
									"mailClass": "MEDIA_MAIL",
									"productName": "",
									"productDefinition": "",
									"processingCategory": "NONSTANDARD",
									"rateIndicator": "SP",
									"destinationEntryFacilityType": "NONE",
									"SKU": "DMXX0XXXUR00550"
								}
							],
							"extraServices": [
								{
									"name": "USPS Tracking",
									"price": 0,
									"extraService": "920",
									"priceType": "RETAIL",
									"warnings": [],
									"SKU": "DXTM0EXXXRX0000"
								}
							]
						}
					]
				}
			],
			"priceType": "RETAIL"
		}
	]
}
"""
