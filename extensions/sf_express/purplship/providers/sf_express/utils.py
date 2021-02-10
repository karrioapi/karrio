from purplship.core import Settings as BaseSettings


class Settings(BaseSettings):
    """SF-Express connection settings."""

    # Carrier specific properties
    partner_id: str
    checkword: str

    id: str = None

    @property
    def carrier_name(self):
        return "sf_express"

    @property
    def server_url(self):
        return (
            "https://sfapi-sbox.sf-express.com/std/service"
            if self.test
            else "https://sfapi.sf-express.com/std/service"
        )
