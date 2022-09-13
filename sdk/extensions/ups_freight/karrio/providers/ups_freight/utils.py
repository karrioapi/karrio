import karrio.core as core


class Settings(core.Settings):
    """UPS Freight connection settings."""

    # required carrier specific properties
    username: str  # type:ignore
    password: str  # type:ignore
    access_license_number: str  # type:ignore
    account_number: str = None

    @property
    def carrier_name(self):
        return "ups_freight"

    @property
    def server_url(self):
        return (
            "https://wwwcie.ups.com"
            if self.test_mode
            else "https://onlinetools.ups.com"
        )
