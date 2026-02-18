"""MyDHL Express shipment operations."""

from karrio.providers.mydhl.shipment.create import (
    parse_shipment_response,
    shipment_request,
)
from karrio.providers.mydhl.shipment.return_shipment import (
    parse_return_shipment_response,
    return_shipment_request,
)
