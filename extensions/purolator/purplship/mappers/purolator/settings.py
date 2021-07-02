"""Purplship Purolator connection settings."""
import attr
from purplship.providers.purolator.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Purolator connection settings."""
    username: str
    password: str
    account_number: str
    language: str = "en"
    user_token: str = None
    id: str = None
    test: bool = False
    carrier_id: str = "purolator"
