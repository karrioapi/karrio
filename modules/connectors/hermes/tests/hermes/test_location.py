"""Hermes ParcelShop finder (karrio.Location) tests. See SPECS.md."""

import logging
import unittest
from unittest.mock import patch

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.hermes as provider
import karrio.sdk as karrio

from .fixture import gateway

logger = logging.getLogger(__name__)


class TestHermesLocationRequest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_location_request_by_address(self):
        request = gateway.mapper.create_location_request(
            models.LocationRequest(
                address=models.Address(
                    address_line1="Essener Bogen 1",
                    city="Hamburg",
                    postal_code="22419",
                    country_code="DE",
                ),
                radius_km=20,
                max_results=10,
            )
        )
        self.assertEqual(request.ctx["endpoint"], "findParcelShopByAddress")
        self.assertDictEqual(
            request.serialize(),
            {
                "country": "DE",
                "maxDist": 20,
                "maxResult": 10,
                "city": "Hamburg",
                "zipCode": "22419",
                "street": "Essener Bogen",
                "houseNumber": "1",
            },
        )

    def test_location_request_by_coordinates(self):
        request = gateway.mapper.create_location_request(
            models.LocationRequest(
                address=models.Address(country_code="DE"),
                options={"lat": "53.5896", "lng": "10.0716"},
            )
        )
        self.assertEqual(request.ctx["endpoint"], "findParcelShopByLocation")
        self.assertDictEqual(
            request.serialize(),
            {"country": "DE", "lat": "53.5896", "lng": "10.0716"},
        )

    def test_location_request_by_address_string(self):
        request = gateway.mapper.create_location_request(
            models.LocationRequest(address=models.Address(postal_code="22419", country_code="DE"))
        )
        self.assertEqual(request.ctx["endpoint"], "findParcelShopByAddressString")
        self.assertDictEqual(
            request.serialize(),
            {"country": "DE", "adressSearchString": "22419"},
        )


class TestHermesLocation(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_get_locations_proxy_call(self):
        request = gateway.mapper.create_location_request(
            models.LocationRequest(
                address=models.Address(
                    address_line1="Essener Bogen 1",
                    city="Hamburg",
                    postal_code="22419",
                    country_code="DE",
                )
            )
        )
        with patch("karrio.mappers.hermes.proxy.lib.request") as mock:
            mock.return_value = ParcelShopSearchResponse
            gateway.proxy.get_locations(request)

        self.assertIn("/psfinder-api/findParcelShopByAddress/?", mock.call_args[1]["url"])
        self.assertEqual(mock.call_args[1]["headers"]["apiKey"], "test-psf-key")

    def test_parse_location_response(self):
        locations, messages = provider.parse_location_response(
            lib.Deserializable(ParcelShopSearchResponse, lib.to_dict),
            gateway.settings,
        )
        self.assertEqual(messages, [])
        self.assertListEqual(lib.to_dict(locations), ParsedLocationResponse)

    def test_location_search_interface(self):
        with patch("karrio.mappers.hermes.proxy.lib.request") as mock:
            mock.return_value = ParcelShopSearchResponse
            locations, messages = (
                karrio.Location.search(
                    models.LocationRequest(
                        address=models.Address(
                            address_line1="Essener Bogen 1",
                            city="Hamburg",
                            postal_code="22419",
                            country_code="DE",
                        )
                    )
                )
                .from_(gateway)
                .parse()
            )

        self.assertEqual(messages, [])
        self.assertEqual(len(locations), 1)
        self.assertEqual(locations[0].location_id, "DE40501")
        self.assertEqual(locations[0].location_type, "parcel_shop")

    def test_get_locations_missing_api_key(self):
        no_key_gateway = karrio.gateway["hermes"].create(
            dict(
                id="hermes_no_psf",
                test_mode=True,
                carrier_id="hermes",
                username="test_user",
                password="test_password",
                client_id="test_client_id",
                client_secret="test_client_secret",
            )
        )
        request = no_key_gateway.mapper.create_location_request(
            models.LocationRequest(address=models.Address(postal_code="22419", country_code="DE"))
        )
        with patch("karrio.mappers.hermes.proxy.lib.request") as mock:
            locations, messages = provider.parse_location_response(
                no_key_gateway.proxy.get_locations(request), no_key_gateway.settings
            )

        mock.assert_not_called()
        self.assertEqual(locations, [])
        self.assertEqual(messages[0].code, "MISSING_PSF_API_KEY")


if __name__ == "__main__":
    unittest.main()


ParcelShopSearchResponse = """[
    {
        "parcelShopNumber": "DE40501",
        "typeID": 0,
        "name": "Hermes PaketShop",
        "description": "Kiosk am Essener Bogen",
        "street": "Essener Bogen",
        "houseNumber": "1a",
        "city": "Hamburg",
        "zip": "22419",
        "countryIsoA2Code": "DE",
        "countryIsoA3Code": "DEU",
        "phone": "040 / 76114143",
        "latitude": 53.5896,
        "longitude": 10.0716,
        "distance": 0.35,
        "openToday": "08:00-18:00",
        "hours": [
            {"weekday": 1, "openFrom": "08:00", "openTil": "18:00"}
        ]
    }
]"""

ParsedLocationResponse = [
    {
        "carrier_id": "hermes",
        "carrier_name": "hermes",
        "location_id": "DE40501",
        "location_type": "parcel_shop",
        "name": "Hermes PaketShop",
        "address": {
            "address_line1": "Essener Bogen 1a",
            "city": "Hamburg",
            "postal_code": "22419",
            "country_code": "DE",
            "phone_number": "040 / 76114143",
            "residential": False,
        },
        "latitude": 53.5896,
        "longitude": 10.0716,
        "distance": 0.35,
        "opening_hours": [{"weekday": 1, "openFrom": "08:00", "openTil": "18:00"}],
    }
]
