import pytest
import os


# Configure test environment
@pytest.fixture
def client_id():
    """Return the Chit Chats Client ID for testing."""
    return os.environ.get('CHITCHATS_CLIENT_ID', '208472')


@pytest.fixture
def api_key():
    """Return the Chit Chats API Key for testing."""
    return os.environ.get('CHITCHATS_API_KEY', 'test_api_key')


@pytest.fixture
def base_url():
    """Return the Chit Chats API base URL for testing."""
    return os.environ.get(
        'CHITCHATS_BASE_URL',
        'https://staging.chitchats.com/api/v1'
    )


@pytest.fixture
def destination_address():
    """Return a test destination address."""
    return {
        "name": "John Doe",
        "company": "ACME Inc.",
        "address_1": "123 Main St",
        "address_2": "Apt 4B",
        "city": "New York",
        "province_code": "NY",
        "postal_code": "10001",
        "country_code": "US",
        "phone": "555-123-4567",
        "email": "john.doe@example.com"
    }


@pytest.fixture
def test_parcel():
    """Return a test parcel."""
    return {
        "weight": 0.5,
        "weight_unit": "kg",
        "length": 20,
        "width": 15,
        "height": 10,
        "size_unit": "cm",
        "packaging_type": "small_box"
    }


@pytest.fixture
def headers(api_key):
    """Return authentication headers for API requests."""
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Token {api_key}'
    } 
