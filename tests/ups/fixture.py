import purplship
from purplship.mappers.ups.settings import Settings

gateway = purplship.gateway["ups"].create(
    Settings(
        username="username",
        password="password",
        access_license_number="FG09H9G8H09GH8G0",
        account_number="Your Account Number",
    )
)
