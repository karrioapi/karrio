"""PurplShip FedEx client settings."""

from purplship.domain.client import Client


class FedexClient(Client):
    """FedEx connection settings."""

    def __init__(
        self,
        user_key: str,
        password: str,
        meter_number: str,
        account_number: str,
        carrier_name: str = "Fedex",
        server_url: str = "",
    ):
        """Fedex client constructor."""
        self.server_url = server_url
        self.user_key = user_key
        self.password = password
        self.account_number = account_number
        self.meter_number = meter_number
        self.carrier_name = carrier_name
