#!/usr/bin/env python
"""
Test script for Chit Chats API integration.
This script directly tests the Chit Chats API using requests library.
"""

import requests
import json
import sys

# Test credentials
CLIENT_ID = "208472"
ACCESS_TOKEN = "9d778e133a0e4b1b94708b332350141d"
BASE_URL = "https://staging.chitchats.com/api/v1/clients"  # Add /clients path

# Test addresses
ORIGIN = {
    "name": "John Doe",
    "company": "Karrio Shipper",
    "address_1": "5840 Oak St",
    "city": "Vancouver",
    "province_code": "BC",
    "postal_code": "V6M2V9",
    "country_code": "CA",
    "phone": "6135710000",
    "email": "shipper@karrio.io"
}

DESTINATION = {
    "name": "Jane Smith",
    "company": "Karrio Recipient",
    "address_1": "123 Main St",
    "city": "Toronto",
    "province_code": "ON",
    "postal_code": "M5V2A1",
    "country_code": "CA",
    "phone": "4165550199",
    "email": "recipient@karrio.io"
}

# Package information
PARCEL = {
    "length": 15.0,
    "width": 10.0,
    "height": 10.0,
    "weight": 1.0,
    "weight_unit": "kg",
    "size_unit": "cm",
    "package_type": "parcel",
    "package_contents": "merchandise",
    "value": "50.00",
    "value_currency": "CAD"
}


def get_headers():
    """Return authentication headers."""
    # Note: The direct token is used, not "Bearer" prefix
    return {
        "Content-Type": "application/json",
        "Authorization": ACCESS_TOKEN
    }


def test_list_shipments():
    """Test listing shipments."""
    print("\n=== Testing List Shipments ===")
    url = f"{BASE_URL}/{CLIENT_ID}/shipments?limit=5"
    
    print(f"GET {url}")
    response = requests.get(url, headers=get_headers())
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        shipments = response.json()
        if isinstance(shipments, list):
            print(f"Found {len(shipments)} shipments")
        else:
            print("Unexpected response format:")
            print(json.dumps(shipments, indent=2)[:200] + "...")
        return shipments
    else:
        print(f"Error: {response.text}")
        return None


