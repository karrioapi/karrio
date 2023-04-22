import unittest
from karrio.core.utils import DP, Serializable
from karrio.core.models import RateRequest
from karrio.universal.mappers.rating_proxy import (
    RatingMixinSettings,
    RatingMixinProxy,
)
from karrio.universal.providers.rating.rate import parse_rate_response


class TestUniversalRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.settings = RatingMixinSettings(**settings_data)
        self.proxy = RatingMixinProxy(self.settings)

    def test_rate_without_service_selection_request(self):
        RateRequestWithoutSelection = Serializable(RateRequest(**rate_request_data))
        response_data = self.proxy.get_rates(RateRequestWithoutSelection)
        rates = parse_rate_response(response_data, self.settings)

        self.assertListEqual(
            DP.to_dict(rates),
            ParsedRateResponseWithoutSelection,
        )

    def test_rate_standard_service_request(self):
        RateRequestStandardService = Serializable(
            RateRequest(**{**rate_request_data, "services": ["carrier_standard"]})
        )
        response_data = self.proxy.get_rates(RateRequestStandardService)
        rates = parse_rate_response(response_data, self.settings)

        self.assertListEqual(
            DP.to_dict(rates),
            ParsedRateResponseStandardService,
        )

    def test_rate_high_weight_request(self):
        RateRequestHighWeight = Serializable(
            RateRequest(
                **{
                    **rate_request_data,
                    "services": ["carrier_standard", "carrier_premium"],
                    "parcels": [
                        {
                            **rate_request_data["parcels"][0],
                            "weight": 6.0,
                        }
                    ],
                }
            )
        )
        response_data = self.proxy.get_rates(RateRequestHighWeight)
        rates = parse_rate_response(response_data, self.settings)

        self.assertListEqual(
            DP.to_dict(rates),
            ParsedRateResponseHighWeightService,
        )

    def test_international_rate_request(self):
        InternationalRateRequest = Serializable(
            RateRequest(
                **{
                    **rate_request_data,
                    "recipient": {"postal_code": "11111", "country_code": "US"},
                }
            )
        )
        response_data = self.proxy.get_rates(InternationalRateRequest)
        rates = parse_rate_response(response_data, self.settings)

        self.assertListEqual(
            DP.to_dict(rates),
            ParsedInternationalRateResponseService,
        )

    def test_international_high_weight_rate_request(self):
        InternationalRateRequestHighWeight = Serializable(
            RateRequest(
                **{
                    **rate_request_data,
                    "services": ["carrier_interational_parcel"],
                    "recipient": {"postal_code": "11111", "country_code": "US"},
                    "parcels": [
                        {
                            **rate_request_data["parcels"][0],
                            "weight": 10.0,
                        }
                    ],
                }
            )
        )
        response_data = self.proxy.get_rates(InternationalRateRequestHighWeight)
        rates = parse_rate_response(response_data, self.settings)

        self.assertListEqual(
            DP.to_dict(rates),
            ParsedInternationalRateResponseHighWeightService,
        )

    def test_multi_piece_rate_request(self):
        MultiPieceRateRequest = Serializable(
            RateRequest(
                **{
                    **rate_request_data,
                    "parcels": [
                        rate_request_data["parcels"][0],
                        rate_request_data["parcels"][0],
                    ],
                }
            )
        )
        response_data = self.proxy.get_rates(MultiPieceRateRequest)
        rates = parse_rate_response(response_data, self.settings)

        self.assertListEqual(
            DP.to_dict(rates),
            ParsedMultiPieceRateResponse,
        )


if __name__ == "__main__":
    unittest.main()


settings_data = {
    "carrier_id": "universal",
    "services": [
        {
            "service_name": "Standard",
            "service_code": "carrier_standard",
            "currency": "USD",
            "max_weight": 5.0,
            "weight_unit": "LB",
            "domicile": True,
            "international": False,
            "zones": [{"rate": 10.00}],
        },
        {
            "service_name": "Premium",
            "service_code": "carrier_premium",
            "currency": "USD",
            "max_weight": 8.0,
            "weight_unit": "LB",
            "domicile": True,
            "international": False,
            "zones": [{"rate": 15.00}],
        },
        {
            "service_name": "International Parcel",
            "service_code": "carrier_interational_parcel",
            "currency": "USD",
            "max_weight": 5.0,
            "weight_unit": "LB",
            "domicile": False,
            "international": True,
            "zones": [{"rate": 25.00}],
        },
    ],
}

rate_request_data = {
    "shipper": {"postal_code": "H8Z 2Z3", "country_code": "CA"},
    "recipient": {"postal_code": "h8z2V4", "country_code": "CA"},
    "parcels": [
        {
            "height": 3.0,
            "length": 5.0,
            "width": 3.0,
            "weight": 4.0,
            "dimension_unit": "IN",
            "weight_unit": "LB",
        }
    ],
    "services": [],
}


ParsedRateResponseWithoutSelection = [
    [
        {
            "carrier_id": "universal",
            "currency": "USD",
            "meta": {"service_name": "Standard"},
            "service": "carrier_standard",
            "total_charge": 10.0,
        },
        {
            "carrier_id": "universal",
            "currency": "USD",
            "meta": {"service_name": "Premium"},
            "service": "carrier_premium",
            "total_charge": 15.0,
        },
    ],
    [],
]

ParsedRateResponseStandardService = [
    [
        {
            "carrier_id": "universal",
            "currency": "USD",
            "meta": {"service_name": "Standard"},
            "service": "carrier_standard",
            "total_charge": 10.0,
        }
    ],
    [],
]

ParsedRateResponseHighWeightService = [
    [
        {
            "carrier_id": "universal",
            "currency": "USD",
            "meta": {"service_name": "Premium"},
            "service": "carrier_premium",
            "total_charge": 15.0,
        }
    ],
    [
        {
            "carrier_id": "universal",
            "code": "invalid_weight",
            "message": "the weight exceeds service carrier_standard max weight",
        }
    ],
]

ParsedInternationalRateResponseService = [
    [
        {
            "carrier_id": "universal",
            "currency": "USD",
            "meta": {"service_name": "International Parcel"},
            "service": "carrier_interational_parcel",
            "total_charge": 25.0,
        }
    ],
    [],
]

ParsedInternationalRateResponseHighWeightService = [
    [],
    [
        {
            "carrier_id": "universal",
            "code": "invalid_weight",
            "message": "the weight exceeds service carrier_interational_parcel max weight",
        }
    ],
]

ParsedMultiPieceRateResponse = [
    [
        {
            "carrier_id": "universal",
            "currency": "USD",
            "meta": {"service_name": "Standard"},
            "service": "carrier_standard",
            "total_charge": 20.0,
        },
        {
            "carrier_id": "universal",
            "currency": "USD",
            "meta": {"service_name": "Premium"},
            "service": "carrier_premium",
            "total_charge": 30.0,
        },
    ],
    [],
]
