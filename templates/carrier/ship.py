from typing import List, Any, Dict
import requests
import xml.etree.ElementTree as ET
from karrio.core.models import ShipmentRequest, ShipmentDetails
from karrio.core.errors import ShippingSDKError


class Ship:
    """[CARRIER_NAME] Shipping API implementation."""

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
            carrier_name="[CARRIER_NAME]",
            carrier_id="[carrier_slug]",
            tracking_number=tracking_number,
            label_url=label_url,
            label_type="URL",
            shipment_identifier=tracking_number,
            selected_rate=None,
            meta={"response": response_text},
        ) 