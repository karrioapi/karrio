import karrio

gateway = karrio.gateway["dicom"].create(
    dict(
        username="username",
        password="password",
        billing_account="billing_account",
    )
)
