import base64
import karrio.lib as lib
import karrio.core as core
import dpdhl_lib.business_interface as dpdhl

AuthentificationType = lib.mutate_xml_object_type(
    dpdhl.AuthentificationType,
    tag_name="Authentification",
)


class Settings(core.Settings):
    """Deutsche Post DHL connection settings."""

    # required carrier specific properties
    username: str  # type:ignore
    password: str  # type:ignore
    signature: str  # type:ignore
    app_id: str  # type:ignore
    account_number: str = None
    language_code: str = "en"

    @property
    def carrier_name(self):
        return "dpdhl"

    @property
    def server_url(self):
        return (
            "https://cig.dhl.de/services/sandbox"
            if self.test_mode
            else "https://cig.dhl.de/services/production"
        )

    @property
    def AuthentificationType(self):
        return AuthentificationType(
            user=self.app_id,
            signature=self.signature,
        )

    @property
    def basic_authentication(self):
        pair = "%s:%s" % (self.username, self.password)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")


# class Authentification(dpdhl.AuthentificationType):
#     def __init__(self, user=None, signature=None, gds_collector_=None, **kwargs_):
#         super().__init__(user, signature, gds_collector_, **kwargs_)
#         self.original_tagname_ = "Authentification"
