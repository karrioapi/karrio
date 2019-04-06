import purplship
from purplship.mappers.sendle import SendleClient

proxy = purplship.gateway["sendle"].create(
    SendleClient(
        server_url="https://sandbox.sendle.com",
        sendle_id="username",
        api_key="password",
    )
)
