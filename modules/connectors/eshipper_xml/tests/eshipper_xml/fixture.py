import karrio

gateway = karrio.gateway["eshipper_xml"].create(
    dict(
        username="username",
        password="password",
    )
)
