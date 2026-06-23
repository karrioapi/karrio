"""Karrio GLS Group provider imports."""

from karrio.providers.gls.document import (
    document_upload_request,
    parse_document_upload_response,
)
from karrio.providers.gls.location import (
    location_request,
    parse_location_response,
)
from karrio.providers.gls.pickup import (
    parse_pickup_response,
    pickup_request,
)
from karrio.providers.gls.shipment import (
    parse_return_shipment_response,
    parse_shipment_cancel_response,
    return_shipment_request,
    shipment_cancel_request,
)
from karrio.providers.gls.shipment.create import (
    parse_shipment_response,
    shipment_request,
)
from karrio.providers.gls.tracking import (
    parse_tracking_response,
    tracking_request,
)
from karrio.providers.gls.utils import Settings
