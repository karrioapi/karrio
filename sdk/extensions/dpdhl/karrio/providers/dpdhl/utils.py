import karrio.lib as lib
import karrio.core as core
import dpdhl_lib.business_interface as dpdhl


class Settings(core.Settings):
    """Deutsche Post DHL connection settings."""

    # required carrier specific properties
    username: str  # type:ignore
    password: str  # type:ignore
    customer_number: str = None
    language_code: str = "en"

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
        return dpdhl.AuthentificationType(user=self.username, signature=self.password)

    @staticmethod
    def serialize(envelope: lib.Envelope, request_name: str, namesapce: str) -> str:
        namespacedef_ = (
            'xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/"'
            f' xmlns="{namesapce}"'
        )
        envelope.ns_prefix_ = "soap-env"
        envelope.Body.ns_prefix_ = envelope.ns_prefix_

        lib.apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "")
        return (
            lib.to_xml(envelope, namespacedef_=namespacedef_)
            .replace(
                "<%s:%s" % (envelope.ns_prefix_, request_name),
                "<%s%s" % ("", request_name),
            )
            .replace(
                "</%s:%s" % (envelope.ns_prefix_, request_name),
                "</%s%s" % ("", request_name),
            )
        )
