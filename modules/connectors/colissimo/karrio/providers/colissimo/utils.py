import karrio.lib as lib
import karrio.core as core

JSON_START = """<jsonInfos>

{"""
JSON_END = """}
--uuid:"""
LABEL_START = """<label>

"""
LABEL_END = r"""
--uuid:"""


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
        return "https://ws.colissimo.fr/sls-ws/SlsServiceWSRest/2.0"

    @property
    def laposte_server_url(self):
        return "https://api.laposte.fr/suivi/v2"

    @property
    def tracking_url(self):
        return "https://www.laposte.fr/outils/suivre-vos-envois?code={}"


def parse_response(response: str) -> dict:
    """Parse colissimo multipart response."""

    uuid = lib.failsafe(
        lambda: response[
            response.rfind("--uuid:") + len("--uuid:") : response.rfind("--")
        ]
    )
    json_info = lib.failsafe(
        lambda: response[
            response.find(JSON_START) + len(JSON_START) : response.rfind(JSON_END)
        ]
    )
    label = lib.failsafe(
        lambda: (
            response[
                response.find(LABEL_START)
                + len(LABEL_START) : response.rfind(LABEL_END)
            ]
            if "<label>" in response
            else None
        )
    )

    return dict(
        uuid=uuid,
        label=label,
        json_info=lib.to_dict("{" + (json_info or "") + "}"),
    )
