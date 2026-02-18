"""Karrio DPD Group provider imports."""
from karrio.providers.dpd_meta.utils import Settings
from karrio.providers.dpd_meta.shipment import (
    parse_shipment_response,
    shipment_request,

    parse_return_shipment_response,
    return_shipment_request,
)
from karrio.providers.dpd_meta.pickup import (
    parse_pickup_response,
    pickup_request,
)