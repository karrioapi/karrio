
from karrio.providers.colissimo.utils import Settings
from karrio.providers.colissimo.rate import parse_rate_response, rate_request
from karrio.providers.colissimo.shipment import (
    parse_shipment_cancel_response,
    parse_shipment_response,
    shipment_cancel_request,
    shipment_request,
)
from karrio.providers.colissimo.tracking import (
    parse_tracking_response,
    tracking_request,
)
