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
            f"{delis_id}|{password}": dict(
                token="****",
                expiry=expiry.strftime("%Y-%m-%d %H:%M:%S"),
            )
        },
    )
)
