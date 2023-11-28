import karrio.core as core


class Settings(core.Settings):
    """Roadie connection settings."""

    api_key: str

    @property
    def carrier_name(self):
        return "roadie"

    @property
    def server_url(self):
        return "https://connect.roadie.com"

    @property
    def tracking_url(self):
        return "https://track.roadie.com/id/{}"
