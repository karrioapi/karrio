import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """TGE connection settings."""

    api_key: str
    my_toll_identity: str = None
    my_toll_token: str = None
    channel: str = None
    call_id: str = None

    @property
    def carrier_name(self):
        return "tge"

    @property
    def server_url(self):
        return self.connection_config.server_url.state or "https://tge.3plapi.com/"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.tge.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )
