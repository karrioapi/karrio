import karrio
import datetime

expiry = datetime.datetime.now() + datetime.timedelta(days=1)
delis_id="KD*****"
password="****"

gateway = karrio.gateway["dpd"].create(
    dict(
        delis_id=delis_id,
        password=password,
        test_mode=True,
        cache={
            f"dpd|{delis_id}|{password}": dict(
                depot="0530",
                token="****",
                expiry=expiry.strftime("%Y-%m-%d %H:%M:%S"),
            )
        },
    )
)
