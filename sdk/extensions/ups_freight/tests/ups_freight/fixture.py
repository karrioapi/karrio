import karrio

gateway = karrio.gateway["ups_freight"].create(
    dict(
        username="username",
        password="password",
        access_license_number="FG09H9G8H09GH8G0",
        account_number="Your Account Number",
    )
)
