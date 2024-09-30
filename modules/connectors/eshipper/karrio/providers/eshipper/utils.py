import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """eShipper connection settings."""

    principal: str
    credential: str

    @property
    def carrier_name(self):
        return "eshipper"

    @property
    def server_url(self):
        return (
            "https://uu2.eshipper.com" if self.test_mode else "https://ww2.eshipper.com"
        )

    @property
    def access_token(self):
        """Retrieve the "token" using the principal|credential pair
        or collect it from the cache if an unexpired "token" exist.
        """
        cache_key = f"{self.carrier_name}|{self.principal}|{self.credential}"
        now = datetime.datetime.now() + datetime.timedelta(minutes=30)

        auth = self.connection_cache.get(cache_key) or {}
        token = auth.get("token")
        expiry = lib.to_date(auth.get("expiry"), current_format="%Y-%m-%d %H:%M:%S")

        if token is not None and expiry is not None and expiry > now:
            return token

        self.connection_cache.set(cache_key, lambda: login(self))
        new_auth = self.connection_cache.get(cache_key)

        return new_auth["token"]


def login(settings: Settings):
    """Sign in response
    {
      "token": "string",
      "expires_in": "string",
      "token_type": "string",
      "refresh_token": "string",
      "refresh_expires_in": "string"
    }
    """
    import karrio.providers.eshipper.error as error

    result = lib.request(
        url=f"{settings.server_url}/api/v2/authenticate",
        data=lib.to_json(
            {
                "principal": settings.principal,
                "credential": settings.credential,
            }
        ),
        method="POST",
        headers={"content-Type": "application/json"},
    )
    response = lib.to_dict(result)
    messages = error.parse_error_response(response, settings)

    if any(messages):
        raise errors.ParsedMessagesError(messages=messages)

    expiry = datetime.datetime.now() + datetime.timedelta(
        seconds=float(response.get("expires_in", 0))
    )
    return {**response, "expiry": lib.fdatetime(expiry)}
