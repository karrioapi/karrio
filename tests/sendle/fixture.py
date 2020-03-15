import purplship.package as api
from purplship.package.mappers.sendle import Settings

gateway = api.gateway["sendle"].create(
    Settings(
        server_url="https://sandbox.sendle.com",
        sendle_id="username",
        api_key="password",
    )
)
