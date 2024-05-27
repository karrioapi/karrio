import jstruct
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """BoxKnight connection settings."""

    username: str
    password: str

    @property
    def carrier_name(self):
        return "boxknight"

    @property
    def server_url(self):
        return "https://api.boxknight.com/v1"

    @property
    def tracking_url(self):
        return "https://www.tracking.boxknight.com/tracking?trackingNo={}"

    @property
    def auth_token(self):
        """Retrieve the auth token using the username|passwword pair
        or collect it from the cache if an unexpired token exist.
        """
        cache_key = f"{self.carrier_name}|{self.username}|{self.password}"
        auth = self.connection_cache.get(cache_key) or {}
        token = auth.get("token")

        if token is not None:
            return token

        self.connection_cache.set(cache_key, lambda: authenticate(self))
        new_auth = self.connection_cache.get(cache_key)

        if any(self.depot or "") is False:
            self.depot = new_auth["depot"]

        return new_auth["token"]


def authenticate(settings: Settings):
    import karrio.providers.boxknight.error as error

    result = lib.request(
        url=f"{settings.server_url}/soap/services/LoginService/V2_1",
        data=dict(username=settings.username, password=settings.password),
        method="POST",
    )
    response = lib.to_dict(result)
    messages = error.parse_error_response(response, settings)

    if any(messages):
        raise errors.ParsedMessagesError(messages=messages)

    return dict(token=response["token"])
