import karrio.lib as lib
import karrio.core as core


LangEnum = lib.units.create_enum("LangEnum", ["fr_FR", "en_US"])


class Settings(core.Settings):
    """La Poste connection settings."""

    api_key: str
    lang: LangEnum = "fr_FR"  # type: ignore

    @property
    def carrier_name(self):
        return "laposte"

    @property
    def server_url(self):
        return "https://api.laposte.fr/suivi/v2"

    @property
    def tracking_url(self):
        return "https://www.laposte.fr/outils/suivre-vos-envois?code={}"
