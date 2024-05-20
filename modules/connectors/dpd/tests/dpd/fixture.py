import karrio
import datetime
import karrio.lib as lib

expiry = datetime.datetime.now() + datetime.timedelta(days=1)
password = "****"
delis_id = "KD*****"
cached_auth = {
    f"dpd|{delis_id}|{password}": dict(
        depot="0530",
        token="****",
        expiry=expiry.strftime("%Y-%m-%d %H:%M:%S"),
    )
}

gateway = karrio.gateway["dpd"].create(
    dict(
        delis_id=delis_id,
        password=password,
        test_mode=True,
    ),
    cache=lib.Cache(**cached_auth),
)
