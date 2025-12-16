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

    def test_weight_tiered_pricing_light_package(self):
        """Test that correct weight tier is selected for light package (0.3kg)."""
        settings_with_tiers = RatingMixinSettings(**weight_tiered_settings_data)
        proxy = RatingMixinProxy(settings_with_tiers)

        LightPackageRequest = Serializable(
            RateRequest(
                **{
                    **rate_request_data,
                    "parcels": [
                        {
                            **rate_request_data["parcels"][0],
                            "weight": 0.66,  # 0.3kg in LB
                            "weight_unit": "LB",
                        }
                    ],
                }
            )
        )
        response_data = proxy.get_rates(LightPackageRequest)
        rates = parse_rate_response(response_data, settings_with_tiers)

        self.assertListEqual(
            DP.to_dict(rates),
            ParsedWeightTierLightPackage,
        )

    def test_weight_tiered_pricing_medium_package(self):
        """Test that correct weight tier is selected for medium package (0.75kg)."""
        settings_with_tiers = RatingMixinSettings(**weight_tiered_settings_data)
        proxy = RatingMixinProxy(settings_with_tiers)

        MediumPackageRequest = Serializable(
            RateRequest(
                **{
                    **rate_request_data,
                    "parcels": [
                        {
                            **rate_request_data["parcels"][0],
                            "weight": 1.65,  # 0.75kg in LB
                            "weight_unit": "LB",
                        }
                    ],
                }
            )
        )
        response_data = proxy.get_rates(MediumPackageRequest)
        rates = parse_rate_response(response_data, settings_with_tiers)

        self.assertListEqual(
            DP.to_dict(rates),
            ParsedWeightTierMediumPackage,
        )

    def test_weight_tiered_pricing_heavy_package(self):
        """Test that correct weight tier is selected for heavy package (1.5kg)."""
        settings_with_tiers = RatingMixinSettings(**weight_tiered_settings_data)
        proxy = RatingMixinProxy(settings_with_tiers)

        HeavyPackageRequest = Serializable(
            RateRequest(
                **{
                    **rate_request_data,
                    "parcels": [
                        {
                            **rate_request_data["parcels"][0],
                            "weight": 3.31,  # 1.5kg in LB
                            "weight_unit": "LB",
                        }
                    ],
                }
            )
        )
        response_data = proxy.get_rates(HeavyPackageRequest)
        rates = parse_rate_response(response_data, settings_with_tiers)

        self.assertListEqual(
            DP.to_dict(rates),
            ParsedWeightTierHeavyPackage,
        )

    def test_weight_tier_boundary_exact_match(self):
        """Test weight exactly on tier boundary (0.5kg = max of tier 1, min of tier 2)."""
        settings_with_tiers = RatingMixinSettings(**weight_tiered_settings_data)
        proxy = RatingMixinProxy(settings_with_tiers)

        BoundaryPackageRequest = Serializable(
            RateRequest(
                **{
                    **rate_request_data,
                    "parcels": [
                        {
                            **rate_request_data["parcels"][0],
                            "weight": 1.10,  # 0.5kg in LB (exactly)
                            "weight_unit": "LB",
                        }
                    ],
                }
            )
        )
        response_data = proxy.get_rates(BoundaryPackageRequest)
        rates = parse_rate_response(response_data, settings_with_tiers)

        # Should match tier 2 (0.5-1.0kg) not tier 1 (0-0.5kg)
        self.assertListEqual(
            DP.to_dict(rates),
            ParsedWeightTierBoundaryPackage,
        )

    def test_zone_specificity_city_over_country(self):
        """Test that city-specific zone is preferred over country-only zone."""
        settings_with_specific_zones = RatingMixinSettings(
            **zone_specificity_settings_data
        )
        proxy = RatingMixinProxy(settings_with_specific_zones)

        CitySpecificRequest = Serializable(
            RateRequest(
                **{
                    **rate_request_data,
                    "recipient": {
                        "city": "Montreal",
                        "postal_code": "H3A 1A1",
                        "country_code": "CA",
                    },
                }
            )
        )
        response_data = proxy.get_rates(CitySpecificRequest)
        rates = parse_rate_response(response_data, settings_with_specific_zones)

        # Should use city rate (12.00) not country rate (15.00)
        self.assertListEqual(
            DP.to_dict(rates),
            ParsedZoneSpecificityCityMatch,
        )

    def test_no_matching_zone_for_weight(self):
        """Test that no rate is returned when package exceeds all zone weight limits."""
        settings_with_tiers = RatingMixinSettings(**weight_tiered_settings_data)
        proxy = RatingMixinProxy(settings_with_tiers)

        OverweightRequest = Serializable(
            RateRequest(
                **{
                    **rate_request_data,
                    "parcels": [
                        {
                            **rate_request_data["parcels"][0],
                            "weight": 11.0,  # 5kg - exceeds all tiers
                            "weight_unit": "LB",
                        }
                    ],
                }
            )
        )
        response_data = proxy.get_rates(OverweightRequest)
        rates = parse_rate_response(response_data, settings_with_tiers)

        # Should return no rates
        self.assertListEqual(
            DP.to_dict(rates),
            ParsedNoMatchingZone,
        )

    def test_rate_request_with_weight_only(self):
        """Test that rates are returned when only weight and weight_unit are provided.

        When dimensions are absent, validation should assume they are valid.
        This tests the fix for the issue where rates were not returned when
        width/height/length were absent even though the service had dimension restrictions.
        """
        settings_with_dimensions = RatingMixinSettings(**settings_with_dimension_restrictions)
        proxy = RatingMixinProxy(settings_with_dimensions)

        WeightOnlyRequest = Serializable(
            RateRequest(
                **{
                    **rate_request_data,
                    "parcels": [
                        {
                            "weight": 2.0,
                            "weight_unit": "LB",
                            # No dimensions provided - should still return rates
                        }
                    ],
                }
            )
        )
        response_data = proxy.get_rates(WeightOnlyRequest)
        rates = parse_rate_response(response_data, settings_with_dimensions)

        # Should return rates even without dimensions
        self.assertListEqual(
            DP.to_dict(rates),
            ParsedRateResponseWeightOnly,
        )

    def test_rate_with_fixed_surcharges(self):
        """Test that fixed surcharges are correctly applied to base rate."""
        settings_with_surcharges = RatingMixinSettings(**settings_with_fixed_surcharges)
        proxy = RatingMixinProxy(settings_with_surcharges)

        request = Serializable(RateRequest(**rate_request_data))
        response_data = proxy.get_rates(request)
        rates = parse_rate_response(response_data, settings_with_surcharges)

        self.assertListEqual(
            DP.to_dict(rates),
            ParsedRateResponseFixedSurcharges,
        )

    def test_rate_with_percentage_surcharges(self):
        """Test that percentage surcharges are correctly calculated from base rate."""
        settings_with_surcharges = RatingMixinSettings(**settings_with_percentage_surcharges)
        proxy = RatingMixinProxy(settings_with_surcharges)

        request = Serializable(RateRequest(**rate_request_data))
        response_data = proxy.get_rates(request)
        rates = parse_rate_response(response_data, settings_with_surcharges)

        self.assertListEqual(
            DP.to_dict(rates),
            ParsedRateResponsePercentageSurcharges,
        )

    def test_rate_with_mixed_surcharges(self):
        """Test that mixed fixed and percentage surcharges are correctly applied."""
        settings_with_surcharges = RatingMixinSettings(**settings_with_mixed_surcharges)
        proxy = RatingMixinProxy(settings_with_surcharges)

        request = Serializable(RateRequest(**rate_request_data))
        response_data = proxy.get_rates(request)
        rates = parse_rate_response(response_data, settings_with_surcharges)

        self.assertListEqual(
            DP.to_dict(rates),
            ParsedRateResponseMixedSurcharges,
        )

    def test_rate_with_no_surcharges(self):
        """Test that rates work correctly when service has no surcharges defined."""
        # Using standard settings_data which has no surcharges
        settings_no_surcharges = RatingMixinSettings(**settings_data)
        proxy = RatingMixinProxy(settings_no_surcharges)

        request = Serializable(
            RateRequest(**{**rate_request_data, "services": ["carrier_standard"]})
        )
        response_data = proxy.get_rates(request)
        rates = parse_rate_response(response_data, settings_no_surcharges)

        # Should return rate without any surcharges
        self.assertListEqual(
            DP.to_dict(rates),
            ParsedRateResponseStandardService,
        )

    def test_rate_with_multiple_services_different_surcharges(self):
        """Test that different services can have different surcharge configurations."""
        settings_multiple = RatingMixinSettings(**settings_multiple_services_surcharges)
        proxy = RatingMixinProxy(settings_multiple)

        request = Serializable(RateRequest(**rate_request_data))
        response_data = proxy.get_rates(request)
        rates = parse_rate_response(response_data, settings_multiple)

        self.assertListEqual(
            DP.to_dict(rates),
            ParsedRateResponseMultipleServicesSurcharges,
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
            "meta": {
                "service_name": "Standard",
                "shipping_charges": 10.0,
                "shipping_currency": "USD",
            },
            "service": "carrier_standard",
            "total_charge": 10.0,
            "extra_charges": [
                {"amount": 10.0, "currency": "USD", "name": "Base Charge"}
            ],
        },
        {
            "carrier_id": "universal",
            "currency": "USD",
            "meta": {
                "service_name": "Premium",
                "shipping_charges": 15.0,
                "shipping_currency": "USD",
            },
            "service": "carrier_premium",
            "total_charge": 15.0,
            "extra_charges": [
                {"amount": 15.0, "currency": "USD", "name": "Base Charge"}
            ],
        },
    ],
    [],
]

