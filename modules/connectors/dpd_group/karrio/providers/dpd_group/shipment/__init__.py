"""Karrio DPD Group shipment module."""

from karrio.providers.dpd_group.shipment.create import (
    parse_shipment_response,
    shipment_request,
)

__all__ = [
    "parse_shipment_response",
    "shipment_request",
]
