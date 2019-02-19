"""PurplShip DHL client settings."""

from purplship.domain.client import Client


class DHLClient(Client):
    """DHL connection settings."""

    def __init__(
        self,
        site_id: str,
        password: str,
        carrier_name: str = "DHL",
        server_url: str = "https://xmlpi-ea.dhl.com/XMLShippingServlet"
    ):
        """DHL client constructor."""
        self.site_id = site_id
        self.password = password
        self.server_url = server_url
        self.carrier_name = carrier_name
