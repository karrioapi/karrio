"""PurplShip UPS client settings."""

from purplship.domain.client import Client


class UPSClient(Client):
    """UPS connection settings."""

    def __init__(
        self,
        username: str,
        password: str,
        access_license_number: str,
        carrier_name: str = "UPS",
        server_url: str = "https://onlinetools.ups.com/webservices",
    ):
        """UPS client constructor."""
        self.server_url = server_url
        self.username = username
        self.password = password
        self.access_license_number = access_license_number
        self.carrier_name = carrier_name