ParsedRateResponseStandardService = [
    [
        {
            "carrier_id": "universal",
            "currency": "USD",
            "meta": {
                "service_name": "Standard",
                "shipping_charges": 10.0,
                "shipping_currency": "USD",
            },
            "service": "carrier_standard",
            "total_charge": 10.0,
            "extra_charges": [
                {"amount": 10.0, "currency": "USD", "name": "Base Charge"}
            ],
        }
    ],
    [],
]

ParsedRateResponseHighWeightService = [
    [
        {
            "carrier_id": "universal",
            "currency": "USD",
            "meta": {
                "service_name": "Premium",
                "shipping_charges": 15.0,
                "shipping_currency": "USD",
            },
            "service": "carrier_premium",
            "total_charge": 15.0,
            "extra_charges": [
                {"amount": 15.0, "currency": "USD", "name": "Base Charge"}
            ],
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
            "meta": {
                "service_name": "International Parcel",
                "shipping_charges": 25.0,
                "shipping_currency": "USD",
            },
            "service": "carrier_interational_parcel",
            "total_charge": 25.0,
            "extra_charges": [
                {"amount": 25.0, "currency": "USD", "name": "Base Charge"}
            ],
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
            "extra_charges": [
                {"amount": 20.0, "currency": "USD", "name": "Base Charge"}
            ],
            "meta": {
                "service_name": "Standard",
                "shipping_charges": 10.0,
                "shipping_currency": "USD",
            },
            "service": "carrier_standard",
            "total_charge": 20.0,
        },
        {
            "carrier_id": "universal",
            "currency": "USD",
            "extra_charges": [
                {"amount": 30.0, "currency": "USD", "name": "Base Charge"}
            ],
            "meta": {
                "service_name": "Premium",
                "shipping_charges": 15.0,
                "shipping_currency": "USD",
            },
            "service": "carrier_premium",
            "total_charge": 30.0,
        },
    ],
    [],
]

