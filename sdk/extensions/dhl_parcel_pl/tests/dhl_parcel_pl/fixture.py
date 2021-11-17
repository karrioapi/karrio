import purplship

gateway = purplship.gateway["dhl_parcel_pl"].create(
    dict(
        username="username",
        password="password",
    )
)
