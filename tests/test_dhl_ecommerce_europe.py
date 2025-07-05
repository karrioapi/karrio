import unittest
from unittest.mock import Mock, patch
from karrio.core.models import RateRequest, ShipmentRequest, TrackingRequest
from karrio.mappers.dhl_ecommerce_europe.settings import Settings
from karrio.providers.dhl_ecommerce_europe.rate import rate_request, parse_rate_response
from karrio.providers.dhl_ecommerce_europe.shipment import shipment_request, parse_shipment_response
from karrio.providers.dhl_ecommerce_europe.tracking import tracking_request, parse_tracking_response


class TestDHLEcommerceEurope(unittest.TestCase):
    """Test DHL eCommerce Europe integration."""

    def setUp(self):
        """Set up test fixtures."""
        self.settings = Settings(
            username="test_user",
            password="test_password",
            account_number="123456789",
            test_mode=True,
        )

    def test_rate_request_serialization(self):
        """Test rate request serialization."""
        # Mock rate request payload
        mock_payload = Mock(spec=RateRequest)
        mock_payload.shipper = Mock()
        mock_payload.shipper.postal_code = "10115"
        mock_payload.shipper.city = "Berlin"
        mock_payload.shipper.country_code = "DE"
        mock_payload.recipient = Mock()
        mock_payload.recipient.postal_code = "75001"
        mock_payload.recipient.city = "Paris"
        mock_payload.recipient.country_code = "FR"
        mock_payload.parcels = [Mock()]
        mock_payload.parcels[0].weight = Mock()
        mock_payload.parcels[0].weight.KG = 2.5
        mock_payload.parcels[0].length = Mock()
        mock_payload.parcels[0].length.CM = 20
        mock_payload.parcels[0].width = Mock()
        mock_payload.parcels[0].width.CM = 15
        mock_payload.parcels[0].height = Mock()
        mock_payload.parcels[0].height.CM = 10
        mock_payload.parcels[0].options = {}  # Add options to avoid Mock.keys() error
        mock_payload.services = ["V01PAK"]

        # Test rate request
        request = rate_request(mock_payload, self.settings)
        self.assertIsNotNone(request)

    def test_rate_response_parsing(self):
        """Test rate response parsing."""
        mock_response = Mock()
        mock_response.deserialize.return_value = {
            "products": [
                {
                    "name": "DHL Express",
                    "productCode": "V01PAK",
                    "localProductCode": "V01PAK",
                    "deliveryCapabilities": {"totalTransitDays": 2},
                    "totalPrice": [
                        {
                            "priceType": "TOTAL",
                            "price": 25.50,
                            "priceCurrency": "EUR",
                            "breakdown": [
                                {"name": "base", "price": 20.00, "priceCurrency": "EUR"},
                                {"name": "fuel", "price": 5.50, "priceCurrency": "EUR"},
                            ],
                        }
                    ],
                }
            ]
        }

        rates, messages = parse_rate_response(mock_response, self.settings)
        
        self.assertEqual(len(rates), 1)
        self.assertEqual(rates[0].service, "V01PAK")  # Service comes from productCode
        self.assertEqual(float(rates[0].total_charge), 25.50)
        self.assertEqual(rates[0].currency, "EUR")
        self.assertEqual(rates[0].transit_days, 2)

    def test_shipment_request_serialization(self):
        """Test shipment request serialization."""
        # Mock shipment request payload
        mock_payload = Mock(spec=ShipmentRequest)
        mock_payload.shipment_date = "2025-01-20"
        mock_payload.service = "express"
        mock_payload.options = {}  # Add missing options attribute
        mock_payload.parcels = [Mock()]  # Changed from packages to parcels to match our code
        mock_payload.parcels[0].weight = Mock()
        mock_payload.parcels[0].weight.value = 2.5
        mock_payload.parcels[0].length = Mock()
        mock_payload.parcels[0].length.value = 20
        mock_payload.parcels[0].width = Mock()
        mock_payload.parcels[0].width.value = 15
        mock_payload.parcels[0].height = Mock()
        mock_payload.parcels[0].height.value = 10
        mock_payload.shipper = Mock()
        mock_payload.shipper.postal_code = "10115"
        mock_payload.shipper.city = "Berlin"
        mock_payload.shipper.country_code = "DE"
        mock_payload.shipper.address_line1 = "Test Street 1"
        mock_payload.shipper.email = "shipper@test.com"
        mock_payload.shipper.phone_number = "+49123456789"
        mock_payload.shipper.company_name = "Test Company"
        mock_payload.shipper.person_name = "John Doe"
        mock_payload.recipient = Mock()
        mock_payload.recipient.postal_code = "75001"
        mock_payload.recipient.city = "Paris"
        mock_payload.recipient.country_code = "FR"
        mock_payload.recipient.address_line1 = "Test Street 2"
        mock_payload.recipient.email = "recipient@test.com"
        mock_payload.recipient.phone_number = "+33123456789"
        mock_payload.recipient.company_name = "Recipient Company"
        mock_payload.recipient.person_name = "Jane Smith"

        # Test shipment request
        request = shipment_request(mock_payload, self.settings)
        self.assertIsNotNone(request)

    def test_tracking_request_serialization(self):
        """Test tracking request serialization."""
        mock_payload = Mock(spec=TrackingRequest)
        mock_payload.tracking_numbers = ["1234567890", "0987654321"]

        # Test tracking request
        request = tracking_request(mock_payload, self.settings)
        self.assertIsNotNone(request)

    def test_tracking_response_parsing(self):
        """Test tracking response parsing."""
        mock_response = Mock()
        mock_response.deserialize.return_value = {
            "shipments": [
                {
                    "shipmentTrackingNumber": "1234567890",  # Fixed field name
                    "status": {"statusCode": "delivered"},
                    "events": [
                        {
                            "typeCode": "delivered",
                            "description": "Delivered",
                            "timestamp": "2025-01-20T14:30:00",
                            "location": {
                                "address": {"addressLocality": "Paris"}
                            },
                        }
                    ],
                }
            ]
        }

        tracking_details, messages = parse_tracking_response(mock_response, self.settings)
        
        self.assertEqual(len(tracking_details), 1)
        self.assertEqual(tracking_details[0].tracking_number, "1234567890")
        self.assertEqual(tracking_details[0].status, "delivered")
        self.assertEqual(len(tracking_details[0].events), 1)


if __name__ == "__main__":
    unittest.main() 
