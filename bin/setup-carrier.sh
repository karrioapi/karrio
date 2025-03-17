#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to display usage information
usage() {
    echo -e "${BLUE}Usage:${NC} $0 <carrier_slug> \"<Display Name>\" [--no-prompt]"
    echo -e "Example: $0 ontrac \"OnTrac\""
    echo -e "Use --no-prompt to skip all interactive prompts"
    exit 1
}

# Check if carrier slug and display name are provided
if [ $# -lt 2 ]; then
    usage
fi

CARRIER_SLUG=$1
DISPLAY_NAME=$2
FEATURES="tracking,rating,shipping"
VERSION="2024.3"
NO_PROMPT=""
CARRIER_DIR="modules/connectors/${CARRIER_SLUG}"

# Check for --no-prompt flag
if [ "$3" == "--no-prompt" ]; then
    NO_PROMPT="yes"
fi

echo -e "${GREEN}===========================================================${NC}"
echo -e "${GREEN}🚀 Setting up carrier integration for ${DISPLAY_NAME} (${CARRIER_SLUG})...${NC}"
echo -e "${GREEN}===========================================================${NC}"

# Step 1: Create carrier structure
echo -e "${BLUE}📁 Step 1/8: Creating carrier structure...${NC}"
echo "Creating carrier integration for ${DISPLAY_NAME} (${CARRIER_SLUG})..."

# Use the official CLI to create the carrier extension
if [ -n "$NO_PROMPT" ]; then
    # Non-interactive mode - use echo to automatically answer prompts
    echo -e "y\ny\ny\n" | bin/cli sdk add-extension --carrier-slug "${CARRIER_SLUG}" --display-name "${DISPLAY_NAME}" --features "${FEATURES}" --version "${VERSION}" --is-xml-api
else
    # Interactive mode
    bin/cli sdk add-extension --carrier-slug "${CARRIER_SLUG}" --display-name "${DISPLAY_NAME}" --features "${FEATURES}"
fi

# Check if the carrier directory exists
if [ ! -d "$CARRIER_DIR" ]; then
    echo -e "${RED}Error: Failed to create carrier directory.${NC}"
    exit 1
fi

# Step 2: Fix the license configuration in setup.py
echo -e "${BLUE}🔧 Step 2/8: Fixing package configuration...${NC}"
SETUP_FILE="${CARRIER_DIR}/setup.py"

# Check if setup.py exists, if not, create it
if [ ! -f "$SETUP_FILE" ]; then
    echo "Creating setup.py file..."
    cat > "$SETUP_FILE" << EOL
from setuptools import setup, find_namespace_packages

# Read README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name=f"karrio.${CARRIER_SLUG}",
    version="${VERSION}",
    author="Karrio Team",
    author_email="hello@karrio.io",
    description="Karrio ${DISPLAY_NAME} carrier integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://karrio.io",
    project_urls={
        "Bug Tracker": "https://github.com/karrioapi/karrio/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_namespace_packages(include=["karrio.*"]),
    python_requires=">=3.8",
    install_requires=[
        "karrio",
    ],
)
EOL
    echo "Created setup.py file"
fi

# Step 3: Update the settings.py file with our template
echo -e "${BLUE}🔧 Step 3/8: Updating settings.py with template...${NC}"
SETTINGS_FILE="${CARRIER_DIR}/karrio/mappers/${CARRIER_SLUG}/settings.py"
SETTINGS_TEMPLATE="templates/carrier/settings_template.py"

if [ -f "$SETTINGS_TEMPLATE" ]; then
    # Create a temporary file with the carrier name replaced
    sed "s/\[CARRIER_NAME\]/${DISPLAY_NAME}/g" "$SETTINGS_TEMPLATE" > "${SETTINGS_FILE}.tmp"
    sed "s/\[carrier_domain\]/${CARRIER_SLUG}.com/g" "${SETTINGS_FILE}.tmp" > "$SETTINGS_FILE"
    rm "${SETTINGS_FILE}.tmp"
    echo "Updated settings.py with template"
else
    echo -e "${YELLOW}Warning: Settings template not found.${NC}"
fi

# Step 4: Update the ship.py file with our template
echo -e "${BLUE}🔧 Step 4/8: Updating ship.py with template...${NC}"
SHIP_FILE="${CARRIER_DIR}/karrio/providers/${CARRIER_SLUG}/ship.py"
SHIP_TEMPLATE="templates/carrier/ship_template.py"

if [ -f "$SHIP_TEMPLATE" ]; then
    # Create a temporary file with the carrier name replaced
    sed "s/\[CARRIER_NAME\]/${DISPLAY_NAME}/g" "$SHIP_TEMPLATE" > "${SHIP_FILE}.tmp"
    sed "s/\[carrier_slug\]/${CARRIER_SLUG}/g" "${SHIP_FILE}.tmp" > "$SHIP_FILE"
    rm "${SHIP_FILE}.tmp"
    echo "Updated ship.py with template"
else
    echo -e "${YELLOW}Warning: Ship template not found.${NC}"
fi

# Step 5: Update the rate.py file with our template
echo -e "${BLUE}🔧 Step 5/8: Updating rate.py with template...${NC}"
RATE_FILE="${CARRIER_DIR}/karrio/providers/${CARRIER_SLUG}/rate.py"
RATE_TEMPLATE="templates/carrier/rate_template.py"

if [ -f "$RATE_TEMPLATE" ]; then
    # Create a temporary file with the carrier name replaced
    sed "s/\[CARRIER_NAME\]/${DISPLAY_NAME}/g" "$RATE_TEMPLATE" > "${RATE_FILE}.tmp"
    sed "s/\[carrier_slug\]/${CARRIER_SLUG}/g" "${RATE_FILE}.tmp" > "$RATE_FILE"
    rm "${RATE_FILE}.tmp"
    echo "Updated rate.py with template"
else
    echo -e "${YELLOW}Warning: Rate template not found.${NC}"
fi

# Step 6: Make scripts executable
echo -e "${BLUE}🔧 Step 6/8: Making scripts executable...${NC}"
chmod +x ${CARRIER_DIR}/generate

# Step 7: Generate Python types from JSON schemas
echo -e "${BLUE}🔄 Step 7/8: Generating Python types from JSON schemas...${NC}"
cd ${CARRIER_DIR} && ./generate
cd ../../..

# Step 8: Install the package in development mode
echo -e "${BLUE}📦 Step 8/8: Installing the package in development mode...${NC}"
cd ${CARRIER_DIR} && pip install -e .
cd ../../..

# Step 9: Create a basic test file
echo -e "${BLUE}🧪 Step 9/8: Creating basic test file...${NC}"
TEST_FILE="${CARRIER_DIR}/tests/test_${CARRIER_SLUG}.py"

# Create the test directory if it doesn't exist
mkdir -p "${CARRIER_DIR}/tests"

# Create a basic test file
cat > "$TEST_FILE" << EOL
import unittest
from datetime import datetime
from karrio.core.models import (
    RateRequest, TrackingRequest, ShipmentRequest,
    Address, Parcel, Person, Weight, WeightUnit
)
from modules.connectors.${CARRIER_SLUG}.karrio.mappers.${CARRIER_SLUG}.settings import Settings
from modules.connectors.${CARRIER_SLUG}.karrio.providers.${CARRIER_SLUG}.rate import Rate
from modules.connectors.${CARRIER_SLUG}.karrio.providers.${CARRIER_SLUG}.track import Track
from modules.connectors.${CARRIER_SLUG}.karrio.providers.${CARRIER_SLUG}.ship import Ship


class Test$(echo "${DISPLAY_NAME}" | sed 's/[^a-zA-Z0-9]//g')(unittest.TestCase):
    """Test ${DISPLAY_NAME} carrier integration."""

    def setUp(self):
        self.settings = {
            "api_key": "test_api_key",
            "password": "test_password",
            "account_number": "test_account",
            "shipper_number": "test_shipper",
            "test_mode": True,
        }
        self.carrier_settings = Settings(self.settings).carrier_settings

    def test_rate_request(self):
        """Test rate request."""
        request = RateRequest(
            shipper=Person(
                address=Address(
                    address_line1="123 Main St",
                    city="San Francisco",
                    state_code="CA",
                    postal_code="94105",
                    country_code="US",
                )
            ),
            recipient=Person(
                address=Address(
                    address_line1="456 Market St",
                    city="Los Angeles",
                    state_code="CA",
                    postal_code="90001",
                    country_code="US",
                )
            ),
            parcels=[
                Parcel(
                    weight=Weight(10, WeightUnit.LB),
                )
            ],
            date=datetime.now(),
        )
        
        # Mock the API call to avoid actual HTTP requests
        rate = Rate(self.carrier_settings)
        rate._prepare_rate_request = lambda x: "<xml>test</xml>"
        rate._parse_rate_response = lambda x: []
        
        # Test the rate request
        result = rate.create(request)
        self.assertIsInstance(result, list)

    def test_tracking_request(self):
        """Test tracking request."""
        request = TrackingRequest(
            tracking_number="1Z999AA10123456784",
        )
        
        # Mock the API call to avoid actual HTTP requests
        track = Track(self.carrier_settings)
        track._prepare_tracking_request = lambda x: "<xml>test</xml>"
        track._parse_tracking_response = lambda x, y: []
        
        # Test the tracking request
        result = track.create(request)
        self.assertIsInstance(result, list)

    def test_shipment_request(self):
        """Test shipment request."""
        request = ShipmentRequest(
            shipper=Person(
                person_name="John Doe",
                company_name="Test Company",
                phone_number="1234567890",
                email="john@example.com",
                address=Address(
                    address_line1="123 Main St",
                    city="San Francisco",
                    state_code="CA",
                    postal_code="94105",
                    country_code="US",
                )
            ),
            recipient=Person(
                person_name="Jane Smith",
                company_name="Test Recipient",
                phone_number="0987654321",
                email="jane@example.com",
                address=Address(
                    address_line1="456 Market St",
                    city="Los Angeles",
                    state_code="CA",
                    postal_code="90001",
                    country_code="US",
                )
            ),
            parcels=[
                Parcel(
                    weight=Weight(10, WeightUnit.LB),
                    length=10,
                    width=10,
                    height=10,
                )
            ],
            service="Ground",
            date=datetime.now(),
            reference="TEST-REF-123",
        )
        
        # Mock the API call to avoid actual HTTP requests
        ship = Ship(self.carrier_settings)
        ship._prepare_shipment_request = lambda x: "<xml>test</xml>"
        ship._parse_shipment_response = lambda x, y: None
        
        # Test the shipment request
        result = ship.create(request)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
EOL

echo "Created basic test file: $TEST_FILE"

# Run the tests
echo -e "${BLUE}🧪 Running initial tests...${NC}"
python -m unittest discover -v -f ${CARRIER_DIR}/tests

# Fix XML tags in ship.py
echo "Fixing XML tags in ship.py..."
SHIP_PY_PATH="modules/connectors/${CARRIER_SLUG}/karrio/providers/${CARRIER_SLUG}/ship.py"
if [ -f "$SHIP_PY_PATH" ]; then
    # Create a temporary file with the correct XML tags
    cat > /tmp/ship.py.new << 'EOF'
from typing import List, Any, Dict
import requests
import xml.etree.ElementTree as ET
from karrio.core.models import ShipmentRequest, ShipmentDetails
from karrio.core.errors import ShippingSDKError


class Ship:
    """CARRIER_NAME Shipping API implementation."""

    def __init__(self, settings: Dict[str, Any]):
        self.settings = settings
        self.base_url = settings["base_url"]
        self.api_key = settings["api_key"]
        self.password = settings["password"]
        self.account_number = settings["account_number"]
        self.shipper_number = settings.get("shipper_number", "")
        self.timeout = settings.get("timeout", 30)
        self.max_retries = settings.get("max_retries", 3)

    def create(self, payload: ShipmentRequest) -> ShipmentDetails:
        """Create a shipment request."""
        try:
            # Prepare the XML/JSON request
            request_data = self._prepare_shipment_request(payload)
            
            # Send the request to the carrier API
            response = requests.post(
                f"{self.base_url}/shipments",
                headers={
                    "Content-Type": "application/xml",  # or "application/json"
                    "Authorization": f"Bearer {self.api_key}",
                },
                data=request_data,
                timeout=self.timeout,
            )
            
            # Check for errors
            if response.status_code != 200:
                raise ShippingSDKError(
                    f"HTTP Error: {response.status_code}",
                    details={"response": response.text},
                )
            
            # Parse the response
            return self._parse_shipment_response(response.text)
        except requests.RequestException as e:
            raise ShippingSDKError(
                f"Request Error: {str(e)}",
                details={"error": str(e)},
            )
        except Exception as e:
            raise ShippingSDKError(
                str(e),
                details={"error": str(e)},
            )
    
    def _prepare_shipment_request(self, payload: ShipmentRequest) -> str:
        """Prepare the XML/JSON shipment request."""
        # Extract the first package for simplicity
        package = payload.parcels[0]
        
        # Extract origin and destination
        origin = payload.shipper
        destination = payload.recipient
        
        # Create the XML request
        # This is a template - you'll need to adjust it based on the carrier's API
        xml = f"""
        <ShipmentRequest>
            <Authentication>
                <APIKey>{self.api_key}</APIKey>
                <Password>{self.password}</Password>
                <AccountNumber>{self.account_number}</AccountNumber>
            </Authentication>
            <Shipment>
                <Service>{payload.service}</Service>
                <ShipDate>{payload.date.strftime('%Y-%m-%d') if hasattr(payload, 'date') else ''}</ShipDate>
                <Origin>
                    <Name>{origin.person_name}</Name>
                    <Company>{origin.company_name}</Company>
                    <AddressLine1>{origin.address_line1}</AddressLine1>
                    <AddressLine2>{origin.address_line2 or ''}</AddressLine2>
                    <City>{origin.city}</City>
                    <StateCode>{origin.state_code}</StateCode>
                    <PostalCode>{origin.postal_code}</PostalCode>
                    <CountryCode>{origin.country_code}</CountryCode>
                    <Phone>{origin.phone_number}</Phone>
                    <Email>{origin.email}</Email>
                </Origin>
                <Destination>
                    <Name>{destination.person_name}</Name>
                    <Company>{destination.company_name}</Company>
                    <AddressLine1>{destination.address_line1}</AddressLine1>
                    <AddressLine2>{destination.address_line2 or ''}</AddressLine2>
                    <City>{destination.city}</City>
                    <StateCode>{destination.state_code}</StateCode>
                    <PostalCode>{destination.postal_code}</PostalCode>
                    <CountryCode>{destination.country_code}</CountryCode>
                    <Phone>{destination.phone_number}</Phone>
                    <Email>{destination.email}</Email>
                </Destination>
                <Package>
                    <Weight>{package.weight}</Weight>
                    <Length>{getattr(package, 'length', 0)}</Length>
                    <Width>{getattr(package, 'width', 0)}</Width>
                    <Height>{getattr(package, 'height', 0)}</Height>
                </Package>
                <Options>
                    <ResidentialDelivery>{str(payload.options.get('residential_delivery', False)).lower()}</ResidentialDelivery>
                    <SaturdayDelivery>{str(payload.options.get('saturday_delivery', False)).lower()}</SaturdayDelivery>
                </Options>
                <Reference>{payload.reference or ''}</Reference>
            </Shipment>
        </ShipmentRequest>
        """
        return xml
    
    def _parse_shipment_response(self, response_text: str) -> ShipmentDetails:
        """Parse the XML/JSON shipment response."""
        # Parse the XML response
        # This is a template - you'll need to adjust it based on the carrier's API
        root = ET.fromstring(response_text)
        
        # Extract the shipment information
        tracking_number = root.find(".//TrackingNumber").text
        label_url = root.find(".//LabelURL").text
        
        # Create the shipment details
        return ShipmentDetails(
            carrier_name="CARRIER_NAME",
            carrier_id="CARRIER_ID",
            tracking_number=tracking_number,
            label_url=label_url,
            label_type="URL",
            shipment_identifier=tracking_number,
            selected_rate=None,
            meta={"response": response_text},
        )
EOF
    # Replace the carrier name and ID
    sed -i '' "s/CARRIER_NAME/${DISPLAY_NAME}/g" /tmp/ship.py.new
    sed -i '' "s/CARRIER_ID/${CARRIER_SLUG}/g" /tmp/ship.py.new
    # Copy the file to the correct location
    cp /tmp/ship.py.new "$SHIP_PY_PATH"
    echo "Fixed XML tags in ship.py"
fi

echo -e "${GREEN}===========================================================${NC}"
echo -e "${GREEN}✅ Carrier integration setup complete!${NC}"
echo -e "${GREEN}===========================================================${NC}"
echo
echo "Your new carrier integration is ready at:"
echo -e "${BLUE}/Users/shadrackaddo/karrio/${CARRIER_DIR}${NC}"
echo
echo "Next steps:"
echo "1. Customize the API endpoints in the provider files"
echo "2. Update the JSON schema files to match your carrier's API"
echo "3. Run the generate script again if you update the schemas:"
echo -e "   ${YELLOW}cd /Users/shadrackaddo/karrio/${CARRIER_DIR} && ./generate${NC}"
echo
echo "For more information, see the documentation at:"
echo -e "${BLUE}http://localhost:8080${NC} (run ./start-docs.sh to start the docs server)"
echo
echo -e "${GREEN}Happy coding! 🎉${NC}" 