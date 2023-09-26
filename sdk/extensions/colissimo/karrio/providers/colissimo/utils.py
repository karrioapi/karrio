import karrio.core as core


class Settings(core.Settings):
    """Colissimo connection settings."""

    password: str
    contract_number: str
    laposte_api_key: str = None

    account_country_code: str = "FR"
    config: dict = {}

    @property
    def carrier_name(self):
        return "colissimo"

    @property
    def server_url(self):
        return "https://ws.colissimo.fr/sls-ws/SlsServiceWSRest/2.0?_wadl"

    @property
    def laposte_server_url(self):
        return "https://api.laposte.fr/suivi/v2"

    @property
    def tracking_url(self):
        return "https://www.laposte.fr/outils/suivre-vos-envois?code={}"
