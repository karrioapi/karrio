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

# Step 4: Update the rate.py file with our template
echo -e "${BLUE}🔧 Step 4/8: Updating rate.py with template...${NC}"
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

# Step 5: Make scripts executable
echo -e "${BLUE}🔧 Step 5/8: Making scripts executable...${NC}"
chmod +x ${CARRIER_DIR}/generate

# Step 6: Generate Python types from JSON schemas
echo -e "${BLUE}🔄 Step 6/8: Generating Python types from JSON schemas...${NC}"
cd ${CARRIER_DIR} && ./generate
cd ../../..

# Step 7: Install the package in development mode
echo -e "${BLUE}📦 Step 7/8: Installing the package in development mode...${NC}"
cd ${CARRIER_DIR} && pip install -e .
cd ../../..

# Step 8: Create a basic test file
echo -e "${BLUE}🧪 Step 8/8: Creating basic test file...${NC}"
TEST_FILE="${CARRIER_DIR}/tests/test_${CARRIER_SLUG}.py"

# Create the test directory if it doesn't exist
mkdir -p "${CARRIER_DIR}/tests"

# Create a basic test file
cat > "$TEST_FILE" << EOL
import unittest
from datetime import datetime
from karrio.core.models import (
    RateRequest, TrackingRequest, ShipmentRequest,
    Address, Parcel
)
from modules.connectors.${CARRIER_SLUG}.karrio.mappers.${CARRIER_SLUG}.settings import Settings
from modules.connectors.${CARRIER_SLUG}.karrio.providers.${CARRIER_SLUG}.rate import Rate
from modules.connectors.${CARRIER_SLUG}.karrio.providers.${CARRIER_SLUG}.track import Track
from modules.connectors.${CARRIER_SLUG}.karrio.providers.${CARRIER_SLUG}.ship import Ship


class Test$(echo "${DISPLAY_NAME}" | tr -dc '[:alnum:]')(unittest.TestCase):
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
            shipper=Address(
                address_line1="123 Main St",
                city="San Francisco",
                state_code="CA",
                postal_code="94105",
                country_code="US",
            ),
            recipient=Address(
                address_line1="456 Market St",
                city="Los Angeles",
                state_code="CA",
                postal_code="90001",
                country_code="US",
            ),
            parcels=[
                Parcel(
                    weight=10.0,
                    weight_unit="LB",
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
            shipper=Address(
                address_line1="123 Main St",
                city="San Francisco",
                state_code="CA",
                postal_code="94105",
                country_code="US",
                person_name="John Doe",
                company_name="Test Company",
                phone_number="1234567890",
                email="john@example.com",
            ),
            recipient=Address(
                address_line1="456 Market St",
                city="Los Angeles",
                state_code="CA",
                postal_code="90001",
                country_code="US",
                person_name="Jane Smith",
                company_name="Test Recipient",
                phone_number="0987654321",
                email="jane@example.com",
            ),
            parcels=[
                Parcel(
                    weight=10.0,
                    weight_unit="LB",
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