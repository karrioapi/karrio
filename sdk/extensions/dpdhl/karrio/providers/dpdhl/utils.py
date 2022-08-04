import karrio.core as core


class Settings(core.Settings):
    """Deutsche Post DHL connection settings."""

    # required carrier specific properties
    username: str  # type:ignore
    password: str  # type:ignore
    customer_number: str = None

    @property
    def carrier_name(self):
        return "dpdhl"

    @property
    def server_url(self):
        return (
            "https://cig.dhl.de/services/sandbox/soap"
            if self.test_mode
            else "https://cig.dhl.de/services/production/soap"
        )

    @property
    def auth_data(self):
        return AuthData(
            username=self.username,
            password=self.password,
        )

    @staticmethod
    def serialize(envelope: Envelope, request_name: str, namesapce: str) -> str:
        namespacedef_ = (
            'xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/"'
            f' xmlns="{namesapce}"'
        )
        envelope.ns_prefix_ = "soap-env"
        envelope.Body.ns_prefix_ = envelope.ns_prefix_

        apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "")
        return (
            XP.export(envelope, namespacedef_=namespacedef_)
            .replace(
                "<%s:%s" % (envelope.ns_prefix_, request_name),
                "<%s%s" % ("", request_name),
            )
            .replace(
                "</%s:%s" % (envelope.ns_prefix_, request_name),
                "</%s%s" % ("", request_name),
            )
        )
