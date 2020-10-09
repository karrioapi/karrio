import logging
import unittest
from unittest.mock import patch
import purplship
from purplship.core.utils import to_dict
from purplship.core.models import (
    PickupRequest,
    PickupUpdateRequest,
    PickupCancellationRequest,
)
from tests.canpar.fixture import gateway

logger = logging.getLogger(__name__)


class TestCanparPickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = PickupRequest(**pickup_data)
        self.PickupUpdateRequest = PickupUpdateRequest(**pickup_update_data)
        self.PickupCancelRequest = PickupCancellationRequest(**pickup_cancel_data)


if __name__ == "__main__":
    unittest.main()

pickup_data = {
    "date": "2015-01-28",
    "address": {
        "company_name": "Jim Duggan",
        "address_line1": "2271 Herring Cove",
        "city": "Halifax",
        "postal_code": "B3L2C2",
        "country_code": "CA",
        "person_name": "John Doe",
        "phone_number": "1 514 5555555",
        "state_code": "NS",
        "residential": True,
        "email": "john.doe@canpar.ca",
    },
    "instruction": "Door at Back",
    "ready_time": "15:00",
    "closing_time": "17:00",
}

pickup_update_data = {
    "confirmation_number": "0074698052",
    "date": "2015-01-28",
    "address": {
        "person_name": "Jane Doe",
        "email": "john.doe@canpar.ca",
        "phone_number": "1 514 5555555",
    },
    "parcels": [{"weight": 24, "weight_unit": "KG"}],
    "instruction": "Door at Back",
    "ready_time": "15:00",
    "closing_time": "17:00",
    "options": {"LoadingDockAvailable": False, "TrailerAccessible": False},
}

pickup_cancel_data = {"confirmation_number": "0074698052"}

ParsedPickupResponse = [
    {
        "carrier_id": "canpar",
        "carrier_name": "canpar",
        "confirmation_number": "01365863",
    },
    [],
]

ParsedPickupCancelResponse = [
    {
        "carrier_id": "canpar",
        "carrier_name": "canpar",
        "success": True,
    },
    [],
]


PickupRequestXML = """
"""

PickupUpdateRequestXML = """
"""

PickupCancelRequestXML = """
"""

PickupCancelResponseXML = """
"""

PickupValidationResponseXML = """
"""

PickupResponseXML = f"""<wrapper>
    {PickupCancelResponseXML}
    
</wrapper>
"""
