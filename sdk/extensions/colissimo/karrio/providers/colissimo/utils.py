import karrio.core as core


class Settings(core.Settings):
    """Colissimo connection settings."""

    password: str
    contract_number: str
    laposte_api_key: str = None
    lang: str = "fr_FR"

    @property
    def carrier_name(self):
        return "colissimo"

    @property
    def tracking_url(self):
        return "https://www.laposte.fr/outils/suivre-vos-envois?code={}"

    @property
    def server_url(self):
        return (
            "https://carrier.api" if self.test_mode else "https://sandbox.carrier.api"
        )

    @property
    def laposte_server_url(self):
        return "https://api.laposte.fr/suivi/v2"
