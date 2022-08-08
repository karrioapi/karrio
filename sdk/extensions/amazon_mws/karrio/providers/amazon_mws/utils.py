from karrio.core import Settings as BaseSettings


class Settings(BaseSettings):
    """AmazonMws connection settings."""

    seller_id: str
    developer_id: str
    mws_auth_token: str
    x_amz_access_token: str  # This is the access token retrieved from oauth flow
    aws_region: str = "us-east-1"
    account_country_code: str = None
    metadata: dict = {}

    @property
    def server_url(self):
        if self.aws_region == "eu-west-1":
            return (
                "https://sandbox.sellingpartnerapi-eu.amazon.com"
                if self.test_mode
                else "https://sellingpartnerapi-eu.amazon.com"
            )
        if self.aws_region == "us-west-2":
            return (
                "https://sandbox.sellingpartnerapi-fe.amazon.com"
                if self.test_mode
                else "https://sellingpartnerapi-fe.amazon.com"
            )

        return (
            "https://sandbox.sellingpartnerapi-na.amazon.com"
            if self.test_mode
            else "https://sellingpartnerapi-na.amazon.com"
        )

    @property
    def carrier_name(self):
        return "amazon_mws"
