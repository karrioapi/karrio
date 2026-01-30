#!/usr/bin/env python
"""
DHL Parcel DE Tracking API - Live Test Script

This script demonstrates the migrated tracking implementation using the
dedicated DHL Parcel DE Shipment Tracking API (XML-based).

Prerequisites:
    export DHL_PARCEL_DE_API_KEY="your-api-key"
    export DHL_PARCEL_DE_API_SECRET="your-api-secret"

Run from repository root:
    source .venv/karrio/bin/activate
    python modules/connectors/dhl_parcel_de/vendors/test_tracking_live.py
"""
import os
import sys
import json
import karrio.sdk as karrio
import karrio.lib as lib
from karrio.core.models import TrackingRequest

# Get credentials from environment variables
API_KEY = os.environ.get("DHL_PARCEL_DE_API_KEY")
API_SECRET = os.environ.get("DHL_PARCEL_DE_API_SECRET")

# Test tracking numbers available in DHL sandbox
TEST_TRACKING_NUMBERS = [
    "00340434161094015902",
    "00340434161094022115",
    "00340434161094027318",
]


def print_separator(title=""):
    print("\n" + "=" * 70)
    if title:
        print(f"  {title}")
        print("=" * 70)


def check_credentials():
    """Check if required environment variables are set."""
    if not API_KEY or not API_SECRET:
        print("ERROR: Missing required environment variables!")
        print("")
        print("Please set the following environment variables:")
        print("  export DHL_PARCEL_DE_API_KEY=\"your-api-key\"")
        print("  export DHL_PARCEL_DE_API_SECRET=\"your-api-secret\"")
        print("")
        print("You can get these from: https://developer.dhl.com")
        sys.exit(1)


def test_tracking():
    check_credentials()

    print_separator("DHL Parcel DE Tracking API - Live Test")

    print("\n[CONFIG]")
    print(lib.to_json({
        "api_key": "***redacted***",
        "api_secret": "***redacted***",
        "test_mode": True,
        "tracking_appname": "zt12345 (sandbox)",
        "tracking_password": "geheim (sandbox)",
    }))

    gateway = karrio.gateway["dhl_parcel_de"].create({
        "client_id": API_KEY,
        "client_secret": API_SECRET,
        "test_mode": True,
    })

    print(f"\n[ENDPOINT] {gateway.settings.tracking_server_url}")

    for tracking_number in TEST_TRACKING_NUMBERS:
        print_separator(f"Tracking: {tracking_number}")

        # Create request
        request = TrackingRequest(tracking_numbers=[tracking_number])

        # Build the serialized request to show what's being sent
        print("\n[XML REQUEST]")
        mapper_request = gateway.mapper.create_tracking_request(request)
        serialized = mapper_request.serialize()
        for xml_req in serialized:
            import xml.dom.minidom
            try:
                dom = xml.dom.minidom.parseString(xml_req)
                print(dom.toprettyxml(indent="  "))
            except:
                print(xml_req)

        # Execute the request
        print("[EXECUTING] Sending request to DHL API...\n")
        result = karrio.Tracking.fetch(request).from_(gateway)

        # Parse response
        tracking_details, messages = result.parse()

        print("[RESPONSE]")
        print(lib.to_json({
            "tracking_details": [lib.to_dict(d) for d in tracking_details],
            "messages": [lib.to_dict(m) for m in messages],
        }))

    print_separator("Test Complete")


def test_error_handling():
    """Test error handling with invalid tracking number."""
    check_credentials()

    print_separator("Error Handling Test - Invalid Tracking Number")

    gateway = karrio.gateway["dhl_parcel_de"].create({
        "client_id": API_KEY,
        "client_secret": API_SECRET,
        "test_mode": True,
    })

    request = TrackingRequest(tracking_numbers=["INVALID123456789"])

    print("\n[XML REQUEST]")
    mapper_request = gateway.mapper.create_tracking_request(request)
    serialized = mapper_request.serialize()
    for xml_req in serialized:
        import xml.dom.minidom
        try:
            dom = xml.dom.minidom.parseString(xml_req)
            print(dom.toprettyxml(indent="  "))
        except:
            print(xml_req)

    print("[EXECUTING] Sending request to DHL API...\n")
    result = karrio.Tracking.fetch(request).from_(gateway)
    tracking_details, messages = result.parse()

    print("[RESPONSE]")
    print(lib.to_json({
        "tracking_details": [lib.to_dict(d) for d in tracking_details],
        "messages": [lib.to_dict(m) for m in messages],
    }))


if __name__ == "__main__":
    test_tracking()
    test_error_handling()
