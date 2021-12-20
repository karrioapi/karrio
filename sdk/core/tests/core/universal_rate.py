import unittest
from purplship.core.utils import DP, Serializable
from purplship.core.models import RateRequest
from purplship.universal.mappers.rating_proxy import (
    RatingMixinSettings,
    RatingMixinProxy,
)


class TestUniversalRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.settings = RatingMixinSettings(**settings_data)
        self.proxy = RatingMixinProxy(self.settings)

    def test_rate_without_service_selection_request(self):
        RateRequestWithoutSelection = Serializable(RateRequest(**rate_request_data))
        response_data = self.proxy.get_rates(RateRequestWithoutSelection)

        self.assertListEqual(
            DP.to_dict(response_data.deserialize()),
            ParsedRateResponseWithoutSelection,
        )

    def test_rate_standard_service_request(self):
        RateRequestStandardService = Serializable(
            RateRequest(**{**rate_request_data, "services": ["carrier_standard"]})
        )
        response_data = self.proxy.get_rates(RateRequestStandardService)

        self.assertListEqual(
            DP.to_dict(response_data.deserialize()),
            ParsedRateResponseStandardService,
        )

    def test_rate_high_weight_request(self):
        RateRequestHighWeight = Serializable(
            RateRequest(
                **{
                    **rate_request_data,
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

        self.assertListEqual(
            DP.to_dict(response_data.deserialize()),
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

        self.assertListEqual(
            DP.to_dict(response_data.deserialize()),
            ParsedInternationalRateResponseService,
        )

    def test_international_high_weight_rate_request(self):
        InternationalRateRequestHighWeight = Serializable(
            RateRequest(
                **{
                    **rate_request_data,
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

        self.assertListEqual(
            DP.to_dict(response_data.deserialize()),
            ParsedInternationalRateResponseHighWeightService,
        )


if __name__ == "__main__":
    unittest.main()


settings_data = {
    "carrier_id": "universal",
    "services": [
        {
            "service_name": "Standard",
            "service_code": "carrier_standard",
            "cost": "10.00",
            "currency": "USD",
            "max_weight": 5.0,
            "weight_unit": "LB",
            "domicile": True,
            "international": False,
        },
        {
            "service_name": "Premium",
            "service_code": "carrier_premium",
            "cost": "15.00",
            "currency": "USD",
            "max_weight": 8.0,
            "weight_unit": "LB",
            "domicile": True,
            "international": False,
        },
        {
            "service_name": "International Parcel",
            "service_code": "carrier_interational_parcel",
            "cost": "25.00",
            "currency": "USD",
            "max_weight": 5.0,
            "weight_unit": "LB",
            "domicile": False,
            "international": True,
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
            "cost": "10.00",
            "currency": "USD",
            "domicile": True,
            "international": False,
            "max_weight": 5.0,
            "service_code": "carrier_standard",
            "service_name": "Standard",
            "weight_unit": "LB",
            "active": True,
        },
        {
            "cost": "15.00",
            "currency": "USD",
            "domicile": True,
            "international": False,
            "max_weight": 8.0,
            "service_code": "carrier_premium",
            "service_name": "Premium",
            "weight_unit": "LB",
            "active": True,
        },
    ],
    [],
]

ParsedRateResponseStandardService = [
    [
        {
            "cost": "10.00",
            "currency": "USD",
            "domicile": True,
            "international": False,
            "max_weight": 5.0,
            "service_code": "carrier_standard",
            "service_name": "Standard",
            "weight_unit": "LB",
            "active": True,
        },
    ],
    [],
]

ParsedRateResponseHighWeightService = [
    [
        {
            "cost": "15.00",
            "currency": "USD",
            "domicile": True,
            "international": False,
            "max_weight": 8.0,
            "service_code": "carrier_premium",
            "service_name": "Premium",
            "weight_unit": "LB",
            "active": True,
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
            "cost": "25.00",
            "currency": "USD",
            "domicile": False,
            "international": True,
            "max_weight": 5.0,
            "service_code": "carrier_interational_parcel",
            "service_name": "International Parcel",
            "weight_unit": "LB",
            "active": True,
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