# Weight-tiered pricing test data
weight_tiered_settings_data = {
    "carrier_id": "universal",
    "services": [
        {
            "service_name": "Weight Tiered Service",
            "service_code": "carrier_weight_tiered",
            "currency": "USD",
            "weight_unit": "KG",
            "domicile": True,
            "international": False,
            "zones": [
                {
                    "label": "Tier 1 (0-0.5kg)",
                    "country_codes": ["CA"],
                    "min_weight": 0.0,
                    "max_weight": 0.5,
                    "rate": 5.00,
                },
                {
                    "label": "Tier 2 (0.5-1.0kg)",
                    "country_codes": ["CA"],
                    "min_weight": 0.5,
                    "max_weight": 1.0,
                    "rate": 8.00,
                },
                {
                    "label": "Tier 3 (1.0-2.0kg)",
                    "country_codes": ["CA"],
                    "min_weight": 1.0,
                    "max_weight": 2.0,
                    "rate": 12.00,
                },
            ],
        },
    ],
}

ParsedWeightTierLightPackage = [
    [
        {
            "carrier_id": "universal",
            "currency": "USD",
            "meta": {
                "service_name": "Weight Tiered Service",
                "shipping_charges": 5.0,
                "shipping_currency": "USD",
            },
            "service": "carrier_weight_tiered",
            "total_charge": 5.0,  # Tier 1: 0-0.5kg
            "extra_charges": [
                {"amount": 5.0, "currency": "USD", "name": "Base Charge"}
            ],
        }
    ],
    [],
]

