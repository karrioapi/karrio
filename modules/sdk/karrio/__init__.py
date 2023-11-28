"""Karrio package root module

Karrio makes shipping carrier webservices integration easy by providing
a modern and dev friendly library and by providing a unified extensible API
to communicate with all supported carriers.

-- Speak Karrio, Speak carriers...

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        >>> import karrio
        >>> from karrio.core.utils import DP
        >>> from karrio.core.models import Address, Parcel, RateRequest
        >>> canadapost = karrio.gateway["canadapost"].create(
        ...     {
        ...         "username": "username",
        ...         "password": "password",
        ...         "customer_number": "123456789",
        ...         "test": True
        ...     }
        ... )
        >>> shipper = Address(
        ...     postal_code= "V6M2V9",
        ...     city= "Vancouver",
        ...     country_code= "CA",
        ...     state_code= "BC",
        ...     address_line1= "5840 Oak St"
        ... )
        >>> recipient = Address(
        ...     postal_code= "E1C4Z8",
        ...     city= "Moncton",
        ...     country_code= "CA",
        ...     state_code= "NB",
        ...     residential= False,
        ...     address_line1= "125 Church St"
        ... )
        >>> parcel = Parcel(
        ...     height= 3.0,
        ...     length= 6.0,
        ...     width= 3.0,
        ...     weight= 0.5
        ... )
        >>> request = karrio.Rating.fetch(
        ...     RateRequest(
        ...         shipper=shipper,
        ...         recipient=recipient,
        ...         parcels=[parcel],
        ...         services=["canadapost_priority"]
        ...     )
        ... )
        >>> rates = request.from_(canadapost).parse()
        >>> print(DP.to_dict(rates))
        [
            [],
            [
                {
                    "base_charge": 12.26,
                    "carrier_name": "canadapost",
                    "carrier_id": "canadapost",
                    "currency": "CAD",
                    "transit_days": 2,
                    "extra_charges": [
                        {"amount": -0.37, "currency": "CAD", "name": "Automation discount"},
                        {"amount": 1.75, "currency": "CAD", "name": "Fuel surcharge"}
                    ],
                    "service": "canadapost_xpresspost",
                    "total_charge": 13.64
                }
            ]
        ]

Attributes:
    gateway (GatewayInitializer): Gateway initializer singleton instance

"""
__path__ = __import__("pkgutil").extend_path(__path__, __name__)  # type: ignore

from karrio.api.gateway import GatewayInitializer
import karrio.api.interface as interface

gateway = GatewayInitializer.get_instance()
Pickup = interface.Pickup
Rating = interface.Rating
Shipment = interface.Shipment
Tracking = interface.Tracking
Address = interface.Address
Document = interface.Document


__all__ = [
    "gateway",
    "Pickup",
    "Rating",
    "Shipment",
    "Tracking",
    "Address",
    "Document",
]