def test_rate_request():
    print("\n=== Testing Rate Request ===")
    # Create a shipment payload with all required fields
    shipment_payload = {
        "name": "Jane Smith",
        "address_1": "123 Main St",
        "city": "Toronto",
        "province_code": "ON",
        "postal_code": "M5V2A1",
        "country_code": "CA",
        "phone": "4165550199",
        "package_type": "parcel",
        "weight": 1.0,
        "weight_unit": "kg",
        "size_unit": "cm",
        "size_x": 15.0,
        "size_y": 10.0,
        "size_z": 10.0,
        "description": "Test package",
        "value": "50.00",
        "value_currency": "CAD"
    }
    
    # Create the shipment
    url = f"{BASE_URL}/{CLIENT_ID}/shipments"
    response = requests.post(url, headers=get_headers(), json=shipment_payload)
    print(f"POST {url}")
    print(f"Payload: {json.dumps(shipment_payload, indent=2)}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        response_data = response.json()
        
        # Extract the shipment from the nested response
        if 'shipment' in response_data:
            shipment_data = response_data['shipment']
        else:
            shipment_data = response_data
            
        shipment_id = shipment_data.get("id")
        print(f"Shipment created successfully")
        print(f"Shipment ID: {shipment_id}")
        
        # Check shipment status
        status = shipment_data.get('status')
        print(f"Shipment status: {status}")
        
        # Get rates
        rates = shipment_data.get("rates", [])
        
        if rates:
            print(f"Found {len(rates)} rate(s):")
            for rate in rates:
                print(f"Service: {rate.get('service_name')}")
                print(f"Rate: {rate.get('price')} {rate.get('currency')}")
                print(f"Delivery Time: {rate.get('delivery_time_description')}")
                print("---")
        else:
            print("No rates found in the initial shipment response")
            
            # If status is incomplete, we need to complete the shipment to get rates
            if status == 'incomplete':
                print("\nShipment is incomplete. You need to select a postage type or add additional information.")
                print("Available fields to update:")
                for key, value in shipment_data.items():
                    if value is None and key not in ['carrier_tracking_code', 'postage_label_png_url', 'postage_label_zpl_url']:
                        print(f"- {key}")
                
                # Let's try to update with a specific postage type
                update_url = f"{BASE_URL}/{CLIENT_ID}/shipments/{shipment_id}"
                update_payload = {
                    "postage_type": "usps_first_class"  # Try a common postage type
                }
                print(f"\nPUT {update_url}")
                print(f"Update payload: {json.dumps(update_payload, indent=2)}")
                
                update_response = requests.put(update_url, headers=get_headers(), json=update_payload)
                print(f"Update status: {update_response.status_code}")
                
                if update_response.status_code == 200:
                    updated_data = update_response.json()
                    if 'shipment' in updated_data:
                        updated_shipment = updated_data['shipment']
                    else:
                        updated_shipment = updated_data
                        
                    print(f"Updated shipment status: {updated_shipment.get('status')}")
                    
                    # Check for rates again
                    updated_rates = updated_shipment.get('rates', [])
                    if updated_rates:
                        print(f"Found {len(updated_rates)} rate(s) after update:")
                        for rate in updated_rates:
                            print(f"Service: {rate.get('service_name')}")
                            print(f"Rate: {rate.get('price')} {rate.get('currency')}")
                            print(f"Delivery Time: {rate.get('delivery_time_description')}")
                            print("---")
                    else:
                        print("Still no rates found after update")
                else:
                    print(f"Error updating shipment: {update_response.text}")
            
        return response_data
    else:
        print(f"Error creating shipment: {response.text}")
        return None


def test_create_shipment(rates_response=None):
    """Test creating a shipment with Chit Chats API."""
    print("\n=== Testing Creating Shipment ===")
    
    # If no rates provided, get them first
    if not rates_response:
        rates_response = test_rate_request()
        if not rates_response:
            print("No rates available. Cannot create shipment.")
            return None
    
    # Extract shipment from the response
    if 'shipment' in rates_response:
        shipment = rates_response['shipment']
    else:
        shipment = rates_response
    
    # If the shipment already has an ID, it means it's already created
    if 'id' in shipment:
        print(f"Using existing shipment with ID: {shipment.get('id')}")
        return shipment
    
    # Otherwise, try to create a new shipment
    url = f"{BASE_URL}/{CLIENT_ID}/shipments"
    data = {
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
        "value_currency": PARCEL["value_currency"],
        "postage_type": "usps_first_class"  # Use a specific postage type
    }
    
    print(f"POST {url}")
    response = requests.post(url, headers=get_headers(), json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code not in [200, 201]:
        print(f"Error creating shipment: {response.text}")
        return None
    
    response_data = response.json()
    if 'shipment' in response_data:
        shipment = response_data['shipment']
    else:
        shipment = response_data
    
    print("\nShipment created:")
    print(f"- ID: {shipment.get('id')}")
    print(f"- Tracking Number: {shipment.get('tracking_number', 'N/A')}")
    print(f"- Status: {shipment.get('status')}")
    
    return shipment


def test_tracking(shipment=None):
    """Test tracking a shipment with Chit Chats API."""
    print("\n=== Testing Tracking ===")
    
    # If no shipment is provided, create one
    if not shipment or "id" not in shipment:
        print("No shipment provided, creating one...")
        shipment = test_create_shipment()
        if not shipment:
            print("Failed to create shipment for tracking test.")
            return None
    
    shipment_id = shipment.get('id')
    url = f"{BASE_URL}/{CLIENT_ID}/shipments/{shipment_id}"
    
    print(f"GET {url}")
    response = requests.get(url, headers=get_headers())
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
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
        if "tracking_url" in shipment_details:
            print(f"- Tracking URL: {shipment_details.get('tracking_url')}")
            
        # Show tracking events if available
        tracking_events = shipment_details.get('tracking_events', [])
        if tracking_events:
            print("\nTracking Events:")
            for event in tracking_events:
                print(f"- {event.get('created_at')}: {event.get('title')}")
                if event.get('subtitle'):
                    print(f"  {event.get('subtitle')}")
                if event.get('location_description'):
                    print(f"  Location: {event.get('location_description')}")
                    
        return shipment_details
    else:
        print(f"Error tracking shipment: {response.text}")
        return None


if __name__ == "__main__":
    print("Chit Chats API Test Script")
    print(f"Client ID: {CLIENT_ID}")
    print(f"Base URL: {BASE_URL}")
    
    try:
        # Test listing shipments
        test_list_shipments()
        
        # Test rate request
        shipment_data = test_rate_request()
        
        # Test shipment creation
        if shipment_data:
            shipment = test_create_shipment(shipment_data)
            
            # Test tracking
            if shipment:
                test_tracking(shipment)
        
        print("\nAll tests completed")
    except requests.RequestException as e:
        print(f"Network error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 
