from karrio.core.settings import Settings as BaseSettings
from typing import Dict, Any, Optional, List


class Settings(BaseSettings):
    """Chit Chats carrier settings."""

    # Chit Chats API properties
    client_id: str = ""  # Your Chit Chats Client ID
    access_token: str = ""  # Your Chit Chats API access token
    test_mode: bool = False  # Set to True to use the sandbox environment

    # API URLs
    base_url: str = "https://chitchats.com/api/v1/clients"
    test_url: str = "https://staging.chitchats.com/api/v1/clients"
    
    # Service definitions
    services: Dict[str, Dict[str, Any]] = {
        "chit_chats_collect": {
            "name": "Chit Chats Collect",
            "type": "chit_chats",
            "tracking_included": True,
            "domestic": True
        },
        "chit_chats_select": {
            "name": "Chit Chats Select",
            "type": "chit_chats",
            "tracking_included": True,
            "domestic": True
        },
        "chit_chats_canada_tracked": {
            "name": "Chit Chats Canada Tracked",
            "type": "canada_post",
            "tracking_included": True,
            "domestic": True
        },
        "chit_chats_us_edge": {
            "name": "Chit Chats U.S. Edge",
            "type": "usps",
            "tracking_included": True,
            "international": True
        },
        "chit_chats_us_select": {
            "name": "Chit Chats U.S. Select",
            "type": "usps",
            "tracking_included": True,
            "international": True
        },
        "chit_chats_us_slim": {
            "name": "Chit Chats U.S. Slim",
            "type": "usps",
            "tracking_included": True,
            "international": True
        },
        "chit_chats_international_tracked": {
            "name": "Chit Chats International Tracked",
            "type": "various",
            "tracking_included": True,
            "international": True
        },
        "canada_post_tracked_packet_usa": {
            "name": "Canada Post Tracked Packet USA",
            "type": "canada_post",
            "tracking_included": True,
            "international": True
        }
    }
    
    # Default options
    default_options: Dict[str, Any] = {
        "package_contents": "merchandise",
        "currency": "cad",
        "package_type": "parcel",
        "signature_requested": False,
        "insurance_requested": False
    }
    
    # Carrier name and ID
    carrier_name: str = "Chit Chats"
    carrier_id: str = "chitchats"

    class Config:
        env_prefix = "KARRIO_CHITCHATS_" 
