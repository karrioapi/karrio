from purplship.core import Settings as BaseSettings


class Settings(BaseSettings):
    """Yunexpress  connection settings."""

    # Carrier specific properties
    customer_number: str
    api_secret: str

    id: str = None

    @property
    def carrier_name(self):
        return "yunexpress"

    @property
    def server_url(self):
        return "https://api.yunexpress.com/LMS.API/api"
