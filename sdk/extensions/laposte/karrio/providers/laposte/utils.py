import karrio.core as core


class Settings(core.Settings):
    """La Poste connection settings."""

    api_key: str
    lang: str = "fr_FR"

    @property
    def carrier_name(self):
        return "laposte"

    @property
    def server_url(self):
        return "https://api.laposte.fr/suivi/v2"

    @property
    def tracking_url(self):
        return "https://www.laposte.fr/outils/suivre-vos-envois?code={}"
