from karrio.core import Settings as BaseSettings


class Settings(BaseSettings):
    """DHL Universal connection settings."""

    # Carrier specific properties
    consumer_key: str
    consumer_secret: str
    language: str = "en"

    account_country_code: str = "DE"
    metadata: dict = {}

    @property
    def carrier_name(self):
        return "dhl_universal"

    @property
    def server_url(self):
        return "https://api-eu.dhl.com"

    @property
    def tracking_url(self):
        country = self.account_country_code or "DE"
        language = self.language or "en"
        locale = f"{country}-{language}".lower()
        return (
            "https://www.dhl.com/"
            + locale
            + "/home/tracking/tracking-parcel.html?submit=1&tracking-id={}"
        )
