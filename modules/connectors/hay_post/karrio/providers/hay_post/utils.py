import json
import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """HayPost connection settings."""

    username: str
    password: str
    customer_id: str
    customer_type: str

    @property
    def proxy(self):
        # Add proxy for using hay_post API in test mode
        if self.test_mode:
            return "username:passowrd@host:port"
        return None

    @property
    def carrier_name(self):
        return "hay_post"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.hay_post.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def server_url(self):
        if self.test_mode:
            return "https://dev-order.haypost.am"
        return "https://order.haypost.am"

    @property
    def authorization(self):
        url = "https://identity.haypost.am/api/Connect/Token"
        if self.test_mode:
            url = "https://dev-identity.haypost.am/api/Connect/Token"

        try:
            response = lib.request(
                url=url,
                method="POST",
                data=json.dumps(
                    {
                        "username": self.username,
                        "password": self.password,
                        "customerType": self.customer_type,
                    }
                ),
                proxy=self.proxy,
                headers={"Content-Type": "application/json"},
            )

            return lib.to_dict(response).get("accessToken")

        except Exception as e:
            print(f"Request failed: {e}")
            return None
