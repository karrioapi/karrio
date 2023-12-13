import karrio.core as core


class Settings(core.Settings):
    """Allied Express connection settings."""

    username: str
    password: str
    account: str = None

    @property
    def carrier_name(self):
        return "allied_express"

    @property
    def server_url(self):
        return (
            "https://test.aet.mskaleem.com" if self.test_mode else "https://3plapi.com"
        )
