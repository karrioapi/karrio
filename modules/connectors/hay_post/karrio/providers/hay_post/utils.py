import json
import requests

import karrio.core as core
from karrio import lib


class Settings(core.Settings):
    """HayPost connection settings."""

    username: str
    password: str
    customer_id: str
    customer_type: str

    @property
    def proxies(self):
        # Add proxy for using hay_post API in test mode
        if self.test_mode:
            return {
                'http': 'username:ppassword@ip:port',
                'https': 'username:ppassword@ip:port',
            }
        return None

    @property
    def proxy(self):
        # Add proxy for using hay_post API in test mode
        if self.test_mode:
            return 'username:ppassword@ip:port'
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
            response = requests.request(
                method="POST",
                url=url,
                data=json.dumps({
                    "username": self.username,
                    "password": self.password,
                    "customerType": self.customer_type,
                }),
                headers={
                    'Content-Type': 'application/json'
                },
                proxies=self.proxies,
                verify=False
            )

            return response.json().get("accessToken")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
