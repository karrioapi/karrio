import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """DPD connection settings."""

    delis_id: str
    password: str
    depot: str = None
    message_language: str = "en_EN"
    account_country_code: str = "BE"

    @property
    def carrier_name(self):
        return "dpd"

    @property
    def server_url(self):
        if self.account_country_code == "NL":
            return (
                "https://shipperadmintest.dpd.nl/PublicApi"
                if self.test_mode
                else "https://wsshipper.dpd.nl"
            )

        return (
            "https://shipperadmintest.dpd.be/PublicApi"
            if self.test_mode
            else "https://wsshipper.dpd.be"
        )

    @property
    def tracking_url(self):
        lang = (self.message_language or "en_EN").split("_")[0]
        country = (self.account_country_code or "BE").lower()
        return (
            "https://www.dpdgroup.com/"
            + country
            + "/mydpd/my-parcels/track?lang="
            + lang
            + "&parcelNumber={}"
        )
