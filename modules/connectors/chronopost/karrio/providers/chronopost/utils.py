"""Karrio Chronopost client settings."""

import karrio.lib as lib
from karrio.schemas.chronopost.shippingservice import headerValue
from karrio.core.settings import Settings as BaseSettings


LanguageEnum = lib.units.create_enum("LanguageEnum", ["en_GB", "fr_FR"])


class Settings(BaseSettings):
    """Chronopost connection settings."""

    account_number: str
    password: str
    id_emit: str = "CHRFR"
    language: LanguageEnum = "en_GB"  # type: ignore

    account_country_code: str = "FR"
    metadata: dict = {}

    @property
    def carrier_name(self):
        return "chronopost"

    @property
    def server_url(self):
        return "https://ws.chronopost.fr"

    @property
    def tracking_url(self):
        return "https://www.chronopost.fr/tracking-no-cms/suivi-page?listeNumerosLT={}"

    @property
    def header_value(self):
        return headerValue(accountNumber=self.account_number, idEmit=self.id_emit)
