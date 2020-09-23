import purplship.api as api
from purplship.api.mappers.ups_package import Settings

gateway = api.gateway["ups_package"].create(
    Settings(
        username="username",
        password="password",
        access_license_number="FG09H9G8H09GH8G0",
        account_number="Your Account Number",
    )
)