ParsedWeightTierMediumPackage = [
    [
        {
            "carrier_id": "universal",
            "currency": "USD",
            "meta": {
                "service_name": "Weight Tiered Service",
                "shipping_charges": 8.0,
                "shipping_currency": "USD",
            },
            "service": "carrier_weight_tiered",
            "total_charge": 8.0,  # Tier 2: 0.5-1.0kg
            "extra_charges": [
                {"amount": 8.0, "currency": "USD", "name": "Base Charge"}
            ],
        }
    ],
    [],
]

ParsedWeightTierHeavyPackage = [
    [
        {
            "carrier_id": "universal",
            "currency": "USD",
            "meta": {
                "service_name": "Weight Tiered Service",
                "shipping_charges": 12.0,
                "shipping_currency": "USD",
            },
            "service": "carrier_weight_tiered",
            "total_charge": 12.0,  # Tier 3: 1.0-2.0kg
            "extra_charges": [
                {"amount": 12.0, "currency": "USD", "name": "Base Charge"}
            ],
        }
    ],
    [],
]

ParsedWeightTierBoundaryPackage = [
    [
        {
            "carrier_id": "universal",
            "currency": "USD",
            "meta": {
                "service_name": "Weight Tiered Service",
                "shipping_charges": 8.0,
                "shipping_currency": "USD",
            },
            "service": "carrier_weight_tiered",
            "total_charge": 8.0,  # Tier 2: 0.5-1.0kg (0.5 is inclusive min of tier 2)
            "extra_charges": [
                {"amount": 8.0, "currency": "USD", "name": "Base Charge"}
            ],
        }
    ],
    [],
]

ParsedNoMatchingZone = [
    [],  # No rates - weight exceeds all tiers
    [],
]  # type: ignore

# Zone specificity test data
zone_specificity_settings_data = {
    "carrier_id": "universal",
    "services": [
        {
            "service_name": "Zone Specific Service",
            "service_code": "carrier_zone_specific",
            "currency": "USD",
            "weight_unit": "LB",
            "domicile": True,
            "international": False,
            "zones": [
                {
                    "label": "Country Zone",
                    "country_codes": ["CA"],
                    "rate": 15.00,
                },
                {
                    "label": "City Zone (Montreal)",
                    "country_codes": ["CA"],
                    "cities": ["Montreal"],
                    "rate": 12.00,
                },
            ],
        },
    ],
}

