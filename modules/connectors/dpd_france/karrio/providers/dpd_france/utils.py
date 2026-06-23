import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """DPD France connection settings (cargoNET / EPrintWebservice)."""

    userid: str
    password: str
    customer_center_number: str = None
    customer_number: str = None
    language: str = "EN"

    # DPD France is locked to FR (250); exposed with default for future flexibility
    customer_country_code: str = "250"

    account_country_code: str = "FR"
    metadata: dict = {}

    @property
    def carrier_name(self):
        return "dpd_france"

    @property
    def server_url(self):
        return (
            "https://e-station-testenv.cargonet.software/eprintwebservice/eprintwebservice.asmx"
            if self.test_mode
            else "https://e-station.cargonet.software/dpd-eprintwebservice/eprintwebservice.asmx"
        )

    @property
    def tracking_url(self):
        return (
            "https://e-station-testenv.cargonet.software/trace-service/Webtrace_Service.asmx"
            if self.test_mode
            else "https://webtrace.dpd.fr/trace-service/Webtrace_Service.asmx"
        )

    @property
    def shipping_namespace(self):
        # No trailing slash — verified against extracted EPrintWebservice WSDL
        return "http://www.cargonet.software"

    @property
    def tracking_namespace(self):
        # With trailing slash — verified against extracted Webtrace_Service WSDL
        return "http://www.cargonet.software/"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.dpd_france.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )
