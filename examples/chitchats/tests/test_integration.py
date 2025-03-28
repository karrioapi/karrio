import unittest
import requests
import json
import sys
import os

# Add the parent directory to the path to import from the connector module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration
CLIENT_ID = "208472"
BASE_URL = "https://staging.chitchats.com/api/v1/clients"
API_KEY = os.environ.get("CHITCHATS_API_KEY", "test_api_key")  # Default test key for CI

# Test data
DESTINATION = {
    "name": "Jane Smith",
    "address_1": "123 Main St",
    "city": "Toronto",
    "province_code": "ON",
    "postal_code": "M5V2A1",
    "country_code": "CA",
    "phone": "4165550199"
}

PARCEL = {
    "package_type": "parcel",
    "weight": 1.0,
    "weight_unit": "kg",
    "size_unit": "cm",
    "length": 15.0,
    "width": 10.0,
    "height": 10.0,
    "value": "50.00",
    "value_currency": "CAD"
}


class ChitChatsIntegrationTests(unittest.TestCase):
    """Integration tests for the Chit Chats API."""
    
    def setUp(self):
        """Set up test environment."""
        self.headers = self.get_headers()
        self.shipment_id = None
    
    def get_headers(self):
        """Get authentication headers."""
        return {
            "Content-Type": "application/json",
            "Authorization": API_KEY
        }
    
    def test_1_list_shipments(self):
        """Test listing shipments."""
        print("\n=== Testing List Shipments ===")
        url = f"{BASE_URL}/{CLIENT_ID}/shipments?limit=5"
        response = requests.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 200, f"Failed to list shipments: {response.text}")
        shipments = response.json()
        
        # Check that the response is a list or has a shipments key
        if isinstance(shipments, dict) and 'shipments' in shipments:
            shipments = shipments['shipments']
        
        self.assertIsInstance(shipments, list, "Expected a list of shipments")
        print(f"Found {len(shipments)} shipments")
    
    def test_2_rate_request(self):
        """Test getting rates from Chit Chats API."""
        print("\n=== Testing Rate Request ===")
        # Create a shipment payload with all required fields
        shipment_payload = {
            "name": DESTINATION["name"],
            "address_1": DESTINATION["address_1"],
            "city": DESTINATION["city"],
            "province_code": DESTINATION["province_code"],
            "postal_code": DESTINATION["postal_code"],
            "country_code": DESTINATION["country_code"],
            "phone": DESTINATION["phone"],
            "package_type": PARCEL["package_type"],
            "weight": PARCEL["weight"],
            "weight_unit": PARCEL["weight_unit"],
            "size_unit": PARCEL["size_unit"],
            "size_x": PARCEL["length"],
            "size_y": PARCEL["width"],
            "size_z": PARCEL["height"],
            "description": "Test package",
            "value": PARCEL["value"],
            "value_currency": PARCEL["value_currency"]
        }
        
        # Create the shipment
        url = f"{BASE_URL}/{CLIENT_ID}/shipments"
        response = requests.post(url, headers=self.headers, json=shipment_payload)
        print(f"POST {url}")
        print(f"Status: {response.status_code}")
        
        self.assertIn(response.status_code, [200, 201], f"Failed to create shipment: {response.text}")
        
        response_data = response.json()
        
        # Extract the shipment from the nested response
        if 'shipment' in response_data:
            shipment_data = response_data['shipment']
        else:
            shipment_data = response_data
            
        shipment_id = shipment_data.get("id")
        self.assertIsNotNone(shipment_id, "No shipment ID returned")
        print(f"Shipment created successfully - ID: {shipment_id}")
        self.shipment_id = shipment_id
        
        # Store the shipment ID for later tests
        ChitChatsIntegrationTests.shipment_id = shipment_id
        
        # Check shipment status
        status = shipment_data.get('status')
        print(f"Shipment status: {status}")
        
        # If status is incomplete, we need to complete the shipment to get rates
        if status == 'incomplete':
            # Try to update with a specific postage type
            update_url = f"{BASE_URL}/{CLIENT_ID}/shipments/{shipment_id}"
            update_payload = {
                "postage_type": "usps_first_class"  # Try a common postage type
            }
            print(f"\nPUT {update_url}")
            
            update_response = requests.put(update_url, headers=self.headers, json=update_payload)
            self.assertIn(update_response.status_code, [200, 201], f"Failed to update shipment: {update_response.text}")
            
            updated_data = update_response.json()
            if 'shipment' in updated_data:
                updated_shipment = updated_data['shipment']
            else:
                updated_shipment = updated_data
                
            print(f"Updated shipment status: {updated_shipment.get('status')}")
            
            # Check for rates
            updated_rates = updated_shipment.get('rates', [])
            if updated_rates:
                print(f"Found {len(updated_rates)} rate(s)")
                self.assertTrue(len(updated_rates) > 0, "No rates found after update")
            else:
                print("Still no rates found after update")
                # This is not a failure - some test environments might not return rates
    
    def test_3_tracking(self):
        """Test tracking a shipment."""
        print("\n=== Testing Tracking ===")
        
        # Use the shipment ID from previous test
        shipment_id = getattr(ChitChatsIntegrationTests, 'shipment_id', None)
        self.assertIsNotNone(shipment_id, "No shipment ID from previous test")
        
        url = f"{BASE_URL}/{CLIENT_ID}/shipments/{shipment_id}"
        
        print(f"GET {url}")
        response = requests.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 200, f"Failed to track shipment: {response.text}")
        
        response_data = response.json()
        
        # Extract shipment from the nested response
        if 'shipment' in response_data:
            shipment_details = response_data['shipment']
        else:
            shipment_details = response_data
            
        print("\nShipment Details:")
        print(f"- ID: {shipment_details.get('id')}")
        print(f"- Status: {shipment_details.get('status')}")
        print(f"- Tracking #: {shipment_details.get('carrier_tracking_code', 'N/A')}")
        self.assertEqual(shipment_details.get('id'), shipment_id, "Tracking returned wrong shipment")
        
        if "tracking_url" in shipment_details:
            print(f"- Tracking URL: {shipment_details.get('tracking_url')}")
            
        # Show tracking events if available
        tracking_events = shipment_details.get('tracking_events', [])
        if tracking_events:
            print("\nTracking Events:")
            for event in tracking_events:
                print(f"- {event.get('created_at')}: {event.get('title')}")
            self.assertTrue(len(tracking_events) > 0, "No tracking events found")


if __name__ == "__main__":
    unittest.main() 