ParsedZoneSpecificityCityMatch = [
    [
        {
            "carrier_id": "universal",
            "currency": "USD",
            "meta": {
                "service_name": "Zone Specific Service",
                "shipping_charges": 12.0,
                "shipping_currency": "USD",
            },
            "service": "carrier_zone_specific",
            "total_charge": 12.0,  # City-specific rate, not country rate
            "extra_charges": [
                {"amount": 12.0, "currency": "USD", "name": "Base Charge"}
            ],
        }
    ],
    [],
]

# Settings with dimension restrictions test data
settings_with_dimension_restrictions = {
    "carrier_id": "universal",
    "services": [
        {
            "service_name": "Dimensional Service",
            "service_code": "carrier_dimensional",
            "currency": "USD",
            "max_weight": 5.0,
            "weight_unit": "LB",
            "max_length": 20.0,
            "max_width": 15.0,
            "max_height": 10.0,
            "dimension_unit": "IN",
            "domicile": True,
            "international": False,
            "zones": [{"rate": 18.00}],
        },
    ],
}

ParsedRateResponseWeightOnly = [
    [
        {
            "carrier_id": "universal",
            "currency": "USD",
            "meta": {
                "service_name": "Dimensional Service",
                "shipping_charges": 18.0,
                "shipping_currency": "USD",
            },
            "service": "carrier_dimensional",
            "total_charge": 18.0,
            "extra_charges": [
                {"amount": 18.0, "currency": "USD", "name": "Base Charge"}
            ],
        }
    ],
    [],
]


# =============================================================================
# SURCHARGE TEST DATA
# =============================================================================

# Settings with fixed surcharges
settings_with_fixed_surcharges = {
    "carrier_id": "universal",
    "services": [
        {
            "service_name": "Standard with Fixed Surcharges",
            "service_code": "carrier_fixed_surcharge",
            "currency": "USD",
            "max_weight": 5.0,
            "weight_unit": "LB",
            "domicile": True,
            "international": False,
            "zones": [{"rate": 10.00}],
            "surcharges": [
                {"name": "Fuel Surcharge", "amount": 2.50, "surcharge_type": "fixed"},
                {"name": "Handling Fee", "amount": 1.50, "surcharge_type": "fixed"},
            ],
        },
    ],
}

# Expected: base $10 + fuel $2.50 + handling $1.50 = $14.00
ParsedRateResponseFixedSurcharges = [
    [
        {
            "carrier_id": "universal",
            "currency": "USD",
            "meta": {
                "service_name": "Standard with Fixed Surcharges",
                "shipping_charges": 10.0,
                "shipping_currency": "USD",
            },
            "service": "carrier_fixed_surcharge",
            "total_charge": 14.0,
            "extra_charges": [
                {"amount": 10.0, "currency": "USD", "name": "Base Charge"},
                {"amount": 2.5, "currency": "USD", "name": "Fuel Surcharge"},
                {"amount": 1.5, "currency": "USD", "name": "Handling Fee"},
            ],
        }
    ],
    [],
]


# Settings with percentage surcharges
settings_with_percentage_surcharges = {
    "carrier_id": "universal",
    "services": [
        {
            "service_name": "Standard with Percentage Surcharges",
            "service_code": "carrier_pct_surcharge",
            "currency": "USD",
            "max_weight": 5.0,
            "weight_unit": "LB",
            "domicile": True,
            "international": False,
            "zones": [{"rate": 20.00}],
            "surcharges": [
                {"name": "Fuel Surcharge", "amount": 15, "surcharge_type": "percentage"},
            ],
        },
    ],
}

# Expected: base $20 + fuel 15% ($3) = $23.00
ParsedRateResponsePercentageSurcharges = [
    [
        {
            "carrier_id": "universal",
            "currency": "USD",
            "meta": {
                "service_name": "Standard with Percentage Surcharges",
                "shipping_charges": 20.0,
                "shipping_currency": "USD",
            },
            "service": "carrier_pct_surcharge",
            "total_charge": 23.0,
            "extra_charges": [
                {"amount": 20.0, "currency": "USD", "name": "Base Charge"},
                {"amount": 3.0, "currency": "USD", "name": "Fuel Surcharge"},
            ],
        }
    ],
    [],
]


# Settings with mixed surcharges
settings_with_mixed_surcharges = {
    "carrier_id": "universal",
    "services": [
        {
            "service_name": "Standard with Mixed Surcharges",
            "service_code": "carrier_mixed_surcharge",
            "currency": "USD",
            "max_weight": 5.0,
            "weight_unit": "LB",
            "domicile": True,
            "international": False,
            "zones": [{"rate": 100.00}],
            "surcharges": [
                {"name": "Fuel Surcharge", "amount": 10, "surcharge_type": "percentage"},
                {"name": "Residential Fee", "amount": 3.50, "surcharge_type": "fixed"},
                {"name": "Peak Season", "amount": 5, "surcharge_type": "percentage"},
            ],
        },
    ],
}

# Expected: base $100 + fuel 10% ($10) + residential $3.50 + peak 5% ($5) = $118.50
ParsedRateResponseMixedSurcharges = [
    [
        {
            "carrier_id": "universal",
            "currency": "USD",
            "meta": {
                "service_name": "Standard with Mixed Surcharges",
                "shipping_charges": 100.0,
                "shipping_currency": "USD",
            },
            "service": "carrier_mixed_surcharge",
            "total_charge": 118.5,
            "extra_charges": [
                {"amount": 100.0, "currency": "USD", "name": "Base Charge"},
                {"amount": 10.0, "currency": "USD", "name": "Fuel Surcharge"},
                {"amount": 3.5, "currency": "USD", "name": "Residential Fee"},
                {"amount": 5.0, "currency": "USD", "name": "Peak Season"},
            ],
        }
    ],
    [],
]


# Settings with multiple services having different surcharges
settings_multiple_services_surcharges = {
    "carrier_id": "universal",
    "services": [
        {
            "service_name": "Economy",
            "service_code": "carrier_economy",
            "currency": "USD",
            "max_weight": 5.0,
            "weight_unit": "LB",
            "domicile": True,
            "international": False,
            "zones": [{"rate": 8.00}],
            "surcharges": [
                {"name": "Fuel Surcharge", "amount": 1.00, "surcharge_type": "fixed"},
            ],
        },
        {
            "service_name": "Express",
            "service_code": "carrier_express",
            "currency": "USD",
            "max_weight": 5.0,
            "weight_unit": "LB",
            "domicile": True,
            "international": False,
            "zones": [{"rate": 15.00}],
            "surcharges": [
                {"name": "Fuel Surcharge", "amount": 12.5, "surcharge_type": "percentage"},
                {"name": "Priority Handling", "amount": 2.00, "surcharge_type": "fixed"},
            ],
        },
    ],
}

# Expected:
# - Economy: $8 + fuel $1 = $9
# - Express: $15 + fuel 12.5% ($1.88) + handling $2 = $18.88
ParsedRateResponseMultipleServicesSurcharges = [
    [
        {
            "carrier_id": "universal",
            "currency": "USD",
            "meta": {
                "service_name": "Economy",
                "shipping_charges": 8.0,
                "shipping_currency": "USD",
            },
            "service": "carrier_economy",
            "total_charge": 9.0,
            "extra_charges": [
                {"amount": 8.0, "currency": "USD", "name": "Base Charge"},
                {"amount": 1.0, "currency": "USD", "name": "Fuel Surcharge"},
            ],
        },
        {
            "carrier_id": "universal",
            "currency": "USD",
            "meta": {
                "service_name": "Express",
                "shipping_charges": 15.0,
                "shipping_currency": "USD",
            },
            "service": "carrier_express",
            "total_charge": 18.88,
            "extra_charges": [
                {"amount": 15.0, "currency": "USD", "name": "Base Charge"},
                {"amount": 1.88, "currency": "USD", "name": "Fuel Surcharge"},
                {"amount": 2.0, "currency": "USD", "name": "Priority Handling"},
            ],
        },
    ],
    [],
]
