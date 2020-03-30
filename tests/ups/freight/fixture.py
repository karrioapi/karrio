import purplship.freight as api
from purplship.freight.mappers.ups import Settings

gateway = api.gateway["ups"].create(
    Settings(
        username="username",
        password="password",
        access_license_number="FG09H9G8H09GH8G0",
        account_number="Your Account Number",
    )
)
