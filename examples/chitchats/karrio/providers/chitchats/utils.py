from karrio.core.utils import create_envelope, Envelope, XP
from karrio.mappers.chitchats.settings import Settings
import requests


def create_xml_request_header(settings: Settings) -> str:
    """Create XML request header."""
    return f"""
        <AccessRequest>
            <AccessLicenseNumber>{settings.api_key}</AccessLicenseNumber>
            <UserId>{settings.api_secret}</UserId>
            <Password>{settings.account_number}</Password>
        </AccessRequest>
    """


def create_xml_response_header(settings: Settings) -> str:
    """Create XML response header."""
    return """
        <Response>
            <TransactionReference>response</TransactionReference>
        </Response>
    """


def get_api_url(settings: Settings) -> str:
    """Return the appropriate API URL based on test mode."""
    return settings.test_url if settings.test_mode else settings.base_url


def get_headers(settings: Settings) -> dict:
    """Create the HTTP headers for Chit Chats API requests."""
    return {
        "Authorization": settings.access_token,
        "Content-Type": "application/json; charset=utf-8"
    }


def make_request(method: str, endpoint: str, settings: Settings, data: dict=None):
    """Make a request to the Chit Chats API."""
    base_url = get_api_url(settings)
    url = f"{base_url}/{settings.client_id}/{endpoint}"
    headers = get_headers(settings)
    
    response = requests.request(
        method=method,
        url=url,
        headers=headers,
        json=data,
        timeout=30  # 30-second timeout
    )
    
    return response 
