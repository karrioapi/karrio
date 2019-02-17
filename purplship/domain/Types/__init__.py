"""PurplShip types module."""
from .datatypes import *
from .factories import (
    create_shipment_options
)


class Quote:
    """quotes api interface."""

    @staticmethod
    def create(shipper: dict, recipient: dict, shipment: dict) -> shipment_request:
        """Create a quote request payload."""
        return shipment_request(
            shipper=party(**shipper),
            recipient=party(**recipient),
            shipment=create_shipment_options(**shipment),
        )


class Tracking:
    """tracking api interface."""

    @staticmethod
    def create(**args) -> tracking_request:
        """Create a tracking request payload."""
        return tracking_request(**args)


class Shipment:
    """shipment api interface."""

    @staticmethod
    def create(shipper: dict, recipient: dict, shipment: dict) -> shipment_request:
        """Create a shipment details request payload."""
        return shipment_request(
            shipper=party(**shipper),
            recipient=party(**recipient),
            shipment=create_shipment_options(**shipment),
        )


class Pickup:
    """pickup api interface."""

    @staticmethod
    def request(**args) -> pickup_request:
        """Create a pickup request payload."""
        return pickup_request(**args)

    @staticmethod
    def cancellation(**args) -> pickup_cancellation_request:
        """Create a pickup cancel request payload."""
        return pickup_cancellation_request(**args)
