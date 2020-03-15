from purplship.core import Settings as BaseSettings


class Settings(BaseSettings):
    """UPS connection settings."""

    user_token: str
    account_number: str
    language: str = 'en'

