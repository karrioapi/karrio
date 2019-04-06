"""PurplShip Australia post client settings."""

import attr
from purplship.domain.client import Client


@attr.s(auto_attribs=True)
class AustraliaPostClient(Client):
    """Australia post connection settings."""

    api_key: str
    password: str = None  # Required only for Logistic API
    account_number: str = None  # Required only for Logistic API
    carrier_name: str = "AustraliaPost"
    server_url: str = "https://digitalapi.auspost.com.au"
    api: str = "Logistic"  # Possible values: 'Logistic', 'Postage'
