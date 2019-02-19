"""PurplShip Canada post client settings."""

from purplship.domain.client import Client


class CanadaPostClient(Client):
    """Canada post connection settings."""

    def __init__(
        self,
        username: str,
        password: str,
        customer_number: str,
        carrier_name: str = "CanadaPost",
        server_url: str = "https://soagw.canadapost.ca",
    ):
        """Canada Post client constructor."""
        self.username = username
        self.password = password
        self.server_url = server_url
        self.customer_number = customer_number
        self.carrier_name = carrier_name
