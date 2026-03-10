# Testing Patterns

Guide for writing carrier integration tests using unittest. Every feature requires the 4-method test pattern.

## Test Fixture (`tests/[carrier]/fixture.py`)

```python
import karrio.sdk as karrio
import karrio.lib as lib

# Mock auth cache (for OAuth carriers)
cached_auth = {
    f"[carrier]|api_key|secret_key": dict(
        access_token="test_token",
        token_type="bearer",
        expires_in=3599,
        expiry="2099-12-31 00:00:00",
    ),
}

gateway = karrio.gateway["[carrier]"].create(
    dict(
        api_key="api_key",
        secret_key="secret_key",
        account_number="12345",
        test_mode=True,
    ),
    cache=lib.Cache(**cached_auth),
)
```

## 4-Method Test Pattern

Every feature (rate, tracking, shipment, etc.) must have these 4 tests:

```python
import unittest
from unittest.mock import patch
import karrio
import karrio.lib as lib
import karrio.core.models as models
from .fixture import gateway


class TestCarrierRate(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        """Test: unified request → carrier-specific request conversion."""
        request = gateway.mapper.create_rate_request(self.RateRequest)
        print(request.serialize())  # ALWAYS print before assert
        self.assertEqual(lib.to_dict(request.serialize()), RateRequestData)

    def test_get_rate(self):
        """Test: proxy sends HTTP request to correct URL."""
        with patch("karrio.mappers.[carrier].proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/v1/rates",
            )

    def test_parse_rate_response(self):
        """Test: carrier response → unified RateDetails conversion."""
        with patch("karrio.mappers.[carrier].proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )
            print(parsed_response)  # ALWAYS print before assert
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedRateResponse
            )

    def test_parse_error_response(self):
        """Test: carrier error → unified Message conversion."""
        with patch("karrio.mappers.[carrier].proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )
            print(parsed_response)  # ALWAYS print before assert
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedErrorResponse
            )


if __name__ == "__main__":
    unittest.main()
```

## Test Data at Module Level

Define test data as module-level constants at the bottom of each test file:

```python
RatePayload = {
    "shipper": {"postal_code": "10001", "country_code": "US"},
    "recipient": {"postal_code": "90001", "country_code": "US"},
    "parcels": [
        {
            "height": 10,
            "length": 15,
            "width": 12,
            "weight": 5.0,
            "dimension_unit": "IN",
            "weight_unit": "LB",
        }
    ],
}

RateRequestData = {
    "origin": {"postal_code": "10001", "country_code": "US"},
    "destination": {"postal_code": "90001", "country_code": "US"},
    "packages": [
        {
            "weight": {"value": 5.0, "unit": "LB"},
            "dimensions": {"length": 15, "width": 12, "height": 10, "unit": "IN"},
        }
    ],
}

RateResponse = """{
    "rates": [
        {
            "service_code": "EXPRESS",
            "total_charge": 25.99,
            "currency": "USD",
            "transit_days": 2
        }
    ]
}"""

ParsedRateResponse = [
    [
        {
            "carrier_id": "carrier",
            "carrier_name": "carrier",
            "service": "carrier_express",
            "total_charge": 25.99,
            "currency": "USD",
            "transit_days": 2,
        }
    ],
    [],  # Empty messages list (no errors)
]

ErrorResponse = """{
    "errors": [
        {"code": "INVALID_POSTAL", "message": "Invalid postal code"}
    ]
}"""

ParsedErrorResponse = [
    [],  # Empty results list
    [
        {
            "carrier_id": "carrier",
            "carrier_name": "carrier",
            "code": "INVALID_POSTAL",
            "message": "Invalid postal code",
        }
    ],
]
```

## Feature-Specific Test Patterns

### Tracking Tests

```python
class TestCarrierTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(
            tracking_numbers=["1Z999AA10123456784"]
        )

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        self.assertEqual(request.serialize(), ["1Z999AA10123456784"])

    def test_get_tracking(self):
        with patch("karrio.mappers.[carrier].proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)
            # URL varies: may include tracking number in path or query

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.[carrier].proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed = karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            print(parsed)
            self.assertListEqual(lib.to_dict(parsed), ParsedTrackingResponse)
```

### Shipment Tests

```python
class TestCarrierShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(
            shipment_identifier="SHIP123"
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        print(request.serialize())
        self.assertEqual(lib.to_dict(request.serialize()), ShipmentRequestData)

    def test_create_shipment(self):
        with patch("karrio.mappers.[carrier].proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.[carrier].proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed = karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            print(parsed)
            self.assertListEqual(lib.to_dict(parsed), ParsedShipmentResponse)

    def test_cancel_shipment(self):
        with patch("karrio.mappers.[carrier].proxy.lib.request") as mock:
            mock.return_value = CancelResponse
            parsed = karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway).parse()
            print(parsed)
            self.assertListEqual(lib.to_dict(parsed), ParsedCancelResponse)
```

## Running Tests

```bash
# Run all tests for a carrier
python -m unittest discover -v -f [path]/tests

# Run specific test file
python -m unittest tests.[carrier].test_rate -v

# Run SDK-wide tests (must pass for all integrations)
./bin/run-sdk-tests

# Verify plugin registration
./bin/cli plugins list | grep [carrier]
./bin/cli plugins show [carrier]
```

## Common Test Pitfalls

- **Forgetting `print()` before assertions**: Always print response for debugging
- **Using `ANY` for non-deterministic values**: Timestamps, IDs that change per run
- **Not setting `self.maxDiff = None`**: Large diffs get truncated without this
- **Empty string filtering**: `lib.to_dict()` filters empty strings — update test expectations
- **Module-level fixtures**: Keep test data as module constants, not in setUp
