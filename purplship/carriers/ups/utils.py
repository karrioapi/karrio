from purplship.core import Settings as BaseSettings
from pyups.ups_security import UPSSecurity, UsernameTokenType, ServiceAccessTokenType


class Settings(BaseSettings):
    """UPS connection settings."""

    username: str
    password: str
    access_license_number: str
    account_number: str = None

    @property
    def carrier(self):
        return 'ups'

    @property
    def Security(self):
        return UPSSecurity(
            UsernameToken=UsernameTokenType(
                Username=self.username, Password=self.password
            ),
            ServiceAccessToken=ServiceAccessTokenType(
                AccessLicenseNumber=self.access_license_number
            ),
        )
