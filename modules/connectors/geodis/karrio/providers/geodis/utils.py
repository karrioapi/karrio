import json
import time
import hashlib
import karrio.lib as lib
import karrio.core as core

LanguageEnum = lib.units.create_enum("LanguageEnum", ["fr", "en"])


class Settings(core.Settings):
    """GEODIS connection settings."""

    api_key: str
    identifier: str
    code_client: str = None
    language: LanguageEnum = "fr"  # type: ignore

    account_country_code: str = "FR"
    metadata: dict = {}
    config: dict = {}

    @property
    def carrier_name(self):
        return "geodis"

    @property
    def server_url(self):
        return (
            "https://espace-client.geodis.com/services/services-mock"
            if self.test_mode
            else "https://espace-client.geodis.com/services"
        )

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.geodis.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    def get_token(self, service: str, data: dict) -> str:
        timestamp = "%d" % (time.time() * 1000)
        hash = hashlib.sha256(
            ";".join(
                [
                    self.api_key,
                    self.identifier,
                    timestamp,
                    self.language,
                    service,
                    json.dumps(data, separators=(",", ":")),
                ]
            ).encode("utf-8")
        ).hexdigest()

        return ";".join([self.identifier, timestamp, self.language, hash])
