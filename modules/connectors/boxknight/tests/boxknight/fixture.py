import karrio
import karrio.lib as lib

cached_auth = {f"boxknight|username|password": dict(token="****")}

gateway = karrio.gateway["boxknight"].create(
    dict(
        username="username",
        password="password",
    ),
    cache=lib.Cache(**cached_auth),
)
