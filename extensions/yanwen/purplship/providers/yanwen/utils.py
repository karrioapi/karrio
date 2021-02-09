from purplship.core import Settings as BaseSettings


class Settings(BaseSettings):
    """Yanwen connection settings."""

    # username: str
    # password: str
    # account_number: str = None
    id: str = None

    @property
    def carrier_name(self):
        return "yanwen"

    @property
    def server_url(self):
        return (
            "https://secure.shippingapis.com/ShippingAPI.dll"
            if self.test
            else "https://secure.shippingapis.com/ShippingAPI.dll"
        )
